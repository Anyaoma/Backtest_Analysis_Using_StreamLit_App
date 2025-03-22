import pandas as pd
import datetime as dt

BUY = 1
SELL = -1
NONE = 0

def apply_takeprofit(row):
    if row.SIGNAL != NONE:
        if row.SIGNAL == BUY:
            return  row.ask_c + row.GAIN
        else:
            return row.bid_c - row.GAIN       
    else:
        return NONE


def apply_gain(row, PROFIT_FACTOR):
    if row.SIGNAL != NONE:
        if row.pair.split('_')[1] != 'JPY':
            return 30*PROFIT_FACTOR * 0.0001
        else:
            return 30*PROFIT_FACTOR * 0.001
    return NONE


def apply_loss(row):
    if row.SIGNAL != NONE:
        if row.pair.split('_')[1] != 'JPY':
            return 30 * 0.0001
        else:
            return 30 * 0.001
    return NONE


#note: when you buy or sell at the ask and bid price, you already paid the spread, so
#you just have to make sure that your TP level is above your buy or sell price to make gain
#but your stop loss should just be wide enough to account for volatility

def apply_stoploss(row, PROFIT_FACTOR):
    if row.SIGNAL != NONE:
        if row.SIGNAL == BUY:
            return row.ask_c - row.LOSS 
        else: 
            return row.bid_c + row.LOSS
    else:
        return NONE

    
def apply_signal_hour(df, PROFIT_FACTOR, sig):
    df['SIGNAL'] = df.apply(sig, axis=1)
    df['GAIN'] = df.apply(apply_gain, axis=1, PROFIT_FACTOR=PROFIT_FACTOR)
    df['LOSS'] = df.apply(apply_loss, axis=1)
    df['TP'] = df.apply(apply_takeprofit, axis=1)
    df['SL'] = df.apply(apply_stoploss, axis=1, PROFIT_FACTOR=PROFIT_FACTOR )
             

def create_changes(df):
    df_signals = df.copy()
    df_signals.drop([ 'mid_o', 'mid_h', 'mid_l', 'direction'], axis=1, inplace=True)
    df_signals.rename(columns={
        'bid_c':'start_price_SELL',
        'ask_c':'start_price_BUY'
    }, inplace=True)
    return df_signals


class Trade:
    def __init__(self, row):
        self.running = True
        self.start_index_m5 = row.name
        self.loss_in_pips = row.LOSS
        self.gain_in_pips = row.GAIN 
        self.pair = row.pair     

        if row.SIGNAL == BUY:
            self.start_price = row.start_price_BUY
            self.trigger_price = row.start_price_BUY

        if row.SIGNAL == SELL:
            self.start_price = row.start_price_SELL
            self.trigger_price = row.start_price_SELL
        
        self.SIGNAL = row.SIGNAL
        self.TP = row.TP
        self.SL = row.SL
        self.result = 0.0
        self.end_time = row.time
        self.start_time = row.time

    def close_trade(self, row, result, trigger_price):
        self.running = False
        self.result = result
        self.end_time = row.time
        self.trigger_price = trigger_price

    def update(self, row):    
        if self.SIGNAL == BUY:
            if row.time - self.start_time > dt.timedelta(hours=48): #check time
                self.close_trade(row, 'closed trade', row.bid_o)
            elif row.bid_h >= self.TP: #check take profit levels
                self.close_trade(row, 'PROFIT', row.bid_h)
            elif row.bid_l <= self.SL: #check stop loss levels
                self.close_trade(row, 'LOSS', row.bid_l)
            
        elif self.SIGNAL == SELL:
            if row.time - self.start_time > dt.timedelta(hours=48): #check time
                self.close_trade(row, 'closed trade', row.ask_o)
            elif row.ask_l <= self.TP: #check take profit levels
                self.close_trade(row, 'PROFIT', row.ask_l)
            elif row.ask_h >= self.SL: #check stop loss levels
                self.close_trade(row, 'LOSS', row.ask_h)
            


class GuruTester:
    def __init__(self, df_big, apply_signal,price_conv,PROFIT_FACTOR=2,risk_percent=0.05):
        self.df_big = df_big.copy()
        self.PROFIT_FACTOR = PROFIT_FACTOR
        self.apply_signal = apply_signal
        self.prepare_data()
        self.position = 0
        self.risk_percent = risk_percent
        self.initial_amount = 100000
        self.amount = self.initial_amount
        self.units = 0
        self.price_conv = price_conv
        self.result = 0
        #self.realised_pnl = []

    def prepare_data(self):
        apply_signal_hour(self.df_big,
                    self.PROFIT_FACTOR,
                    self.apply_signal)
        
        df_signals = create_changes(self.df_big)
        df_signals['time'] = pd.to_datetime(df_signals['time'], unit='s')
        df_signals['time'] = df_signals['time'].dt.tz_localize(None)
        self.data = df_signals
        #self.data.fillna(0, inplace=True)
        self.data.SIGNAL = self.data.SIGNAL.astype(int)
       

    def cal_risk_amount(self):
        self.risk_amount = self.risk_percent * self.amount

    def calculate_unit(self,pair, loss_in_pips):
        #pair_price = None
        for price in self.price_conv:
            if price.instrument == pair:
                if pair.split('_')[1] != 'GBP':
                    if  pair.split('_')[1] != 'JPY':
                        gbp_base = 1/price.sell_conv
                        risk_in_base = self.risk_amount*gbp_base
                        position_in_lot = risk_in_base/(loss_in_pips/0.0001)
                        self.units = position_in_lot * 10000 * 1
                    else:
                        gbp_base = 1/price.sell_conv
                        risk_in_base = self.risk_amount*gbp_base
                        position_in_lot = risk_in_base/(loss_in_pips/0.0001)
                        self.units = position_in_lot * 10000 * 1
                else:
                    position_in_lot = self.risk_amount/(loss_in_pips/0.0001)
                    self.units = position_in_lot * 10000 * 1

    
    def update_result(self,object):
        price_conv= [price.sell_conv for price in self.price_conv if price.instrument == object.pair]
        if object.result == 'PROFIT':
            self.result = self.units * object.gain_in_pips * price_conv[0]
        elif object.result =='LOSS':
            self.result = -self.units * object.loss_in_pips * price_conv[0]
        else:
            self.result = self.units * (object.trigger_price - object.start_price) * price_conv[0]


    def calculate_returns(self):
        self.returns = self.result/self.amount


    def update_account_balance(self,object):
        price_conv= [price.sell_conv for price in self.price_conv if price.instrument == object.pair]
        if object.result == 'PROFIT':
            self.amount += self.units * object.gain_in_pips* price_conv[0]
        elif object.result =='LOSS':
            self.amount -= self.units * object.loss_in_pips * price_conv[0]
        else:
            self.amount += self.units * (object.trigger_price - object.start_price) * price_conv[0]


    def run_test(self):
        print("run_test...")
        open_trades_m5 = []
        closed_trades_m5 = []

        for index, row in self.data.iterrows():     
            #self.pnl = 0     #useful for multiple trades running at once 
            for ot in open_trades_m5:
                #real_pnl = 0
                ot.update(row)
                if ot.running == False:
                    self.update_result(ot)
                    self.calculate_returns()
                    self.update_account_balance(ot)
                    realised_pnl = self.result
                    ot.amount = round(self.amount,2)
                    ot.result = round(realised_pnl,2)
                    ot.returns = round(self.returns,5)
                    pnl_list.append(round(realised_pnl,2))
                    ot.running_pnl = pnl_list
                    #self.pnl += realised_pnl #useful for multiple trades running at once
                    closed_trades_m5.append(ot)
                    self.position = 0
                    
                else:
                    if ot.SIGNAL == BUY:
                        unrealised_pnl = self.units * (row.start_price_SELL - ot.start_price)
                        unrealised_pnl= [price.sell_conv*unrealised_pnl for price in self.price_conv if price.instrument == ot.pair]
                        
                    else:
                        unrealised_pnl = self.units * (ot.start_price - row.start_price_BUY)
                        unrealised_pnl= [price.sell_conv*unrealised_pnl for price in self.price_conv if price.instrument == ot.pair]
                        
                    #self.pnl += unrealised_pnl[0] #useful for multiple trades running at once
                    pnl_list.append(round(unrealised_pnl[0],2))
                print(pnl_list)
            #self.realised_pnl.append(self.pnl) #useful for multiple trades running at once

            open_trades_m5 = [x for x in open_trades_m5 if x.running == True]

            if self.position == 0:
                  
                if row.SIGNAL != NONE:
                    trade = Trade(row)
                    open_trades_m5.append(trade)
                    pnl_list = [] 
                    self.position = 1
                    self.cal_risk_amount()
                    self.calculate_unit(trade.pair, trade.loss_in_pips)
                    trade.risk_amount = round(self.risk_amount,2)
                    #trade.unit_traded = self.units #in terms of the quote currency
                    

        self.df_results = pd.DataFrame.from_dict([vars(x) for x in closed_trades_m5]) 
        

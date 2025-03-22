import requests
import pandas as pd
import streamlit as st
import quantstats as qs
import plotly.express as px
import constants.constants as comps
from technicals.indicators import RSI
from technicals.patterns import apply_properties_patterns
from oanda_api.oanda_api import oandaApi as api
from Strategy_setter.strategy_setter import GuruTester


SELECT_PAIRS_FROM = ['AUD_JPY','EUR_AUD','EUR_USD','GBP_AUD']

TRADEABLE_PAIRS = ['AUD_JPY','EUR_AUD','EUR_USD','GBP_AUD']

TIME_FRAME = 'H1' #for this strategy, select either H1 or H4

@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode("utf-8")
      

def apply_signal(row):
    if row.ENGULFING == True and row.direction == 1:
        if row.RSI < 30:
            return comps.BUY     
    elif row.ENGULFING == True and row.direction == -1:
        if row.RSI > 70:
             return comps.SELL   
    return comps.NONE


def run_strategy(pair,time_frame, risk_percent):
    data = pd.read_pickle(f"./data/{pair}_{time_frame}.pkl")
    data.reset_index(drop=True, inplace=True)
    data = apply_properties_patterns(data)
    data = RSI(data, n=rsi_value)
    our_cols = ['time','pair', 'mid_o', 'mid_h', 'mid_l', 'mid_c',
                'bid_o', 'bid_h', 'bid_l', 'bid_c', 
                'ask_o', 'ask_h', 'ask_l', 'ask_c',
                'ENGULFING', 'RSI','direction' ]
    df_slim = data[our_cols].copy()
    df_slim.dropna(inplace=True)
        
    df_slim.reset_index(drop=True, inplace=True)
    gt = GuruTester(df_slim, apply_signal,price_conv, risk_percent=risk_percent)   
    gt.run_test()
    return gt.df_results


def calculate_statistics(returns):
    stats = {
        'Sharpe Ratio': qs.stats.sharpe(returns),
        'Annualized Return': qs.stats.cagr(returns),
        'Max Drawdown': qs.stats.max_drawdown(returns),
        'Volatility': qs.stats.volatility(returns),
        'VaR': qs.stats.value_at_risk(returns),
        'CVaR': qs.stats.conditional_value_at_risk(returns),
        '%win': len([x for x in returns if x>0])/len(returns)}
    return stats



if __name__ == '__main__':

    #Define the part of the sidebar used for selecting the ticker and the dates
    
    st.sidebar.header("Forex Pairs Parameters")

    available_pairs = TRADEABLE_PAIRS

    #available_cols = df.columns.tolist()
    column_to_show = st.sidebar.multiselect(
        "Currency Pairs", 
        available_pairs, 
        default=available_pairs,
        key = 'currency_to_show'
    )

    price_conv = api.get_prices(column_to_show)

    # Display a non-editable date range in the sidebar
    st.sidebar.write("Date Range: 2019-01-07  -  2024-12-31")


    # Define the part of the sidebar used for tuning the details of the technical analysis
    st.sidebar.header("Technical Analysis Parameters")
    ENGULFING_STRATEGY = st.sidebar.checkbox(label="Add Engulfing", value=True)
    ENGULFING_STRATEGY = True

    # Add the expander with parameters of the SMA
    exp_rsi = st.sidebar.expander("RSI")
    #rsi_flag = exp_rsi.checkbox(label="Add RSI")
    rsi_value = exp_rsi.number_input(
        label="RSI VALUE", 
        min_value=12, 
        max_value=16, 
        value=14, 
        step=1
    )

    #add a session for backytest controls
    st.sidebar.header("Backtest Controls")
    risk_percent = st.sidebar.number_input(
        label="RISK (%)", 
        min_value=0.1, 
        max_value=100.0, 
        value=0.5, 
        step=0.1
    )

    risk_decimal = risk_percent / 100.0
    st.sidebar.write(f"Risk as a decimal: {risk_decimal:.5f}")

    # Specify the title and additional text in the app’s main body
    st.title("Backtest analysis for Engulfing + RSI strategy")
    st.write("""
    ### User manual
    * You can select any of the currencies that is a component of EUR_USD, GBP_JPY, GBP_USD
    * You can change the RSI components or levels
    * You can apply risk management by selecting the risk amount per trade
    * You can download the selected data as a CSV file
    """)


#create a list and return the result of each strategy by asset
    results = []
    for p in column_to_show:
        result_dict = run_strategy(p, time_frame=TIME_FRAME ,risk_percent=risk_decimal)
        result_df = pd.DataFrame(result_dict)

        if 'result' in result_df.columns:
            result_df['cumulative_gain'] = result_df['result'].cumsum().round(2)

        results.append(result_df)

    df = pd.concat(results, axis=0)
    

#make the datafram available on the site
    data_exp = st.expander("Preview data")
    available_cols = df.columns.tolist()
    columns_to_show = data_exp.multiselect(
        "Columns", 
        available_cols, 
        default=available_cols,
        key = 'columns_to_download'
    )

    # write to side bar downloaded data
    data_exp.dataframe(df[columns_to_show])

    csv_file = convert_df_to_csv(df[columns_to_show])
    data_exp.download_button(
        label="Download selected as CSV",
        data=csv_file,
        file_name="currency pairs_data.csv",
        mime="text/csv",
    )

    # Create a Plotly figure
    fig = px.line(df, x='start_time', y='cumulative_gain', color='pair', title='Cumulative Gain Over Time')
    fig.update_xaxes(title_text='Time')
    fig.update_yaxes(title_text='Cumulative Gain')

    # Streamlit app
    st.title('Cumulative Gain Over Time')
    st.plotly_chart(fig)

    #create table for backtest result
    results_final = {}
    for pair in df.pair.unique():
        new_ = df[df['pair'] == pair]
        new = new_['returns']
        new.index = pd.to_datetime(new_.start_time)
        results_final[pair] = calculate_statistics(new)


    # Convert results to a DataFrame
    results_df = pd.DataFrame(results_final).T.reset_index()
    results_df.rename(columns={'index': 'Asset'}, inplace=True)

    # Display the results in Streamlit
    st.write("Backtest Statistics for Each Asset:")
    st.dataframe(results_df)  # Use st.table(results_df) for a static table



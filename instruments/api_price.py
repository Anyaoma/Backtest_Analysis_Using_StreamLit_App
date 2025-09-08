class ApiPrice:

    def __init__(self, api_ob, homeConversions):
        self.instrument = api_ob['instrument']
        self.ask = float(api_ob['asks'][0]['price'])
        self.bid = float(api_ob['bids'][0]['price'])

        base_instrument = self.instrument.split('_')[1]

        if base_instrument in homeConversions:
            self.sell_conv = float(homeConversions[base_instrument]['positionValue'])
        else:
            self.sell_conv = 1.0  # fallback or raise error
        

    def __repr__(self):

        #return f'{dict(self.instrument=f"{self.sell_conv:.6f}")}'
        return f" {self.instrument},{self.sell_conv:.6f}"




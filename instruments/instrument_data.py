import json
from instruments.instrument import Instrument

class InstrumentCollection:
    FILENAME = "instrument.json"
    API_KEYS = ['name', 'type', 'displayName', 'pipLocation', 'tradeUnitsPrecision', 'marginRate', 'displayPrecision']

    def __init__(self):
        self.instrument_dict = {}

    def loadInstruments(self, path):
        self.instrument_dict = {}
        filename = f"{path}/{InstrumentCollection.FILENAME}"
        with open(filename, 'r') as f:
            data = json.loads(f.read())
            for k, v in data.items():
                self.instrument_dict[k] = Instrument.FromApiObject(v)

    def CreateFile(self, data, path):
        if data is None:
            print("Instrument data failed to download")
            return 
        
        instrument_dict = {}
        for i in data:
            key = i['name']
            instrument_dict[key] = {k: i[k] for k in InstrumentCollection.API_KEYS}

        filename = f"{path}/{InstrumentCollection.FILENAME}"
        with open(filename, 'w') as f:
            f.write(json.dumps(instrument_dict, indent=2))

    def printInstruments(_self):
        [print(k,v) for k,v in _self.instruments_dict.items()]
        print(len(_self.instruments_dict.keys()), "instruments")


instrumentCollection = InstrumentCollection()

    
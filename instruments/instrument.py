

class Instrument:
    def __init__(self, name, ins_type, displayName, pipLocation, tradeUnitsPrecision, marginRate, displayPrecision):
        self.name = name
        self.ins_type = ins_type
        self.displayName = displayName
        self.pipLocation = pow(10, pipLocation)
        self.tradeUnitsPrecision = tradeUnitsPrecision
        self.marginRate = float(marginRate)
        self.displayPrecision = displayPrecision

    def __repr__(self):
        return str(vars(self))
    
    @classmethod
    def FromApiObject(cls, obj):
        return Instrument(
            obj['name'], 
         obj['type'],
         obj['displayName'],
         obj['pipLocation'],
         obj['tradeUnitsPrecision'],
         obj['marginRate'],
         obj['displayPrecision']
        )
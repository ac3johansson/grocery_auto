
class Ingredient:
    unitsWeight = {'g':1, 'hg':100, 'kg':1000} #Valid weight units
    unitsVolume = {'krm':1, 'tsk':5, 'msk':15, 'ml':1, 'cl':10, 'dl':100, 'l':1000} #Valid volume units
    #Also 'st' is valid but don't need dictionary for that


    # Specification of a ingredient. 
    # name - The name of the ingredient
    # unit - The unit the ingredient should be measured in.
    def __init__(self, name, unit):
        self.name = name
        unit = str(unit).lower().strip()
        if (unit in (Ingredient.unitsWeight or Ingredient.unitsVolume)) or unit == 'st':
            self.unit = unit
        else:
            raise ValueError("Enheten finns ej dokumenterad")
        

    #Ändrar dokumenterad enhet. OBS! konventera enheten innan ändring. 
    def changeUnit(self, newUnit):
        if (newUnit in (Ingredient.unitsWeight or Ingredient.unitsVolume)) or newUnit == 'st':
            self.unit = newUnit
        else:
            raise ValueError("Enheten finns ej dokumenterad")

    #Returns the factor of which the new amount should be converted to, to correspond to the correct amount but with the new unit
    def convertUnit(self, fromUnit, toUnit):
        fromUnit = str(fromUnit).lower().strip()
        toUnit = str(toUnit).lower().strip()
        if (fromUnit and toUnit) in Ingredient.unitsVolume:
            return Ingredient.unitsVolume[fromUnit] / Ingredient.unitsVolume[toUnit]
        elif (fromUnit and toUnit) in Ingredient.unitsWeight:
            return Ingredient.unitsWeight[fromUnit] / Ingredient.unitsWeight[toUnit]
        elif (fromUnit or toUnit) == 'st':
            raise ValueError("Kan inte konventera till/från st")
        else: 
            raise ValueError("Enhet finns ej dokumenterad")


    def getUnit(self):
        return self.unit
    
    def getName(self):
        return self.name
    
    def __str__(self):
        return self.name
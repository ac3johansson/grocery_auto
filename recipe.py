from ingredient import Ingredient

class Recipe:

    def __init__(self, name, link, tag):
        #self.filename = filename
        self.name = name
        self.ingredients = {}
        self.link = link
        self.tag = tag
    
    def addIngredient(self, nameIngredient, amount, unit):
        for key in self.ingredients.keys():
            if key.getName() == nameIngredient:
                
                if getattr(key, 'unit') == unit: #Om unit är den samma
                    self.ingredients[nameIngredient] = self.ingredients[nameIngredient] + amount
                else: #annars, gör om unit och amount så att de stämmer överens eller neka ny unit
                    self.ingredients[nameIngredient] = self.ingredients[nameIngredient] + amount * Ingredient.convertUnit(unit, key.getUnit())
            #else:

            #Gör om dict till set och hitta key med get eller [] och skapa metod i ingredient changeUnit(). Ny unit ersätter gamla. 
        else: 
            self.ingredients[Ingredient(nameIngredient, unit)] = int(amount)
    
    #Removes the ingredient with key nameIngredient and returns the total amount of that ingredient
    def removeIngredient(self, nameIngredient):
        return self.ingredients.pop(nameIngredient)

    def getIngredients(self):
        return self.ingredients

    #def getFileName(self):
    #    return self.filename

    def getName(self):
        return self.name 

    def getLink(self):
        return self.link
    
    def getTag(self):
        return self.tag
    
    def __str__(self):
        return self.name



def main():
    r1 = Recipe("Fisk med potatis och ärtor")
    r1.addIngredient("Fisk", 4, "st")

    print(r1.getIngredients().keys())
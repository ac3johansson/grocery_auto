from oldclasses.recipeBank import RecipeBank
from oldclasses.recipe import Recipe
from oldclasses.ingredient import Ingredient
import random

#Vill få ut:
#inköpslista
#Plan i form av en txt fil

class MonthlyPlan:

    def __init__(self):
        self.bank = RecipeBank()
        self.bank.load()
        self.monthlyRecipes = ()

    #Lägger till recept som ska vara en del av planen
    def addMonthlyRecipe(self, recipe):
        self.monthlyRecipes.append(recipe)

    #Tar bort recept från planen
    def removeMonthlyRecipe(self, recipe):
        if recipe in self.monthlyRecipes:
            self.monthlyRecipes.pop(recipe)

    #Returnerar en lista med valbara recept
    #Valbart om en vill ha en lista med en tagg eller ej
    def availableRecipes(self, tag=None):
        if tag == None:
            return self.bank.getRecipes.values()
        else:
            tagList = tagList(tag)
            return tagList
        

    #Radomisera recept med avseende på vilken 'tag' en vill ha
    def randomRecipe(self, tag):
        tagList = tagList(tag)
        random.randint(0,len(tagList)-1)
        return 
    
    #Ger en lista med alla recept med taggen "tag" (TODO: fixa så att tagList bara skapas en gång) (TODO: flera taggar, lista)
    def tagList(self, tag):
        tagList = ()
        for filename, recipe in self.bank.getRecipes().items():
            if recipe.getTag() == tag:
                tagList.append(recipe)
        return tagList
    

    #Samla alla ingredienser och mängd till inköpslista (HÄR SLUTADE JAG)
    def shoppingList(self):
        ingredients = {}
        for monthlyRecipe in self.monthlyRecipes:
            for ingredient, amount in monthlyRecipe.getIngredients().items():
                if ingredient in ingredients.keys():
                    ingredients[ingredient] = ingredients[ingredient] + amount
                else:
                    ingredients[ingredient] = amount
        return ingredients

    #Ändra om ordning bland recepten, ska gå bestämma vilken vecka de ska lagas. 

    #Rapportera vilka ingredisenser och mängder som tillhör vilken vecka. 

    #Koventera till txt fil med standard format 
import csv
import os
from old.recipe import Recipe
from old.ingredient import Ingredient
#import json

class RecipeBank:
    
    def __init__(self):
        self.recipes = {}
    
    def getRecipes(self):
        return self.recipes

    #load all recepies from csv or txt file to an list, the elements of the array should be objects of type recipe (recipe.py)
    def load(self):
        directory_path = 'recipes/'
        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    data = [row for row in reader]
                    r = Recipe(data[0][0], data[0][1], data[0][2])
                    for d in data[1:]:
                        if d:
                            r.addIngredient(d[0], d[1], d[2]) 
                    self.recipes[filename] = r

    def save(self):
        directory_path = 'recipes/'
        for filename, recipe in self.recipes.items():
            file_path = os.path.join(directory_path, filename)
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([recipe.getName(), recipe.getLink(), recipe.getTag()])
                for ingred, amount in recipe.getIngredients().items():
                    writer.writerow([ingred.getName(), amount, ingred.getUnit()])

    #TODO: Ej klar  
    def addRecipe(self, filename, name, link, tag):
        self.recipes[filename] = Recipe(name, link, tag)
    
    def findRecipes(self, name=None, tag=None):
        result = {}
        name = str(name).lower().strip()
        tag = str(tag).lower().strip()

        if ((name and tag) == None) or (name and tag) == "": #Kan man kolla tom string så?
            return "Inga recept hittade" 
        
        for filename, recipe in self.recipes.items():
            if name in recipe.getName() or tag == recipe.getTag():
                result[filename] = recipe
        return result
    

    #TODO: Ska returnera alla recept som innehåller vissa ingrediener
    def findRecipesByIngredient():
        return 





'''
        #First code
        directory_path = 'recipes/' 

        for filename in os.listdir(directory_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(directory_path, filename)
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if filename in self.recipes:
                    writer.writerow(self.recipes[filename])
                    writer.writerow()
                else:
                    writer
        #Second code
        with open(recipes_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            self.recipies = [row for row in reader]
        for r in self.recipies:
            print(r)
        return 
'''


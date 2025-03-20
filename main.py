import recipeBank as st
import numpy as np
import sys
from recipe import Recipe
from ingredient import Ingredient
from recipeBank import RecipeBank

#import tkinter
#print(tkinter.TkVersion)
#adjectives = ['big', 'round', 'massive']
#fruits = ['apple', 'banana', 'pear']
''''
for i in fruits:
    print(i)

for i in "banana":
    print(i)

for i in fruits:
    if i == "banana":
        continue
    print(i)

for i in fruits:
    print(i)
    if i == "banana":
        break
        
for i in range(1,3):
   print(fruits[i]) 


for i in adjectives:
    for j in fruits:
        if i == 'round':
            continue
        print(i, j)
'''''
#input = sys.stdin
#print(np.power(input, 2))



#r1 = Recipe("Fisk med potatis och ärtor", "www", "Storkok")
#r1.addIngredient("Fisk", 4, "st")

rb = RecipeBank()

rb.load()
#print(rb.getRecipes())
rb.getRecipes().get('fiskrecept.csv').addIngredient('fikon', 9, 'st')
rb.save()

#print(r1)



#f = st.storage('recipes.csv')
##f.addRecepie('Gulash', 'www.', 'Fredag')
#f.save('recipes.csv')

#print(f.toString())

from flask import flash, redirect
from models.recipe import Recipe
from models.ingredient import Ingredient
from models import db

def add_ingredient(recipe_id, ingredient_name, amount, unit):
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return "Recipe not found"
    if unit not in (Ingredient.unitsVolume or Ingredient.unitsWeight) or unit == 'st':
        return "Unit not found"
    
    new_ingredient = Ingredient.query.filter_by(name=ingredient_name).first()

    if not new_ingredient:
        new_ingredient = Ingredient(name=ingredient_name, amount=amount, unit=unit, recipe=recipe)
        try: 
            db.session.add(new_ingredient)
            db.session.commit()
            flash(f"Added {ingredient_name} to {recipe.name}")
            return redirect(f'/user/{user_id}/recipebank')
        except:
            flash("Kunde inte lägga till recept")
            return redirect(f'/user/{user_id}/recipebank')
    else:
        if new_ingredient.unit == unit:
            new_ingredient.amount = new_ingredient.amount + amount
        else: 
            new_ingredient.amount = new_ingredient.amount + amount * convert_unit(unit, new_ingredient.unit)
        db.session.commit()
        return f"Uppdated {ingredient_name} amount in {recipe.name}"



#Modify amount of ingredient
def edit_ingredient_amount():
    pass

#Remove the ingredient from recipe
def remove_ingredient(recipe_id, ingredient_name):
    pass

def convert_unit(fromUnit, toUnit):
    fromUnit = str(fromUnit).lower().strip()
    toUnit = str(toUnit).lower().strip()
    if (fromUnit and toUnit) in Ingredient.unitsVolume:
        return Ingredient.unitsVolume[fromUnit] / Ingredient.unitsVolume[toUnit]
    elif (fromUnit and toUnit) in Ingredient.unitsWeight:
        return Ingredient.unitsWeight[fromUnit] / Ingredient.unitsWeight[toUnit]
    elif (fromUnit or toUnit) == 'st':
        #HUR SKA ERRORS HANTERAS?
        raise ValueError("Kan inte konventera till/från st")
    else: 
        #HUR SKA ERRORS HANTERAS?
        raise ValueError("Enhet finns ej dokumenterad")
    
#Ändrar dokumenterad enhet. OBS! konventera enheten innan ändring. 
def change_unit(newUnit, ingredient_id):
    if (newUnit in (Ingredient.unitsWeight or Ingredient.unitsVolume)) or newUnit == 'st':
        #self.unit = newUnit
        Ingredient.query.get(ingredient_id).unit = newUnit
    else:
        raise ValueError("Enheten finns ej dokumenterad")
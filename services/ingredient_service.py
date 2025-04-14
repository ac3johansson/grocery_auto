from flask import flash, redirect
from models.recipe import Recipe
from models.ingredient import Ingredient
from models import db


def add_ingredient(user_id, recipe_id, ingredient_name, amount, unit):
    recipe = Recipe.query.get(recipe_id)
    input_check = True
    # try:
    ingredient_name = str(ingredient_name).strip().lower()
    unit = str(unit).strip().lower()
    if (unit not in Ingredient.unitsVolume.keys() and unit not in Ingredient.unitsWeight.keys() and unit not in Ingredient.unitsDistinct):
        input_check = False
        flash("Enheten finns ej")
    # except ValueError:
    #     input_check = False
    #     flash("Enheten finns ej")

    if not recipe:
        return "Recipe not found"
    
    try:
        amount = float(amount)
    except ValueError:
        input_check = False
        flash("Mängden måste vara ett nummer")
    if input_check:
        new_ingredient = Ingredient.query.filter_by(name=ingredient_name, recipe_id=recipe_id).first()
        if not new_ingredient:
            new_ingredient = Ingredient(name=ingredient_name, amount=amount, unit=unit, recipe_id=recipe_id)
            db.session.add(new_ingredient)
            db.session.commit()
            flash(f"Added {ingredient_name} to {recipe.name}")
        else:
            try:
                if new_ingredient.unit == unit:
                    new_ingredient.amount = float(new_ingredient.amount) + amount
                else: 
                    new_ingredient.amount = float(new_ingredient.amount) + amount * convert_unit(unit, new_ingredient.unit)
                db.session.commit()
                flash(f"Uppdaterade mängden för {ingredient_name} i {recipe.name}")            
            except:
                flash("Ingrediensen kunde ej läggas till")
    return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')
    

def remove_ingredient(user_id, recipe_id, ingredient_id):
    try:
        db.session.delete(Ingredient.query.get(ingredient_id))
        db.session.commit()
    except:
        flash("Ingrediensen kunde ej tas bort")
    return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')


#Converts units. 
def convert_unit(fromUnit, toUnit):
    fromUnit = str(fromUnit).lower().strip()
    toUnit = str(toUnit).lower().strip()
    if fromUnit in Ingredient.unitsVolume and toUnit in Ingredient.unitsVolume:
        return Ingredient.unitsVolume[fromUnit] / Ingredient.unitsVolume[toUnit]
    elif fromUnit in Ingredient.unitsWeight.keys() and toUnit in Ingredient.unitsWeight.keys():
        return Ingredient.unitsWeight[fromUnit] / Ingredient.unitsWeight[toUnit]
    else:
        raise TypeError
    
#Changes the unit specified to the ingredient_id and the 
def change_unit(user_id, recipe_id, newUnit, ingredient_id):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        ingredient.amount = ingredient.amount * convert_unit(ingredient.unit, newUnit)
        ingredient.unit = newUnit
        db.session.commit()
        flash("Enhet uppdaterad")
    except:
        flash("Kunde inte ändra enhet")
    return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')
    # if newUnit not in (Ingredient.unitsWeight.keys() or Ingredient.unitsVolume.keys() or Ingredient.unitsDistinct):
    #     flash("Enheten finns ej")
    # elif ingredient == None:
    #     flash("Ingrediensen hittades ej")
    # else:
    #     ingredient.amount = ingredient.amount * convert_unit(newUnit, ingredient.unit)
    #     ingredient.unit = newUnit
    #     db.session.commit()
    # redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')


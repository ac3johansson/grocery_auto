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
    if (unit not in Ingredient.unitsVolume.keys() and unit not in Ingredient.unitsWeight.keys() and unit not in Ingredient.unitsDistinct.keys()):
        input_check = False
        flash('Enheten finns ej', 'warning')
    # except ValueError:
    #     input_check = False
    #     flash("Enheten finns ej")

    if not recipe:
        return "Recipe not found"
    
    try:
        amount = float(amount)
    except ValueError:
        input_check = False
        flash('Mängden måste vara ett nummer', 'warning')
    if input_check:
        new_ingredient = Ingredient.query.filter_by(name=ingredient_name, recipe_id=recipe_id).first()
        if not new_ingredient:
            new_ingredient = Ingredient(name=ingredient_name, amount=amount, unit=unit, recipe_id=recipe_id)
            db.session.add(new_ingredient)
            db.session.commit()
            flash(f"La till {ingredient_name} till {recipe.name}", 'success')
        else:
            try:
                if new_ingredient.unit == unit:
                    new_ingredient.amount = float(new_ingredient.amount) + amount
                else: 
                    new_ingredient.amount = float(new_ingredient.amount) + amount * convert_unit(unit, new_ingredient.unit)
                db.session.commit()
                flash(f"Uppdaterade mängden för {ingredient_name} i {recipe.name}", 'success')            
            except:
                flash('Ingrediensen kunde ej läggas till', 'warning')
    return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')
    

def remove_ingredient(user_id, recipe_id, ingredient_id):
    try:
        db.session.delete(Ingredient.query.get(ingredient_id))
        db.session.commit()
    except:
        db.session.rollback()
        flash('Ingrediensen kunde ej tas bort' , 'warning')
    return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')


#Converts units. 
def convert_unit(fromUnit, toUnit):
    fromUnit = str(fromUnit).lower().strip()
    toUnit = str(toUnit).lower().strip()
    if fromUnit in Ingredient.unitsVolume and toUnit in Ingredient.unitsVolume:
        return Ingredient.unitsVolume[fromUnit] / Ingredient.unitsVolume[toUnit]
    elif fromUnit in Ingredient.unitsWeight.keys() and toUnit in Ingredient.unitsWeight.keys():
        return Ingredient.unitsWeight[fromUnit] / Ingredient.unitsWeight[toUnit]
    elif fromUnit in Ingredient.unitsDistinct.keys() and toUnit in Ingredient.unitsDistinct.keys():
        return Ingredient.unitsDistinct[fromUnit] / Ingredient.unitsDistinct[toUnit]
    else:
        raise TypeError
    
#Changes the unit specified to the ingredient_id and the 
def change_unit(user_id, recipe_id, newUnit, ingredient_id):
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        ingredient.amount = ingredient.amount * convert_unit(ingredient.unit, newUnit)
        ingredient.unit = newUnit
        db.session.commit()
        flash('Enhet uppdaterad', 'success')
    except:
        flash('Kunde inte ändra enhet', 'warning')
    if recipe_id:
        return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')
    else:
        return 

def edit_ingredient(new_name, new_amount, new_unit, ingredient_id):
    try:
        new_amount = float(new_amount)
    except ValueError:
        flash('Mängden måste vara ett nummer', 'warning')
        return
    if not (new_unit in Ingredient.unitsWeight.keys() or new_unit in Ingredient.unitsVolume.keys() or new_unit in Ingredient.unitsDistinct.keys()):
        flash('Enheten finns ej', 'warning')
        return
    try:
        ingredient = Ingredient.query.get(ingredient_id)
        ingredient.name = new_name
        ingredient.amount = new_amount
        ingredient.unit = new_unit
        db.session.commit()
        flash('Ingrediensen redigerad', 'success')
    except Exception as e:
        flash('Ingrediensen kunde ej ändras', 'warning')


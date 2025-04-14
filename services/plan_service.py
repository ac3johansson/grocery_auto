from flask import flash, redirect
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.plan import Plan
from models import db
from services import ingredient_service
import random


def add_plan(user_id, recipe_name):
    if recipe_name:
        new_recipe = Plan(name=recipe_name, user_id=user_id)
        try:
            db.session.add(new_recipe)
            db.session.commit()
            flash('Månadsplanen tillagd', 'success')
        except:
            flash('Kunde inte lägga till månadsplan', 'error')
    else:
        flash('Kunde inte lägga till månadsplan', 'error')
    return redirect(f'/user/{user_id}/planbank')

def remove_plan(user_id, plan_id):
    try:
        db.session.delete(Plan.query.get(plan_id))
        db.session.commit()
    except:
        flash("Månadsplanen kunde ej tas bort")
    return redirect(f'/user/{user_id}/planbank')

def find_recipes(user_id, recipe_name=None, recipe_ingredient=None, recipe_tag=None):
    #Ingredient.query.filter(Ingredient.name.icontains(recipe_ingredient)).all() # Lista med ingredeiens objekt 
    query = Recipe.query
    if user_id:
        query = query.filter(Recipe.user_id == user_id)
    if recipe_name:
        query = query.filter(Recipe.name.icontains(recipe_name))
    if recipe_tag:
        query = query.filter(Recipe.tag.icontains(recipe_tag))
    if recipe_ingredient:
        query = query.outerjoin(Recipe.ingredients).filter(Ingredient.name.icontains(recipe_ingredient))
    if query.count() == 0:
        flash("Inga recept hittade", "warning")
        return []
    else:
        return query.distinct().all()

def random_recipes(user_id, recipe_tag=None):
    query = Recipe.query
    if user_id is not None:
        query = query.filter(Recipe.user_id == user_id)
    if recipe_tag is not None:
        query = query.filter(Recipe.tag.icontains(recipe_tag))
    if query.count() == 0:
        flash("Inga recept hittade", "warning")
        return []
    else:
        return [random.choice(query.distinct().all())]
    
def add_to_plan(plan, recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe in plan.recipes:
        flash('Receptet finns redan i månadsplanen', 'error')
        return
    else:
        try:
            plan.recipes.append(recipe)
            db.session.commit()
            flash('Recept tillagt i inköpslistan', 'success')
        except Exception as e:
            db.session.rollback()  # Important to prevent session corruption
            flash('Kunde inte lägga till recept', 'error')

def remove_from_plan(plan, recipe_id):
    recipe = Recipe.query.get(recipe_id)
    try:
        if recipe in plan.recipes:
            plan.recipes.remove(recipe)
            db.session.commit()
            flash('Recept borttaget från inköpslistan', 'success')
        else:
            flash('Recept finns inte i inköpslistan', 'warning')
    except:
        db.session.rollback()  # Important to prevent session corruption
        flash('Receptet kunde ej tas bort från inköpslistan', 'error')

def generate_plan_ingredients(plan):
    # ingredient_list = {name; Ingredient}
    ingredient_dict = {}
    for recipe in plan.recipes:
        recipe_ingredients = Ingredient.query.filter(Ingredient.recipe_id == recipe.id).all()
        for ingredient in recipe_ingredients:
            if str(ingredient.name).lower().strip() in ingredient_dict.keys():
                ingre = ingredient_dict[ingredient.name] #Ingredient already in the dictionary
                if can_convert_unit(ingredient_dict[ingredient.name], ingredient):
                    ingre.amount = ingre.amount + ingredient.amount * ingredient_service.convert_unit(ingredient.unit, ingre.unit)
            else: 
                ingredient_dict[ingredient.name] = ingredient
    return ingredient_dict.values()

# Checks if units of 2 ingredients can be converted to the same unit 
def can_convert_unit(i1, i2):
    if (i1.unit == i2.unit):
        return True
    elif (i1.unit in Ingredient.unitsWeight) and (i2.unit in Ingredient.unitsWeight):
        return True
    elif(i1.unit in Ingredient.unitsVolume) and (i2.unit in Ingredient.unitsVolume):
        return True
    else:
        return False
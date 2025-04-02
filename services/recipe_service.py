from flask import flash, redirect
from models.recipe import Recipe
from models.ingredient import Ingredient
from models import db

def add_recipe(user_id, recipe_name, recipe_link, recipe_tag):
    if recipe_name and recipe_link and recipe_tag:
        new_recipe = Recipe(name=recipe_name, link=recipe_link, tag=recipe_tag, user_id=user_id)
        try:
            db.session.add(new_recipe)
            db.session.commit()
            flash('Receptet tillagt', 'success')
        except:
            flash('Kunde inte lägga till recept', 'error')
    else:
        flash('Kunde inte lägga till recept', 'error')
    return redirect(f'/user/{user_id}/recipebank')

def remove_recipe(user_id, recipe_id):
    try:
        db.session.delete(Recipe.query.get(recipe_id))
        db.session.commit()
    except:
        flash("Receptet kunde ej tas bort")
    return redirect(f'/user/{user_id}/recipebank')

def find_by_name(user_id, recipe_name):
    pass

def find_by_ingredient(user_id, recipe_ingredient):
    pass

def find_by_tag(user_id, recipe_tag):
    pass
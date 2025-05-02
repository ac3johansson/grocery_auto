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
        except Exception as e:
            db.session.rollback()  # Important to prevent session corruption
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

def edit_recipe(new_name, new_link, new_tag, recipe_id):
    try:
        recipe = Recipe.query.get(recipe_id)
        recipe.name = new_name
        recipe.link = new_link
        recipe.tag = new_tag
        db.session.commit()
        flash('Receptet redigerad', 'success')
    except Exception as e:
        flash('Receptet kunde ej ändras', 'warning')
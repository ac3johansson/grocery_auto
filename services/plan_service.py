from flask import flash, redirect
from models.recipe import Recipe
from models.plan import Plan
from models import db


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
    pass

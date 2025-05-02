from flask import flash, redirect
from models.recipe import Recipe
from models.ingredient import Ingredient
from models.plan import Plan
from models.plan_ingredient import PlanIngredient
from models import db
from services import ingredient_service
import random
from collections import defaultdict


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
        flash('Receptet finns redan i månadsplanen', 'warning')
        return
    else:
        try:
            plan.recipes.append(recipe)
            db.session.commit()
            flash('Recept tillagt i inköpslistan', 'success')
        except Exception as e:
            db.session.rollback()  # Important to prevent session corruption
            flash('Kunde inte lägga till recept', 'warning')

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
    for recipe in plan.recipes:
        recipe_ingredients = recipe.ingredients
        for recipe_ingredient in recipe_ingredients:
            plan_ingredient = PlanIngredient.query.filter(PlanIngredient.name==str(recipe_ingredient.name).lower().strip(), PlanIngredient.plan_id==plan.id).first()
            try:
                plan_ingredient.amount = plan_ingredient.amount + recipe_ingredient.amount * ingredient_service.convert_unit(recipe_ingredient.unit, plan_ingredient.unit)
            except Exception as e:
                plan_ingredient = PlanIngredient(name=recipe_ingredient.name, amount=recipe_ingredient.amount, unit=recipe_ingredient.unit, plan_id=plan.id, fromRecipe=True)
                try:
                    db.session.add(plan_ingredient)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()  # Important to prevent session corruption
    return plan.ingredients

def change_planingredient_unit(user_id, plan_id, newUnit, ingredient_id):
    try:
        ingredient = PlanIngredient.query.get(ingredient_id)
        ingredient.amount = ingredient.amount * ingredient_service.convert_unit(ingredient.unit, newUnit)
        ingredient.unit = newUnit
        db.session.commit()
        flash('Enhet uppdaterad', 'success')
    except:
        flash('Kunde inte ändra enhet', 'warning')

def merge_ingredients(name, ingredient_ids, plan_id):
    total_amount = 0
    unit = None
    try:
        for ingredient_id in ingredient_ids:
            ingredient = PlanIngredient.query.get(ingredient_id)
            if not unit:
                unit = ingredient.unit
                total_amount = ingredient.amount
            else:
                total_amount += ingredient.amount * ingredient_service.convert_unit(ingredient.unit, unit)
            db.session.delete(ingredient)
        merge_ingredient = PlanIngredient(name=name, amount=total_amount, unit=unit, plan_id=plan_id, fromRecipe=True)
        db.session.add(merge_ingredient)
        db.session.commit()
        flash('Ingredienserna slogs ihop', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Kunde inte slå ihop ingredienser', 'warning')


def clear_plan_ingredients(plan):
    try:
        PlanIngredient.query.filter_by(plan_id=plan.id, fromRecipe=True).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def add_extra_ingredient(ingredient_name, amount, unit, plan_id):
    try:
        amount = float(amount)
    except ValueError:
        input_check = False
        flash('Mängden måste vara ett nummer', 'warning')
    
    new_ingredient = PlanIngredient.query.filter_by(name=str(ingredient_name).strip().lower(), plan_id=plan_id).first()
    if not new_ingredient:
        try:
            new_ingredient = PlanIngredient(name=ingredient_name, amount=amount, unit=unit, plan_id=plan_id, fromRecipe=False)
            db.session.add(new_ingredient)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash("Kunde inte lägga till recept")

    else:
        try:
            new_ingredient.amount += amount * ingredient_service.convert_unit(unit, new_ingredient.unit)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('Enheten finns ej', 'warning')

def remove_plan_ingredient(ingredient_id):
    try:
        db.session.delete(PlanIngredient.query.get(ingredient_id))
        db.session.commit()
    except:
        db.session.rollback()
        flash('Ingrediensen kunde ej tas bort' , 'warning')

def edit_extra_ingredient(new_name, new_amount, new_unit, ingredient_id):
    try:
        new_amount = float(new_amount)
    except ValueError:
        flash('Mängden måste vara ett nummer', 'warning')
        return
    if not (new_unit in PlanIngredient.unitsWeight.keys() or new_unit in PlanIngredient.unitsVolume.keys() or new_unit in PlanIngredient.unitsDistinct.keys()):
        flash('Enheten finns ej', 'warning')
        return
    try:
        ingredient = PlanIngredient.query.get(ingredient_id)
        ingredient.name = new_name
        ingredient.amount = new_amount
        ingredient.unit = new_unit
        db.session.commit()
        flash('Ingrediensen redigerad', 'success')
    except Exception as e:
        flash('Ingrediensen kunde ej ändras', 'warning')
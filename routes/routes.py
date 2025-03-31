from flask import request, Blueprint, render_template, url_for, redirect, session, flash
from services.recipe_service import *
from services.ingredient_service import *
from services.user_service import *


routes = Blueprint('routes', __name__)  # Create a Blueprint

#Homepage route
@routes.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')    
        if action == 'add':
            add_username = request.form.get('add_username')
            if add_username and not User.query.filter_by(username=add_username).first():
                new_user = User(username=request.form['add_username'])
                if new_user:
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Användare skapad", "success")  # Flash error message
            else:
                flash("Användarnamnet är upptaget eller ogiltigt", "error")  # Flash error message
            return redirect('/')

        elif action == 'remove': 
            remove_username = request.form.get('remove_username')
            if remove_username:
                remove_user = User.query.filter_by(username=request.form['remove_username']).first() 
                if remove_user:
                    db.session.delete(remove_user)
                    db.session.commit()
            return redirect('/')


    else:
        users = User.query.order_by(User.username).all()
        return render_template('index.html', users=users)

#Recipebank route
@routes.route('/user/<int:user_id>/recipebank', methods=['GET', 'POST'])
def recipebank(user_id):
    if 'prev_url' not in session:  # Store previous page URL if not already set
        session['prev_url'] = request.referrer


    if request.method == 'POST':
        recipe_name = request.form['name']
        recipe_link = request.form['link']
        recipe_tag = request.form['tag']
        #recipe_tags_string = request.form['tag']
        #recipe_tags = recipe_tags_string.split()
        if recipe_name and recipe_link and recipe_tag:
            new_recipe = Recipe(name=recipe_name, link=recipe_link, tag=recipe_tag, user_id=user_id)
            try:
                db.session.add(new_recipe)
                db.session.commit()
                flash('Receptet tillagt', 'success')
                return redirect(f'/user/{user_id}/recipebank')
            except:
                flash('Kunde inte lägga till recept', 'error')
                return redirect(f'/user/{user_id}/recipebank')

    else:
        user = User.query.get(user_id)  # Find the user by ID
        if not user:
            return "User not found", 404  # Handle invalid users

        recipes = Recipe.query.filter_by(user_id=user.id).all()  # Get only this user's recipes
        return render_template('recipebank.html', recipes=recipes, user=user)
        
        # recipes = Recipe.query.order_by(Recipe.name).all()
        # return render_template('recipebank.html', recipes=recipes)

#HÄR ÄR JAG!
#Ingredient for recipe route
@routes.route('/user/<int:user_id>/recipebank/<int:recipe_id>/ingredients', methods=['GET', 'POST'])
def ingredients(user_id, recipe_id):
    if 'prev_url' not in session:  # Store previous page URL if not already set
        session['prev_url'] = request.referrer

    if request.method == 'POST':
        value = request.form.get('action')
        if value == "add":
            ingredient_name = request.form['name']
            ingredient_amount = request.form['amount']
            ingredient_unit = request.form['unit']
            if ingredient_name and ingredient_amount and ingredient_unit:
                return add_ingredient(user_id=user_id, recipe_id=recipe_id, ingredient_name=ingredient_name, amount=ingredient_amount, unit=ingredient_unit)
        elif value in Ingredient.unitsWeight.keys() or value in Ingredient.unitsVolume.keys() or value in Ingredient.unitsDistinct:
            return change_unit(user_id, recipe_id , value, request.form.get('ingredient_id'))
        elif value == "remove":
            return remove_ingredient(user_id, recipe_id, request.form.get('ingredient_id'))
        else:
            return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')
    else:
        user = User.query.get(user_id) # Find the user by ID
        recipe = Recipe.query.get(recipe_id) # Find the recipe by ID
        if not recipe:
            return "Recipe not found", 404  # Handle invalid recipe
        if not user:
            return "User not found", 404 # Handle invalid user

        ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()  # Get only this user's recipes
        return render_template('ingredients.html', ingredients=ingredients, recipe=recipe, user=user) 
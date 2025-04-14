from flask import request, Blueprint, render_template, url_for, redirect, session, flash
from services.recipe_service import *
from services.ingredient_service import *
from services.user_service import *
from services.plan_service import *


routes = Blueprint('routes', __name__)  # Create a Blueprint

#Homepage route
@routes.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            username = request.form.get('add_username')
            return create_user(username)
        elif action == 'remove': 
            username = request.form.get('remove_username')
            return remove_user(username)
    else:
        users = User.query.order_by(User.username).all()
        return render_template('index.html', users=users)

#Recipebank route
@routes.route('/user/<int:user_id>/recipebank', methods=['GET', 'POST'])
def recipebank(user_id):
    if 'prev_url' not in session:  # Store previous page URL if not already set
        session['prev_url'] = request.referrer

    if request.method == 'POST':
        value = request.form.get('action')
        if value == "add":
            recipe_name = request.form['name']
            recipe_link = request.form['link']
            recipe_tag = request.form['tag']
            #recipe_tags_string = request.form['tag']
            #recipe_tags = recipe_tags_string.split()
            return add_recipe(user_id, recipe_name, recipe_link, recipe_tag)
        elif value == "remove":
            return remove_recipe(user_id, request.form.get('recipe_id'))
        else:
            return redirect(f'/user/{user_id}/recipebank')

    else:
        user = User.query.get(user_id)  # Find the user by ID
        if not user:
            return "User not found", 404  # Handle invalid users

        recipes = Recipe.query.filter_by(user_id=user.id).all()  # Get only this user's recipes
        return render_template('recipebank.html', recipes=recipes, user=user)
        
        # recipes = Recipe.query.order_by(Recipe.name).all()
        # return render_template('recipebank.html', recipes=recipes)

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
    
#Plans route
@routes.route('/user/<int:user_id>/planbank', methods=['GET', 'POST'])
def plans(user_id):
    if 'prev_url' not in session:  # Store previous page URL if not already set
        session['prev_url'] = request.referrer

    if request.method == 'POST':
        value = request.form.get('action')
        if value == "add":
            plan_name = request.form['name']
            return add_plan(user_id, plan_name)
        elif value == "remove":
            return remove_plan(user_id, request.form.get('plan_id'))
        else:
            return redirect(f'/user/{user_id}/planbank')

    else:
        user = User.query.get(user_id) # Find the user by ID
        if not user:
            return "User not found", 404 # Handle invalid user

        plans = Plan.query.filter_by(user_id=user.id).all()  # Get only this user's plans
        return render_template('planbank.html', plans=plans, user=user) 
    
#Planmaker route
@routes.route('/user/<int:user_id>/planbank/<int:plan_id>/planmaker', methods=['GET', 'POST'])
def planmaker(user_id, plan_id):
    if 'prev_url' not in session:  # Store previous page URL if not already set
        session['prev_url'] = request.referrer

    # Get user and plan (with 404 handling)
    user = User.query.get_or_404(user_id)
    plan = Plan.query.get_or_404(plan_id)

    if request.method == 'POST':
        #Initalize passing strings 
        recipe_name = None
        recipe_ingredient = None
        recipe_tag_search = None
        recipe_tag_random = None

        #Initalize search and random lists
        found_recipes = []
        randomized_recipes = []

        #POST Requests
        value = request.form.get('action')

        if value == "search":
            recipe_name = request.form.get('recipe_name', '')
            recipe_ingredient = request.form.get('recipe_ingredient', '')
            recipe_tag_search = request.form.get('tag_search', '')
            found_recipes = find_recipes(user_id, recipe_name, recipe_ingredient, recipe_tag_search) #Returns list of found recipes using search function
        elif value == "random":
            recipe_tag_random = request.form.get('tag_random', '')
            randomized_recipes = random_recipes(user_id, recipe_tag_random) #Returns list of randomized recipes using random function
        elif value == "add":
            recipe_id = request.form.get('recipe_id')
            add_to_plan(plan, recipe_id)
            found_recipes = find_recipes(user_id, recipe_name, recipe_ingredient, recipe_tag_search) #Returns list of found recipes using search function
        elif value == "remove_recipe":
            recipe_id = request.form.get('recipe_id')
            remove_from_plan(plan, recipe_id)
        elif value == "edit_recipe":
            pass
        else:
            pass

        recipes_plan = plan.recipes  # Get only this plan's recipes

        return render_template(
            'planmaker.html', 
            #lists
            recipes_search=found_recipes, 
            recipes_random=randomized_recipes, 
            recipes_plan=recipes_plan,
            #strings
            recipe_name=recipe_name,
            recipe_ingredient=recipe_ingredient,
            recipe_tag_search=recipe_tag_search,
            recipe_tag_random=recipe_tag_random,
            #objects
            user=user,
            plan=plan
        )

    else:
        recipes_plan = plan.recipes  # Get only this plan's recipes
        return render_template(
            'planmaker.html',
            
            #objects
            user=user,
            plan=plan,
            
            #lists
            recipes_plan=recipes_plan
        )

#HÄR ÄR JAG
#Planmaker route 
@routes.route('/user/<int:user_id>/planbank/<int:plan_id>/planmaker/ingredients', methods=['GET', 'POST'])
def planmaker_ingredients(user_id, plan_id):
    if 'prev_url' not in session:  # Store previous page URL if not already set
        session['prev_url'] = request.referrer

    # Get user and plan (with 404 handling)
    user = User.query.get_or_404(user_id)
    plan = Plan.query.get_or_404(plan_id)

    ingredients = generate_plan_ingredients(plan)  # Get only this user's recipes
    return render_template('planmaker_ingredients.html', ingredients=ingredients, recipe=None, plan=plan, user=user) 
from flask import request, Blueprint, render_template, url_for, redirect, session, flash
from sqlalchemy import func
from services.recipe_service import *
from services.ingredient_service import *
from services.user_service import *
from services.plan_service import *


routes = Blueprint('routes', __name__)  # Create a Blueprint

@routes.before_request
def track_history():
    if 'history' not in session:
        session['history'] = []

    # Only track GET requests, to avoid form posts messing it up
    if request.method == 'GET' and request.endpoint not in ('static',):
        current_url = request.path  # only the path, not full URL
        history = session['history']

        # Don't duplicate if refreshing the page
        if not history or history[-1] != current_url:
            history.append(current_url)

        # Keep the history from getting too big (optional)
        if len(history) > 10:
            history.pop(0)

    session.modified = True  # Ensure changes are saved

@routes.context_processor
def inject_back_url():
    history = session.get('history', [])
    if len(history) >= 2:
        back_url = history[-2]
    else:
        back_url = url_for('routes.index')
    return dict(back_url=back_url)

@routes.route('/back', endpoint='go_back')
def go_back():
    history = session.get('history', [])

    if len(history) >= 2:
        history.pop()  # Remove current page from history
        history.pop()
        back_url = history[-1]  # Go to the previous page

        # If the back URL is the same as the current one, then just go to the homepage
        if back_url == request.path:
            return redirect(url_for('routes.index'))

        session['history'] = history
        session.modified = True
        return redirect(back_url)
    else:
        return redirect(url_for('routes.index'))


#Homepage route
@routes.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        value = request.form.get('action')
        if value == 'add':
            username = request.form.get('add_username')
            return create_user(username)
        elif value == 'remove': 
            username = request.form.get('remove_username')
            return remove_user(username)
        elif value == 'edit':
            user_id = request.form.get('user_id')
            new_username = request.form.get('name')
            edit_user(user_id=user_id, new_username=new_username)
        return redirect('/')
    else:
        users = User.query.order_by(func.lower(User.username)).all()
        return render_template('index.html', users=users)

#Recipebank route
@routes.route('/user/<int:user_id>/recipebank', methods=['GET', 'POST'])
def recipebank(user_id):
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
        elif value == "edit":
            recipe_name = request.form['name']
            recipe_link = request.form['link']
            recipe_tag = request.form['tag']
            recipe_id = request.form['recipe_id']
            edit_recipe(recipe_name, recipe_link, recipe_tag, recipe_id)
        return redirect(f'/user/{user_id}/recipebank')

    else:
        user = User.query.get(user_id)  # Find the user by ID
        highlight_id = request.args.get('highlight_id')
        if not user:
            return "User not found", 404  # Handle invalid users

        recipes = Recipe.query.filter_by(user_id=user.id).all()  # Get only this user's recipes
        return render_template('recipebank.html', 
                               highlight_id=highlight_id,
                               recipes=recipes, 
                               user=user)
        
        # recipes = Recipe.query.order_by(Recipe.name).all()
        # return render_template('recipebank.html', recipes=recipes)

#Ingredient for recipe route
@routes.route('/user/<int:user_id>/recipebank/<int:recipe_id>/ingredients', methods=['GET', 'POST'])
def ingredients(user_id, recipe_id):
    if request.method == 'POST':
        value = request.form.get('action')
        if value == "add":
            ingredient_name = request.form['name']
            ingredient_amount = request.form['amount']
            ingredient_unit = request.form['unit']
            if ingredient_name and ingredient_amount and ingredient_unit:
                return add_ingredient(user_id=user_id, recipe_id=recipe_id, ingredient_name=ingredient_name, amount=ingredient_amount, unit=ingredient_unit)
        elif value == "edit":
            edit_name = request.form['name']
            edit_amount = request.form['amount']
            edit_unit = request.form['unit']
            ingredient_id = request.form['ingredient_id']
            edit_ingredient(edit_name, edit_amount, edit_unit, ingredient_id=ingredient_id)
        elif value in Ingredient.unitsWeight.keys() or value in Ingredient.unitsVolume.keys() or value in Ingredient.unitsDistinct.keys():
            return change_unit(user_id, recipe_id=recipe_id, newUnit=value, ingredient_id=request.form.get('ingredient_id'))
        elif value == "remove":
            return remove_ingredient(user_id, recipe_id, request.form.get('ingredient_id'))

        return redirect(f'/user/{user_id}/recipebank/{recipe_id}/ingredients')
    else:
        user = User.query.get(user_id) # Find the user by ID
        recipe = Recipe.query.get(recipe_id) # Find the recipe by ID
        if not recipe:
            return "Recipe not found", 404  # Handle invalid recipe
        if not user:
            return "User not found", 404 # Handle invalid user

        ingredients = Ingredient.query.filter_by(recipe_id=recipe.id).all()  # Get only this user's recipes
        return render_template('ingredients.html', 
                               ingredients=ingredients, 
                               recipe=recipe, 
                               user=user) 
    
#Plans route
@routes.route('/user/<int:user_id>/planbank', methods=['GET', 'POST'])
def plans(user_id):
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
        return render_template('planbank.html',
                               plans=plans, 
                               user=user) 
    
#Planmaker route
@routes.route('/user/<int:user_id>/planbank/<int:plan_id>/planmaker', methods=['GET', 'POST'])
def planmaker(user_id, plan_id):
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
            session['prev_value'] = "search"
        elif value == "random":
            recipe_tag_random = request.form.get('tag_random', '')
            randomized_recipes = random_recipes(user_id, recipe_tag_random) #Returns list of randomized recipes using random function
            session['prev_value'] = "random"
        elif value == "add":
            recipe_id = request.form.get('recipe_id')
            add_to_plan(plan, recipe_id)
            if session['prev_value'] == "search":
                found_recipes = find_recipes(user_id, recipe_name, recipe_ingredient, recipe_tag_search) #Returns list of found recipes using search function
            else:
                found_recipes = []
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

#Planmaker route 
@routes.route('/user/<int:user_id>/planbank/<int:plan_id>/planmaker/ingredients', methods=['GET', 'POST'])
def planmaker_ingredients(user_id, plan_id):
    # Get user and plan (with 404 handling)
    user = User.query.get_or_404(user_id)
    plan = Plan.query.get_or_404(plan_id)

    plan_ingredients = PlanIngredient.query.filter_by(plan_id = plan.id, fromRecipe = True).all() 
    plan_ingredients_extra = PlanIngredient.query.filter_by(plan_id = plan.id, fromRecipe = False).all() 

    if request.method == 'POST':
        value = request.form.get('action')
        if value == "add":
            name = request.form.get('name')
            amount = request.form.get('amount')
            unit = request.form.get('unit')
            add_extra_ingredient(ingredient_name=name, amount=amount, unit=unit, plan_id=plan_id)
        elif value in PlanIngredient.unitsWeight.keys() or value in PlanIngredient.unitsVolume.keys() or value in PlanIngredient.unitsDistinct.keys():
            change_planingredient_unit(user_id=user_id, plan_id=plan_id, newUnit=value, ingredient_id=request.form.get('ingredient_id'))
            #change_unit_dict(newUnit=value, key=key, ingredient_dict=plan_ingredients[key])
        elif value == "merge":
            ingredients = request.form.get("selected_ingredients")  # e.g., "1,2,3"
            name = request.form.get("assembled_name")
            ingredient_ids = [int(i) for i in ingredients.split(",")] if ingredients else []
            merge_ingredients(name=name, ingredient_ids=ingredient_ids, plan_id=plan_id)
        elif value == "generate":
            clear_plan_ingredients(plan)
            generate_plan_ingredients(plan)
        elif value == "remove_ingredient":
            ingredient_id = request.form.get('ingredient_id')
            remove_plan_ingredient(ingredient_id=ingredient_id)
        elif value == "remove_recipe":
            recipe_id = request.form.get('recipe_id')
            remove_from_plan(plan, recipe_id)
        elif value == "edit_ingredient":
            edit_name = request.form['name']
            edit_amount = request.form['amount']
            edit_unit = request.form['unit']
            ingredient_id = request.form['ingredient_id']
            edit_extra_ingredient(edit_name, edit_amount, edit_unit, ingredient_id=ingredient_id)
        return render_template(
            'planmaker_ingredients.html',
            ingredients=PlanIngredient.query.filter_by(plan_id = plan.id, fromRecipe = True).all(), 
            ingredients_extra=PlanIngredient.query.filter_by(plan_id = plan.id, fromRecipe = False).all(), 
            recipe=None, 
            recipes_plan=plan.recipes, 
            plan=plan, 
            user=user
            )
    else:
        return render_template(
            'planmaker_ingredients.html', 
            ingredients=plan_ingredients,
            ingredients_extra=plan_ingredients_extra, 
            recipe=None, 
            recipes_plan=plan.recipes, 
            plan=plan, user=user) 
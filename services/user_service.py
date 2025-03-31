from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models import db

def create_user(username):
    new_user = User.query.filter_by(name=username).first()
    
    if not new_user:
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return "Användare skapad"
    else:
        return "Användarnamnet är upptaget"

def remove_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return "Kunde inte hitta användaren"
    
    db.session.delete(user)
    db.session.commit()
    


def add_recipe(user_id, recipe_name, link, tag):
    user = User.query.get(user_id)

    if not user:
        return "Kunde inte hitta användaren"

    new_recipe = Recipe(name=recipe_name, link=link, tag=Tag(name=tag))
    db.session.add(new_recipe)
    db.session.commit()
    return f"La till {recipe_name} till {user.name}s receptbank"

def remove_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    
    if not recipe:
        return "Receptet hittades ej"

    db.session.delete(recipe)
    db.session.commit()
    return f"Borttaget {recipe.name}"



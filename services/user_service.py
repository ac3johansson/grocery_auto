from flask import request, redirect, flash
from models.user import User
from models.recipe import Recipe
from models.tag import Tag
from models import db

def create_user(username):
    try:
        if not User.query.filter_by(username=username).first():
            new_user = User(username=username)
            if new_user:
                db.session.add(new_user)
                db.session.commit()
                flash("Användare skapad", "success")  # Flash error message
            else:
                flash("Användare kunde ej skapas", "error")
        else: 
            flash("Användarnamnet är upptaget", "error")
    except: 
        flash("Användaren kunde ej skapas", "error")
    return redirect('/')

def remove_user(username):
    try:
        remove_user = User.query.filter_by(username=username).first() 
        if remove_user:
            db.session.delete(remove_user)
            db.session.commit()
        else:
            flash("Användaren hittades ej", "error")
    except:
        flash("Användaren kunde ej raderas", "error")
    return redirect('/')
    


# def add_recipe(user_id, recipe_name, link, tag):
#     user = User.query.get(user_id)

#     if not user:
#         return "Kunde inte hitta användaren"

#     new_recipe = Recipe(name=recipe_name, link=link, tag=Tag(name=tag))
#     db.session.add(new_recipe)
#     db.session.commit()
#     return f"La till {recipe_name} till {user.name}s receptbank"



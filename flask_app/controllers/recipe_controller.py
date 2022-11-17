import re
from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.recipe_model import Recipe
from flask_app.models.user_model import User



@app.route( "/display/recipe" )
def display_recipe():
  if User.validate_session():
    return render_template( "recipe.html" )
  else:
    return redirect ("/")


@app.route( "/recipe/new", methods = [ 'POST'] )
def create_recipe():
  # TODO: Validate that fields are not empty
  data = {
    "names" : request.form[ 'names' ],
    "image" : request.form[ 'image'],
    "descriptions" : request.form[ 'descriptions' ],
    "instructions" : request.form[ 'instructions' ],
    "under_thirty" : request.form[ 'under_thirty' ],
    "user_id" : session[ 'user_id' ]
  }
  Recipe.create( data )
  
  return redirect( "/dashboard" )

@app.route ( "/dashboard" )
def get_recipes():
  if User.validate_session():
    recipes = Recipe.get_all()
    return render_template( "dashboard.html", recipes = recipes )
  else:
    return redirect("/")



@app.route( "/recipe/<int:id>")
def recipe_get_one( id ):
  data = {
    "id" : id
  }
  
  recipe = Recipe.get_one( data )
  
  return render_template( "display_Recipe.html", recipe = recipe )


@app.route( "/recipe/delete/<int:id>" )
def delete_recipe( id ):
  data = {
    "id" : id 
  }
  Recipe.delete_one( data )
  return redirect( "/dashboard" )

@app.route( "/recipe/edit/<int:id>")
def display_recipe_edit( id ):
  if User.validate_session():
    data = {
      "id" : id
    }
    recipe = Recipe.get_one( data )
    return render_template( "displayEditRecipe.html", recipe = recipe )
  else:
    return redirect("/")

@app.route( "/recipe/edit/<int:id>", methods = [' POST '] )
def update_recipe( id ):
  data = {
    "id" : id,
    "names" : request.form [ 'names' ],
    "image" : request.form[ 'image' ],
    "descriptions" : request.form [ 'descriptions' ],
    "instructions" : request.form[ 'instructions' ],
    "under_thirty" : request.form[ 'under_thirty' ],
    "user_id" : session[ 'user_id' ],
    "created_at" : request.form [ 'created_at']
  }
  Recipe.update_one( data )
  return redirect( "/dashboard" )
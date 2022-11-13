from flask import session, request, render_template, redirect, flash
from flask_app import app
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt ( app )

@app.route( "/" )
def display_login_registration():
  return render_template( "loginRegistration.html" )


# This is validating the email exist
# If it doesnt exit then you create a new one
@app.route( "/user/new", methods = ['POST'] )
def create_user():
  
  if User.validate_register == True:
  
    data = {
      "email" : request.form[ 'email' ]
    }
    result = User.get_one( data )
    if result == None:
      # Add the new user
      data ={
        "email" : request.form['email'],
        "first_name" :request.form['first_name'],
        "last_name" :request.form['last_name'],
        "password" : bcrypt.generate_password_hash( request.form[ 'password'] )
      }
      user_id = User.create( data )
      
      session[ 'email' ] = request.form[ 'email' ],
      session[ 'first_name' ] = request.form[ 'first_name' ],
      session[ 'last_name' ] = request.form[ 'last_name' ]
      session[ 'user_id' ] = user_id
      return redirect ( "/dashboard" )
    else:
      flash( "That email already exists, please select another one.", "error_register_email" )
      pass
  else:
    return redirect ( "/" )



@app.route( "/logout" )
def logout():
  session.clear()
  return redirect ("/")



@app.route( "/login", methods = [ 'POST' ] )
def login():
  data = {
    "email" : request.form [ 'email' ] #Making sure to validate the email
  }
  result = User.get_one( data ) 
  
  if result == None:
    flash( "Wrong credentials.", "error_login")
    return redirect ("/") #if wrong conditions back to index.html
  else:
    if not bcrypt.check_password_hash( result.password, request.form[ 'password'] ):
      flash( "wrong password", "error_login")
      return redirect ("/") #if wrong conditions back to index.html
    else:
      session[ 'email' ] = result.email
      session[ 'first_name' ] = result.first_name
      session[ 'last_name' ] = result.last_name
      session[ 'user_id' ] = result.id
      return redirect( "/dashboard" ) #If all conditions meet it will go to dashboard

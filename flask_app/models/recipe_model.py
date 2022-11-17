from flask_app import DATABASE

from flask_app.config.mysqlconnection import connectToMySQL


class Recipe:
  def __init__( self, data ):
    self.id = data[ 'id']
    self.names = data ['names']
    self.image = data ['image']
    self.descriptions = data [ 'descriptions' ]
    self.instructions = data ['instructions']
    self.created_at = data ['created_at']
    self.updated_at = data ['updated_at']
    self.under_thirty = data ['under_thirty']
    self.user_id = data ['user_id']

  @classmethod
  def create( cls, data ):
    query = "INSERT INTO recipes ( names, image, descriptions, instructions, under_thirty, user_id ) VALUES ( %(names)s, %(image)s, %(descriptions)s, %(instructions)s, %(under_thirty)s, %(user_id)s );"
    return connectToMySQL( DATABASE ).query_db( query, data )

  @classmethod
  def get_all( cls ):
    query = "SELECT * "
    query += "FROM recipes;"
    
    result = connectToMySQL( DATABASE ).query_db( query )
    recipes = []
    
    if len( result ) > 0:
      for recipe in result:
        recipes.append( cls( recipe ) )
    return recipes

  @classmethod
  def get_one(cls, data):
    query = "SELECT * "
    query += "FROM recipes "
    query += "WHERE id = %(id)s;"
    
    result = connectToMySQL( DATABASE ).query_db( query, data )
    
    if len( result ) > 0:
      return cls( result[0] )
    else: 
      return None

  @classmethod
  def delete_one( cls, data ):
    query = "DELETE FROM recipes "
    query += "WHERE id = %(id)s;"
    
    return connectToMySQL( DATABASE ).query_db( query, data )

  @classmethod
  def update_one( cls, data):
    query = "UPDATE recipes "
    query += "SET names = %(names)s, %(image)s, description = %(descriptions)s, instructions = %(instructions)s, "
    query += "user_id = %(user_id)s, under_thirty = %(under_thirty)s, created_at = %(created_at)s;"
    
    return connectToMySQL( DATABASE ).query_db( query, data )
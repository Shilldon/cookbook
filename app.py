import os
from flask import Flask, render_template, request, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)

app.config["MONGO_DBNAME"]='milestone-3'
app.config["MONGO_URI"]='mongodb+srv://Shilldon:Palad1n1@myfirstcluster-gzjbi.mongodb.net/milestone-3'

mongo=PyMongo(app)

@app.route("/")

def index():
   # return "<h1>Hello world.</h1><h2>This is a recipe book.</h2>"

   return render_template("display_recipe.html",recipes=mongo.db.recipeDB.find())

@app.route('/display_recipe',)
def display_recipe():
    return render_template("display_recipe.html",recipes=mongo.db.recipeDB)
    
    
if __name__ =="__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)    
    
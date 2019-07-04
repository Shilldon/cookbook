import os
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)

app.config["MONGO_DBNAME"]='milestone-3'
app.config["MONGO_URI"]='mongodb+srv://Shilldon:Palad1n1@myfirstcluster-gzjbi.mongodb.net/milestone-3'

mongo=PyMongo(app)

@app.route("/")

def index():
   return render_template("index.html",title_text="Perfect dishes on demand")

@app.route("/add_recipe")

def add_recipe():
    return render_template("add_recipe.html", title_text='Add recipe')

@app.route("/insert_recipe")

def insert_recipe():
    recipes=mongo.db.recipes
    new_recipe=request.form.to_dict
    recipes.insert_one(new_recipe)
    return redirect(url_for('index'))

@app.route("/search")

def search():
    return render_template("search.html",title_text="Find your favourites")

@app.route('/display_recipe')
def display_recipe():
    return render_template("display_recipe.html",title_text="Your recipes",recipes=mongo.db.recipeDB.find())
    
    
if __name__ =="__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)    
    
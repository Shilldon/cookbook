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

@app.route("/insertrecipe", methods=['POST'])
def insertrecipe():
    recipes=mongo.db.recipeDB
    #request form data not in flat format - arrays are created in the form for ingredients and allergen information
    new_recipe=request.form.to_dict(flat=False)
    ingredients=[]
    ingredient={}
    for key, key_name in new_recipe.items():
        #flatten dict for non-array items which have become arrays through request object
        if key!='type' and key!='amount' and key!='unit' and key!='allergens':
            new_recipe[key]=new_recipe[key][0] 
        elif key=='type':
            #cycle through the ingredient information and create objects for each ingredient with key values of ingredient type, amount and units
            i=0
            for ingredient_type in key_name:
                ingredient={ 'type' : ingredient_type , 'amount' : new_recipe['amount'][i] , 'unit' : new_recipe['unit'][i] }
                print(ingredient)
                #insert ingredient object into array of ingredients
                ingredients.append(ingredient)
                print(ingredients)
                i+=1       
    #insert the new ingredients array into the new_receipe dict
    new_recipe['ingredients']=ingredients            
    
    #need to remove the type, amount and unit arrays from the dict having imported them into ingredients objects
    #done by error testing because ingredients may not have been added via the form
    try:
        del new_recipe['type']
    except KeyError:
        pass
    try:
        del new_recipe['amount']
    except KeyError:
        pass    
    try:
        del new_recipe['unit']
    except KeyError:
        pass    
    
    print("ingredients=", ingredients)        
    print("amended recipe=",new_recipe)


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
    
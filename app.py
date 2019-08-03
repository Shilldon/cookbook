import os
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)

app.secret_key=os.getenv("SECRET","randomstring123")

app.config["MONGO_DBNAME"]='milestone-3'
app.config["MONGO_URI"]='mongodb+srv://Shilldon:Palad1n1@myfirstcluster-gzjbi.mongodb.net/milestone-3'

mongo=PyMongo(app)

@app.route("/check_user",methods=['POST','GET'])
def check_user():
    usersdb=mongo.db.usersDB
    
    user=request.form.to_dict()
    if user['username']=="logout":
        session.pop('user')
    else:    
        session["user"]=user['username']
        #check if the user exists in the userDB - if not (by counting results = 0) create user
        print("users db result ",usersdb.find({"name" : user['username']}).count())
        if usersdb.find({"name" : user['username']}).count()==0: 
            usersdb.insert({'name':user['username'],'favourites':[], 'liked':[]})  
        
    return redirect(url_for('index'))

@app.route("/")
def index():
    session["filters"]={}
    return render_template("index.html",title_text='Perfect dishes on demand')

@app.route("/add_recipe")
def add_recipe():
    #get list of ingredients to display in auto complete form for ingredients in add_recipe.html
    ingredientsdb=mongo.db.ingredientsDB
    ingredients=ingredientsdb.find()
    _ingredients={}
    for ingredient in ingredients:
        new_ingredient={ingredient["name"].capitalize():None}
        _ingredients.update(new_ingredient)
        
    #get list of authors to display in auto complete form for authors in add_recipe.html
    authordb=mongo.db.authorDB
    authors=authordb.find()
    _authors={}
    for author in authors:
        new_author={author["name"]:None}
        _authors.update(new_author)

    #get list of countries to display in auto complete form for countries in add_recipe.html
    countrydb=mongo.db.countriesDB
    countries=countrydb.find()
    _countries={}
    for country in countries:
        new_country={country["name"]:None}
        _countries.update(new_country)

    return render_template("add_recipe.html", title_text='Add recipe',ingredients_list=_ingredients, author_list=_authors, country_list=_countries)

@app.route("/insertrecipe/", methods=['POST'])
def insertrecipe():
    #check whether the user is adding a new recipe or editting a recipe
    edit=request.args.get('edit',None)
        
    recipes=mongo.db.recipeDB
    usersdb=mongo.db.usersDB
    
    #if editing a recipe get the ID of the recipe to edit
    if edit=='True':
        recipe_id=ObjectId(request.args.get('recipe_id'))
    else:
        recipe_id=recipes.insert({'name':'new','favourite':[]})
    
    #request form data not in flat format - arrays are created in the form for ingredients and allergen information
    new_recipe=request.form.to_dict(flat=False)
    print("new_recipe unflattened",new_recipe)
    ingredients=[]
    ingredient={}
    #initialise cook time variable to convert hours and minutes to minutes total for ease of search DB in recipe_list
    cook_time=0
    for key, key_name in new_recipe.items():
        #flatten dict for non-array items which have become arrays through request object
        if key!='type' and key!='amount' and key!='unit' and key!='allergens':
            new_recipe[key]=new_recipe[key][0]
            if key=='favourite':
                #get the list of users for whom this is a favourite recipe
                recipe_doc=recipes.find_one({"_id" : ObjectId(recipe_id)})
                favourites=recipe_doc["favourite"]                   
                #check whether a user is logged on and if this user has marked this recipe as a favourite
                if "user" in session:
                    user_doc=usersdb.find_one({"name":session["user"]})
                    if new_recipe[key].lower() =='true':
                        #if they have and their ID is not marked in this recipe as being one of their favorites
                        #add the user id to the list of users in the recipe favourites array
                        if recipe_id not in user_doc["favourites"]:
                            usersdb.update({"name": session["user"]},{"$push":{"favourites" : recipe_id}})
                            favourites.append(str(user_doc["_id"]))
                            new_recipe[key]=favourites
                    else:
                        #if they not marked it as a favourite and their ID is in the list of users
                        #remove the user id to the list of users in the recipe favourites array                    
                        if recipe_id in user_doc["favourites"]:
                            usersdb.update({"name": session["user"]},{"$pull":{"favourites" : recipe_id}}) 
                            favourites.remove(str(user_doc["_id"]))
                        new_recipe[key]=favourites
            if key=='hours' or key=='minutes' or key=='calories':
                #convert from string to int, if needed
                try:
                    new_recipe[key]=int(new_recipe[key])
                except ValueError:
                    new_recipe[key]=0
            if key=='hours':
                #convert hours to minutes and add to cook time
                cook_time=new_recipe[key]*60
            if key=='minutes':
                cook_time=cook_time+new_recipe[key]
        elif key=='type':
            #cycle through the ingredient information and create objects for each ingredient with key values of ingredient type, amount and units
            i=0
            
            for ingredient_type in key_name:
                ingredient={ 'type' : ingredient_type.lower() , 'amount' : new_recipe['amount'][i] , 'unit' : new_recipe['unit'][i] }
                #insert ingredient object into array of ingredients
                ingredients.append(ingredient)
                i+=1       
                
    #insert the new cook_time key into the new_recipe dict
    new_recipe["cook_time"]=cook_time
    #insert the new ingredients array into the new_receipe dict
    new_recipe['ingredients']=ingredients  
    print("new_recipe[ingredients]",new_recipe['ingredients'])

    current_recipe=recipes.find_one({"_id" : ObjectId(recipe_id)})
    new_ingredients=ingredients
    print("new ingredients ",new_ingredients)
    ingredientsdb=mongo.db.ingredientsDB

    for ingredient in new_ingredients:
        ingredient_type=ingredient
        if edit=="True":
            current_ingredients=current_recipe["ingredients"]
            if ingredient in current_ingredients:
                ingredient_index=current_ingredients.index(ingredient)
                current_ingredients.remove(ingredient)
        #find the ingredient document in the ingredients database        
        new_ingredient_doc=ingredientsdb.find_one({"name" : ingredient["type"].lower()})
        
        if new_ingredient_doc!=None:
            new_ingredient_id=new_ingredient_doc["_id"]
        else:
            #if the ingredient is new and has no document create a new ID
            print("on adding ingredient[type] is ",ingredient["type"].lower())
            new_ingredient_id=ingredientsdb.insert({"name" : ingredient["type"].lower(), "recipe":[]})
            new_ingredient_doc=ingredientsdb.find_one({"_id" : new_ingredient_id})
        if recipe_id not in new_ingredient_doc["recipe"]:
            ingredientsdb.update({"_id": new_ingredient_id},{"$push":{"recipe" : recipe_id}})

    if edit=="True":
        for ingredient in current_ingredients:
            if ingredient not in new_ingredients:
                current_ingredient_doc=ingredientsdb.find_one({"name" : ingredient["type"].lower()})  
                current_ingredient_id=current_ingredient_doc["_id"]
                ingredientsdb.update({"_id": current_ingredient_id},{"$pull":{"recipe" : recipe_id}})
                current_ingredient_doc=ingredientsdb.find_one({"_id": current_ingredient_id})
                if len(current_ingredient_doc["recipe"])==0:
                    ingredientsdb.remove({"_id": current_ingredient_id})  
    
    categories=["allergens","meal","country","author"]
    for category in categories:
        if category in new_recipe:
            if type(new_recipe[category]) is list:
                new_category=new_recipe[category]
            else:    
                new_category=[]
                new_category.append(new_recipe[category])
        else:
            new_category=[]
        
        if category=="allergens":    
            categorydb=mongo.db.allergensDB
        elif category=="meal":
            categorydb=mongo.db.mealDB
        elif category=="country":
            categorydb=mongo.db.countriesDB
        elif category=="author":
            categorydb=mongo.db.authorDB            
        elif category=="difficulty":
            categorydb=mongo.db.difficultyDB   

        for value in new_category:
            #check if we are editting an existing recipe, if so check whether any values existing in both the updated and current recipes 
            #if so remove them from the list to later delete the recipe ID from the values that remain in the list
            if edit=="True":
                if category in current_recipe:
                    if type(new_recipe[category]) is list:
                        current_category=current_recipe[category]
                    else:    
                        current_category=[]
                        current_category.append(new_recipe[category])                    
                    if value in current_category:
                        category_index=current_category.index(value)
                        current_category.remove(value)
        
            #get the name of the new value in this category        
            new_category_doc=categorydb.find_one({"name" : value}) 
            if new_category_doc!=None:
                #if the particular object exists then get the associated doc
                new_category_id=new_category_doc["_id"]
            else:
                #if it doesn't exist createa a new doc with the name and the ID of this recipe
                new_category_id=categorydb.insert({"name" : value.lower(), "recipe":[]})
                new_category_doc=categorydb.find_one({"_id" : new_category_id})
            if recipe_id not in new_category_doc["recipe"]:
                #check if the recipe is already in the new doc, if it isn't add the recipe ID to this particular category in the DB
                categorydb.update({"_id" : new_category_id},{"$push":{"recipe":recipe_id}})

        if edit=="True":
            #if we are editing a recipe check whether there are any remaining values in the category list
            if category in current_recipe:
                #if so, then for all the values remove the recipe ID from the particular category in the DB
                for value in current_category:
                    if value not in new_category:
                        current_category_doc=categorydb.find_one({"name" : value})
                        current_category_id=current_category_doc["_id"]
                        categorydb.update({"_id" : current_category_id},{"$pull" : {"recipe" : recipe_id}})
                        current_category_doc=categorydb.find_one({"_id" : current_category_id})
                        #if this particular category is empty, delete it from the DB
                        if len(current_category_doc["recipe"])==0:
                            categorydb.remove({"_id" : current_category_id})


                    
    #need to remove the favourite, type, amount and unit arrays from the dict having imported them into ingredients objects and favourite array
    #done by error testing because ingredients/favourite may not have been added via the form
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

    
    #if edit=='True':
        #recipes.update({'_id':ObjectId(recipe_id)},new_recipe)
    #else:
    recipes.update({'_id':ObjectId(recipe_id)},new_recipe)
        
    return redirect(url_for('show_recipe',recipe_id=recipe_id,added_recipe="true"))

@app.route("/search")
def search():
    
    categories=["ingredients","allergens","difficulty","meal","country","author"]
    _category_lists={}
    
    for category in categories:
        item_list=[]
        if category=="ingredients":
            database=mongo.db.ingredientsDB.find().sort("name")
        elif category=="allergens":
            database=mongo.db.allergensDB.find().sort("name")
        elif category=="meal":
            database=mongo.db.mealDB.find().sort("name")
        elif category=="country":
            database=mongo.db.countriesDB.find().sort("name")

        for item in database:
            item_list.append(item["name"].capitalize())   
        
        _category_lists[category]=item_list  
    print("country list",_category_lists["allergens"])
    return render_template("search.html",title_text="Find your favourites",category_list=_category_lists)

@app.route("/recipe_list", methods=['POST','GET'])
def recipe_list():
    if session.get('sort')==True:
        _sort=session["sort"]
    else:
        _sort='none'
    _filter_dict=session["filters"]
    if _filter_dict==None:
        _filter_dict={}
        
    allergen_list=[]
    #get the action request from the page to determine what sort of list is to be displayed and display appropriate title text 
    _todo=request.args.get('action',None)
    if _todo=="delete":
        title_text_value="Delete recipes"
    elif _todo=="edit":
        title_text_value="Edit recipes"
    else:
        title_text_value="Your recipes"

    #check if the results are to be filtered/sorted using variable passed from recipe_list
    filter=request.args.get('filter',None)

    #create a list of countries and authors referred to in recipe db to generate filters in recipe_list
    list_of_countries=mongo.db.countriesDB.find()
    list_of_authors=mongo.db.authorDB.find()

    #define filter author and country for passing to filter list in recipe_list.html.
    #Will check for "" value and if so, not display author/country filter
    filter_country=""
    filter_author=""

    if filter=='true':    
        _currentsort=request.form.get('sort_by')
        print("_sort=",_sort)
        if _currentsort!=None:
            _sort=_currentsort
            session["sort"]=_sort
        else:
            filter_favourites=request.form.get('favourite')
            if filter_favourites=='true':
                user_doc=mongo.db.usersDB.find_one({"name":session["user"]})
                user_id=str(user_doc["_id"])
                _filter_dict.update({"favourite" : { "$in" : [user_id]}})
            else:
                _filter_dict.pop("favourite",None)            
                    
            filter_meal=request.form.get('meal')
            print("filter meal ",filter_meal)
            if filter_meal!="" and filter_meal!=None:
                _filter_dict.update({"meal":filter_meal})
            else:
                _filter_dict.pop("meal",None)
            
            filter_allergens=request.form.getlist('allergens')
            if filter_allergens:
                loop=0
                for allergen in filter_allergens:
                    allergen_list.append(allergen)
                filter_allergens={  '$nin' : allergen_list }   
                _filter_dict.update({"allergens" : filter_allergens}) 
            else:
                _filter_dict.pop("allergens",None)
                
            filter_calories=request.form.get('calories')
            if filter_calories!="" and filter_calories!=None:
                if filter_calories==999:
                    filter_calories={'$gt':filter_calories}
                else:
                    filter_calories={'$lt':filter_calories}  
                _filter_dict.update({"calories":filter_calories})
            else:
                _filter_dict.pop("calories",None)
                
            filter_cooktime=request.form.get('cook_time')
            if filter_cooktime!="" and filter_cooktime!=None:
                if filter_cooktime==179:
                    filter_cooktime={'$gt':filter_cooktime}
                else:
                    filter_cooktime={'$lt':filter_cooktime}  
                _filter_dict.update({"cook_time" : filter_cooktime})
            else:
                _filter_dict.pop("cook_time",None)
            filter_country=request.form.get('country')
            if filter_country!="" and filter_country!=None:
                _filter_dict.update({"country" : filter_country })
            else:
                _filter_dict.pop("country",None)
            
            filter_author=request.form.get('author')
            if filter_author!="" and filter_author!=None:
                _filter_dict.update({"author" : filter_author})
            else:
                _filter_dict.pop("author",None)
                
            session["filters"]=_filter_dict
    print("_sort",_sort)
    if filter=='true':
    #do the appropriate search and sort against the mongoDB depending on input from form/session variable

        if _sort!=None and _sort!="none":
            _recipe_list=mongo.db.recipeDB.find(_filter_dict).sort(_sort,1) 
        else:
            _recipe_list=mongo.db.recipeDB.find(_filter_dict)
    else:
        if _sort!="none" and _sort!=None:
            _recipe_list=mongo.db.recipeDB.find().sort(_sort,1) 
        else:      
            _recipe_list=mongo.db.recipeDB.find()

    #remove duplicates from the lists
    _author_list=[]
    for author in list_of_authors:
        _author_list.append(author["name"])
            
    _country_list=[]
    for country in list_of_countries:
        _country_list.append(country["name"])    
    
    _total_results=_recipe_list.count()
    return render_template("recipe_list.html",title_text=title_text_value,recipes=_recipe_list,selected_country=filter_country, selected_author=filter_author,countries=_country_list,authors=_author_list,action=_todo,filters=_filter_dict, allergens=allergen_list, sort=_sort, total_results=_total_results)

@app.route('/show_recipe/<recipe_id>')
def show_recipe(recipe_id):
    _recipe=mongo.db.recipeDB.find_one({"_id":ObjectId(recipe_id)})
    _added=request.args.get('added_recipe',None)
    #check if the user is logged on, if not pass false value for favourite so no star is shown on display_recipe.html
    if "user" in session:
        user_doc=mongo.db.usersDB.find_one({"name" : session["user"]})
        #check if this recipe is stored in this user's favourite list. If so mark pass value to mark with a star on display_recipe.html
        if ObjectId(recipe_id) in user_doc["favourites"]:
            _recipe["favourite"]=True
        else:
            _recipe["favourite"]=False    
    else:
        _recipe["favourite"]=False               
    title_text='Your recipe'
    return render_template('display_recipe.html',title_text='Your recipe',recipe=_recipe,added=_added)

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    _recipe=mongo.db.recipeDB.find_one({"_id":ObjectId(recipe_id)})
    #get list of ingredients to display in auto complete form for ingredients in add_recipe.html
    ingredientsdb=mongo.db.ingredientsDB
    ingredients=ingredientsdb.find()
    _ingredients={}
    for ingredient in ingredients:
        new_ingredient={ingredient["name"]:None}
        _ingredients.update(new_ingredient)
        
    #get list of authors to display in auto complete form for authors in add_recipe.html
    authordb=mongo.db.authorDB
    authors=authordb.find()
    _authors={}
    for author in authors:
        new_author={author["name"]:None}
        _authors.update(new_author)

    #get list of countries to display in auto complete form for countries in add_recipe.html
    countrydb=mongo.db.countriesDB
    countries=countrydb.find()
    _countries={}
    for country in countries:
        new_country={country["name"]:None}
        _countries.update(new_country)
        
    return render_template('edit_recipe.html',title_text="Edit your recipes",recipe=_recipe,ingredients_list=_ingredients, author_list=_authors, country_list=_countries)

@app.route('/delete_recipe',methods=['POST'])
def delete_recipe():
    recipe_id=request.form.get('recipe_id')
    _recipe=mongo.db.recipeDB.remove({"_id":ObjectId(recipe_id)})
    return redirect(url_for('.recipe_list',action='delete'))

@app.route('/filter_recipes', methods=['POST'])
def filter_recipes():
    session["filters"]=request.form.to_dict()
    calories=request.form["calories"]
    if calories:
        session["filters"]["calories"]=calories
    return redirect('recipe_list')

@app.route('/display_categories', methods=['POST'])
def display_categories():
    selected_categories=request.form.to_dict(flat=False)
    category=list(selected_categories.keys())[0]    
    _item_list=[]
    for key in selected_categories:
        for item in selected_categories[key]:
            if category!="country" and category!="author":
                _item_list.append(item.lower())
            else:
                _item_list.append(item)    
    category=list(selected_categories.keys())[0]
    
    i=0
    recipes_in_category={}
    search_value="$in"
    if category=="allergens":
        database=mongo.db.allergensDB
        search_value="$nin"
    elif category=="meal":
        database=mongo.db.mealDB
    elif category=="ingredients":
        database=mongo.db.ingredientsDB
    elif category=="country":
        database=mongo.db.countriesDB        
    elif category=="author":
        database=mongo.db.authorDB     
        
    for i in range(0,len(_item_list)):
        recipe_objects=database.find({"name" : {'$eq' : _item_list[i]}})
        print("recipe_objets",recipe_objects)
        recipe_ids=[]
        for recipe in recipe_objects:
            for id in recipe["recipe"]:
                recipe_ids.append(ObjectId(id))
        print("recipe_ids",recipe_ids)
        recipes_in_category[_item_list[i]]=list(mongo.db.recipeDB.find({'_id' : {search_value : recipe_ids}}))            

    
    return render_template('display_category.html',category=category,items=_item_list,recipes=recipes_in_category, title_text="Your recipes")
    
if __name__ =="__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=True)    
    
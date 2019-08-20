import os
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)

app.secret_key=os.getenv("SECRET","randomstring123")

app.config["MONGO_DBNAME"]='milestone-3'
app.config["MONGO_URI"]=os.getenv("MONGO_URI")

mongo=PyMongo(app)


#session variables:
#user - the username of the user currently logged in
#sort - a check to determine if the recipes returned in the search, delete or edit requests should be sorted into order
#filters - a list of the filters currently applied to the recipe results returned. Needed to ensure the filter is applied after leaving the search page. 
#category-form - the categories against which the user is searching

@app.route("/check_user",methods=['POST','GET'])
def check_user():
    #called on submitting login request modal form
    usersdb=mongo.db.usersDB
    
    user=request.form.to_dict()
    #logout button sends value "logout". If logout request received delete the user session variable
    if user['username']=="logout":
        session.pop('user')
    else:    
        #set the user session variable to the name submitted
        session["user"]=user['username']
        #check if the user exists in the userDB - if not (by counting results = 0) create user
        if usersdb.find({"name" : user['username']}).count()==0: 
            usersdb.insert({'name':user['username'],'favourites':[]})  
    
    #return to the index page. This is important to ensure recipes are only added or deleted when the user is logged in.
    return redirect(url_for('index'))

@app.route("/")
def index():
    #on entering the index page clear any filters and sort criteria that have been applied to search results.
    session["filters"]={}
    session["sort"]={}
    return render_template("index.html",title_text='Perfect dishes on demand')

@app.route("/add_recipe")
def add_recipe():
    #called on selecting the 'add recipe' menu option.
    
    #return all the results from the ingredients collection to create an array of ingredients names.
    #This array is passed to the autocomplete function on the page
    ingredientsdb=mongo.db.ingredientsDB
    ingredients=ingredientsdb.find()
    _ingredients={}
    for ingredient in ingredients:
        new_ingredient={ingredient["name"].capitalize():None}
        _ingredients.update(new_ingredient)

    #return all the results from the countries collection to create an array of ingredients names.
    #This array is passed to the autocomplete function on the page
    countrydb=mongo.db.countriesDB
    countries=countrydb.find()
    _countries={}
    for country in countries:
        new_country={country["name"].capitalize():None}
        _countries.update(new_country)

    return render_template("add_recipe.html", title_text='Add recipe',ingredients_list=_ingredients, country_list=_countries)

@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    #called on selecting 'edit recipe' from the menu options
    
    _recipe=mongo.db.recipeDB.find_one({"_id":ObjectId(recipe_id)})
    
    #get a list of ingredients from ingredients collection to display in the auto complete input field 
    ingredientsdb=mongo.db.ingredientsDB
    ingredients=ingredientsdb.find()
    _ingredients={}
    for ingredient in ingredients:
        new_ingredient={ingredient["name"][0].capitalize():None}
        _ingredients.update(new_ingredient)
        
    #get a list of countries from countries collection to display in the auto complete input field 
    countrydb=mongo.db.countriesDB
    countries=countrydb.find()
    _countries={}
    for country in countries:
        new_country={country["name"][0].capitalize():None}
        _countries.update(new_country)
        
    return render_template('edit_recipe.html',title_text="Edit your recipes",recipe=_recipe,ingredients_list=_ingredients, country_list=_countries)

@app.route("/insertrecipe/", methods=['POST'])
def insertrecipe():
    #called on editting an existing recipe or creating a new one in order to update or add to the recipe collection.
    
    #set variables for the recipes, user and ingredients collections
    recipes=mongo.db.recipeDB
    usersdb=mongo.db.usersDB
    ingredientsdb=mongo.db.ingredientsDB

    #check whether the user is adding a new recipe or editting a recipe
    edit=request.args.get('edit',None)
        
    #if editing a recipe get the ID of the recipe to edit
    if edit=='True':
        recipe_id=ObjectId(request.args.get('recipe_id'))
    else:
        #if the user is not editting an existing recipe create a new entry in the recipe collection
        recipe_id=recipes.insert({'name':'new','favourite':[]})
    
    #request form data is not in flat format - arrays are created in the form for ingredients and allergen information
    new_recipe=request.form.to_dict(flat=False)
    #set up a list of ingredients that will be added to the recipe in the collection
    ingredients=[]
    #set up a dictionary for each individual ingredient which will consist of the name, quantity and unit for each ingredient.
    ingredient={}
    #initialise cook_time variable to convert hours and minutes to minutes total to enable easy sorting by cook time against the recipes returned from a search
    cook_time=0

    #iterate through the form dictionary to correctly format the user input to add to the new recipe document
    #each recipe ID is stored against the relevant document in each category collection:
    #allergens, authors, countries, difficulty, ingredients, meals and users (for favourites)
    
    for key, key_name in new_recipe.items():
        #flatten dict for non-list items which have become lists through request object
        if key!='type' and key!='amount' and key!='unit' and key!='allergens':
            new_recipe[key]=new_recipe[key][0].lower()
            #check if the recipe has been marked as the user's favourite
            if key=='favourite':
                #get the list of users for whom this is a favourite recipe
                recipe_doc=recipes.find_one({"_id" : ObjectId(recipe_id)})
                #get the list of users for whom this is a favourite recipe from the recipe document 'favourite' list element
                favourites=recipe_doc["favourite"]                   
                #check whether a user is logged in and if this user has marked this recipe as a favourite
                
                if "user" in session:
                    user_doc=usersdb.find_one({"name":session["user"]})
                    if new_recipe[key].lower() =='true':
                        #if the user has  logged in and their ID is not stored in the favourites list for this recipe document then add the user ID to the favourites list 
                        #also add the recipe id to the favourites list element in the user document. 
                        if recipe_id not in user_doc["favourites"]:
                            usersdb.update({"name": session["user"]},{"$push":{"favourites" : recipe_id}})
                            favourites.append(str(user_doc["_id"]))
                    else:
                        #if the user has not marked this recipe as a favourite and the user ID is in the favourites list for the recipe document
                        #then remove the user id  from the favourites list and remove the recipe ID from the user document favourites list                     
                        if recipe_id in user_doc["favourites"]:
                            usersdb.update({"name": session["user"]},{"$pull":{"favourites" : recipe_id}}) 
                            favourites.remove(str(user_doc["_id"]))
                
            if key=='hours' or key=='minutes' or key=='calories':
                #convert from string to int, if needed
                try:
                    new_recipe[key]=int(new_recipe[key])
                except ValueError:
                    new_recipe[key]=0
            if key=='hours':
                #convert hours to minutes and add to cook time variable
                cook_time=new_recipe[key]*60
            if key=='minutes':
                cook_time=cook_time+new_recipe[key]
        
        #iterate through the ingredients submitted
        elif key=='type':
            #create dictionaries for each ingredient with key values of ingredient type, amount and units
            #update the list of ingredients with each ingredient dictionary
            i=0
            for ingredient_type in key_name:
                ingredient={ 'type' : ingredient_type.lower() , 'amount' : new_recipe['amount'][i] , 'unit' : new_recipe['unit'][i] }
                #insert ingredient object into array of ingredients
                ingredients.append(ingredient)
                i+=1       

    #update the new_recipe dict with the elements that have been formatted, above.
    #insert the list of user IDs in the favourite lists to the new_recipe dict
    new_recipe["favourite"]=favourites    
    #insert the new cook_time key into the new_recipe dict
    new_recipe["cook_time"]=cook_time
    #insert the new ingredients array into the new_receipe dict
    new_recipe['ingredients']=ingredients  

    #the recipe dictionary is now ready to add/update the document in the recipes collection


    #The recipe ID, however needs to be added to/removed from the recipe lists in other collections.
    
    #check if the ingredients submitted are in the ingredients collection and add/remove ingredients from the collection
    #get the ID of the current recipe that has been added/is being editted
    current_recipe=recipes.find_one({"_id" : ObjectId(recipe_id)})
    #create list of the 'new' ingredients that have been submitted
    new_ingredients=ingredients

    for ingredient in new_ingredients:
        ingredient_type=ingredient
        #check if this is an existing recipe that is being editted
        if edit=="True":
            #if so get a list of the ingredients that are currently in the recipe document (before it was editted)
            #this is to check whether the ingredients have been changed. If so the ingredients may need to be added or removed from the igredients collection
            current_ingredients=current_recipe["ingredients"]
            #check if each new ingredient is already in the list of ingredients for this recipe.
            #if it is there is no need to take further action (it does not need to be added to the ingredients collection)
            if ingredient in current_ingredients:
                ingredient_index=current_ingredients.index(ingredient)
                current_ingredients.remove(ingredient)
        #find the ingredient document in the ingredients collection        
        new_ingredient_doc=ingredientsdb.find_one({"name" : ingredient["type"].lower()})
        
        #for each ingredient, check whether it exists in the ingredient collection.
        if new_ingredient_doc!=None:
            #if it already exists, get the ingredient ID
            new_ingredient_id=new_ingredient_doc["_id"]
        else:
            #if the ingredient is new and has no document create a new ID
            new_ingredient_id=ingredientsdb.insert({"name" : ingredient["type"].lower(), "recipe":[]})
            new_ingredient_doc=ingredientsdb.find_one({"_id" : new_ingredient_id})
        #check if the id of the recipe is stored in the ingredient doc in the ingredient collection.
        #if not add the recipe to the recipe list in the ingredient doc
        if recipe_id not in new_ingredient_doc["recipe"]:
            ingredientsdb.update({"_id": new_ingredient_id},{"$push":{"recipe" : recipe_id}})

    #the current_ingredients list now only contains those ingredients which have been removed from the recipe.
    #the recipe ID needs to be removed from each recipe list in each ingredient doc.
    if edit=="True":
        for ingredient in current_ingredients:
            if ingredient not in new_ingredients:
                current_ingredient_doc=ingredientsdb.find_one({"name" : ingredient["type"].lower()})  
                current_ingredient_id=current_ingredient_doc["_id"]
                ingredientsdb.update({"_id": current_ingredient_id},{"$pull":{"recipe" : recipe_id}})
                current_ingredient_doc=ingredientsdb.find_one({"_id": current_ingredient_id})
                #if the list of recipes for this ingredient is empty then this ingredient is not used in any recipes and can be removed from the ingredients collection.
                if len(current_ingredient_doc["recipe"])==0:
                    ingredientsdb.remove({"_id": current_ingredient_id})  
    
    #check each of the input fields - allergens, meal, country, author and difficulty
    #to see if values have been changed
    categories=["allergens","meal","country","author","difficulty"]
    for category in categories:
        #check if the category is in the recipe dict. if it is then format correctly if the category itself contains a list of elements (e.g. allergens)
        if category in new_recipe:
            if type(new_recipe[category]) is list:
                new_category=new_recipe[category]
            else:    
                new_category=[]
                new_category.append(new_recipe[category])
        else:
            #otherwise set the category list to empty
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
            #check if we are editting an existing recipe, if so check whether any values exist in both the updated and current recipes 
            #if so remove them from the list to later delete the recipe ID from the values that remain in the list (like ingredients iteration, above)
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
            new_category_doc=categorydb.find_one({"name" : value.lower()})
            if value:
                if new_category_doc!=None:
                    #if the particular element exists then get the associated doc from the relevant category collection
                    new_category_id=new_category_doc["_id"]
                else:
                    #if it doesn't exist and is not blank create a new doc with the name of the element 
                    #and create a recipe list in the document containing the ID of this recipe
                    new_category_id=categorydb.insert({"name" : value.lower(), "recipe":[]})
                    new_category_doc=categorydb.find_one({"_id" : new_category_id})
                if recipe_id not in new_category_doc["recipe"]:
                    #check if the recipe is already in the new doc, if it isn't add the recipe ID to this particular category in the DB
                    categorydb.update({"_id" : new_category_id},{"$push":{"recipe":recipe_id}})

        if edit=="True":
            #if we are editing a recipe check whether there are any remaining values in the category list
            #if so this means that the recipe has been removed from the relevant category
            if category in current_recipe:
                #for all the values remove the recipe ID from the particular category in the relevant collection/
                for value in current_category:
                    if value not in new_category:
                        current_category_doc=categorydb.find_one({"name" : value})
                        current_category_id=current_category_doc["_id"]
                        categorydb.update({"_id" : current_category_id},{"$pull" : {"recipe" : recipe_id}})
                        current_category_doc=categorydb.find_one({"_id" : current_category_id})
                        #if this particular category is empty, delete it from the DB
                        if len(current_category_doc["recipe"])==0:
                            categorydb.remove({"_id" : current_category_id})

    #update the recipe document in the recipe collection with the new recipe dictionary
    recipes.update({'_id':ObjectId(recipe_id)},new_recipe)
        
    #display the newly added/edited recipe. 
    return redirect(url_for('display_recipe',recipe_id=recipe_id,added_recipe="true"))

@app.route("/search")
def search():
    #called on selecting the 'search categories' menu option
    
    #check the category_form session variable - these are the categories selected by the user to search against.
    #e.g. particular allergens such as eggs, dairy, meat etc.
    #if the category form exists, delete it.
    try:
        session.pop("category_form")
    except KeyError:
        pass    
    categories=["ingredients","allergens","difficulty","meal","country","author"]
    _category_lists={}
    
    #for each category create a list of the items in each category collection.
    #These will provide the filters against which the user can search
    for category in categories:
        item_list=[]
        if category=="ingredients":
            coll=mongo.db.ingredientsDB.find().sort("name")
        elif category=="allergens":
            coll=mongo.db.allergensDB.find().sort("name")
        elif category=="meal":
            coll=mongo.db.mealDB.find().sort("name")
        elif category=="country":
            coll=mongo.db.countriesDB.find().sort("name")
        elif category=="author":
            coll=mongo.db.authorDB.find().sort("name")
        elif category=="difficulty":
            coll=mongo.db.difficultyDB.find().sort("name")
            
        for item in coll:
            item_list.append(item["name"].capitalize())   
        
        _category_lists[category]=item_list  
    
    #display the search page and pass the list of items against which the user can filter their results.
    return render_template("search.html",title_text="Find your favourites",category_list=_category_lists)

@app.route("/recipe_list", methods=['POST','GET'])
def recipe_list():
    #called on selecting the search recipes option from the menu or 'apply filters' button
    
    #need to check if the category_form session variable exists.
    #if it does it needs to be deleted so that, after displaying a recipe selecting 'back' will return to recipe_list not category_search
    try:
        session.pop("category_form")
    except KeyError:
        pass
    
    #check if the session variable sort exists. If it does not then get the value from the form and set it to the session variable.
    #the sort variable is used to sort the results list into order, depending on the criteria chosen by the user on the recipe_list page
    if session.get('sort'):
        _sort=session["sort"]
    else:
        _sort=request.form.get('sort_by')
        session["sort"]=_sort
    
    #the user can select various filters on the recipe_list page.
    #if returning to the recipe list page from the display recipe page the results will need to be pre-filtered, based on the filter criteria the user
    #chose previously. This is shown by the filter variable set as 'existing'. If there is a session variable for filters the filter dictionary is taken from this.
    #if new filter criteria are being used (because the apply filters button has been clicked) then the filter dictionary is pulled from the form
    #if neither existing or new filter criteria are being used (because the page has been accessed for the first time, or the filter criteria have been cleared) initialise the filter dictionary
    #the filter dictionary is later applied to the mongo search 
    filter=request.args.get('filter',None)    
    if filter=='existing' and session["filters"]:
        _filter_dict=session["filters"]
    elif filter=="new":
        _filter_dict=request.form.to_dict() 
    else:
        _filter_dict={}
    
    #get the action request from the page to determine what sort of list is to be displayed and display appropriate title text 
    _todo=request.args.get('action',None)

    if _todo=="delete":
        title_text_value="Delete recipes"
    elif _todo=="edit":
        title_text_value="Edit recipes"
    else:
        title_text_value="Your recipes"


    #if the user is editting or deleting recipes then they can only edit or delete their own recipes.
    #accordingly automatically set up a filter for the user's ID.
    #otherwise get the filter_author from the form
    if _todo=="delete" or _todo=="edit":
        filter_author=session["user"].lower()
        _filter_dict.update({"author" : filter_author.lower()})
    else:
        filter_author=request.form.get('author')

    #if the user has selected filter values and/or if the user is editing/deleting recipes) then create a dictionary to pass to mongo to filter the results
    if filter=='new':    
        #first remove the sort_by value from the input received from the form.
        #sort_by is not a filter but used to sort results.
        try:
            _filter_dict.pop("sort_by")
        except KeyError:
            pass
        
        #check if each filter has input provided from the form, if not, remove the filter from the dictionary
        #favourites are filtered by the recipe ID held in the user doc favourites element
        filter_favourites=request.form.get('favourite')
        if filter_favourites:
            user_doc=mongo.db.usersDB.find_one({"name":session["user"]})
            user_id=str(user_doc["_id"])
            _filter_dict.update({"favourite" : { "$in" : [user_id]}})
        else:
            _filter_dict.pop("favourite",None)            
                
        filter_meal=request.form.get('meal')
        if filter_meal:
            _filter_dict.update({"meal":filter_meal})
        else:
            _filter_dict.pop("meal",None)
        
        filter_allergens=request.form.getlist('allergens')
        if filter_allergens:
            _filter_dict.update({"allergens" : {  '$nin' : filter_allergens }}) 
        else:
            _filter_dict.pop("allergens",None)
            
        filter_calories=request.form.get('calories')
        if filter_calories:
            if filter_calories==999:
                filter_calories={'$gt':int(filter_calories)}
            else:
                filter_calories={'$lt':int(filter_calories)}  
            _filter_dict.update({"calories":filter_calories})
        else:
            _filter_dict.pop("calories",None)
            
        #the cook time filter needs further definition. A simply int is passed from the form. For filtering this needs to be
        #converted to a $gt or $lt key pair
        filter_cooktime=request.form.get('cook_time')
        if filter_cooktime:
            if filter_cooktime==179:
                filter_cooktime={'$gt':int(filter_cooktime)}
            else:
                filter_cooktime={'$lt':int(filter_cooktime)}  
            _filter_dict.update({"cook_time" : filter_cooktime})
        else:
            _filter_dict.pop("cook_time",None)
            
        filter_country=request.form.get('country')
        if filter_country:
            _filter_dict.update({"country" : filter_country.lower() })
        else:
            _filter_dict.pop("country",None)
        
        if filter_author:
            _filter_dict.update({"author" : filter_author.lower()})
        else:    
            _filter_dict.pop("author",None)

        #once the dictionary has been set up save it to the session variable.
        #session variable is required for moving between pages so that, when returning to the search page the filter criteria are retained.
        session["filters"]=_filter_dict

    if _sort:
        _recipe_list=mongo.db.recipeDB.find(_filter_dict).sort(_sort,1) 
    else:
        _recipe_list=mongo.db.recipeDB.find(_filter_dict)

    #create lists for dropdown filter menus for authors and countries on the recipe_list page
    list_of_countries=mongo.db.countriesDB.find()
    list_of_authors=mongo.db.authorDB.find()
    _author_list=[]
    for author in list_of_authors:
        _author_list.append(author["name"].capitalize())
    _country_list=[]
    for country in list_of_countries:
        _country_list.append(country["name"].capitalize())    

    #find the total number of results returned to display to the user.
    _total_results=_recipe_list.count()
    
    return render_template("recipe_list.html",title_text=title_text_value,recipes=_recipe_list, countries=_country_list,authors=_author_list,action=_todo,filters=_filter_dict, sort=_sort, total_results=_total_results)

@app.route('/display_recipe/<recipe_id>')
def display_recipe(recipe_id):
    #called from selecting a recipe in the recipe list, display category or after submitting add/edit input forms
    
    #get the recipe documentment from the recipe collection
    _recipe=mongo.db.recipeDB.find_one({"_id":ObjectId(recipe_id)})
    
    #check request came from add or edit recipe to ensure clicking back will render the edit recipe page correctly
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

@app.route('/delete_recipe',methods=['POST'])
def delete_recipe():
    
    #called from confirming deletion of recipe on delete modal
    #get the ID of the recipe being deleted
    recipe_id=request.form.get('recipe_id')
    #get the recipe document from the recipe collection
    recipe=mongo.db.recipeDB.find_one({"_id":ObjectId(recipe_id)})

    #iterate through the elements in the document and remove the recipe ID from each element in each category for which the recipe has an entry
    for key in recipe:
        if key=='favourite':
            #need to iterate through the complete list of users who have marked this recipe as favourite and remove it from their favourite recipe list elements in the relevant user doc
            for value in recipe[key]:
                mongo.db.usersDB.update({"_id" : ObjectId(value)},{"$pull" : {"favourites" : ObjectId(recipe_id)}})
        if key=="meal":
            mongo.db.mealDB.update({"name" : recipe[key].lower()},{"$pull" : {"recipe" : ObjectId(recipe_id)}})
        if key=="difficulty":
            mongo.db.difficultyDB.update({"name" : recipe[key].lower()},{"$pull" : {"recipe" : ObjectId(recipe_id)}})
        if key=="allergens":
            #need to iterate through all allergens and remove the recipe ID from each allergen document recipe list
            for value in recipe[key]:
                mongo.db.allergensDB.update({"name" : value},{"$pull" : {"recipe" : ObjectId(recipe_id)}})
        if key=="country":
            mongo.db.countriesDB.update({"name" : recipe[key].lower()},{"$pull" : {"recipe" : ObjectId(recipe_id)}})
            #check if there are any recipes stored against this country. If not delete the country doc from the country collection 
            check_and_delete_empty_doc(recipe[key].lower(),mongo.db.countriesDB) 
        if key=="author":
            mongo.db.authorDB.update({"name" : recipe[key].lower()},{"$pull" : {"recipe" : ObjectId(recipe_id)}})
            #check if there are any recipes stored against this author. If not delete the author doc from the author collection
            check_and_delete_empty_doc(recipe[key].lower(),mongo.db.authorDB)            
        if key=="ingredients":
            for value in recipe[key]:
                mongo.db.ingredientsDB.update({"name" : value["type"]},{"$pull" : {"recipe" : ObjectId(recipe_id)}})
                #check if there are any recipes stored against this ingredient. If not delete the ingredient doc from the ingredient collection
                check_and_delete_empty_doc(value["type"],mongo.db.ingredientsDB)
               
    #finally relete the recipe doc from the recipe collection
    mongo.db.recipeDB.remove({"_id":ObjectId(recipe_id)})
    
    #return to the recipe list page
    return redirect(url_for('.recipe_list',action='delete'))

def check_and_delete_empty_doc(item,coll):
    #called from the delete_recipe function.
    document=coll.find_one({"name" : item})
    #check if the document exists, if so and there are no recipes registered against the document delete it from the collection
    if document!=None:
        if len(document["recipe"])==0:
            coll.remove({"name" : item})                      

@app.route('/display_categories', methods=['POST','GET'])
def display_categories():
    #called from the search page after user selects filters to determine which categories are to be displayed
    #check if the user has already submitted the form listing the categories to be displayed.
    #This session variable ensures, after displaying a recipe, the selected categories are correctly displayed again
    try:
        selected_categories=session["category_form"]  
    except KeyError:
        #if no session variable exists get the categories from the user submitted form.
        selected_categories=request.form.to_dict(flat=False)
        session["category_form"]=selected_categories        
  
    #get the categories against which the user is searching
    category=list(selected_categories.keys())[0]    
    _item_list=[]

    #iterate through the categories selected for filtering and create lists of the items in each category that have been selected.    
    for key in selected_categories:
        for item in selected_categories[key]:
            _item_list.append(item.lower())

    i=0
    #initialise a dictionary of recipes that are in each selected category
    recipes_in_category={}
    #set a search value, for all categories except allergens the recipes returned need to contain the element searched against
    #in the case of allergens the recipes returned must not contain the specific element.
    search_value="$in"
    if category=="allergens":
        coll=mongo.db.allergensDB
        search_value="$nin"
    elif category=="meal":
        coll=mongo.db.mealDB
    elif category=="ingredients":
        coll=mongo.db.ingredientsDB
    elif category=="country":
        coll=mongo.db.countriesDB        
    elif category=="author":
        coll=mongo.db.authorDB   
    elif category=="difficulty":
        coll=mongo.db.difficultyDB    
    
    #perform mongo search against each category item and crate list of recipes to display for each category.
    for i in range(0,len(_item_list)):
        category_objects=coll.find({"name" : {'$eq' : _item_list[i]}})
        recipe_ids=[]

        for object in category_objects:
            for recipe in object["recipe"]:
                recipe_ids.append(ObjectId(recipe))

        recipes=mongo.db.recipeDB.find({'_id' : {search_value : recipe_ids}})
        recipes_in_category[_item_list[i]]=list(recipes)

    return render_template('display_category.html',category=category,items=_item_list,recipes=recipes_in_category, title_text="Your recipes")
    
if __name__ =="__main__":
    app.run(host=os.environ.get("IP"), port=int(os.environ.get("PORT")), debug=False)    
    
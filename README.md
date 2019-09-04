# Community recipe website

## Overview

### Brief
This website has been created to enable users from any location to upload their own recipes to a community site to share with others.

The objectives are to:

1 - provide a community website

2 - Enable users to:

        read recipes created by others
        create their own recipes
        edit and delete their own recipes
        quickly return a list of recipes based on search criteri
        shortlist recipes by marking them as favourites

3 - Provide a visually appealing environment for users to encourage others to use the site and share recipes

### User Stores
As well as considering the community's needs consideration has been given to the needs of prospective users of the website:

Users are likely to fall into 3 categories. Users will be:

1 - looking for one off inspiration

2 - wanting to share knowledge

3 - creating a list of recipes to refer to back to on repeat occasions

#### Looking for inspiration
- I would like to find recipes:
    - by meal type 
    - containing specific ingredients
    - that cater for specific dietary requirements
    - of a particular cuisine
    - are quick to cook
    - contain less calories

#### Wanting to share knowledge
- I would like to be able to:
    - add my recipes to the site
    - provide details about the ingredients, cook time, calories and allergens relevant to the recipes
    - easily edit my recipes
    - delete recipes that I no longer wish to share
    - let others know what recipes I have uploaded

#### Creating a list of recipes
- I would like to find recipes by the individuals who have uploaded them
- I would like to book mark recipes to create a personal list 
- Create search list of recipes matching certain criteria and sort them into a sensible order

### Purpose
This website is designed as an interactive front end website with a neat appearance and clear buttons to enable users to easily navigate around the site and to achieve their aims, above.
Users recipes are stored in a mongo non-SQL database accessed via python backend code.

The main menu is displayed at top right of the page in full on tablets devices and larger or behind a burger button for smaller devices.
Upon accessing the site users can search the database by recipe or category. To access the full functionality of the site a user must 'log in' before they can add, edit or delete recipes.
To avoid confusion for the user options to add, edit or delete recipes are hidden from the menu until they have logged in.
A user can log into the site by clicking the 'person' icon and entering their name in the modal displayed.

At this stage full functionality to enable a user to create a unique profile and password has not been implemented.

The site comprises 7 pages that can be accessed from the main navigation bar and button options on the site.
The main navbar is displayed on all pages for ease of access to all pages in the site.
A website map is contained within the respository.

#### Base Template
Pages are called using backend Flask framework and rendered using Jinja2 templating logic. A base template provides the main layout of the pages including navbar, title element and error modals. On each page Flask provides updated text for the title element so it is clear to the user which page they are on.

#### Index
The index page provides an overview of the site and options available to users.

On mobile devices the index page is deliberately spartan with only essential detail due to viewport size limitations.

#### Search Recipes
Clicking the search button in the navigation bar provides two options:

1 - search recipes
2 - search categories

##### Search recipes
This page displays an unfiltered list of all recipes in the database.
The list is paginated, limited to 10 results per page, to avoid excessive page length.

At the top of the search list the user can select options to filter the search and reduce the number of results returned. The filter options are:
- Favourites - only recipes marked as favourites by the user will be shown in the list
- Meal - The user can select a specific meal type - "breakfast, lunch, dinner, snack, dessert or beverage"
- Allergens - The user can select several allergens from "Dairy, Fish, Gluten, Nuts, Shellfish, Eggs and Vegetarian" to excludes recipes containing specific allergens/dietary requirements
- Calories - The user can select to filter results by recipes that are below specific calorie levels, banded by <100, <200, <300, <500, <750, <1000 and >1000
- Cooking Time - The user can select to filter results by the time they take to cook, banded by <10 minutes, <20 minutes, <30 minutes, <1 hour, <2 hours, <3 hours, >3 hours
- Country - The user can filter the results by a cuisine, based on countries contained in the backend collection (determined by the recipes entered on the site) If none of the recipes contain information about their country of origin this filter option is omitted
- Author - The user can filter the results by a specific author, based on the users contained in the backend collection.

Also at the top of the search list the user can select options to sort the list into ascending order based on:
- Recipe Name
- Cooking time
- Calories or
- Meal type

A list of recipes matching the filter criteria is retrieved from the back end through Flask and displayed to the user via Jinja2 template logic to build a list of the filtered recipes. 
The user can click on any recipe which will then display, on the 'Display Recipe' page (below), the full information about that recipe.

The 'home' button at the end of the page will take the user back to the index page.

##### Search by category
Search by categories is accessed, like search recipes, from the main search button, or from the browse button in the call to action on the index page.

This page displays 6 categories against which the user can search:
- Ingredients
- Dietary
- Difficulty
- Meal
- Country
- Author

Clicking on any option brings up the filter criteria. The filter criteria are generated from all documents in the specific backend collection relating to that category.

By using the search category option the user can filter the results by several elements in one category (e.g. recipes containing several ingredients, recipes from more than one author or country and one more more meal type). The category search provides more focussed search results for users who may have a better idea of the specific type of recipe they are after compared the straight search results, above.
Once the search options for the specific category have been selected by the user clicking 'search' will display a list of recipes, broken down by category.

Again the user can return to the index page via the 'home' button at the bottom of the page.

#### Display search by category results
This page is accessed by clicking 'search' in the search by category page, above.
The search results are grouped by the options selected on the previous page, e.g. all recipes containing Olive Oil.
As there are likely to be several results in each option the results are contained within a 'collapsible' element which can be expanded by the user clicking on the caret. This avoids cluttering the page and providing a more pleasing visual experience for the user.

In the mobile view a list of recipe names and pictures is displayed on collapsible elements that can be expanded to show further information (cooking time, calories and difficulty to cook) with the option to view the recipe in full. 

On tablet and desktop devices this information is displayed immediately, not within a collapsible, as viewport space is not so much at a premium.

Clicking on the 'eye' icon against the relevant recipe will display the full details of the recipe including cooking instructions.

Session variables are used to store the user's choice of filters/sort fields to ensure, on returning to search page the filters are reapplied to the returned list of recipes.

The 'back' button at the end of the page returns the user to the search by category page. 

#### Add
The option to add recipes is only displayed in the navigation bar if the user is logged in.
This page can be accessed by the Add tab in the navigation bar.
On loading this page displays a form that can be populated by the user with all information about the recipe they intend to upload.
Required fields are:
- Name of Recipe
- Method (cooking instructions)
- At least one ingredient with quantity (number of units are optional)

The framework, Materialize, form validation class is used to highlight errors on data entered in 'Cooking Time - minutes' and 'Calories' fields. These fields can accept numbers 0-59 and 0-5000 respectively. If invalid data is entered the input field is highlighted with a red line. 
For fields 'ingredient name', 'hours', 'minutes', 'calories', 'ingredient quantity' jQuery code prevents the user entering anything but text or numbers as appropriate to the field.
Further data validation is undertaken by jQuery script on form submission. An error modal with full error message noting the invalid data if the user:
- Does not input a name for the recipe
- Does not input a method for cooking the recipe
- Does not include at least one ingredient
- Inputs a figure of less than 0 or more than 59 minutes for cooking time
- Inputs a figure of less than 0 or more than 5000 for calories.

On submission of the ingredient by clicking the '+' button jQuery script validation is undertaken against the data entered. An error modal is displayed detailing the invalid data if the user:
- Does not enter a name for the ingredient
- Does not enter a quantity for the ingredient

The user can add the recipe to their list of favourites (or filtered searching, above) by clicking the star. Clicking again will remove the recipe from the list of favourites.

On submission of a valid form the data is sent to the back end via jQuery form submission to the Flask framework. The recipe submitted is then displayed to the user on the 'Display Recipe' page (below).

#### Edit
The option to edit recipes is only displayed in the navigation bar if the user is logged in.

If the user is viewing a recipe in the 'display recipe' page (below) selecting the 'Edit' menu tab open this page.

If, on the other hand, the user is not viewing a recipe the 'Edit' menu tab will bring up a list of recipes, in the same manner as the 'Search Recipes' list above.
The recipes are, however, automatically filtered by the Flask back end framework with the user as the author. This ensures that recipes that have not been created by the user are not displayed for them to edit.
An 'edit' icon is displayed against each recipe, in place of the 'favourite star' on the search recipe list, to denote to the user that they are in the 'edit recipe' list.
Selecting a recipe from the list will open the Edit page for that specific recipe.

The Edit page can also be accessed directly from the display recipe page, see below.

This page is, in essence, the same as the Add recipe page but the fields are pre-populated with the data retrieved via Flask from the recipe in the mongo collection.
Data lists and dictionaries are submitted via Flask from the back end. The page detail is then rendered using Jinja2 templating logic.

The user can return to Index or back to the list of recipes they can edit via the Home and Back buttons at the bottom of the page.

#### Delete
The option to delete recipes is only displayed in the navigation bar if the user is logged in.

If the user is viewing a recipe in the 'display recipe' page (below) selecting the 'Delete' menu tab will open a modal asking the user to confirm whether they wish to delete the recipe currently being viewed.

If, on the other hand, the user is not viewing a recipe the 'Delete' menu tab will bring up a list of recipes, in the same manner as the 'Search Recipes' list above.
The recipes are, however, automatically filtered by the Flask back end framework with the user as the author. This ensures that recipes that have not been created by the user are not displayed for them to delete.
A 'delete' icon is displayed against each recipe, in place of the 'favourite star' on the search recipe list, to denote to the user that they are in the 'delete recipe' list.

Selecting a recipe from the list will bring up a modal asking the user to confirm whether they wish to delete the selected recipe. The recipe selected for deletion is highlighted in red so it is clear to the user which has been selected.

The Edit page can also be accessed directly from the display recipe page, see below.

#### Display recipe
This page is displayed via:
- Selecting a recipe from the 'Search recipes' list
- Submitting a valid 'add recipe' form
- Submitting a valid 'edit recipe' form

If the user is logged in a dropdown button is displayed enabling the user to choose options to edit or delete the recipe.

The recipe data is provided to the front end by the Flask framework and rendered using Jinja2 template logic.

The user can mark the recipe as a favourite by clicking the 'star' icon. Clicking again on the star removes the recipe from the user's list of favourites.

### How does it work?

#### Data processing and entry
Recipe data is entered in the front end forms which are processed and validated using ***jQuery*** scripting and submitted to the back end which uses the ***Flask*** framework.
***Python*** scripting is used to convert the received data into the appropriate format and submitted to the ***MongoDB*** collections.
***Python***/***Flask*** is used to retrieve, filter and sort data from the ***MongoDB*** collections and pass to the front end for display.

#### Database structure
Conceptual database design was undertaken considering the entities, their relationships and attributes for the recipe data required for the site. (See 'Conceptual Database Design' document in the repository).
Analysis of the data that would be handled and required by the site was undertaken before development. A list of attributes and data types was compiled (see database layout document in repository).
A number of relationships were identified and an SQL relational database structure was considered. However as a community based website that anyone can access and upload recipes there is potential for the database size to increase drastically and the need for agile and flexible database management is required.
There are many data elements for recipes and it is likely that further elements will need to be added in the future. The schema requirements of SQL databases would be unduly restrictive and require significant recoding if additional elements need to be added in the future.

A noSQL document oriented database design was, therefore, preferred and MongoDB selected as the appropriate document database provider.
The MongoDB milestone-3 database contains 8 collections:
- recipeDB
- allergensDB
- authorDB
- countriesDB
- difficultyDB
- ingredientsDB
- mealDB
- usersDB

The main collection, recipeDB, contains all recipes added to the site with primary information:
- Name - string element
- Favourite - array element of all users who have marked the recipe as their favourite for ease of sorting
- Country - string element - country of origin of the recipe - this element is not required for all recipes.
- Picture - string element - URL of picture of dish - this element is not required for all recipes.
- Allergens - array of allergens that the recipe contains
- Meal - string element - type of meal for which the recipe is appropriate - this element is not required for all recipes.
- Difficulty - string element - indicates level of difficulty of the recipe - this element is not required for all recipes.
- Hours and minutes - number elements - cooking time of the recipe - this element is not required for all recipes.
- Calories - number element - number of calories contained in the recipe - this element is not required for all recipes.
- Method - string element - details on how to cook the recipe
- cook_time - number element calculated from hours and minutes for ease of sorting - this element is not required for all recipes.
- Ingredients - array - contains dictionaries of all ingredients in the recipe (name, amount and unit)

The usersDB collection contains documents of each user who has created an ID on the site. Against each user document contains an array of their favourite recipeIDs.
This array cross refers to the Favourite array in the recipe document. 

The following collections which each contain an array of the recipeID to which they apply are used to populate dropdown/filter and sort options across the site.
The allergensDB collection contains a list of all allergens that it is envisaged will apply to any recipe. This collection is used to populate allergen drop down lists for editing and adding new recipes.

The authorDB collection contains a list of all users who have added recipes to the site.  It is not possible for a recipe to be added without an author.

The countriesDB collection contains a list of all countries added by users for recipes uploaded. 

The difficultDB collection contains a list of the 3 difficulty levels applicable to recipes (Easy, Medium and Hard)

The ingredientsDB collection contains a list of all ingredients added by users across the various recipes uploaded

The mealDB collection contains a list of the 6 meal types it is envisaged will apply to any recipe (Breakfast, Lunch, Dinner, Dessert, Snack, Beverage)


Although not implemented in this release it is envisaged that users will be able to add to the Allergens and Meal collections to provide further options.

### Features
#### Existing
- Responsive design for ease of readability on various device sizes
- Collapsible headers and bodies for search/filter options and recipe results to provide better read format
- Hidden options to prevent users who are not logged in from editting, deleting or adding recipes
- Ability for users to mark recipes as favourites to build up their own filtered list of results
- Branded colour co-ordinated style
- Large, obvious buttons to help the user navigate the site
- Animated and hidden menus on mobile devices for better user experience
- Functionality for users to Create, Read, Update and Delete recipes from the site
- Defensive design to prevent users from entering invalid data
        - Add/Edit recipes pages dropdown select menus for allergens, meal types ingredient units prevent user adding unexpected data
        - jQuery form validation ensures the user cannot submit a recipe within all required fields completed
        - jQuery form control prevents user entering text in number fields and vice versa
        - Autocomplete of ingredient and countries field assists the user to user existing entries
        - Lists of authors and countries in filter search is backend validated before supply to front end drop down list 
        - Minutes field is jQuery validated to ensure minutes entered cannot be less than 0 or more than 59
        - Calories field is jQuery validated to ensure calories entered cannot be less than 0 or more than 5000
        - jQuery validation of category searches prevents user searching against an empty field
        - Backend conversion of user entries to appropriate formate for holding in mongoDB collections

#### Potential
- Within add/edit recipe forms - A feature that will automatically convert the minutes added to hours and minutes (if greated than 59)
- Customisable units - A feature that will enable users to add other unit types
- The potential for users to add to the allergies and meal types collections providing greater options
- Ingredient review/match - a feature to reduce multiple entries of same ingredient but to provide a preparation type (e.g. Beef - types Mince, Steak, Cutlet etc.)
- Creation of unique user profile and password
- Inclusion of an 'admin' account with privileges to edit and delete all recipes - this would, however, require password protection

#### Tech Used
Styling:

The front-end site is styled using ***Materialize 1.0.0*** framework

***Flask*** framework is used for back end application and interaction with front end 

***Jinja2*** templating is used to iterate through data from backend for correct rendering of front end display

A combination of ***Materialize 1.0.0*** and ***font-awesome 4.7.0*** icons were used throughout the site.

Languages used:

***Python3*** for back end implementation

***jQuery*** and ***Javascript*** for front end interaction:

- Menu animations
- Button functionality
- Form submission
- Form data validation
- Modal display

### Testing
Code was written through the AWS Cloud9 IDE.
The website has been tested during production on Chrome and then on IE, Safari and Opera browsers.
See additional README document for specific testing undertaken.

### Initial Wireframes
Wireframes were designed using MarvelApp and can be located here:
https://marvelapp.com/4b6hce4

### Deployment
The Cookbook website is deployed using the Heroku platform.

#### Deployment process
The app and all associated documents were developed through AWS Cloud9 IDE.
A git respository was created through the bash terminal and the the project was committed to the repository using the standard bash commit command.
Commits to the respository were made at each major development stage or as issues were identified and fixed.

The project was then deployed to Heroku through the Heroku online console, using the following steps:
- Having logged into the Heroku platform a new app was created, titled 'milestone-3-recipebook'.
- A git url was provided by Heroku on creating the app, 'https://git.heroku.com/milestone-3-recipebook.git'
- The local git respository was linked to Heroku through the bash terminal command 'git remote add heroku https://git.heroku.com/milestone-3-recipebook.git
- A requirements.txt file was created through the bash terminal command 'sudo pip3 freeze --local>requirements.txt'
- The requirements.txt file was commited to the local git repository
- A Procfile was created by bash terminal command 'echo web: python app.py > Procfile
- The Procfile was commited to the local git respository
- The local git repository was deployed to heroku via the bash terminal command 'git push'
- Local environment variables for:
        - IP,
        - PORT,
        - SECRET, and
        - MONGO_URI
were set using the Heroku console.

The deployed project can be viewed at 'https://milestone-3-recipebook.herokuapp.com/'

To edit/run the code locally it is necessary to pull the code from the Heroku repository. This can be achieved directly through the Git command:

$ heroku git: clone -a milestone-3-recipebook
$ cd milestone-3-recipebook

Changes can then be made to the cloned code and deployed to Heroku using Git:

$ git add .
$ git commit -m "commit message"
$ git push heroku master

There are no differences between the development and deployed versions.
Other than a standard browser no further software or implementation is required and the site can be accessed at 'https://milestone-3-recipebook.herokuapp.com/'.
To run the app through IDE input bash terminal ensure all requirements are installed:
$ sudo pip3 install –r requirements.txt
The app can then be run by navigating to the root folder and using bash command:
python3 app.py

### Validation
- CSS
        jigsaw.w3.org was used for validation of css code and did not generate significant errors
- HTML
        validator.w3.org was used for validation of HTML code. Errors were thrown by the use of jinja templating language which was not recognised by the validator.
        The only errors of note were:
                Labels applying to hidden form element - however the syntax used was required to comply with the requirements of the Materialize framework
                Link for google font was rejected by the validator but the link is as provided from Google Fonts
                Element ul is not allowed as child of ul - again, however, this syntax is required to comply with the requirements of the Materialize framework
                Duplicate ID errors - however these errors were caused by the use of jinja templating. In the rendered versions IDs are not duplicated.
- jQuery
        codebeautify.org/jsvalidate was used for validation of jQuery code. No significant erros were generated

- Python
        pep8online.come was used to validate Python code and did not generate any errors.

### Credits

#### Images
Images used under creative commons licence CC0
Main background image - https://images.unsplash.com/photo-1496412705862-e0088f16f791?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80 by Brooke Lark on Unsplash
Burger - https://c.pxhere.com/photos/e4/cb/bread_bun_burger_cheese_cheeseburger_close_up_delicious_fast_food-1556449.jpg!d
Fish and chips - https://c.pxhere.com/photos/a0/1b/beef_chips_diet_dinner_dish_eat_food_french-1153129.jpg!d
Lamb Curry - https://c.pxhere.com/images/e6/3f/2384e87f95318077922edc6b9f79-1430223.jpg!d
Vegetarian Fajitas - https://c.pxhere.com/photos/1b/62/tortillas_white_mexican_food_taco_lunch_dinner_traditional-1330790.jpg!d
Pizza - https://c.pxhere.com/photos/71/8e/pizza_stone_oven_pizza_stone_oven_salami_cheese-1411428.jpg!d
Toast - https://c.pxhere.com/photos/8b/2d/toast_toaster_food_white_bread_slices_of_toast_eat_breakfast_discs-670056.jpg!d

Category button images linked from pxhere.com used under Creative Commons CC0 licence
Category button - Ingredients - https://pxhere.com/en/photo/1433267
Category button - Dietary - https://pxhere.com/en/photo/1435829
Category button - Difficulty - https://pxhere.com/en/photo/228377
Category button - Meal - https://pxhere.com/en/photo/1516443
Category button - Country - https://pxhere.com/en/photo/1521383
Category button - Author - https://pxhere.com/en/photo/1401823

Images compressed using compressjpeg.com

#### Example recipes
Sausage and Mash - https://www.bbcgoodfood.com/recipes/1359634/sausage-and-mash
Burger - https://www.bbcgoodfood.com/recipes/1514/beef-burgers-learn-to-make
Fish and chips - https://www.bbcgoodfood.com/recipes/5544/the-ultimate-makeover-fish-and-chips
Lamb Curry - https://www.bbcgoodfood.com/recipes/slow-cooker-lamb-curry
Vegetarian Fajitas - https://www.bbcgoodfood.com/recipes/veggie-fajitas
Spaghetti Bolognese - https://www.bbcgoodfood.com/recipes/1502640/the-best-spaghetti-bolognese
Pizza - https://www.bbcgoodfood.com/recipes/4683/pizza-margherita-in-4-easy-steps

#### Code
##### Individual functions:
Pagination jQuery plug in for materialize by Mirjam Skarica mirjamskarica@gmail.com - used under MIT licence (https://github.com/mirjamsk/materialize-pagination/blob/master/LICENSE) - https://github.com/mirjamsk/materialize-pagination
Text/number only input for form fields jQuery plug in by Kevin Sheedy  - used under MIT licence (https://github.com/KevinSheedy/jquery.alphanum/blob/master/MIT-LICENSE.txt) - https://github.com/KevinSheedy/jquery.alphanum

##### Libraries
Automated testing:
- Jasmine - https://jasmine.github.io

#### Fonts/Icons
Google Fonts - fonts.google.com - Roboto and Abril Fatface
Font Awesome - https://fontawesome.com/v4.7.0/icons/
Materialize css - https://materializecss.com/icons

#### Framework
Materialize 1.0.0 - https://materializecss.com/
Flask - https://www.fullstackpython.com/flask.html

#### Database
MongoDB - https://www.mongodb.com/
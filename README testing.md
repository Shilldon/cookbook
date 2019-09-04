# Community recipe website

## Testing

### Automated testing:

Automated testing of add and edit recipe forms was undertaken using the ***Jasmine*** testing framework.

Data entries for recipe name, ingredients, method, amount of ingredients, calories and cooking time were tested through the framework to ensure error modals were correctly called with appropriate error text.

Back end testing undertaken during development using ***Python*** try and exception commands to test data types received and passed to mongoDB collections.

### Manual testing undertaken for

#### Buttons:

* Base Template
    * Log in/out button correctly displays modal depending on existence of session["user"] variable
    * Cookbook logo appropriately returns to index page
    * Search button correctly displays dropdown options to search by recipe or by category
    * Search recipes correctly takes user to recipe_list page with a list of all recipes available in the collection displayed
    * Search categories correctly takes the user to the search page.
    * If session["user"] variable is defined Add, Edit and Delete buttons are correctly displayed
    * Add correctly takes user to add_recipe form
    * Edit (if no recipe currently displayed) correctly takes user to recipe_list page with all recipes created by that user displayed
    * Edit (if recipe displayed) correctly takes user to edit_recipe form with all fields pre-populated with the correct information
    * Delete (if no recipe currently displayed) correctly takes user to recipe_list page with all recipes created by that user displayed
    * Delete (if recipe displayed) correctly brings up a modal to confirm whether the user wishes to delete the displayed recipe
    * Burger button on mobile/tablet device view correctly displays navbar
    * Search icon on mobile/tablet device correctly takes user to the recipe_list page with a list of all recipes available in the collection displayed
    * Delete Modal - correctly cancels or deletes chose recipe
    * Login/out modal - correctly displayed depending on existence of session["user"] and appropriately creates or deletes session["user"]
    
* Index Page 
    * Browse - correctly takes user to the search page                 
    
* Recipe List Page
    * The filter and sort options collapsibles are correctly show and hidden when clicked
    * Apply filters correctly applies the relevant filters to the list of recipes displayed
    * Clicking on recipes correctly takes the user to display_recipe page populated with the detail for that recipe
    * If navigated to from edit button - clicking on recipes correctly takes the user to the edit_recipe page populated with the detail for that recipe
    * If navigated to from the delete button - clicking on recipes correctly displays an error modal confirming if the user wishes to delete the recipe clicked on.
    * Home correctly returns the user to the index page
                    
                    
* Search Page
    * Category buttons correctly show and hide the category search collapsible
    * Cancel correctly hides the category search collapsible
    * Search correctly displays an error modal if no options are chosen
    * Search correctly takes the user to display_category page with a list of filtered recipes by category displayed based on the filter options input
    * Home correctly takes the user to the index page
                    
* Categories
    * Clicking on categories correctly opens and closes the collapsible to show/hide the list of recipes in each category
    * Clicking on the recipe name (for mobile) devices correctly opens/closes the collapsible with brief details about the recipe
    * Clicking the eye icon correctly takes the user to display_recipe page populated with the details of that recipe.
    * Home correctly takes the user to the index page

* Add
    * Favourite 'star' automated testing undertaken, see above
    * Add - automated testing undertaken, see above. Users undertook manual testing, inputting a wide array of entries into the form. Users were encouraged to input non-standard and unexpected responses to form queries.
    * Home - correctly takes the user to the index page
    
* Edit
    * Favourite 'star' automated testing undertaken, see above
    * Update - automated testing undertaken, see above. Users undertook manual testing, inputting a wide array of entries into the form. Users were encouraged to input non-standard and unexpected responses to form queries.
    * Home - correctly takes the user to the index page
                    
* Display recipe  
    * Drop down button correctly displayed only if user is logged in an is author of the recipe displayed
    * Drop down option to edit recipe correctly takes the user to the edit_recipe page populated with details of that recipe
    * Drop down option to delete recipe correctly displays a modal asking for confirmation to delete the recipe
    * Edit button in nav bar correctly takes the user to the edit_recipe page populated with details of that recipe
    * Delete button in nav bar correctly displays a modal asking for confirmation to delete the recipe
    * Back correctly takes the user to edit_recipe page/recipe_list page depending if the user navigated to display_recipe from add_recipe/edit_recipe or the recipe_list
    * Home correctlys takes the user to the index page.
                    
### Mobile first design
Site tested using Google Developer Tools and screenfly (http://quirktools.com/screenfly), resizing viewport to various resolutions:

Desktop - 1280x1024,

Galaxy S5 360x640,

iPad - vertical 768x1024,

iPad - horizontal 1024x768,

iPhone5 320x568,

iPhone7/6/8 375x667,

iPhoneX 375x812,

Laptop 1366x768

to ensure design responded appropriately.    

### External feedback
After deploying to Heroku user feedback from a 10 person focus group was requested and acted upon.

Users were encouraged to add, edit and delete recipes to ensure database functionality worked as expected.
Where errors were encountered Heroku logs were examined to identify and fix bugs.
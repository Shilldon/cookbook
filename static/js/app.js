//----GENERAL SCRIPTS----//
//initialisation for materialize framework
$(document).ready(function() {
    $('.sidenav').sidenav({
        edge: "right"
    });
    $('.modal').modal({
        //defensive - prevent modals from being closed by clicking on background - so an option has to be selected
        dismissible: false
    });
    $('.collapsible').collapsible();
    $('.dropdown-trigger').dropdown();
    //important - must be called last
    $('select').formSelect();
});

//display a preloader on inserting or deleting recipes as collection query can take some time
$(".call-preloader").on("click", function() {
    $(".modal").modal("close");
    $("#loader-modal").modal('open');
});

$(".collapsible").on("click", function() {
    $('html, body').animate({
        scrollTop: $(this).offset().top
    }, 1000);
});

//----EDIT AND ADD RECIPE PAGE SCRIPTS----//

//favourite button function
$("#favourite").on("click", function() {
    //ensure the favourite variable is a boolean value
    var favourite = $("#favourite_input").val();
    //toggle favourite status - appearance and value
    if (favourite === "false") {
        $("i", this).text("star");
        $("i", this).addClass("gold-star");
        $("#favourite_input").val("true");
    }
    else {
        $("i", this).text("star_border");
        $("i", this).removeClass("gold-star");
        $("#favourite_input").val("false");
    }
});

$("#add_ingredient").on("click", function() {
    var totalIngredients = $("#ingredients").data("total_ingredients");
    totalIngredients++;
    $("#ingredients").data("total_ingredients", totalIngredients);
    var currentIngredient = $("#ingredient").val();
    var currentAmount = $("#amount").val();
    var currentUnit = $("#unit option:selected").val();
    var currentIngredients = $("#ingredients").html();
    var callErrorModal = errorCheckIngredient(currentIngredient, currentAmount);
    if (callErrorModal[0] === true) {
        openErrorModal(callErrorModal[1]);
    }
    else {
        addIngredient(currentIngredients, currentIngredient, currentAmount, currentUnit);
    }
});

//function check ingredients submitted for validity and throw error modal if invalid
function errorCheckIngredient(ingredient, amount) {
    var errorText = "";
    var error = false;
    //check if ingredient name has been entered
    if (ingredient.length === 0 || ingredient === undefined || jQuery.type(ingredient)!="string") {
        errorText = errorText + ("Please enter ingredient name <br>");
        error = true;
    }
    //check if amount of ingredients has been entered - check against whether a number is input and whether string is empty
    if (isNaN(amount) || amount.length === 0 || amount === undefined) {
        errorText = errorText + ("Please enter amount of ingredients <br>");
        error = true;
    }
    return [error, errorText];
}

//function to add to and display ingredients after ingredient input form submitted
function addIngredient(currentIngredients, currentIngredient, currentAmount, currentUnit) {
    if (currentUnit === "0") { currentUnit = ""; }
    //on successful completion of ingredients form create line above form with ingredients details and button to click to remove the ingredient if a mistake has been made
    $("#ingredients").html(currentIngredients + "<div class='row'><div class='col s1 offset-s1 l1'><a id='remove_ingredient' class='right btn-floating btn-small waves-effect waves-light highlight3-background valign-wrapper'><i class='material-icons'>delete</i></a></div><div class='col s10 l5 valign-wrapper'><p>" + currentAmount + " " + currentUnit + " " + currentIngredient + " </p><input type='hidden' name='type' value=\'" + currentIngredient + "\'></input><input type='hidden'name='amount' value=" + currentAmount + "></input><input type='hidden' name='unit' value=" + currentUnit + "></input></div>");
    //reset the form values
    $("#ingredient").val('');
    $("#amount").val('');
    $("#select-unit").val('');
    $('#select-unit').formSelect();
}

//function for remove ingredient button. Created as click function on body of page because it was not possible to bind click event to elements dynamically created through jquery/jinja
$('body').on("click", "#remove_ingredient", function() {
    $(this).parent().parent().slideUp(500);
    var ingredientLine = $(this).parent().parent();
    setTimeout(function() { ingredientLine.remove(); }, 500);
});

$(".submit-recipe").on("click", function() {
    var name = $("#name").val();
    var ingredient = $('#ingredients').find('input').filter(':hidden:first').val();
    var method = $('#method').val();
    var minutes = $("#minutes").val();
    var calories = $("#calories").val();
    var callErrorModal = errorCheckRecipe(name, ingredient, method, minutes, calories);
    if (callErrorModal[0] === true) {
        openErrorModal(callErrorModal[1]);
    }
    else {
        $("#loader-modal").modal('open');
        $("#recipe-form").submit();
    }
});

//Function to check the data submitted for the recipe for validity and throw error modal if invalid.
function errorCheckRecipe(name, ingredient, method, minutes, calories) {
    var errorText = "";
    var error = false;
    //ensure the recipe has a name
    if (name === undefined || name === "") {
        errorText = errorText + ("You need to name your recipe <br>");
        error = true;
    }
    //ensure the recipe has at least one ingredient
    if (ingredient === undefined || ingredient === "") {
        errorText = errorText + ("You need at least one ingredient <br>");
        error = true;
    }
    //ensure the user has entered instructions on how to make the recipe
    if (method === undefined || method === "") {
        errorText = errorText + ("You need to provide instructions to make the recipe <br>");
        error = true;
    }
    //ensure, if minutes are added, they are between 0 and 60
    if (minutes != undefined) {
        if (minutes > 59 || minutes < 0 || isNaN(minutes)) {
            errorText = errorText + ("Number of minutes needs to be between 0 and 59 <br>");
            error = true;
        }
    }
    //ensure, if calories are added, they are between 0 and 5000
    if (calories != undefined) {
        if (calories > 5000 || calories < 0 || isNaN(calories)) {
            errorText = errorText + ("Number of calories needs to be between 0 and 5000 <br>");
            error = true;
        }
    }
    return [error, errorText];
}

//open an error modal with appropriate error
function openErrorModal(errorText) {
    $("#error-modal").modal('open');
    $("#error-modal p").html(errorText);
}



//----RECIPE LIST PAGE SCRIPTS ---//
//function called on clicking delete icon on list of recipes. Bound to page body because it was not possible to bind a click event to an element created dynamically through flask
$('body').on('click', '.delete_button', function() {
    //need to obtain the id of the recipe selected for deletion and store this on the modal to pass to backend if deletion is confirmed
    var recipe_id = $(this).attr("recipe_id");
    $('#recipe_id_input').val(recipe_id);
    //highligh the recipe line selected for deletion
    $(this).find(".row").addClass("selected-for-deletion");
    //need to set the row object on the reset modal button to remove the red highlight if cancelling deletion
    $('#modal_reset').data("row_to_delete", $(this).find(".row"));
});

//on cancelling the deletion modal ensure the recipe selected for deletion is unhighlighted
$('#modal_reset').on('click', function() {
    var row = $(this).data("row_to_delete");
    //on cancelling deletion remove the red highlight on the row
    //first check if there is a highlighted recipe because the delete modal was called on 'recipe list page' 
    if (row != undefined) {
        //if so remove the highlight
        row.removeClass("selected-for-deletion");
        //and reset the row variable
        $(this).data("row_to_delete", "");
    }
});

//function called on applying filters to list of recipes
$('.filter-button').on("click", function() {
    //close the collapsible
    $(".collapsible-header").removeClass(function() {
        return "active";
    });
    $(".collapsible").collapsible({ accordion: true });
    $(".collapsible").collapsible({ accordion: false });
    //disable all empty form fields to avoid sending blank fields for filter search in flask against DB
    $("#filters_form option[value='']").attr("disabled", "disabled");
    $("#filters_form input[value='']").attr("disabled", "disabled");
});

//called on clicking sort button
$(".sort_by").change(function() {
    $("#sort-form").submit();
});

//called to check if no allergens are selected in filter, if so revert to 'not filtered option'
$("#allergens_list").change(function() {
    if ($("#allergens_list").val() != "") {
        $("#allergens-unfiltered").prop("selected", false);
    }
    else {
        $("#allergens-unfiltered").prop("selected", "selected");
    }
});


//---search page scripts---//
$(".category-search-button").on("click", function() {
    var inputValid = false;
    $("form select").each(function() {
        if ($(this).val().length > 0) {
            inputValid = true;
            return false;
        }
    });
    if (inputValid === false) {
        openErrorModal("You need to select at least one option");
    }
    else {
        $("#categories").submit();
    }
});

$(".category-close-button").on("click", function() {
    $("#category-search-form-container").slideUp();
    $("#category-search-form-container").removeAttr("data");
    $(".search-button").removeClass("search-button-clicked");
});

$(".search-button").on("click", function() {
    var category = $(this).children("p").text();
    if (category != "") {
        var categorySearchPane = $("#category-search-form-container");
        var listElement = "#list-element-" + category.toLowerCase();
        var previousCategory = $(categorySearchPane).attr("data");
        $(".list-category").hide();
        //reset the form to ensure only one category is returned to display_category when submitting 
        $('#categories')[0].reset();
        if ($(categorySearchPane).attr("data")) {
            if (previousCategory != category) {
                $(categorySearchPane).attr("data", category);
                $(listElement).show();
                $("#category-to-search").text(category);
                $(this).addClass("search-button-clicked");
                $("#search-" + previousCategory.toLowerCase()).removeClass("search-button-clicked");
            }
            else {
                $(categorySearchPane).slideUp();
                $(categorySearchPane).removeAttr("data");
                $(this).removeClass("search-button-clicked");
            }
        }
        else {
            $(categorySearchPane).slideDown();
            $(categorySearchPane).attr("data", category);
            $(listElement).show();
            $("#category-to-search").text(category);
            $(this).addClass("search-button-clicked");
        }
    }
});

//----display recipe page scripts ----//
//favourite button function
$("#mark-favourite").on("click", function() {
    var favourite = $("input", this).val();
    //toggle favourite status - appearance and value
    if (favourite === "false") {
        $("i", this).text("star");
        $("i", this).addClass("gold-star");
        $("input", this).val("true");
    }
    else {
        $("i", this).text("star_border");
        $("i", this).removeClass("gold-star");
        $("input", this).val("false");
    }
    $("#favourite-button").submit();

});

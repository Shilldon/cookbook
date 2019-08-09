function myFunc() {
  return ingredient_list
}

$(document).ready(function() {
  $('.sidenav').sidenav();
  $('.modal').modal({
    //defensive - prevent modals from being closed by clicking on background - so an option has to be selected
    dismissible: false,
  });
  $('.collapsible').collapsible();
  $('.dropdown-trigger').dropdown();
});

$("#favourite").on("click", function() {
  //ensure the favourite variable is a boolean value
  var favourite = $("#favourite_input").val();
  if (typeof(favourite) != Boolean) {
    favourite = (favourite.toLowerCase() == "true");
  }
  if (favourite == false) {
    $("i", this).text("star");
    $("i", this).addClass("gold-star");
    $("#favourite_input").val(true);
  }
  else {
    $("i", this).text("star_border");
    $("i", this).removeClass("gold-star");
    $("#favourite_input").val(false);
    favourite = $("#favourite_input").val();
  }
})

//----edit recipe scripts----//
$("#add_ingredient").on("click", function() {
  var totalIngredients = $("#ingredients").data("total_ingredients");
  totalIngredients++;
  $("#ingredients").data("total_ingredients", totalIngredients);
  var currentIngredient = $("#ingredient").val();
  var currentAmount = $("#amount").val();
  var currentUnit = $("#unit option:selected").val()
  var currentIngredients = $("#ingredients").html()
  //check if amount of ingredients has been entered - check against whether a number is input and whether string is empty
  if (isNaN(currentAmount) || currentAmount.length == 0 || currentAmount == undefined) {
    //display error modal
    $("#error-modal p").text("Please enter amount of ingredients")
    $("#error-modal").modal('open');
  }
  else if (currentIngredient.length == 0 || currentIngredient == undefined) {
    //display error modal
    $("#error-modal p").text("Please enter ingredient name")
    $("#error-modal").modal('open');
  }
  else {
    if (currentUnit === "0") { currentUnit = "" }
    $("#ingredients").html(currentIngredients + "<div class='row'><div class='col s1 valign-wrapper'><p>" + currentAmount + "</p></div><div class='col s2 valign-wrapper'><p>" + currentUnit + "</p></div><div class='col s7'><p>" + currentIngredient + " </p></div><div class='col s1'><a id='remove_ingredient' class='btn-floating btn-small waves-effect waves-light highlight3-background'><i class='material-icons'>delete</i></a></div></div><input type='hidden' name='type' value=\'" + currentIngredient + "\'></input><input type='hidden' name='amount' value=" + currentAmount + "></input><input type='hidden' name='unit' value=" + currentUnit + "></input>")
    $("#ingredient").val('');
    $("#amount").val('');
    $("#select-unit").val('');
    $('#select-unit').formSelect();
  }
});

$('body').on("click", "#remove_ingredient", function() {
  $(this).parent().parent().slideUp(500);
  var ingredientLine = $(this).parent().parent();
  setTimeout(function() { ingredientLine.remove(); }, 500);
});

$("#submit-recipe").on("click", function() {
  var name = $("#name").val();
  var ingredient = $('#ingredients').find('input').filter(':hidden:first').val();
  var method = $('#method').val();
  if (name == "") {
    $("#error-modal p").text("You need to name your receipe")
    $("#error-modal").modal('open');
  }
  else if (ingredient == undefined || ingredient == "") {
    $("#error-modal p").text("You need at least one ingredient for your recipe")
    $("#error-modal").modal('open');
  }
  else if (method == "") {
    $("#error-modal p").text("You need to provide instructions as to how to make your recipe")
    $("#error-modal").modal('open');
  }
  else {
    $("#recipe-form").submit();
  }
})

//--recipe list scripts ---//
$('body').on('click', '.delete_button', function() {
  //need to obtain the id of the recipe selected for deletion and store this on the modal to pass to flask if deletion is confirmed
  recipe_id = $(this).attr("recipe_id");
  $('#recipe_id_input').val(recipe_id)
  $(this).find(".row").addClass("selected-for-deletion")
  //need to set the row object on the reset modal button to remove the red highlight if cancelling deletion
  $('#modal_reset').data("row_to_delete", $(this).find(".row"))
})

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
})

$('.filter_button').on("click", function() {
  //disable all empty form fields to avoid sending blank fields for filter search in flask against DB
  $(".collapsible-header").removeClass(function() {
    return "active";
  });
  $(".collapsible").collapsible({ accordion: true });
  $(".collapsible").collapsible({ accordion: false });
  $("#filters_form option[value='']").attr("disabled", "disabled");
  $("#filters_form input[value='']").attr("disabled", "disabled");
});

$(".sort_by").change(function() {
  $("#sort-form").submit()
})

$("#allergens_list").change(function() {
  if ($("#allergens_list").val() != "") {
    $("#allergens-unfiltered").prop("selected", false)
  }
  else {
    $("#allergens-unfiltered").prop("selected", "selected")
  }
})

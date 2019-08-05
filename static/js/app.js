function myFunc() {
    return ingredient_list
}

    $(document).ready(function() {
      $('.sidenav').sidenav();
      $('select').formSelect();
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
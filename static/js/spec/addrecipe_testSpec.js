describe("test 1 - add recipe form error on providing no input",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $(".submit-recipe").eq(0).trigger("click");
    });

    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("You need to name your recipe You need at least one ingredient You need to provide instructions to make the recipe");
        modal.modal("close");
        $('#recipe-form').trigger("reset");
    })
})

describe("test 2 - add recipe form error on providing recipe name but nothing else",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#name").val("Test name");
        $(".submit-recipe").eq(0).trigger("click");
    });    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("You need at least one ingredient You need to provide instructions to make the recipe");        
        modal.modal("close");
        $('#recipe-form').trigger("reset");
        
    })
})

describe("test 3 - add recipe form error on providing method but nothing else",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#method").val("Test method");
        $(".submit-recipe").eq(0).trigger("click");
    });    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("You need to name your recipe You need at least one ingredient");        
        modal.modal("close");
        $('#recipe-form').trigger("reset");
        
    })
})

describe("test 4 - add recipe form error on providing no ingredients",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#name").val("Test name");
        $("#method").val("Test method");
        $(".submit-recipe").eq(0).trigger("click");
    });    
    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("You need at least one ingredient");        
        modal.modal("close");
        $('#recipe-form').trigger("reset");
    })
})

describe("test 5 - add ingredient form error on giving an ingredient name but no quantity",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
    });    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("Please enter amount of ingredients");
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})


describe("test 6 - add ingredient form error on providing an ingredient quantity but no name",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#amount").val("1");
        $("#add_ingredient").trigger("click");
    });    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("Please enter ingredient name");
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})


describe("test 7 - add recipe form error on providing no method",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#amount").val("1");
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
        
        $("#name").val("Test name");
        $(".submit-recipe").eq(0).trigger("click");

    });    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("You need to provide instructions to make the recipe");  
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
        
    })
})

describe("test 8 - add recipe form error on providing no recipe name",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#ingredients").html("");        
        $("#amount").val("1");
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
        
        $("#method").val("Test method");
        $(".submit-recipe").eq(0).trigger("click");   
    });    
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("You need to name your recipe");  
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})

describe("test 9 - add recipe form error on inputting more than 59 for minutes",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#amount").val("1");
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
        
        $("#name").val("Test name");
        $("#method").val("Test method");     
        
        $("#minutes").val("70");
        $(".submit-recipe").eq(0).trigger("click");
    });
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("Number of minutes needs to be between 0 and 60");
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})

describe("test 10 - add recipe form error on inputting less than 0 for minutes",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#amount").val("1");
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
        
        $("#name").val("Test name");
        $("#method").val("Test method");
        
        $("#minutes").val("-50");
        $(".submit-recipe").eq(0).trigger("click");      
    });
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("Number of minutes needs to be between 0 and 60");
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})


describe("test 11 - add recipe form error on inputting more than 5000 for calories",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#amount").val("1");
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
        
        $("#name").val("Test name");
        $("#method").val("Test method");
        
        $("#calories").val("5500");
        $(".submit-recipe").eq(0).trigger("click");      
    });
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("Number of calories needs to be between 0 and 5000");
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})

describe("test 12 - add recipe form error on inputting more than 5000 for calories",function() {
    let modal=$("#error-modal");
    beforeEach(function() { 
        $("#amount").val("1");
        $("#ingredient").val("Test ingredient");
        $("#add_ingredient").trigger("click");
        
        $("#name").val("Test name");
        $("#method").val("Test method");
        $("#calories").val("-200");
        $(".submit-recipe").eq(0).trigger("click");
    });
    it("should show an error modal", function() {
        expect(modal.is(":visible")).toBe(true);
        expect($("p", modal)).toHaveText("Number of calories needs to be between 0 and 5000");
        modal.modal("close");
        $("#ingredients").html("");
        $('#recipe-form').trigger("reset");
    })
})



//test favourite toggle
describe("Toggle favourite button", function() {
    let button=$("#favourite"),star=$("#star");
    //click once
    beforeEach(function() {
        value=$("#favourite_input").val(); 
    })
    it("should change the value from false to true and vice versa and add/remove gold-star class on first click", function() {
        button.trigger("click");
        var newValue=$("#favourite_input").val();
        if(value=="true") {
            expect(newValue).toBe("false");
            expect(star).not.toHaveClass("gold-star");
        }
        else if(value=="false") {
            expect(newValue).toBe("true");  
            expect(star).toHaveClass("gold-star");
        }
    })
    beforeEach(function() {
        value=$("#favourite_input").val(); 
    })    
    it("should revert the values on second click", function() {
        button.trigger("click");
        var newValue=$("#favourite_input").val();
        if(value=="true") {
            expect(newValue).toBe("false");
            expect(star).not.toHaveClass("gold-star");
        }
        else if(value=="false") {
            expect(newValue).toBe("true");  
            expect(star).toHaveClass("gold-star");
        }
    })    
})

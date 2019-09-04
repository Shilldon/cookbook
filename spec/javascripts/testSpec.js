//Check submit recipe form
describe("test 1 - display error modal on providing no input", function() {
    let name="", ingredient="", method="";
    it("should show an error modal and should display error message for method, ingredient and name", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need to name your recipe <br>You need at least one ingredient <br>You need to provide instructions to make the recipe <br>");
    });
});

describe("test 2 - display error modal on providing only name", function() {
    let name="Test Recipe", ingredient="", method="";
    it("should show an error modal and should display error message for method and ingredient", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need at least one ingredient <br>You need to provide instructions to make the recipe <br>");
    });
});

describe("test 3 - display error modal on providing only ingredient", function() {
    let name="", ingredient="Test ingredient", method="";
    it("should show an error modal and should display error message for method and name", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need to name your recipe <br>You need to provide instructions to make the recipe <br>");
    });
});

describe("test 4 - display error modal on providing only method", function() {
    let name="", ingredient="", method="Test method";
    it("should show an error modal and should display error message for ingredient and name", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need to name your recipe <br>You need at least one ingredient <br>");
    });
});

describe("test 5 - display error modal on providing only name and ingredient", function() {
    let name="Test name", ingredient="Test ingredient", method="";
    it("should show an error modal and should display error message for ingredient and name", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need to provide instructions to make the recipe <br>");
    });
});

describe("test 6 - display error modal on providing only name and method", function() {
    let name="Test name", ingredient="", method="Test method";
    it("should show an error modal and should display error message for ingredient and name", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need at least one ingredient <br>");
    });
});

describe("test 7 - display error modal on providing only ingredient and method", function() {
    let name="", ingredient="Test ingredient", method="Test method";
    it("should show an error modal and should display error message for ingredient and name", function() {
        var error=errorCheckRecipe(name,ingredient,method);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("You need to name your recipe <br>");
    });
});

describe("test 8 - display error modal on providing incorrect minutes value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", minutes=-50;
    it("should show an error modal and should display error message saying minutes should be between 0 and 59", function() {
        var error=errorCheckRecipe(name,ingredient,method,minutes);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Number of minutes needs to be between 0 and 59 <br>");
    });
});

describe("test 9 - display error modal on providing incorrect minutes value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", minutes=70;
    it("should show an error modal and should display error message saying minutes should be between 0 and 59", function() {
        var error=errorCheckRecipe(name,ingredient,method,minutes);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Number of minutes needs to be between 0 and 59 <br>");
    });
});

describe("test 10 - display error modal on providing incorrect minutes value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", calories=10000;
    it("should show an error modal and should display error message saying calories should be between 0 and 5000", function() {
        var error=errorCheckRecipe(name,ingredient,method, undefined, calories);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Number of calories needs to be between 0 and 5000 <br>");
    });
});

describe("test 11 - display error modal on providing incorrect minutes value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", calories=-100;
    it("should show an error modal and should display error message saying calories should be between 0 and 5000", function() {
        var error=errorCheckRecipe(name,ingredient,method, undefined, calories);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Number of calories needs to be between 0 and 5000 <br>");
    });
});

describe("test 12 - display error modal on providing incorrect minutes value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", minutes="one hundred";
    it("should show an error modal and should display error message saying calories should be between 0 and 5000", function() {
        var error=errorCheckRecipe(name,ingredient,method, minutes);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Number of minutes needs to be between 0 and 59 <br>");
    });
});

describe("test 13 - do not display error modal on blank minutes value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", minutes=undefined;
    it("should show an error modal and should display error message saying calories should be between 0 and 5000", function() {
        var error=errorCheckRecipe(name,ingredient,method, minutes);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(false);
        expect(errorMessage).not.toContain("Number of minutes needs to be between 0 and 59 <br>");
    });
});

describe("test 14 - do not display error modal on blank calories value", function() {
    let name="Test Name", ingredient="Test ingredient", method="Test method", minutes=10,calories=undefined;
    it("should show an error modal and should display error message saying calories should be between 0 and 5000", function() {
        var error=errorCheckRecipe(name,ingredient,method, minutes, calories);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(false);
        expect(errorMessage).not.toContain("Number of minutes needs to be between 0 and 59 <br>");
    });
});

//check add ingredients form
describe("test 15 - display error modal on providing no ingredient name or amount", function() {
    let name="", amount="";
    it("should show an error modal and should display error message saying ingredient name and amount are missing", function() {
        var error=errorCheckIngredient(name,amount);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Please enter ingredient name <br>Please enter amount of ingredients <br>");
    });
});

describe("test 16 - display error modal on providing no ingredient amount", function() {
    let name="Test ingredient", amount="";
    it("should show an error modal and should display error message saying ingredient amount is missing", function() {
        var error=errorCheckIngredient(name,amount);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Please enter amount of ingredients <br>");
    });
});

describe("test 17 - display error modal on providing no ingredient name", function() {
    let name="", amount="2";
    it("should show an error modal and should display error message saying ingredient name is missing", function() {
        var error=errorCheckIngredient(name,amount);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Please enter ingredient name <br>");
    });
});

describe("test 18 - display error modal on providing non-string ingredient", function() {
    let name=123, amount="1";
    it("should show an error modal and should display error message saying ingredient name is incorrect", function() {
        var error=errorCheckIngredient(name,amount);
        var callModal=error[0];
        var errorMessage=error[1];
        expect(callModal).toBe(true);
        expect(errorMessage).toContain("Please enter ingredient name <br>");
    });
});

describe("test 19 - valid ingredients expect no error modal", function() {
    let name="Test Name", amount="1";
    it("should not show an error modal", function() {
        var error=errorCheckIngredient(name,amount);
        var callModal=error[0];
        expect(callModal).toBe(false);
    });
});
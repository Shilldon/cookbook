




//test favourite toggle
describe("Toggle favourite button", function() {
    let value,button=$("#mark-favourite");
    //click once
    beforeEach(function() {
        value=$("input", button).val();   
    })
    it("should change the value to false to true when clicked and back when clicked again", function() {
        button.trigger("click");
        var newValue=$("input", button).val();
        if(value=="true") {
            expect(newValue).toBe("false");
            expect(button).not.toHaveClass("gold-star")
        }
        else {
            expect(newValue).toBe("true");  
            expect(button).toHaveClass("gold-star");
        }
    })
})




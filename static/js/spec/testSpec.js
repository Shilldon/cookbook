




describe("test 1 - add recipe form error on providing no input", function() {
    let errorModal = $("#error-modal");
    it("open an error modal", function() {
        errorCheckRecipe("","","","","")
        spyOn($modal,"open")
        expect($modal).toHaveBeenCalled();
    })
})




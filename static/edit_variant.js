function updateMsg() {
    const checkboxes = document.querySelectorAll('input[name="review"]:checked');
    console.log(checkboxes)
    if (checkboxes.length > 0) {
        return confirm('Do you want to update?');
    }
    return true;
}
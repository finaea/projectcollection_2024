var exp = document.getElementsByClassName("expand");

for (var i = 0; i < exp.length; i++) {
    exp[i].addEventListener("click", function () {
        this.classList.toggle("pressed");
        var content = this.nextElementSibling;
        if (content.style.display === "block") {
            content.style.display = "none";
        } else {
            content.style.display = "block";
        }
    });
}

function validate() {
    var t_name = document.forms["form"]["name"].value;
    var t_email = document.forms["form"]["email"].value;
    var t_desc = document.forms["form"]["desc"].value;

    if (t_name == "" || t_email == "" || t_desc == "") {
        alert("Please fill in all the blanks.");
        return false;
    }
    else {
        alert('Your form has been submitted.')
        return true;
    }
}
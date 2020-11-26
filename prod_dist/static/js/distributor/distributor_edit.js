function validate_mobile()
{
    var mobile = document.getElementById("Mobile").value;
    var mobile_help = document.getElementById("mobile-help");

    if (mobile.length!=10)
    {
        console.log(mobile);
        mobile_help.innerHTML = "Mobile number has to have 10 digits";
        mobile_help.className = "text-danger";
        mobile_help.style.display = "block";
        return false;
    }
    else
    {
        mobile_help.innerHTML = "";
        mobile_help.className = "";
        mobile_help.style.display = "none";
        return true;
    }
}

function validate_form()
{
    var distributor_edit_form = document.getElementById("distributor_edit_form");
    if(validate_mobile())
    {
        distributor_edit_form.submit();
    }
}
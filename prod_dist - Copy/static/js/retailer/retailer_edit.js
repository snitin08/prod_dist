function validate_form()
{
    var form = document.getElementById("retailer edit");
    console.log("Insided validate form");
    var address = validate_address();
    var city= validate_city();
    var name = validate_first_name();
    var gst = validate_gst();
    var mobile = validate_mobile();
    var state = validate_state();
    var val = address && city && name 
    && gst && mobile && state;
    if(val)
    {
        form.submit();
    }
}

function validate_mobile()
{
    var mobile = document.getElementById("Mobile").value;
    var mobile_help = document.getElementById("mobile-help");

    if(mobile.length!=10)
    {
        mobile_help.innerHTML="Mobile number should be 10 digits long.";
        mobile_help.style.display="block";  
        return false;
    }
    else
    {
        var count = 0;
        for(var i=0;i<mobile.length;i++)
        {
            if(mobile[i]>='0' && mobile[i]<='9')
                count++;
        }
        if(count!=10)
        {
            mobile_help.innerHTML="Mobile number should have only numbers";
            mobile_help.style.display="block";
            return false;
        }
        else
        {
            mobile_help.innerHTML="";
            mobile_help.style.display="none";
            return true;
        }
    }
}

function validate_first_name()
{
    var first_name = document.getElementById("first name").value;
    var first_name_help = document.getElementById("first_name_help");

    if(first_name.length>0)
    {
        first_name_help.innerHTML="";
        first_name_help.style.display="none";
        return true;
    }
    else
    {
        first_name_help.innerHTML="First name cannot be empty";
        first_name_help.style.display="block";
        return false;
    }
}

function validate_gst()
{
    var gst_number = document.getElementById("gst number").value;
    var gst_help = document.getElementById("gst-help");

    if(gst_number.length>0)
    {
        gst_help.innerHTML="";
        gst_help.style.display = "none";
        return true;
    }
    else
    {
        gst_help.innerHTML="GST number cannot be empty."
        gst_help.style.display="block";
        return false;        
    }
}

function validate_address()
{
    var address = document.getElementById("address").value;
    var address_help = document.getElementById("address_help");

    if(address.length>0)
    {
        address_help.innerHTML="";
        address_help.style.display = "none";
        return true;
    }
    else
    {
        address_help.innerHTML="Address cannot be empty."
        address_help.style.display="block";
        return false;        
    }
}

function validate_state()
{
    var state = document.getElementById("state").value;
    var state_help = document.getElementById("state_help");

    if(state.length>0)
    {
        state_help.innerHTML="";
        state_help.style.display = "none";
        return true;
    }
    else
    {
        state_help.innerHTML="State cannot be empty."
        state_help.style.display="block";
        return false;        
    }
}

function validate_city()
{
    var city = document.getElementById("city").value;
    var city_help = document.getElementById("city_help");

    if(city.length>0)
    {
        city_help.innerHTML="";
        city_help.style.display = "none";
        return true;
    }
    else
    {
        city_help.innerHTML="city cannot be empty."
        city_help.style.display="block";
        return false;        
    }
}




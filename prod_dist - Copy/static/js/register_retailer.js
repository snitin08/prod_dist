function validate_form()
{
    const pass = document.getElementById('Password').value;
    const re_password = document.getElementById('re-password').value;
    const submit_button = document.getElementById('submit');
    const register_retailer_form = document.getElementById('retailer register');
    var pass_not_match = document.getElementById('pass_not_match');
    console.log("password=re",pass===re_password);
    
    var mobile_validate = validate_mobile_number();
    if(pass!==re_password)
    {
        var pass_not_match = document.getElementById("pass_not_match");
        pass_not_match.innerHTML="Passwords do not match";
        pass_not_match.style.display = 'block';
        var pass_help = document.getElementById('pass-help');
        var repass_help = document.getElementById('repass-help');
        pass_help.className="";
        repass_help.className="";
       
    }
    else{
        pass_not_match.style.display = 'none';
        if(validate_password() && mobile_validate)
        {
            
            console.log(pass);
            console.log(re_password);
            register_retailer_form.submit();
        }
    }
}

function validate_password()
{
    // Minimum of 6 chars
    // Atleast one uppercase letter
    // Atleast one lowercase letter
    // Atleast one number
    const pass = document.getElementById('Password').value;
    const re_password = document.getElementById('re-password').value;

    var pass_length = pass.length;
    
    if(pass_length<6)
    {
        var pass_help = document.getElementById('pass-help');
        var repass_help = document.getElementById('repass-help');
        pass_help.className="text-danger";
        repass_help.className="text-danger";
        return false;
    }
    else
    {
        var n_upper= 0, n_lower=0, n_number = 0;
        var i=0;
        var character = '';
        while(i<pass.length)
        {
            character = pass.charAt(i);
            if(character>='0' && character<='9')
                n_number++;
            else if(character===character.toLowerCase())
                n_lower++;
            else if(character===character.toUpperCase())
                n_upper++;            
            i++;
        }
        if(n_upper>=1 && n_lower>=1 && n_number>=1)
            return true;
        else
        {
            var pass_help = document.getElementById('pass-help');
            var repass_help = document.getElementById('repass-help');
            pass_help.className="text-danger";
            repass_help.className="text-danger";
            return false;
        }
    }
    
}

function validate_mobile_number()
{
    var mobile = document.getElementById('Mobile').value;
    console.log("Mobile number",mobile);
    var mobile_help = document.getElementById('mobile-help');
    if(mobile.length!=10)
    {
        
        mobile_help.style.display='block';
        mobile_help.className="text-danger";
        mobile_help.innerHTML = "Not a valid mobile number. Should have 10 digits";
        return false;
    }
    else
    {
        
        mobile_help.style.display='none';
        return true;
    }
    
}
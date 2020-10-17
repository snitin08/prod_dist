function validate_login()
{
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    var email_help = document.getElementById('email-help');
    var password_help = document.getElementById('password-help');

    if(email.length===0)
    {
        email_help.innerHTML = "Email is required";        
    }
    if(password.length===0)
    {
        password_help.innerHTML= "Password is required";
    }
    if(email.length>0 && password.length>=6)
    {
        var f = document.getElementById('login-form');
        f.submit();
    }
}
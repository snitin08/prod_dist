function update_receipt(url)
{
    var comments = document.getElementById("comments").value;
    var defects = document.querySelectorAll("input[name='defective']");
    var form = document.getElementById("send_fedback");
    var url = form.getAttribute("action");
    defective_forms = document.querySelectorAll(".defective_form");
    var satisfy = true;
    for(var i=0;i<defective_forms.length;i++)
    {
        satisfy = defective_forms[i].checkValidity();
        if(!satisfy)
        {
            defective_forms[i].reportValidity();
            break;
        }
    }

    if(satisfy)
    {
        var csrf_token = document.querySelector("input[name='csrfmiddlewaretoken']").value;
        var defect_numbers = [];
        data = {};
        for(var i=0;i<defects.length;i++)
        {
            defect_numbers[i] = defects[i].value;
        }
        data["defects"] = JSON.stringify(defect_numbers);
        data["comments"] = comments;
        data["csrfmiddlewaretoken"] = csrf_token;
        
        console.log(data)
        $.post(url, data,function(data){
            console.log(data);
            if(data.status==1)
            {    
                var success_element = document.getElementById("success-alert");
                success_element.innerHTML = "Feedback sent successfully."
                $("#success-alert").show();
                setTimeout(function() { $("#success-alert").hide(); }, 5000);
                var timer = setTimeout(function() {
                    window.location = "{% url 'receipt:receipt_list' %}";
                }, 3000);
            }
        });
    }    
    
}
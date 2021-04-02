console.log("mounted carry on")


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var form = document.getElementById('userform')
var ref_code = document.getElementById('ref0code').value
 form.addEventListener('submit', function(e){
 e.preventDefault()
 console.log(ref_code);
 sendData();
// window.location.reload();

})
function sendData() {

 var form = {
     "ref_code" : ref_code,
    
 }

 var url = "/super/admin/users/disable/"
 fetch(url, {
     method:'POST',
     headers:{
         'Content-Type':'applicaiton/json',
         "X-CSRFToken": getCookie("csrftoken"),
     },
     body:JSON.stringify({'form':form}),

 })
 .then((response) => response.json())
 .then((data) => {
     console.log('Success:', data);
     document.getElementById("ifot").innerText = data.user


     })

}











var formE = document.getElementById('enableForm')
var ref_code_e = document.getElementById('ref000code').value
formE.addEventListener('submit', function(e){
 e.preventDefault()
 console.log(ref_code_e);
 sendDataE()
// window.location.reload();
})
function sendDataE() {

 var form = {
     "ref_code_e" : ref_code_e,
    
 }

 var url = "/super/admin/users/enable/"
 fetch(url, {
     method:'POST',
     headers:{
         'Content-Type':'applicaiton/json',
         "X-CSRFToken": getCookie("csrftoken"),
     },
     body:JSON.stringify({'form':form}),

 })
 .then((response) => response.json())
 .then((data) => {
     console.log('Success:', data);
     document.getElementById("ifot").innerText = data.user

     })

}


var formAdd = document.getElementById('formAdd')
formAdd.addEventListener('submit', function(e){
 e.preventDefault()
 ajaxLogin();
// window.location.reload();
})



function ajaxLogin(){
 
    $.ajax({
        type: "POST",
        url: "/super/admin/users/add_fund/",
        data: {
            amount:$('#amountAdd').val(),
            ref:$('#re-0099').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        beforeSend: function(){
            $("#userloader").show();
          },
        success: function(data) {
            document.getElementById("ifot").innerText = data.user
        }   
     }); 
     return false;   
}






var deductForm = document.getElementById('deductForm')
deductForm.addEventListener('submit', function(e){
 e.preventDefault()

 deductFee()
 // window.location.reload();

})



function deductFee(){
 
    $.ajax({
        type: "POST",
        url: "/super/admin/users/deduct/",
        data: {
            amountbal:$('#amountDeduct').val(),
            reffer:$('#userr').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success: function(data) {
            document.getElementById("ifot").innerText = data.user
        }   
     }); 
     return false;   
}







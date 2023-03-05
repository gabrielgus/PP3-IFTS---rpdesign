//validaciones del formulario de alta de usuario

function validarForm(){

  var regex = new RegExp('^[A-Z\u00E0-\u00FC]+$', 'i'); //expresion regular para validar solo letras y acentos
  var regex2 = new RegExp(/(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])/)//expresion regular para validar correo
  var regex3 = new RegExp('^[A-Z0-9]+$', 'i'); //expresion regular para validar solo letras y números
  var regex4 = new RegExp(/^[0-9]{7,8}$/); //expresion regular para validar solo números
  var regex5 = new RegExp(/^[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]{8,15}$/); //expresion regular para validar

  
function validaNombre(){
  
  var your_name = document.getElementById("id_first_name").value;
  var elemento = document.getElementById("id_first_name");

  if(regex.test(your_name) && (your_name != "null")){
    elemento.className = "form-control";
    return true;
  }
  else {
    elemento.className += " erro";
    alert("Ingrese un nombre válido");
    return false;
  }
}

function validaApellido(){

  var your_surname = document.getElementById("id_last_name").value;
  var elemento = document.getElementById("id_last_name");

  if(regex.test(your_surname) && (your_surname != "null")){
    elemento.className = "form-control";
    return true;
  }  
  else {
    elemento.className += " erro";
    alert("Ingrese un apellido válido");
    return false;
  }    
}

function validaMail(){

  var your_email = document.getElementById("id_email").value;
  var elemento = document.getElementById("id_email");

  if(regex2.test(your_email) && (your_email != "null")){
    elemento.className = "form-control";
    return true;
  }  
  else {
    elemento.className += " erro";
    alert("Ingrese una dirección de correo válida");
    return false;
  }    
}

function validaUser(){

  var your_user = document.getElementById("id_username").value;
  var elemento = document.getElementById("id_username");

  if(regex3.test(your_user) && (your_user != "null")){
    elemento.className = "form-control";
    return true;
  }  
  else {
    elemento.className += " erro";
    alert("Ingrese un usuario válido");
    return false;
  }    
}

function validaDni(){

  var your_dni = document.getElementById("id_dni").value;
  var elemento = document.getElementById("id_dni");

  if(regex4.test(your_dni) && (your_dni != "null") && (your_dni > 0 && your_dni <= 99999999)){
    elemento.className = "form-control";
    return true;
  }  
  else {
    elemento.className += " erro";
    alert("Ingrese un documento válido");
    return false;
  }    
}

function validaPass(){

  var your_pass = document.getElementById("id_password1").value;
  var your_passb = document.getElementById("id_password2").value;
  var elemento = document.getElementById("id_password1");
  var elemento2 = document.getElementById("id_password2");

  if (your_pass === your_passb){
      if(regex5.test(your_pass) && (your_pass != "null")){
        elemento.className = "form-control";
        return true;
      } else {
        elemento.className += " erro";
        alert("La contraseña debe tener entre 8 y 15 caracteres");
        return false;
      }  
    } else {
      elemento2.className += " erro";
      alert("La contraseña no coincide");
      return false;
    }
}

  if((validaNombre() == true) && (validaApellido() == true) && (validaMail() == true) && (validaUser() == true) && (validaDni() == true) && (validaPass() == true)){
      return true;
  }  
  else
    return false;
}
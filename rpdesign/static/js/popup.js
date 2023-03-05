//popup debe estar registrado para comprar

var btnAbrir = document.getElementsByClassName('card-button');
var overlay = document.getElementById('overlay');
var popup = document.getElementById('popup');
var btnCerrar = document.getElementById('btn-cerrar-popup');

for (i=0; i < btnAbrir.length; i++) {
  btnAbrir[i].addEventListener("click",function(){
    overlay.classList.add("active");
  });
}

btnCerrar.addEventListener("click", function(){
  overlay.classList.remove("active");
});
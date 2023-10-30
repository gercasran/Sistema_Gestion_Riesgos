function mostrarSubTabla(button) {
    var idElemento = button.getAttribute("idelemento");
    var subtabla = document.getElementById("subtable_" + idElemento);
    if(subtabla.style.display == 'none') subtabla.style.display = '';
    else subtabla.style.display = 'none';
}
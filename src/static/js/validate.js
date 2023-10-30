document.addEventListener('DOMContentLoaded', function () {
    const expresionCorreo = /^[a-zA-Z0-9._%+-]+@(gmail|hotmail|outlook|live|msn|yahoo)\.(com|es|mx|co\.uk|fr|de|it)$/;

    const formulario = document.getElementById("formulario");
    const emailInput = document.getElementsByName("email");

    formulario.addEventListener('submit', function (e) {
        const emailValue = emailInput[0].value.trim();

        if (!expresionCorreo.test(emailValue)) {
            e.preventDefault();
            alert("Por favor, ingrese una dirección de correo electrónico válida (Gmail, Hotmail, Outlook, Live, MSN o Yahoo).");
        }
    });
});


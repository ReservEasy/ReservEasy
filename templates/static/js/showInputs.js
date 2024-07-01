document.addEventListener('DOMContentLoaded', function() {
    var discenteRadio = document.getElementById("discente");
    var servidorRadio = document.getElementById("servidor");
    var inputsComuns = document.getElementById("inputs-comuns");
    var inputsDiscente = document.getElementById("inputs-discente");
    var inputsServidor = document.getElementById("inputs-servidor");
    var formCheckFinal = document.getElementById("formCheckFinal");

    function exibirFormularioSelecionado() {
        inputsComuns.style.display = "flex";
        formCheckFinal.style.display = "flex";
        if (discenteRadio.checked) {
            inputsDiscente.style.display = "flex";
            inputsServidor.style.display = "none";
        } else if (servidorRadio.checked) {
            inputsDiscente.style.display = "none";
            inputsServidor.style.display = "flex";
        }
    }

    if (inputsDiscente.querySelectorAll('.error').length > 0) {
        inputsComuns.style.display = "flex";
        inputsDiscente.style.display = "flex";
        formCheckFinal.style.display = "flex";
        inputsServidor.style.display = "none";
        discenteRadio.checked = true;
    } else if (inputsServidor.querySelectorAll('.error').length > 0) {
        inputsComuns.style.display = "flex";
        inputsDiscente.style.display = "none";
        formCheckFinal.style.display = "flex";
        inputsServidor.style.display = "flex";
        servidorRadio.checked = true;
    } else {
        inputsComuns.style.display = "none";
        formCheckFinal.style.display = "none";
    }

    discenteRadio.addEventListener('change', exibirFormularioSelecionado);
    servidorRadio.addEventListener('change', exibirFormularioSelecionado);
});



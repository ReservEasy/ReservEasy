function showInputsForm() {
    var discenteRadio = document.getElementById("discente");
    var servidorRadio = document.getElementById("servidor");
    var servidorInputs = document.getElementById("cadastro-form-servidor");
    var discenteInputs = document.getElementById("cadastro-form-discente");

    if (discenteRadio.checked) {
        discenteInputs.style.display = "flex";
        servidorInputs.style.display = "none";
    } else if (servidorRadio.checked) {
        discenteInputs.style.display = "none";
        servidorInputs.style.display = "flex";
        var cargoInput = servidorInputs.querySelector("[name='cargo']");
    cargoInput.value = "";
    }
    
}; 

document.addEventListener('DOMContentLoaded', (event) => {
    var passwordField = document.getElementById('id_password');
    passwordField.setAttribute('type', 'password');
});
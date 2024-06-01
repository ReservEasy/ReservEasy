document.addEventListener('DOMContentLoaded', function() {
    const passwordField = document.getElementById('id_password');

    // Criar um contêiner ao redor do campo de senha
    const wrapper = document.createElement('div');
    wrapper.classList.add('password-wrapper');
    passwordField.parentNode.insertBefore(wrapper, passwordField);
    wrapper.appendChild(passwordField);

    // Criar o ícone de olho
    const toggleIcon = document.createElement('i');
    toggleIcon.classList.add('fas', 'fa-eye', 'toggle-password');
    wrapper.appendChild(toggleIcon);

    // Adicionar o evento de clique para mostrar/esconder a senha
    toggleIcon.addEventListener('click', function() {
        const isPassword = passwordField.type === 'password';
        passwordField.type = isPassword ? 'text' : 'password';
        toggleIcon.classList.toggle('fa-eye');
        toggleIcon.classList.toggle('fa-eye-slash');
    });
});
// document.getElementById("btnVoltar").onclick = function() {
//     window.history.back();
// };

document.getElementById("btnVoltar").onclick = function() {
    // Verifica se há uma página anterior ou se o document.referrer está vazio
    if (document.referrer === "" || window.history.length === 1) {
        // Redireciona para a página padrão
        window.location.pathname = "/recursos/";
    } else {
        // Obter o caminho da URL da página anterior (após o domínio)
        var previousPath = new URL(document.referrer).pathname;

        // Define os caminhos das páginas permitidas para navegação
        var allowedPaths = [
            "/setor/listar",     // Caminho da página de listar setores
            "/usuario/listar",   // Caminho da página de listar usuários
            "/recurso/listar"    // Caminho da página de listar recursos
        ];

        // Define um caminho padrão para redirecionar se a anterior não for permitida
        var defaultPath = "/recursos/";

        // Verifica se o caminho da página anterior está na lista de caminhos permitidos
        if (allowedPaths.includes(previousPath)) {
            // Volta para a página anterior
            window.history.back();
        } else {
            // Redireciona para o caminho padrão
            window.location.pathname = defaultPath;
        }
    }
};

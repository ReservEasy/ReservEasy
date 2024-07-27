document.getElementById("btnVoltar").onclick = function() {
    // Obtém a lista de páginas visitadas
    let visitedPages = JSON.parse(sessionStorage.getItem('visitedPages')) || [];

    // Encontra a página anterior na lista
    let currentPageIndex = visitedPages.indexOf(window.location.href);
    if (currentPageIndex > 0) {
        // Se houver uma página anterior na lista de páginas visitadas, redireciona para ela
        let previousPage = visitedPages[currentPageIndex - 1];
        window.location.href = previousPage;
    } else if (window.history.length > 1) {
        // Caso contrário, tenta usar o histórico do navegador
        window.history.go(-1);
    } else {
        // Caso contrário, redireciona para uma URL padrão
        window.location.href = '/recurso/';
    }
};

// SEARCH 

function normalizeText(text) {
    return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function search() {
    let input = normalizeText(document.getElementById("searchbar").value);
    let rows = document.querySelectorAll('.tr-row');
    let count = 0;

    rows.forEach(row => {
        let nameCell = row.querySelector('.recurso-view');
        if (nameCell) {
            let normalizedText = normalizeText(nameCell.textContent);
            if (normalizedText.includes(input)) {
                row.style.display = "";
                count++;
            } else {
                row.style.display = "none";
            }
        }
    });

    document.getElementById("resource-count").textContent = count;
}

document.addEventListener('DOMContentLoaded', (event) => {
    let rows = document.querySelectorAll('.tr-row');
    // Ignora o cabeçalho da tabela ao contar
    let initialCount = rows.length > 0 ? rows.length - 1 : 0;
    document.getElementById("resource-count").textContent = initialCount;
});
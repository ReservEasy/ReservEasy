document.addEventListener('DOMContentLoaded', function() {
    // Obtém o input file e o parágrafo pai
    var inputFile = document.getElementById('id_imagem');
    var parentParagraph = inputFile.parentNode;

    // Cria uma div para agrupar o rótulo personalizado e o botão de remoção
    var wrapperDiv = document.createElement('div');
    wrapperDiv.className = 'file-input-wrapper';

    // Cria o label personalizado
    var customLabel = document.createElement('label');
    customLabel.setAttribute('for', 'id_imagem');
    customLabel.className = 'person-file-label';
    customLabel.textContent = 'Clique aqui para escolher um arquivo';

    // Cria o botão de remoção de arquivo
    var removeButton = document.createElement('button');
    removeButton.className = 'remove-file-btn';
    removeButton.textContent = 'Remover arquivo';
    removeButton.type = 'button';

    // Insere o label e o botão personalizados na div de agrupamento
    wrapperDiv.appendChild(customLabel);
    wrapperDiv.appendChild(removeButton);

    // Insere a div de agrupamento após o input file
    parentParagraph.insertBefore(wrapperDiv, inputFile.nextSibling);

    // Adiciona o evento de mudança no input file
    inputFile.addEventListener('change', function() {
        var fileName = this.files[0] ? this.files[0].name : 'Nenhum arquivo selecionado';
        customLabel.textContent = fileName;
        customLabel.classList.add('attached'); // Adiciona a classe para mudar a cor
        removeButton.classList.add('visible'); // Torna o botão visível
    });

    // Adiciona o evento de clique no botão de remoção
    removeButton.addEventListener('click', function() {
        inputFile.value = ''; // Limpa o valor do input file
        customLabel.textContent = 'Clique aqui para escolher um arquivo';
        customLabel.classList.remove('attached'); // Remove a classe para mudar a cor
        removeButton.classList.remove('visible'); // Esconde o botão
    });
});

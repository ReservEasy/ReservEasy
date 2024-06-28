function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#image-preview').html('<img src="' + e.target.result + '" alt="Pré-visualização">');
        };
        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function() {
    $('#id_imagem').on('change', function() {
        readURL(this);
    });

    $('.remove-file-btn').on('click', function() {
        $('#id_imagem').val(''); // Limpa o valor do input
        $('#image-preview').html('<span>Pré-visualização da imagem</span>');
        $('#image-preview').css('background-color', '#f0f0f0');
    });
});
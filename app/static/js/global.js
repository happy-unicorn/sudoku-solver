$(document).ready(function() {
    $('.input-file').change(function() {
        console.log($(this).val());
        if ($(this).val() !== '') {
            $('#button-submit').prop('disabled', false);
            $('.input-wrapper-file').addClass('input-wrapper-file-busy');
        } else {
            $('.input-wrapper-file').removeClass('input-wrapper-file-busy');
            $('#button-submit').prop('disabled', true);
        }
    });

    $('#button-reset').click(function () {
        $('.input-file').val('').trigger('change');
    });
});
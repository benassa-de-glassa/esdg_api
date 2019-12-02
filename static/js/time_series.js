
$(document).ready(function() {
    $('#query-button-time-series').on('click', function(event) {
    $.ajax({
        data : {
            selected_folder: $('#listbox-folder').val(),
            selected_dataset: $('#listbox-dataset').val(),
            selected_countries: $('#listbox-country').val(),
            selected_products: $('#listbox-products').val(),
            selected_elements: $('#listbox-elements').val()
                },
            type : 'GET',
            url : '/ajax/timeseries/plot'
            })
        .done(function(output) {
            $('#time-series').html(output)

        });
    event.preventDefault();
    });
});
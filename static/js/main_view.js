// get folders for first listbox
$(document).ready(function() {
    $.ajax({
        data : {},
            type : 'GET',
            url : '/ajax/index/folder_listbox'
            })
        .done(function(output) {
            $('#listbox-folder').html(output);
        });
    });

// get folders for second listbox
$(document).ready(function() {
    $('#listbox-folder').on('change', function(event) {
    $.ajax({
        data : {
            selected_folder: $('#listbox-folder').val()
                },
            type : 'GET',
            url : '/ajax/index/dataset_listbox'
            })
        .done(function(data) {
            $('#listbox-dataset').html(data);
        });
    event.preventDefault();
    });
});

// get countries for third listbox, products for fourth and elements for fifth
$(document).ready(function() {
    $('#listbox-dataset').on('change', function(event) {
    $.ajax({
        data : {
            selected_folder: $('#listbox-folder').val(),
            selected_dataset: $('#listbox-dataset').val()
                },
            type : 'GET',
            url : '/ajax/index/country_listbox'
            })
        .done(function(output) {
            $('#listbox-country').html(output['countries']);
            $('#listbox-products').html(output['products']);
            $('#listbox-elements').html(output['elements']);
        });
    event.preventDefault();
    });
});

// table for displaying data
$(document).ready(function() {
    $('#query-button').on('click', function(event) {
    $.ajax({
        data : {
            selected_folder: $('#listbox-folder').val(),
            selected_dataset: $('#listbox-dataset').val(),
            selected_countries: $('#listbox-country').val(),
            selected_products: $('#listbox-products').val(),
            selected_elements: $('#listbox-elements').val()
                },
            type : 'GET',
            url : '/ajax/index/data_table'
            })
        .done(function(output) {
            $('#data-table').html(output);
        });
    event.preventDefault();
    });
});


// TODO write JS skript which takes JSON and returns it in html form for reduced traffic
// $(document).ready(function(){
//     $('#query-button').on('click', function(event) {
//     $.ajax({
//         data : {
//             selected_folder: $('#listbox-folder').val(),
//             selected_dataset: $('#listbox-dataset').val(),
//             selected_countries: $('#listbox-country').val(),
//             selected_products: $('#listbox-products').val(),
//             selected_elements: $('#listbox-elements').val()
//                 },
//             type : 'GET',
//             url : '/ajax/index/data_table_json'
//             })
//         .done(function(output) {
//             var html_rows = []
//             var keys = []

//             for (let i = 0; i < output.length; i++) {
//                 const element = output[i];
//                 if (element.key )
                
//             }
//             $.each( output, function(key, val){
//                 rows[key].push("<tr id='" + key + "'>" + val + "</td>")
//             })
                
//             }
//         });
//     event.preventDefault();
//     });
// });

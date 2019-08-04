// get folders for first listbox
$(document).ready(function() {
    $.ajax({
        data : {
                },
            type : 'GET',
            url : '/ajax/folder_listbox'
            })
        .done(function(data) {
            $('#listbox-folder').text(data.output).show();
        });
    });

// get foldes for second listbox
$(document).ready(function() {
    $('#listbox-folder').on('change', function(event) {
    $.ajax({
        data : {
                },
            type : 'GET',
            url : '/ajax/dataset_listbox'
            })
        .done(function(data) {
            $('#testingparagraph').text(data);
        });
    event.preventDefault();
    });
});
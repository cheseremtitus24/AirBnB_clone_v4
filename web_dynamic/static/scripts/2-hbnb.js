// Executes Once all Dom Objects including images.. have loaded
const dictionary = new Object();
$(window).on('load', function () //executed only when DOM is loaded
{
    // create and empty dictionary to store checked - checkboxes
    // Iterates through all list items and sets their id and data-name
    // to the dynamically generated checkboxes
    function paint_amenities(dictionary)
    {
        let display_string = "";
        let counter = 0;
        for (let key in dictionary) {
            if (counter == 0) {
                display_string += dictionary[key];
                counter += 1;
            }
            else
                display_string += ","+dictionary[key];
        }
        return display_string;
    }
    $(".amenities .popover li").each(function () {
        let li_id = $(this).attr('id');
        let d_name = $(this).attr('data-name');
        $(this).prepend('<input type="checkbox" data-name="' + d_name + '" data-id="' + li_id + '"  style="padding-right: 10px">')

    });
    // Listen for changes on each input checkbox tag
    // Works with dictionaries since lookup & CRUD is very fast
    $(".amenities .popover ul li :checkbox").change(function () {
        if ($(this).is(':checked')) {
            console.log($(this).attr('data-id') + 'is now checked');
            // Add item to dictionary
            dictionary[$(this).attr('data-id')] = $(this).attr('data-name');

            $(".amenities h4").html( paint_amenities(dictionary));

        } else {
            // delete item when unchecked
            delete dictionary[$(this).attr('data-id')];

            $(".amenities h4").html( paint_amenities(dictionary));

            console.log($(this).attr('data-id') + 'is now unchecked');

        }
    })
    $(function () {
        const selected = $('DIV#api_status');
        const api_color = $('#api_status');
            $.ajax(
                {
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://0.0.0.0:5001/api/v1/status/',
                    success: function (results) {
                        if (results.status == "OK")
                        {
                            $('#api_status').css({'background-color':'#ff545f'});
                            selected.addClass('available');
                            console.log("API endpoint is current active on port 0.0.0.0:5001/api/v1/status")
                            // selected.style('background-color')
                        }
                        else
                        {
                            if (selected.hasClass('available'))
                                selected.removeClass('available');
                            $('#api_status').css({'background-color':'#cccccc'});


                        }

                    },
                    error: function () {
                        if (selected.hasClass('available'))
                            selected.removeClass('available');
                        $('#api_status').css({'background-color':'#cccccc'});
                        console.error("API endpoint is offline on port 0.0.0.0:5001/api/v1/status")
                    }
                });
        }
    );


});

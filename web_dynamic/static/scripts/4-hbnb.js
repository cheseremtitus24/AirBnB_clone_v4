// Executes Once all Dom Objects including images.. have loaded
const dictionary = new Object();
// Makes use of Async Await ChatGPT Help
function makeGetRequest(url) {
    return new Promise(function(resolve, reject) {
        $.get(url, function(data) {
            resolve(data);
        }).fail(function(error) {
            reject(error);
        });
    });
}
$(window).on('load', function () //executed only when DOM is loaded
{
    // create and empty dictionary to store checked - checkboxes
    // Iterates through all list items and sets their id and data-name
    // to the dynamically generated checkboxes
    function paint_amenities(dictionary) {
        let display_string = "";
        let counter = 0;
        for (let key in dictionary) {
            if (counter == 0) {
                display_string += dictionary[key];
                counter += 1;
            } else
                display_string += "," + dictionary[key];
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

            $(".amenities h4").html(paint_amenities(dictionary));

        } else {
            // delete item when unchecked
            delete dictionary[$(this).attr('data-id')];

            $(".amenities h4").html(paint_amenities(dictionary));

            console.log($(this).attr('data-id') + 'is now unchecked');

        }
    });
    $(function () {
            const selected = $('DIV#api_status');
            const api_color = $('#api_status');
            $.ajax(
                {
                    type: 'GET',
                    dataType: 'json',
                    url: 'http://0.0.0.0:5001/api/v1/status/',
                    success: function (results) {
                        if (results.status == "OK") {
                            $('#api_status').css({'background-color': '#ff545f'});
                            selected.addClass('available');
                            console.log("API endpoint is current active on port 0.0.0.0:5001/api/v1/status")
                            // selected.style('background-color')
                        } else {
                            if (selected.hasClass('available'))
                                selected.removeClass('available');
                            $('#api_status').css({'background-color': '#cccccc'});


                        }

                    },
                    error: function () {
                        if (selected.hasClass('available'))
                            selected.removeClass('available');
                        $('#api_status').css({'background-color': '#cccccc'});
                        console.error("API endpoint is offline on port 0.0.0.0:5001/api/v1/status")
                    }
                });
        }
    );
// Make the initial POST request

    const places_section_item = $('.places');
    $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/places_search/',
       contentType: 'application/json',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(new Object()),
        success: function (response) {
            try {
                // Assuming the response is an array of dictionaries
                $.each(response, async function (index, place) {
                    let id = place.user_id; // Assuming 'id' is a key in the dictionary
                    let url = 'http://0.0.0.0:5001/api/v1/users/' + id;

                    // Create a new element to store the data

                        // Make a GET request for each dictionary and wait for the response
                    let place_user;
                    $.ajax(
                        {
                            type: 'GET',
                            dataType: 'json',
                            url: url,
                            success: function (results) {
                                place_user = results;
                                places_section_item.append('<article>' +
                                    ' <div class="title_box"> ' +
                                    '<h2>' + place.name + '</h2> <div class="price_by_night">' + place.price_by_night + '</div>' +
                                    ' </div> <div class="information"> <div class="max_guest">' + place.max_guest +
                                    ` Guest${place.max_guest !== 1 ? 's' : ''}`+
                                    '  </div>' +
                                    ' <div class="number_rooms">' + place.number_rooms +
                                    ` Bedroom${place.number_rooms !== 1 ? 's' : ''}`+
                                    '  </div>' +
                                    ' <div class="number_bathrooms">' + place.number_bathrooms +
                                    ` Bathroom${place.number_bathrooms !== 1 ? 's' : ''}`+
                                    '  </div>' +
                                    ' </div> <div class="user"> <b>Owner:</b> ' + place_user.first_name + ' ' + place_user.last_name + ' </div> ' +
                                    '<div class="description"> ' + place.description + ' </div> ' +
                                    '</article>');
                            }
                        });
                        // Handle the response for this dictionary

                });
            } catch (error) {
                // Handle any errors that occurred during the POST request
                console.error(error);
            }
        }
    ,
        error: function(){
            alert("Error");
        }}
    );
});

// Filter by Amenities
function filter_by_amenities(data)
{
    const places_section_item = $('.places');
    $.ajax({
        url: 'http://0.0.0.0:5001/api/v1/places_search/',
        contentType: 'application/json',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(data),
        success: function (response) {
            try {
                // Assuming the response is an array of dictionaries
                $.each(response, async function (index, place) {
                    let id = place.user_id; // Assuming 'id' is a key in the dictionary
                    let url = 'http://0.0.0.0:5001/api/v1/users/' + id;

                    // Create a new element to store the data

                    // Make a GET request for each dictionary and wait for the response
                    let place_user;
                    places_section_item.empty();
                    $.ajax(
                        {
                            type: 'GET',
                            dataType: 'json',
                            url: url,
                            success: function (results) {
                                place_user = results;
                                places_section_item.append('<article>' +
                                    ' <div class="title_box"> ' +
                                    '<h2>' + place.name + '</h2> <div class="price_by_night">' + place.price_by_night + '</div>' +
                                    ' </div> <div class="information"> <div class="max_guest">' + place.max_guest +
                                    ` Guest${place.max_guest !== 1 ? 's' : ''}`+
                                    '  </div>' +
                                    ' <div class="number_rooms">' + place.number_rooms +
                                    ` Bedroom${place.number_rooms !== 1 ? 's' : ''}`+
                                    '  </div>' +
                                    ' <div class="number_bathrooms">' + place.number_bathrooms +
                                    ` Bathroom${place.number_bathrooms !== 1 ? 's' : ''}`+
                                    '  </div>' +
                                    ' </div> <div class="user"> <b>Owner:</b> ' + place_user.first_name + ' ' + place_user.last_name + ' </div> ' +
                                    '<div class="description"> ' + place.description + ' </div> ' +
                                    '</article>');
                            }
                        });
                    // Handle the response for this dictionary

                });
            } catch (error) {
                // Handle any errors that occurred during the POST request
                console.error(error);
            }
        }
        ,
        error: function(){
            alert("Error");
        }}
    );
}

const search_btn = $('SECTION.filter BUTTON');
search_btn.on("click",function(){filter_by_amenities({'amenities':Object.keys(dictionary)})});

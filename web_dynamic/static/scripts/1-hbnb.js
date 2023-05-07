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


});

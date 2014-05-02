$(document).ready(function() {
    $(".add-button").click(function() {
        var id = $(this).attr('goalid');
        $.ajax({
            url: "/increment/",
            dataType: "json",
            data: {
                id: id
            },
            success: function(data, textStatus, jqXHR) {
                //console.log(data.quantity);
                $("#goal_" + id + " .remaining").html(data.quantity);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                //console.log(errorThrown);
            }
        });
    });
    $(".remove-button").click(function() {
        var id = $(this).attr('goalid');
        $.ajax({
            url: "/decrement/",
            dataType: "json",
            data: {
                id: id
            },
            success: function(data, textStatus, jqXHR) {
                //console.log(data.quantity);
                $("#goal_" + id + " .remaining").html(data.quantity);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                //console.log(errorThrown);
            }
        });
    });
});

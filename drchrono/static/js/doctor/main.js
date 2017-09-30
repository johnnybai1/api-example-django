function getCookie(name) {
    // Get cookies by name
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function checkin_table_refresher() {
    // Ran in a loop to update our check in table based on local db
    var csrftoken = getCookie('csrftoken')
    // Do set up just in case
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        url: 'refresh_table/', // logic to get table data
        contentType: 'application/json',
        success: function(response) {
            var rows = '';
            // Note that we dynamically build the table here; could have
            // relied on Django {{ }} notation + context parameters, but
            // that would require refreshing the page
            $.each(response['appointments'], function(index, item) {
                rows += row_builder(item.id, item.first_name, item.last_name,
                                    item.hours, item.minutes, item.seconds,
                                    $("#average_wait_today").get(0).value);
            });
            // Set the html of the table to the rows we created
            $('#check_in_table_body').html(rows);
        }
    });
}

function row_builder(id, first_name, last_name, hours, minutes, seconds, avg_wait) {
    // Helper function to build rows. Will also color the row's text if the
    // patient has been waiting longer than today's average waiting period
    var color = 'black';
    curr_wait = time_string(hours, minutes, seconds);
    if (curr_wait >= avg_wait) {
        color = 'orange'; // change color to orange
    }
    var row = "<tr data-toggle=\'modal\' data-target=\'#see_patient_modal\'" +
        "class=\'see_patient\' id=\'" + id + "\'>";
    row += wrap_td_p_color('id', id, color);
    row += wrap_td_p_color('name', first_name + ' ' + last_name, color);
    row += wrap_td_p_color('curr_wait', curr_wait, color);
    row += '</tr>';
    return row;
}

function wrap_td_p_color(cls, item, color) {
    // Helper function for dynamically building our checked-in table
    var s = '<td><p>'
    s += '<font color=\'' + color + '\''
    s += 'class =\'' + cls + '\'>'
    s += item + '</td></p>'
    return s
}

function time_string(hours, minutes, seconds) {
    // Returns a time string in hh:mm:ss
    // This also lets us apply gt or lt operators on them
    if (parseInt(hours) < 10) hours = '0' + hours;
    if (parseInt(minutes) < 10) minutes = '0' + minutes;
    if (parseInt(seconds) < 10) seconds = '0' + seconds;
    return hours + ':' + minutes + ':' + seconds;
}

function get_wait() {
    // Ran in a loop to update today's average wait time
    var csrftoken = getCookie('csrftoken')
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    $.ajax({
        url: 'refresh_wait/',
        dataType: 'json',
        contentType: 'application/json',
        success: function(data) {
            $('#average_wait_today').get(0).value =
                time_string(data['hours'], data['minutes'], data['seconds']);
        }
    });
}

function get_patient_url(id) {
    // Returns direct url of our patient page. Perhaps not the best way.
    return "/doctor/patient/" + id + "/"
    // {{ % url get_patient(url) % }}
}

// light blue: #8cbbf0
// dark blue: #4b9cf6
function build_stats_chart() {
    $('#modChart').on('shown.bs.modal', function(event) {
        // Do this when the mod chart modal is opened
        datasets = []
        var link = $(event.relatedTarget);
        var source = link.attr('data-source').split(',');
        datasets.push({
                fillColor: "#8cbbf0",
                strokeColor: "#4b9cf6",
                highlightFill: "#4b9cf6",
                highlightStroke: "#4b9cf6",
                data: source
                });
        var options = {
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Minutes'
                    }
                }]
            }
        };
        var table = link.parents('table'); // table element
        var labels = [] // x axis labels
        $('#'+table.attr('id')+'>thead>tr>th').each(function(index,value){
            // Access the appropriate table (via id) headers
            if (index > 0) {labels.push($(value).html());}
        });
        var modal = $(this);
        var canvas = modal.find('.modal-body canvas');
        var ctx = canvas[0].getContext("2d");
        var chart = new Chart(ctx).Bar({
            responsive: true,
            labels: labels,
            datasets: datasets,
            options: options
        });
    })
    // TODO: fix destroying previous chart
    $('#modChart').on('hidden.bs.modal', function(event){
        var modal = $(this);
        var canvas = modal.find('.modal-body canvas');
        canvas.attr('width', '568px');
        canvas.attr('height', '300px');
        console.log(canvas);
        $(this).data('bs.modal',null);
    });
}
/*
$('#modChart').on('shown.bs.modal', function(event){
        var link = $(event.relatedTarget);
        var source = link.attr('data-source').split(',');
        var table = link.parents('table');
        var labels = [];
        $('#'+table.attr('id')+'>thead>tr>th').each(function(index,value){
            if (index > 0) {labels.push($(value).html());}
        });
        var target = link.attr('data-target-source').split(',');
        var modal = $(this);
        var canvas = modal.find('.modal-body canvas');
        var ctx = canvas[0].getContext("2d");
        var options = {
            scales: {
                xAxes: [{
                    stacked: true,
                }],
                yAxes: [{
                    stacked: false,
                }]
            }
        };
        var chart = new Chart(ctx).Bar({
            responsive: true,
            labels: labels,
            datasets: [{
                fillColor: "rgba(151,187,205,0.2)",
                strokeColor: "rgba(151,187,205,1)",
                pointColor: "rgba(151,187,205,1)",
                pointStrokeColor: "#fff",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "rgba(151,187,205,1)",
                data: source
                },{
                fillColor: "rgba(220,220,220,0.2)",
                strokeColor: "#F7464A",
                pointColor: "#FF5A5E",
                pointStrokeColor: "#FF5A5E",
                pointHighlightFill: "#fff",
                pointHighlightStroke: "red",
                data: target
            }],
            options: options,
        });
    }).on('hidden.bs.modal', function(event){
        var modal = $(this);
        var canvas = modal.find('.modal-body canvas');
        canvas.attr('width', '568px');
        canvas.attr('height', '300px');
        $(this).data('bs.modal',null);
    });
*/
function get_drchrono(endpoint, access_token, query) {
    // TODO: Finish/test this in case i want to use it
    var csrftoken = getCookie('csrftoken')
    $.ajax({
        url: 'https://drchrono.com/api/' + endpoint,
        headers: {'Authorization': 'Bearer ' + access_token},
        data: query,
        success: function(response) {
            console.log(response);
        },
        error: function(xhr) {
            console.log(xhr);
        }
    });
}
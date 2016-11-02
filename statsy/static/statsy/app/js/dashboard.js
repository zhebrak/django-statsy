function getStats(url, callback) {
    $.get(url, {}, function(data) {
        callback(data);
    })
}


function drawStats(dashboard, label, data, aggr_period) {
    var series = [];
    var stats;
    var timeData;

    var year, month, day, hour, minute, tmp;

    data.forEach(function(stats_data) {
        stats = [];
        for (timeData in stats_data.data) {
            tmp = stats_data.data[timeData][0].split(':');
            year = tmp[0];
            month = tmp[1];
            day = tmp[2];
            hour = tmp[3];
            minute = tmp[4];

            stats.push(
                [
                    Date.UTC(parseInt(year), parseInt(month) - 1, parseInt(day), parseInt(hour), parseInt(minute)),
                    stats_data.data[timeData][1]
                ]
            )
        }

        series.push(
            {
                'name': stats_data.name,
                'data': stats
            }
        );
    });


    createChart(dashboard, series, label, aggr_period);
};

function addMinutes(date, minutes) {
    return new Date(date.getTime() + minutes * 60000);
}

function createChart(chart, series, label, aggr_period) {
    chart.highcharts({
        chart: {
            type: 'spline'
        },
        title: {
            text: label
        },
        xAxis: {
            type: 'datetime',
            title: {
                text: 'Time'
            }
        },
        yAxis: {
            title: {
                text: 'Average in ' + aggr_period + ' min'
            },
            min: 0
        },
        tooltip: {
            valueDecimals: 2,
            useHTML: true,
            formatter: function() {
                var date = new Date(this.x);
                return  '<table><tr><td>' + Highcharts.dateFormat('%A, %b %e, %H:%M — ', date) + Highcharts.dateFormat('%H:%M', addMinutes(date, 15)) + '</td><tr/>' +
                     '<td style="text-align: center;"><em style="display: inline-block; height:8px; width: 8px; border-radius: 50%; background-color:' + this.series.color +';"></em><span style="color:' + this.series.color + ';">  ' + this.series.name + '</span>: <b>' + this.y.toFixed(2) + '</b> per min</td></table>';
            }
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: false,
                    symbol: 'circle'
                }
            }
        },

        // colorbrewer2.org — qualitative palette
        colors: [
            'rgb(141,211,199)', 'rgb(255,255,179)', 'rgb(190,186,218)',
            'rgb(251,128,114)', 'rgb(128,177,211)', 'rgb(253,180,98)',
            'rgb(179,222,105)', 'rgb(252,205,229)', 'rgb(217,217,217)',
            'rgb(188,128,189)', 'rgb(204,235,197)', 'rgb(255,237,111)'
        ],

        series: series
    });
};


$(function () {
    var chart = $('#dashboardTodayContainer');
    getStats(chart.attr('data-url'), function(data) {
        drawStats(chart, chart.attr('data-title'), data.stats, data.aggregation_period);
    })

    $('.statsy__group_select, .statsy__event_select').each(function() {
        if ($(this).find('option').length) {
            $(this).select2({
                placeholder: $(this).data('placeholder')
            })
        } else {
            $(this).css('display', 'none');
        }
    });

    $('.statsy__date_select').select2();
    $('input[name="daterange"]').daterangepicker({
        "opens": "left",
        locale: {
            format: 'DD/MM/YY',
            "firstDay": 1
        }
    });

    $('.lazy-load').css('display', 'block');

    var lastLoad = moment().unix();
    $('.statsy__group_select, .statsy__event_select').on('change', function() {
        if (moment().unix() - lastLoad <= 1) {
            return false;
        }

        var groups = $('.statsy__group_select').val();
        var events = $('.statsy__event_select').val();

        var interval = $('input[name="daterange"]').val().split(' - ')

        var data = {
            'groups': groups,
            'events': events,
            'start': interval[0],
            'end': interval[1]
        }
        $.get('/stats/get_stats/', data, function(data) {
            if (data.events && groups.length) {
                currentOptions = [];
                $('.statsy__event_select').find('option').each(function(idx, option) {
                    if ($.inArray(option.value, data.events) == -1) {
                        $(this).remove();
                    } else {
                        currentOptions.push(option.value);
                    }
                });


                data.events.forEach(function(event) {
                    if ($.inArray(event, currentOptions) == -1) {
                        option = new Option(event, event)
                        $('.statsy__event_select').append(option);
                    }
                });


                $('.statsy__event_select').css('display', 'block');
                $('.statsy__event_select').select2();
            } else {
                $('.statsy__event_select').css('display', 'none');
            }
            drawStats(chart, 'Stats', data.stats, data.aggregation_period);
        });
    });

    $('input[name="daterange"]').on('change', function() {
        $('.statsy__group_select').trigger('change');
    })

});

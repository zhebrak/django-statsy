var drawStats = function(dashboard, label, url) {
    $.get(url, {}, function(data) {
        var series = [];
        var stats;
        var timeData;

        var today = new Date();
        var year = today.getFullYear();
        var month = today.getMonth();

        var day, hour, minute, tmp;

        for (var name in data) {
            stats = [];
            for (timeData in data[name]) {
                tmp = data[name][timeData][0].split(':');
                day = tmp[0];
                hour = tmp[1];
                minute = tmp[2];

                stats.push(
                    [
                        Date.UTC(year, month, parseInt(day), parseInt(hour), parseInt(minute)),
                        data[name][timeData][1]
                    ]
                )
            }

            series.push(
                {
                    'name': name,
                    'data': stats
                }
            )
        }

        createChart(dashboard, series, label);
    })
};

var createChart = function(chart, series, label) {
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
                text: 'Count (15 min)'
            },
            min: 0
        },
        tooltip: {
            valueDecimals: 2,
            useHTML: true,
            formatter: function() {
                return  '<table><tr><td>' + Highcharts.dateFormat('%A, %b %e, %H:%M ', new Date(this.x)) +'</td><tr/>' +
                     '<td style="text-align: center;"><em style="display: inline-block; height:8px; width: 8px; border-radius: 50%; background-color:' + this.series.color +';"></em><span style="color:' + this.series.color + ';">  ' + this.series.name + '</span>: <b>' + this.y.toFixed(2) + '</b></td></table>';
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
        colors: [
            '#7cb5ec', '#90ed7d', '#f7a35c', '#8085e9',
            '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'
        ],

        series: series
    });
};


$(function () {
    var groupChart = $('#dashboardGroupContainer');
    drawStats(groupChart, groupChart.attr('data-title'), groupChart.attr('data-url'));

    var eventChart = $('#dashboardEventContainer');
    drawStats(eventChart, eventChart.attr('data-title'), eventChart.attr('data-url'));

    $('.btn-group button').on('click', function() {
        var self = $(this);
        if ( ! self.hasClass('active') ) {
            self.parent().find('.btn-default').removeClass('active');
            self.addClass('active');

            var chart = $('#' + self.parent().attr('data-chart'));
            drawStats(chart, chart.attr('data-title'), self.attr('data-url'));
        }

        return false;
    })

});


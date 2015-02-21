var drawStats = function(dashboard, label) {
    $.get(dashboard.attr('data-url'), {}, function(data) {
        var series = [];
        var stats = [];
        var timeData = [];

        var today = new Date();
        var year = today.getFullYear();
        var month = today.getMonth();
        var day = today.getDate();

        var hour, minute, tmp;

        for (var name in data) {
            stats = [];
            for (timeData in data[name]) {
                tmp = data[name][timeData][0].split(':');
                hour = tmp[0];
                minute = tmp[1];

                stats.push(
                    [
                        Date.UTC(year, month, day, hour, minute),
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

var createChart = function(groupDashboard, series, label) {
    groupDashboard.highcharts({
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
                text: 'Count'
            },
            min: 0
        },
        plotOptions: {
            spline: {
                marker: {
                    enabled: true,
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
    drawStats($('#dashboardGroupContainer'), 'Count per Group');
    drawStats($('#dashboardEventContainer'), 'Count per Event');
});


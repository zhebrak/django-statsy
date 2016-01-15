function drawStats(dashboard, label, url) {
    $.get(url, {}, function(data) {
        var series = [];
        var stats;
        var timeData;

        var year, month, day, hour, minute, tmp;

        stats = [];
        for (timeData in data) {
            tmp = data[timeData][0].split(':');
            year = tmp[0];
            month = tmp[1];
            day = tmp[2];
            hour = tmp[3];
            minute = tmp[4];

            stats.push(
                [
                    Date.UTC(parseInt(year), parseInt(month), parseInt(day), parseInt(hour), parseInt(minute)),
                    data[timeData][1]
                ]
            )
        }

        series.push(
            {
                'name': 'all stats',
                'data': stats
            }
        );

        console.log(stats);

        createChart(dashboard, series, label);
    })
};

function addMinutes(date, minutes) {
    return new Date(date.getTime() + minutes * 60000);
}

function createChart(chart, series, label) {
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
    var todayChart = $('#dashboardTodayContainer');
    drawStats(todayChart, todayChart.attr('data-title'), todayChart.attr('data-url'));

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


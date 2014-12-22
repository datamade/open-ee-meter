var ScatterHelper = {};
ScatterHelper.create = function(element_id, title, yaxisLabel, xaxisLabel, dataseries, plotmax) {

  return new Highcharts.Chart({

    chart: {
        renderTo: element_id,
        type: 'scatter',
        zoomType: 'xy'
    },
    title: {
        text: title
    },
    xAxis: {
        title: {
            enabled: true,
            text: xaxisLabel
        },
        startOnTick: true,
        endOnTick: true,
        showLastLabel: true
    },
    yAxis: {
        title: {
            text: yaxisLabel
        }
    },
    legend: {
        layout: 'vertical',
        align: 'left',
        verticalAlign: 'top',
        x: 80,
        y: 45,
        floating: true,
        backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
        borderWidth: 1
    },
    plotOptions: {
        scatter: {
            marker: {
                radius: 4,
                symbol: 'circle',
                states: {
                    hover: {
                        enabled: true,
                        lineColor: 'rgb(100,100,100)'
                    }
                }
            },
            states: {
                hover: {
                    marker: {
                        enabled: false
                    }
                }
            },
            tooltip: {
                headerFormat: '<p><span style="color:{series.color}">{series.name}</span></p><br>',
                pointFormat: '<p>Predicted: {point.x} <br>Actual: {point.y}</p>'
            }
        }
    },
    series: [{
            type: 'spline',
            color: '#1186BB',
            name: '100% Realization',
            data: [[0, 0], [plotmax, plotmax]],
            marker: {
                enabled: false
            },
            enableMouseTracking: false
            }, dataseries[0], dataseries[1], dataseries[2]]

  });

}

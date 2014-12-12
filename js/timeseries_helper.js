var TimeseriesHelper = {};
TimeseriesHelper.create = function(element_id, title, yaxisLabel, xaxisLabel, xCategories, dataseries, errors) {

  type = "column"

  return new Highcharts.Chart({
      chart: {
          renderTo: element_id,
          type: type,
          height: 350
      },
      credits: { 
        enabled: false 
      },
      title: {
            text: title
      },
      xAxis: {
          categories: xCategories,
          title: {
                text: "Project End Date"
            }
      },
      legend: false,
      yAxis: {
          title: {
                text: yaxisLabel
            }
      },
      tooltip: {
            shared: true
        },
      series: [{
        name: yaxisLabel,
        color: "#1186BB",
        type: 'spline',
        data: dataseries,
        tooltip: {
          pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: <b>{point.y:.2f}</b><br/>'
        }
      },
      {
        name: 'Error',
        type: 'errorbar',
        data: errors,
        tooltip: {
                pointFormat: 'Error Range: {point.low:.2f} - {point.high:.2f}<br/>'
            }
      }
      ]
    });
}

var HistHelper = {};
HistHelper.create = function(element_id, title, yaxisLabel, xaxisLabel, xCategories, dataseries, dataType) {

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
          labels: {
                rotation: 270
            },
          title: {
                text: "Realization Rate (actual savings relative to predicted savings)"
            }
      },
      legend: false,
      yAxis: {
          title: {
                text: "Number of Projects"
            }
      },
      series: dataseries,
      plotOptions: {
        column: {
            groupPadding: 0,
            pointPadding: 0,
            borderWidth: 0
        }
      }

    });
}

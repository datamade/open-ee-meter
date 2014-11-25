var BarHelper = {};
BarHelper.create = function(element_id, title, yaxisLabel, xaxisLabel, xCategories, dataseries, dataType) {

  type = dataType
  console.log(xCategories)
  console.log(dataseries)

  return new Highcharts.Chart({
      chart: {
          renderTo: element_id,
          type: type,
          height: xCategories.length * 18 + 200
      },
      credits: { 
        enabled: false 
      },
      title: {
            text: title
      },
      xAxis: {
          categories: xCategories
      },
      yAxis: {
          title: {
                text: yaxisLabel
            }
      },
      tooltip: {
            shared: true
        },
      series: dataseries,
      legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -40,
            y: 100,
            floating: true,
            borderWidth: 1,
            backgroundColor: ((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'),
        }
    });
}

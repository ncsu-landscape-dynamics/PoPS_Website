function spreadRatePlot(last_year) {
  var data = [];
  //console.log('Spread rate inside function: ')
  //console.log(spread_rate);
  //console.log(spread_rate.length);
  var slider_year = parseInt($('#year-slider').find('input').val());
  var year_count = parseInt($(".timeline-year-container.year_active").attr('data-year-counter'));
  if (year_count == 0) {
    year_color = 'grey';
  } else {
    year_color = colors[year_count - 1];
  }
  //console.log(slider_year)

  if (slider_year > last_year) {
    $('#spread_rate_title span').text(slider_year);
    for (var i = 0; i < spread_rate.length; i++) {
      if (spread_rate[i].year == slider_year) {
        //console.log(spread_rate[i]);
        data.push({
          type: "scatterpolar",
          r: [parseFloat(spread_rate[i].spreadrate__east_rate), parseFloat(spread_rate[i].spreadrate__north_rate), parseFloat(spread_rate[i].spreadrate__west_rate), parseFloat(spread_rate[i].spreadrate__south_rate), parseFloat(spread_rate[i].spreadrate__east_rate)],
          theta: ["E", "N", "W", "S", "E"],
          fill: "toself",
          marker: {
            color: year_color,
            size: 2,
          },
          line: {
            width: 2,
          },
        });
      };
    };
  } else {
    $('#spread_rate_title span').text('');
    data.push({
      type: "scatterpolar",
      r: [0, 0, 0, 0],
      theta: ["E", "N", "W", "S", "E"],
      fill: "toself",
      marker: {
        color: 'grey',
        size: 0,
      },
      line: {
        width: 0,
      },


    });
  }
  //console.log(data);
  //console.log('Max spread rate: ' + max_spread_rate);

  var layout = {
    font: {
      size: 15,
      color: "white",
      border: "transparent"
    },
    showlegend: false,
    legend: {
      font: {
        size: 16
      }
    },
    polar: {
      bgcolor: "#2e3236",
      angularaxis: {
        tickwidth: 2,
        linewidth: 3,
        showline: false,

        layer: "below traces"
      },
      radialaxis: {
        range: [0, max_spread_rate],
        showline: false,
        showticklabels: false,
        showgrid: true,
        zeroline: false,
        autotick: true,
        ticks: '',

        visible: true,
        linewidth: 2,
        tickwidth: 2,
        gridcolor: "#4A5158",
        gridwidth: 2
      }
    },
    orientation: 0,
    paper_bgcolor: 'transparent',
    plot_bgcolor: 'black',
    margin: {
      l: 40,
      r: 40,
      b: 50,
      t: 30,
      pad: 0
    },
  };

  Plotly.newPlot('spread_plot', data, layout, {
    displayModeBar: false,
    responsive: true
  });
};

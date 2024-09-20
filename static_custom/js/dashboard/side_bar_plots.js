function area_plot(defaults, steering_outputs, initial_infected_area, initial_number_infected, first_year, last_year) {
  //console.log('Creating sidebar area plot.')
  $("#eradication-status-indicator").hide();
    var initial_infected_area = initial_infected_area; //{{historic_data.last.infected_area}};
    var initial_number_infected = initial_number_infected; //{{historic_data.last.number_infected}};
    var data_area = [];
    var data_number = [];
    var year_list = [];
    var infected_area_list = [];
    var number_infected_list = [];
    var eradication_check = false;
    for (var j = -1; j < defaults.output.length; j++) {
      if (j == -1) {
        year_list.push(defaults.output[0].year);
        infected_area_list.push(initial_infected_area*acre_to_meter_ratio);
        number_infected_list.push(initial_number_infected);
      } else {
        year_list.push(defaults.output[j].year + 1);
        infected_area_list.push(defaults.output[j].infected_area*acre_to_meter_ratio);
        number_infected_list.push(defaults.output[j].number_infected);
      }
    };
    var opacity = 0.7;
    data_area.push({
      x: year_list,
      y: infected_area_list,
      name: 'No management',
      type: 'scatter',
      mode: 'lines',
      opacity: 0.7,
      line: {
        color: 'grey',
        width: 4,
      }
    });  
    data_number.push({
      x: year_list,
      y: number_infected_list,
      name: 'No management',
      type: 'scatter',
      mode: 'lines',
      opacity: 0.7,
      line: {
        color: 'grey',
        width: 4,
      }
    });
  
    for (var i = 0; i < steering_outputs.length; i++) {
      var steering_year = steering_outputs[i].steering_year;
      var year_list = [];
      var infected_area_list = [];
      var number_infected_list = [];
  
      for (var j = -1; j < steering_outputs[i].output.length; j++) {
        if (j == -1) {
          if (i == 0) {
            year_list.push(steering_outputs[i].output[0].year);
            infected_area_list.push(initial_infected_area*acre_to_meter_ratio);
            number_infected_list.push(initial_number_infected);
  
          } else {
            year_list.push(steering_outputs[i].output[0].year);
            infected_area_list.push(steering_outputs[i - 1].output[0].infected_area*acre_to_meter_ratio);
            number_infected_list.push(steering_outputs[i - 1].output[0].number_infected);
          }
        } else {
          year_list.push(steering_outputs[i].output[j].year + 1);
          infected_area_list.push(steering_outputs[i].output[j].infected_area*acre_to_meter_ratio);
          number_infected_list.push(steering_outputs[i].output[j].number_infected);
          if (eradication_check == false) {
            if (steering_outputs[i].output[j].number_infected == 0) {
              console.log('ERADICATION HAPPENED IN ' + steering_outputs[i].output[j].year);
              eradication_check = true;
              $("#eradication-status-indicator").show();
              $('#eradication_container span').text(steering_outputs[i].output[j].year);
            }
          };
        }
      };
  
      data_area.push({
        x: year_list,
        y: infected_area_list,
        name: steering_year.toString(),
        mode: 'lines',
        opacity: opacity,
        line: {
          color: colors[i],
          width: 4,
        }
      });   
      data_number.push({
        x: year_list,
        y: number_infected_list,
        name: steering_year.toString(),
        mode: 'lines',
        opacity: opacity,
        line: {
          color: colors[i],
          width: 4,
        }
      });
    };
      var xaxis_template = {
        range: [first_year-0.5, last_year+1.5],
        showline: true,
        showticklabels: true,
        showgrid: true,
        zeroline: true,
        autotick: true,
        ticks: '',
        visible: true,
        linewidth: 1,
        tickwidth: 1,
        gridcolor: "#4A5158",
        gridwidth: 1,
        tickfont: {
          size: 12,
          color: 'rgb(107, 107, 107)'
        }
      };
      var yaxis_template = {
        showline: true,
        showticklabels: false,
        showgrid: true,
        zeroline: true,
        autotick: true,
        ticks: '',
        visible: true,
        linewidth: 1,
        tickwidth: 1,
        gridcolor: "#4A5158",
        gridwidth: 1,
        titlefont: {
          size: 12,
          color: 'white',
        },
        tickfont: {
          size: 12,
          color: 'rgb(107, 107, 107)'
        }
      };
    var yaxis_area={
        title: 'Occurence area (acres)',
    }
    var yaxis_number={
        title: 'Number of occurences',
    }
    
    var layout_area = {
          xaxis: xaxis_template,
          yaxis: $.extend({}, yaxis_template, yaxis_area),
  
      showlegend: false,
      paper_bgcolor: 'transparent',
      plot_bgcolor: '#2e3236',
      margin: {
        l: 30,
        r: 20,
        b: 25,
        t: 10,
        pad: 0
      },
    };  
    var layout_number= {
          xaxis: xaxis_template,
          yaxis: $.extend({}, yaxis_template, yaxis_number),
  
      showlegend: false,
      paper_bgcolor: 'transparent',
      plot_bgcolor: '#2e3236',
      margin: {
        l: 30,
        r: 20,
        b: 25,
        t: 10,
        pad: 0
      },
    };
  
    Plotly.newPlot("area_infected_side_plot", data_area, layout_area, {
      displayModeBar: false,
      responsive: true
    });
    Plotly.newPlot("number_infected_side_plot", data_number, layout_number, {
      displayModeBar: false,
      responsive: true
    });
  };

function budget_plot(defaults, steering_outputs, first_year, last_year) {
  //console.log('Creating sidebar budget plot.')
    if ($('#input_budget span').text()) {
      var max_budget = parseInt($('#input_budget span').text());
    }
    else {
      max_budget = 0;
    }
    var max_budget_million = max_budget/1000000;
    var data = [];
    var color_list = [];
      var year_list = [];
      var budget_list = [];
      if (steering_outputs.length>0) {
    for (var i = 0; i < steering_outputs.length; i++) {
      year_list.push(steering_outputs[i].steering_year);
      budget_list.push(steering_outputs[i].management_cost);
      color_list.push(colors[i]);
    };
      data.push({
        x: year_list,
        y: budget_list,
    marker:{
      color: colors,
    },
    type: 'bar'
      });
      }
      else {
        data.push({
        x: [0,1],
        y: [0,0],
    marker:{
      color: colors,
    },
    type: 'bar'
      });
      }
  
  
  
  var layout = {
          showlegend:false,
          shapes: [
      {
          type: 'line',
          xref: 'paper',
          x0: 0,
          y0: max_budget,
          x1: 1,
          y1: max_budget,
          line:{
              color: 'grey',
              width: 2,
              dash:'dot'
          }
      }
      ],
          annotations: [
      {
        x: 0.5,
        y: max_budget,
        xref: 'paper',
        yref: 'y',
        font: {
              color: 'grey',
            size: 12
          },
        text: 'Max budget: $'+ max_budget_million.toString() + 'mil',
        showarrow: true,
        arrowhead: 1,
        ax: 0,
        ay: -10
      }
    ],
      xaxis: {
        range: [first_year-0.5, last_year+1.5],
        showline: true,
        showticklabels: true,
        showgrid: true,
        zeroline: true,
        autotick: true,
        ticks: '',
        visible: true,
        linewidth: 1,
        tickwidth: 1,
        gridcolor: "#4A5158",
        gridwidth: 1,
        tickfont: {
          size: 12,
          color: 'rgb(107, 107, 107)'
        }
      },
          yaxis: {
            range: [0, 1.2*max_budget],
        showline: true,
        showticklabels: false,
        showgrid: true,
        zeroline: true,
        autotick: true,
        ticks: '',
        visible: true,
        linewidth: 1,
        tickwidth: 1,
        gridcolor: "#4A5158",
        gridwidth: 1,
        title: 'Area infected',
            tickprefix:'$',
            overlaying: 'y',
            showticklabels: false,
            title: 'Management cost',
            titlefont: {
              size: 12,
              color: 'white',
            },
  
            tickfont: {
              size: 12,
              color: 'rgb(107, 107, 107)'
            }      
            },
  
          paper_bgcolor:'rgba(0,0,0,0)',
      plot_bgcolor: '#2e3236',
          margin: {
        l: 30,
        r: 20,
        b: 25,
        t: 10,
        pad: 0
          },
          bargap: 0.3,
          };
  
  
    Plotly.newPlot("budget_plot", data, layout, {
      displayModeBar: false,
      responsive: true
    });
};

  function spreadRatePlot(last_year) {
    //console.log('Creating sidebar spread rate plot.')
    var data = [];
    var slider_year = parseInt($('#year-slider').find('input').val());
    var year_count = parseInt($(".timeline-year-container.year_active").attr('data-year-counter'));
    if (year_count == 0) {
      year_color = 'grey';
    } else {
      year_color = colors[year_count - 1];
    }  
    if (slider_year > last_year) {
      $('#spread_rate_title span').text(slider_year);
      for (var i = 0; i < spread_rate.length; i++) {
        if (spread_rate[i].year == slider_year) {
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

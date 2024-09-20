function insertRunButton(run_id, name, date, description, infected_number, infected_area, cost) {
  //var run_pk = run_id.toString();
  var run_pk = run_id;
  if (cost > max_cost) {
    max_cost = cost;
  };
  if (infected_number > max_number) {
    max_number = infected_number;
  };
  if (infected_area > max_area) {
    max_area = infected_area;
  };
  if (name.length > 18) {
    var short_name = name.substring(0, 18) + '...';
  } else {
    short_name = name;
  }
  if (!(document.getElementById("run_" + run_pk))) {

    $('<button id="run_button_' + run_pk +
        '" type="button" class="btn run-link pb-2" data-active-users="[]" data-run-collection = "' + run_pk +
        '"> <div><div class="user_count"><a><i class="fas fa-user"></i></a></div><div class="run_button_links">'+
        '<a class="load_run_text" data-toggle="tooltip" title="Load results" data-placement="left">'+
        '<i class="fas fa-play-circle"></i></a>' +
        '<a class="run_info_button" tabindex="0" data-toggle="popover" title="<div><strong>' + name +
        '</strong></div><small><em>' + date +
        '</em></small>" data-content="<div>' + description +
        '</div>" data-placement="top"> <i class="fas fa-plus-circle"></i></a> '+
        '<a class="delete_run_collection" data-toggle="tooltip" title="Delete" data-placement="left"><i class="fas fa-trash-alt"></i></a></div>' +
        '</div><div id="run_' + run_pk +
        '" class="comparison_plot" style="width:150px; height:120px;"></div></button>').prependTo($('#run-preview-container'));

    $(function () {
      $('[data-toggle="popover"]').popover({
        boundary: 'viewport',
        html: true,
        trigger: 'hover focus',
        template: '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-header"></div><div class="popover-body"></div></div>'
      })
    })

    $("#run_button_" + run_pk).on('click', function () {
      console.log("Run collection " + run_id + " link clicked.");
      $('#run-preview-container button').removeClass('active');
      $(this).addClass('active');
      var run_collection_id = $(this).attr('data-run-collection');
      get_run_collection(run_collection_id);
      getThisRunCollectionManagement(run_collection_id);
    });

    $("#run_button_" + run_pk + ' a.load_run_text').on('click', function (event) {
      event.stopPropagation();
      //console.log('Run button icon clicked.')
      $(this).parent().trigger("click");
      //console.log('Triggered parent button click.')
    });
    $("#run_button_" + run_pk + ' a.run_info_button').on('click', function (event) {
      event.stopPropagation();
      //console.log('Run info icon clicked.')
    });
    $('[data-toggle="tooltip"]').tooltip({
      trigger: 'hover'
    })
  };
  $(run_comparison_plot('run_' + run_pk, short_name, infected_number, infected_area, cost));

  };

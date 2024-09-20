function updateDrawColor (year_count) {
  //console.log('Updating draw color to ' + colors[year_count-1]);
  disableDrawTools();
  enableDrawTools();
  map.removeControl(draw);
  if (year_count) {
    var draw_color = colors[year_count-1];
    var host_removal_pattern = host_removal_patterns[year_count-1];
    var pesticide_application_pattern = pesticide_application_patterns[year_count-1];
  }
  else {
    var draw_color = '#000';
    var host_removal_pattern = '';
    var pesticide_application_pattern = '';
  }
  draw = setDrawColor(draw_color,host_removal_pattern,pesticide_application_pattern);
  map.addControl(draw);
  return;
};

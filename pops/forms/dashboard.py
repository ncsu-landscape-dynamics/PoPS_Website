# pops/forms.py
from django import forms
from django.forms import BaseInlineFormSet

from ..models import *


def fields_required_conditionally(self, fields):
    """Used for conditionally marking fields as required."""
    for field in fields:
        value = self.cleaned_data.get(field, '')
        if not value and value != 0:
            msg = forms.ValidationError("This field is required.")
            self.add_error(field, msg)

#function to convert "bytes" to human readable file size
def human_readable_size(num, suffix='B'):
    for unit in ['','K','M','G']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

#Validate the files are smaller than the max file size set in settings.py
def validate_file_size(self, fields):
    for field in fields:
        data_file = self.cleaned_data.get(field)
        if data_file:
            print('Data file is here')
            print(field)
            print(data_file)
            print(type(data_file))
            print(hasattr(data_file, 'instance'))
            if not hasattr(data_file, 'instance'):
                print('Instance check is true')
                if data_file.content_type in settings.CASE_STUDY_UPLOAD_FILE_TYPES:
                    if data_file.size > settings.CASE_STUDY_UPLOAD_FILE_MAX_SIZE:
                        msg = forms.ValidationError("File size must be less than %s. Selected file was: %s" % (human_readable_size(settings.CASE_STUDY_UPLOAD_FILE_MAX_SIZE), human_readable_size(data_file.size)))
                        self.add_error(field, msg)
                else:
                    msg = forms.ValidationError("File type must be TIFF (.tif)")
                    self.add_error(field, msg)

class CaseStudyForm(forms.ModelForm):
    fields_required = fields_required_conditionally

    class Meta:
        model = CaseStudy
        fields = ['name', 'description','number_of_pests',
                'number_of_hosts','time_step_unit','time_step_n',
                'first_calibration_date','last_calibration_date',
                'first_forecast_date','last_forecast_date']

    def __init__(self, *args, **kwargs):
        super(CaseStudyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

    def clean(self):
        print("VALIDATING CASE STUDY FORM")
        self.fields_required(['name','number_of_pests','number_of_hosts'])
        first_year = self.cleaned_data.get("start_year")
        last_year = self.cleaned_data.get("end_year")
        final_sim_year = self.cleaned_data.get("future_years")
        if first_year and last_year and final_sim_year:
            if first_year >= last_year:
                msg = forms.ValidationError("Final calibration year must be greater than first calibration year.")
                self.add_error("end_year", msg)
            if last_year >= final_sim_year:
                msg = forms.ValidationError("Final model year must be greater than final calibration year.")
                self.add_error("future_years", msg)
        return self.cleaned_data


class SessionForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    class Meta:
        model = Session
        fields = ['case_study','name','description','reproductive_rate','distance_scale','final_date','weather'] 
    
    def clean(self):
        self.fields_required(['case_study','name','description','reproductive_rate','distance_scale','final_date','weather'])
        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})
 
class RunCollectionForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    class Meta:
        model = RunCollection
        fields = ['session','name','description',
        'tangible_landscape','budget','random_seed']
    
    def clean(self):
        self.fields_required(['session','name','description',
        'tangible_landscape','budget','random_seed'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(RunCollectionForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

class RunForm(forms.ModelForm):
    fields_required = fields_required_conditionally
    class Meta:
        model = Run
        fields = ['run_collection',
        'management_polygons','management_cost',
        'management_area','steering_year']
    
    def clean(self):
        self.fields_required(['run_collection',
        'management_polygons','management_cost',
        'management_area','steering_year'])

        return self.cleaned_data

    def __init__(self, *args, **kwargs):
        super(RunForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            help_text = self.fields[field].help_text
            input_type=self.fields[field].widget.__class__.__name__
            if input_type != 'CheckboxInput':
                self.fields[field].help_text = None
            if help_text != '':
                self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


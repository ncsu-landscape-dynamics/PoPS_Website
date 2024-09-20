# pops/forms.py
from django import forms
from django.forms import BaseInlineFormSet



from ..models import *

from crispy_forms.bootstrap import Field, InlineRadios, TabHolder, Tab, PrependedText, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset, Row, HTML

# def fields_required_conditionally(self, fields):
#     """Used for conditionally marking fields as required."""
#     for field in fields:
#         value = self.cleaned_data.get(field, '')
#         if not value and value != 0:
#             msg = forms.ValidationError("This field is required.")
#             self.add_error(field, msg)

# #function to convert "bytes" to human readable file size
# def human_readable_size(num, suffix='B'):
#     for unit in ['','K','M','G']:
#         if abs(num) < 1024.0:
#             return "%3.1f%s%s" % (num, unit, suffix)
#         num /= 1024.0
#     return "%.1f%s%s" % (num, 'Yi', suffix)

# #Validate the files are smaller than the max file size set in settings.py
# def validate_file_size(self, fields):
#     for field in fields:
#         data_file = self.cleaned_data.get(field)
#         if data_file:
#             print('Data file is here')
#             print(field)
#             print(data_file)
#             print(type(data_file))
#             print(hasattr(data_file, 'instance'))
#             if not hasattr(data_file, 'instance'):
#                 print('Instance check is true')
#                 if data_file.content_type in settings.CASE_STUDY_UPLOAD_FILE_TYPES:
#                     if data_file.size > settings.CASE_STUDY_UPLOAD_FILE_MAX_SIZE:
#                         msg = forms.ValidationError("File size must be less than %s. Selected file was: %s" % (human_readable_size(settings.CASE_STUDY_UPLOAD_FILE_MAX_SIZE), human_readable_size(data_file.size)))
#                         self.add_error(field, msg)
#                 else:
#                     msg = forms.ValidationError("File type must be TIFF (.tif)")
#                     self.add_error(field, msg)

# class CaseStudyForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = CaseStudy
#         fields = ['name', 'description','number_of_pests','number_of_hosts','start_year','end_year','future_years',
#                 'time_step']

#     def __init__(self, *args, **kwargs):
#         super(CaseStudyForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

#     def clean(self):
#         print("VALIDATING CASE STUDY FORM")
#         self.fields_required(['name','number_of_pests','number_of_hosts','start_year','end_year','time_step','future_years'])
#         first_year = self.cleaned_data.get("start_year")
#         last_year = self.cleaned_data.get("end_year")
#         final_sim_year = self.cleaned_data.get("future_years")
#         if first_year and last_year and final_sim_year:
#             if first_year >= last_year:
#                 msg = forms.ValidationError("Final calibration year must be greater than first calibration year.")
#                 self.add_error("end_year", msg)
#             if last_year >= final_sim_year:
#                 msg = forms.ValidationError("Final model year must be greater than final calibration year.")
#                 self.add_error("future_years", msg)
#         return self.cleaned_data

# class AllPlantsDataForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size

#     class Meta:
#         model = AllPlantsData
#         fields = ['user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self):
#         self.fields_required(['user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(AllPlantsDataForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class HostForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = Host
#         fields = ['name','score','mortality_on']

#     def clean(self):
#         print('VALIDATING HOST FORM')
#         self.fields_required(['name','score',])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(HostForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class HostDataForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = HostData
#         fields = ['user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self):
#         self.fields_required(['user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(HostDataForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class MortalityForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = Mortality
#         fields = ['method','user_file','rate','time_lag']
#         widgets = {'method': forms.RadioSelect(attrs={'display':'inline-block'}),'user_file': forms.FileInput}
    
#     def clean(self):
#         self.fields_required(['method'])
#         method = self.cleaned_data.get('method')
#         if method:
#             if method == "USER":
#                 print('method true')
#                 self.fields_required(['rate','time_lag'])
#             else:
#                 self.fields_required(['user_file'])
#                 self.validate_size(['user_file'])

#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(MortalityForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class PestForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = Pest
#         fields = ['pest_information','name','model_type','vector_born','use_treatment']
    
#     def clean(self):
#         print('VALIDATING PEST FORM')
#         self.fields_required(['pest_information','model_type'])
#         pest_information = self.cleaned_data.get('pest_information')
#         if pest_information:
#             if pest_information.common_name == "Other":
#                 self.fields_required(['name'])
#             else:
#                 self.cleaned_data['name'] = ''

#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(PestForm, self).__init__(*args, **kwargs)
#         self.fields['pest_information'].queryset = PestInformation.objects.filter(staff_approved=True)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class InitialInfestationForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = InitialInfestation
#         fields = ['user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self): 
#         self.fields_required(['user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(InitialInfestationForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class CalibrationInfestationForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = CalibrationInfestation
#         fields = ['user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self): 
#         self.fields_required(['user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(CalibrationInfestationForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class ValidationInfestationForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = ValidationInfestation
#         fields = ['user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self): 
#         self.fields_required(['user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(ValidationInfestationForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class PriorTreatmentForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = PriorTreatment
#         fields = ['user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self):
#         self.fields_required(['user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(PriorTreatmentForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# class VectorForm(forms.ModelForm):
#     fields_required = fields_required_conditionally
#     validate_size = validate_file_size
#     class Meta:
#         model = Vector
#         fields = ['common_name','scientific_name','user_file']
#         widgets = {'user_file': forms.FileInput}

#     def clean(self):
#         self.fields_required(['common_name','scientific_name','user_file'])
#         self.validate_size(['user_file'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(VectorForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# class NaturalDistanceForm(forms.ModelForm):

#     class Meta:
#         model = NaturalDistance
#         exclude = ['pest']

# class AnthropogenicDistanceForm(forms.ModelForm):

#     class Meta:
#         model = AnthropogenicDistance
#         exclude = ['pest']

# class CrypticToInfectedForm(forms.ModelForm):

#     class Meta:
#         model = CrypticToInfected
#         exclude = ['pest']

# class InfectedToDiseasedForm(forms.ModelForm):

#     class Meta:
#         model = InfectedToDiseased
#         exclude = ['pest']

# class WeatherForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = Weather
#         fields = ['wind_on', 'seasonality_on','lethal_temp_on','temp_on','precipitation_on']

#     def __init__(self, *args, **kwargs):
#         super(WeatherForm, self).__init__(*args, **kwargs)


# class WindForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = Wind
#         fields = ['wind_direction','kappa']

#     def clean(self):
#         self.fields_required(['wind_direction','kappa'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(WindForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# class SeasonalityForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = Seasonality
#         fields = ['first_month','last_month']

#     def clean(self):
#         self.fields_required(['first_month','last_month'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(SeasonalityForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class LethalTemperatureForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = LethalTemperature
#         fields = ['lethal_type','month','value']
#         widgets = {'lethal_type': forms.RadioSelect(attrs={'display':'inline-block'})}
#     def clean(self):
#         self.fields_required(['lethal_type','month','value'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(LethalTemperatureForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

# class TemperatureForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = Temperature
#         fields = ['method']
#         widgets = {'method': forms.RadioSelect(attrs={'display':'inline-block'})}

#     def clean(self):
#         self.fields_required(['method'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(TemperatureForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# class PrecipitationForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = Precipitation
#         fields = ['method']
#         widgets = {'method': forms.RadioSelect(attrs={'display':'inline-block'})}

#     def clean(self):
#         self.fields_required(['method'])
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(PrecipitationForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# class TemperatureReclassForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = TemperatureReclass
#         fields = ['min_value','max_value','reclass']
    
#     def clean(self):
#         self.fields_required(['min_value','max_value','reclass'])
#         min_val = self.cleaned_data.get("min_value")
#         max_val = self.cleaned_data.get("max_value")
#         if min_val and max_val:
#             if min_val >= max_val:
#                 msg = forms.ValidationError("Min temp must be less than max temp in each row.")
#                 self.add_error("min_value", msg)
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(TemperatureReclassForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# #TemperatureReclassFormSet = forms.modelformset_factory(TemperatureReclass, form=TemperatureReclassForm, min_num=2)

# class PrecipitationReclassForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = PrecipitationReclass
#         fields = ['min_value','max_value','reclass']
    
#     def clean(self):
#         self.fields_required(['min_value','max_value','reclass'])
#         min_val = self.cleaned_data.get("min_value")
#         max_val = self.cleaned_data.get("max_value")
#         if min_val and max_val:
#             if min_val >= max_val:
#                 msg = forms.ValidationError("Min precip must be less than max precip in each row.")
#                 self.add_error("min_value", msg)
#         return self.cleaned_data

#     def __init__(self, *args, **kwargs):
#         super(PrecipitationReclassForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


# #PrecipitationReclassFormSet = forms.modelformset_factory(PrecipitationReclass, form=PrecipitationReclassForm, min_num=2)

# class TemperaturePolynomialForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = TemperaturePolynomial
#         fields = ['degree','a0','a1','a2','a3','x1','x2','x3']
#         widgets = {'degree': forms.RadioSelect(attrs={'display':'inline-block'})}

#     def __init__(self, *args, **kwargs):
#         super(TemperaturePolynomialForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})


#     def clean(self):
#         degree = self.cleaned_data.get('degree')
#         self.fields_required(['degree'])
#         if degree == 1:
#             self.fields_required(['a0','a1','x1'])
#         if degree == 2:
#             self.fields_required(['a0','a1','a2','x1','x2'])
#         if degree == 3:
#             self.fields_required(['a0','a1','a2','a3','x1','x2','x3'])
#         return self.cleaned_data

# class PrecipitationPolynomialForm(forms.ModelForm):
#     fields_required = fields_required_conditionally

#     class Meta:
#         model = PrecipitationPolynomial
#         fields = ['degree','a0','a1','a2','a3','x1','x2','x3']
#         widgets = {'degree': forms.RadioSelect(attrs={'display':'inline-block'})}

#     def __init__(self, *args, **kwargs):
#         super(PrecipitationPolynomialForm, self).__init__(*args, **kwargs)
#         for field in self.fields:
#             help_text = self.fields[field].help_text
#             input_type=self.fields[field].widget.__class__.__name__
#             if input_type != 'CheckboxInput':
#                 self.fields[field].help_text = None
#             if help_text != '':
#                 self.fields[field].widget.attrs.update({'data-toggle':'tooltip', 'data-placement':'top', 'title':help_text, 'data-container':'body'})

#     def clean(self):
#         degree = self.cleaned_data.get('degree')
#         self.fields_required(['degree'])
#         if degree == 1:
#             self.fields_required(['a0','a1','x1'])
#         if degree == 2:
#             self.fields_required(['a0','a1','a2','x1','x2'])
#         if degree == 3:
#             self.fields_required(['a0','a1','a2','a3','x1','x2','x3'])
#         return self.cleaned_data

# def continuity_check(self):
#     i=0
#     ranges=[]
#     deleted = self.deleted_forms
#     print(deleted)
#     for form in self.forms:
#         if form.cleaned_data and form not in deleted:
#             min_val = form.cleaned_data["min_value"]
#             max_val = form.cleaned_data['max_value']
#             group=(i,min_val,max_val)
#             if min_val != None and max_val != None:
#                 ranges.append(group)
#         i += 1
#     continuity = True
#     ranges.sort(key=lambda tup: tup[1])  
#     for i in range(len(ranges)-1):
#         if ranges[i][2] != ranges[i+1][1]:
#             target_max_error=ranges[i][0]
#             target_min_error=ranges[i+1][0]
#             self.forms[target_max_error].add_error("max_value", "No matching min value.")
#             self.forms[target_min_error].add_error("min_value", "No matching max value.")
#             continuity = False
#     if continuity == False:
#         raise forms.ValidationError('Continuity error! Every max value must have a corresponding (and unique) min value for' 
#             ' continuity. Please double check your min and max values.', code='continuity_error')
                
# class BaseReclassFormSet(forms.BaseModelFormSet):
#     continuity_check = continuity_check

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
    
#     def clean(self):
#         super().clean()
#         """
#         Check reclass formsets for continuity
#         """
#         if any(self.errors):
#             return
#         self.continuity_check()


# class BaseInlineReclassFormSet(forms.BaseInlineFormSet):
#     continuity_check = continuity_check

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
    
#     def clean(self):
#         super().clean()
#         """
#         Check reclass formsets for continuity
#         """
#         if any(self.errors):
#             return
#         self.continuity_check()

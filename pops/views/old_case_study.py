from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.decorators import login_required
from rest_framework import serializers
from django.forms import ModelForm, modelform_factory
from django.db.models import Q

from ..models import *
from ..forms import *

def testcase(post_data, files_data):
    case_study_form = CaseStudyForm(post_data, files_data, prefix="cs")
    if case_study_form.is_valid():
        new_case_study = case_study_form.save(commit=False)
        print(new_case_study.name)
#@login_required
def create_case_study(request):
    '''
    Overview of case study creation form:

    If request is GET, create an empty instance of all forms, add to context dict, pass to
    the template.

    If request is POST, create instance of forms with request.POST (and request.FILES, if needed) 
    data. Check validity of required forms and save (with commit=False). Check for conditionally
    required forms, then check the validity of conditionally required forms and save (with commit=
    False). IF all required forms (including conditionally required forms) pass validation, 
    save forms AND set foreign keys, then redirect the user to a page detailing the case study. 
    IF any required form fails validation, pass the request.POST data (which now includes error 
    fields) back to the form template so that the user can correct any mistakes.
    '''
    custom_error = []
    #Initialize all of the forms
    case_study_form = CaseStudyForm(prefix="cs")
    host_form = HostForm(prefix="host")
    mortality_form = MortalityForm(prefix="mortality")
    pest_form = PestForm(prefix="pest")
    vector_form = VectorForm(prefix="vector")
    weather_form = WeatherForm(prefix="weather")
    wind_form = WindForm(prefix="wind")
    seasonality_form = SeasonalityForm(prefix="seasonality")
    lethal_temp_form = LethalTemperatureForm(prefix="lethal_temp")
    temperature_form = TemperatureForm(prefix="temp")
    precipitation_form = PrecipitationForm(prefix="precip")
    temperature_reclass_form = TemperatureReclassForm(prefix="temp_reclass")
    temperature_polynomial_form = TemperaturePolynomialForm(prefix="temp_polynomial")
    precipitation_polynomial_form = PrecipitationPolynomialForm(prefix="precip_polynomial")
    precipitation_reclass_formset = PrecipitationReclassFormSet(queryset=PrecipitationReclass.objects.none(), prefix="precip_reclass")
    temperature_reclass_formset = TemperatureReclassFormSet(queryset=TemperatureReclass.objects.none(), prefix="temp_reclass")
    #If the user has submitted the form
    if request.method == "POST":
        testcase(request.POST,request.FILES)
        '''
        Create empty arrays to track models that need to be saved after all models pass validation.
        They are assigned to an array based on the Foreign Key that needs to be addded (e.g. mortality
        has a foreign key to host, so it would be added to host_success_models).
        '''
        host_success_models = []
        pest_success_models = []
        weather_success_models = []
        temperature_success_models = []
        precipitation_success_models = []
        '''
        Create instances of the forms populated with the request data 
        (i.e. the data entered by the user).
        
        Note: Doing this checks for errors and adds the errors to the form. This way
        if there are any errors in the forms, ALL errors get passed back to the user
        if any of the forms fail in the series of IF statements below.

        Note: Any form that contains a file field needs to be passed request.FILES
        in addition to request.POST.
        '''
        case_study_form = CaseStudyForm(request.POST, request.FILES, prefix="cs")
        host_form = HostForm(request.POST, request.FILES, prefix="host")
        pest_form = PestForm(request.POST, prefix="pest")
        weather_form = WeatherForm(request.POST, prefix="weather")
        mortality_form = MortalityForm(request.POST, request.FILES, prefix="mortality")
        vector_form = VectorForm(request.POST, request.FILES, prefix="vector")
        wind_form = WindForm(request.POST, prefix="wind")
        seasonality_form = SeasonalityForm(request.POST, prefix="seasonality")
        lethal_temp_form = LethalTemperatureForm(request.POST, prefix="lethal_temp")
        temperature_form = TemperatureForm(request.POST, prefix="temp")
        precipitation_form = PrecipitationForm(request.POST, prefix="precip")
        temperature_polynomial_form = TemperaturePolynomialForm(request.POST, prefix="temp_polynomial")
        precipitation_polynomial_form = PrecipitationPolynomialForm(request.POST, prefix="precip_polynomial")
        precipitation_reclass_formset = PrecipitationReclassFormSet(request.POST, prefix="precip_reclass")
        temperature_reclass_formset = TemperatureReclassFormSet(request.POST, prefix="temp_reclass")
        '''
        In the model schema: host, pest, and weather have foreign keys (or M2M) to case study. These
        forms are all required. All other forms are conditionally required based on selections in the
        main forms. Therefore, we want to check if the main 4 are valid, and get their data to see
        what other forms are required. We do this by saving an instance of the form, however, we
        set commit=False because we do NOT want to save it to the database YET. We only want to save
        the forms to the database if ALL forms are valid. After we check the validity of all the other
        forms, we can then save all the forms.

        Based on the data in the forms, we determine what other forms are required and check
        the validity of those forms (i.e. if host.mortality_on == True, then we need to check
        the validity of the Mortality form and save it (with commit=False) if it is
        valid. Otherwise we ignore it).

        Running .is_valid() cleans and validates the data using Django's default cleaning and 
        validation methods based on the field type. It also does any custom cleaning or validation
        in the clean method in forms.py. 

        We track whether any forms failed validation by setting success=False for any failed validation.
        '''
        if case_study_form.is_valid() and host_form.is_valid() and pest_form.is_valid() and weather_form.is_valid():
            new_case_study = case_study_form.save(commit=False)
            new_host = host_form.save(commit=False)
            new_pest = pest_form.save(commit=False)
            new_weather = weather_form.save(commit=False)

            success = True

            if new_host.mortality_on == True:
                mortality_form = MortalityForm(request.POST, request.FILES, prefix="mortality")
                if mortality_form.is_valid():
                    print("Mortality form is valid")
                    new_mortality = mortality_form.save(commit=False)
                    host_success_models.append(new_mortality)
                else:
                    success = False
                    custom_error.append("Error in mortality.")
                    print("Mortality form is INVALID")

            if new_pest.vector_born == True:
                if vector_form.is_valid():
                    print("Vector form is valid")
                    new_vector = vector_form.save(commit=False)
                    pest_success_models.append(new_vector)
                else:
                    success = False
                    print("Vector form is INVALID")

            if new_weather.wind_on == True:
                wind_form = WindForm(request.POST, prefix="wind")
                if wind_form.is_valid():
                    print("Wind form is valid")
                    new_wind = wind_form.save(commit=False)
                    weather_success_models.append(new_wind)
                else:
                    success = False
                    print("Wind form is INVALID")

            if new_weather.seasonality_on == True:
                seasonality_form = SeasonalityForm(request.POST, prefix="seasonality")
                if seasonality_form.is_valid():
                    print("Seasonality form is valid")
                    new_seasonality = seasonality_form.save(commit=False)
                    weather_success_models.append(new_seasonality)
                else:
                    success = False
                    print("Seasonality form is INVALID")

            if new_weather.lethal_temp_on == True:
                lethal_temp_form = LethalTemperatureForm(request.POST, prefix="lethal_temp")
                if lethal_temp_form.is_valid():
                    print("Lethal temp form is valid")
                    new_lethal_temp = lethal_temp_form.save(commit=False)
                    weather_success_models.append(new_lethal_temp)
                else:
                    success = False
                    print("Lethal Temp form is INVALID")

            if new_weather.temp_on == True:
                temperature_form = TemperatureForm(request.POST, prefix="temp")
                if temperature_form.is_valid():
                    print("Temp form is valid")
                    new_temperature = temperature_form.save(commit=False)
                    weather_success_models.append(new_temperature)
                    if new_temperature.method == "RECLASS":
                        if temperature_reclass_formset.is_valid():
                            print("temp Reclass formset is valid")
                            instances = temperature_reclass_formset.save(commit=False)
                            for instance in instances:
                                temperature_success_models.append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Temp reclass formset form is INVALID")
                    if new_temperature.method == "POLYNOMIAL":
                        temperature_polynomial_form = TemperaturePolynomialForm(request.POST, prefix="temp_polynomial")
                        if temperature_polynomial_form.is_valid():
                            print("Temp Polynomial form is valid")
                            new_temperature_polynomial = temperature_polynomial_form.save(commit=False)
                            temperature_success_models.append(new_temperature_polynomial)
                        else:
                            success = False
                            print("Temp Polynomial form is INVALID")
                else:
                    success = False
                    print("Temp form is INVALID")

            if new_weather.precipitation_on == True:
                precipitation_form = PrecipitationForm(request.POST, prefix="precip")
                if precipitation_form.is_valid():
                    print("Precipitation form is valid")
                    new_precipitation = precipitation_form.save(commit=False)
                    weather_success_models.append(new_precipitation)
                    if new_precipitation.method == "RECLASS":
                        if precipitation_reclass_formset.is_valid():
                            print("Precip Reclass formset is valid")
                            print(precipitation_reclass_formset)
                            instances = precipitation_reclass_formset.save(commit=False)
                            for instance in instances:
                                precipitation_success_models.append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Precip reclass formset form is INVALID")
                    if new_precipitation.method == "POLYNOMIAL":
                        precipitation_polynomial_form = PrecipitationPolynomialForm(request.POST, prefix="precip_polynomial")
                        if precipitation_polynomial_form.is_valid():
                            print("precipitation Polynomial form is valid")
                            new_precipitation_polynomial = precipitation_polynomial_form.save(commit=False)
                            precipitation_success_models.append(new_precipitation_polynomial)
                        else:
                            success = False
                            print("Temp Polynomial form is INVALID")
                else:
                    success = False
                    print("Precipitation form is INVALID")
        else:
            success = False

        '''
        If all forms pass validation (i.e. success=True), then we can save all of the forms to the
        database.

        We also need to set the Foreign Key assignments. Host, Pest and Weather receive the
        Case Study FK. All other forms receive a FK based on host, pest, weather, temp or precip.
        These foreign keys are assigned in a loop and each model is saved to the Database.
        '''    
        if success:
            print("Success!")
            print(success)
            new_case_study.created_by = request.user
            new_case_study.save()
            new_host.case_study=new_case_study
            new_host.save()
            new_pest.case_study=new_case_study
            new_pest.save()
            new_weather.case_study = new_case_study
            new_weather.save()
            for model in host_success_models:
                model.host = new_host
                model.save()
            for model in pest_success_models:
                model.pest = new_pest
                model.save()
            for model in weather_success_models:
                model.weather = new_weather
                model.save()
            for model in temperature_success_models:
                model.temperature = new_temperature
                model.save()
            for model in precipitation_success_models:
                model.precipitation = new_precipitation
                model.save()
            #If successful, send the user to a page showing all of the case study details.
            return redirect('case_study_review', pk=new_case_study.pk)
        else:
            '''
            If any of the forms failed, create an error message and send the user
            back to the forms page with the errors.
            '''
            print("Something went wrong.")
            custom_error.append("Please correct the errors below:")
    else:
        print("Not a POST")
    #Context is a dictionary of data to pass to the template
    context = {
        'case_study_form': case_study_form,
        'host_form': host_form,
        'mortality_form': mortality_form,
        'pest_form': pest_form,
        'vector_form': vector_form,
        'weather_form': weather_form,
        'wind_form': wind_form,
        'seasonality_form': seasonality_form,
        'lethal_temp_form': lethal_temp_form,
        'temperature_form': temperature_form,
        'precipitation_form': precipitation_form,
        'temperature_reclass_form': temperature_reclass_form,
        'temperature_polynomial_form': temperature_polynomial_form,
        'precipitation_polynomial_form': precipitation_polynomial_form,
        'precipitation_reclass_formset': precipitation_reclass_formset,
        'temperature_reclass_formset': temperature_reclass_formset,
        'error_message': custom_error,
        }
    return render(request, 'pops/create_case_study.html', context)

class CaseStudyListView(ListView):

    model = CaseStudy
    paginate_by = 10  # if pagination is desired
    template_name = 'pops/case_study_list.html'

    def get_queryset(self):
        return CaseStudy.objects.filter(Q(staff_approved = True ) | Q(created_by = self.request.user))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def case_study_submitted(request):
    return render(request, 'pops/case_study_submitted.html',)

import plotly.offline as opy
import plotly.graph_objs as go
import numpy as np

class SomeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = "__all__"

class CaseStudyDetailView(DetailView):

    model = CaseStudy
    template_name = 'pops/case_study_details.html'

def case_study_details(request, pk):
    case_study = get_object_or_404(CaseStudy, pk=pk)
    class HostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Host
            fields = "__all__"
    class CaseStudySerializer(serializers.ModelSerializer):
        hosts=HostSerializer(many=True, read_only=True)
        class Meta:
            model = CaseStudy
            fields = "__all__"
            print(fields)

    casestudy = CaseStudySerializer(case_study).data
    return render(request, 'pops/case_study_details.html', {'case_study': case_study, 'casestudy': casestudy })#,'graph':graph})

def case_study_review(request, pk):
    case_study = CaseStudy.objects.select_related('weather').get(pk=pk) #get_object_or_404(CaseStudy, pk=pk)
    hosts = Host.objects.filter(case_study__pk=pk)
    pests = Pest.objects.filter(case_study__pk=pk).select_related('pest_information')
    context={}
    context['case_study'] = case_study
    context['hosts'] = hosts
    context['pests'] = pests
    temp_data=[]
    precip_data=[]
    if case_study.weather.temp_on:
        if case_study.weather.temperature.method == "RECLASS":
            for row in case_study.weather.temperature.temperaturereclass_set.all():
                temp_data.append(go.Scatter(x=[row.min_value, row.max_value], y=[row.reclass, row.reclass],
                    marker = dict(
                        size = 4,
                        color = 'black',
                        line = dict(
                            width = 1,
                            color = 'cyan'
                        )
                    ),
                    line = dict(
                            width = 2,
                            color = 'cyan'
                    )
                ))
                temp_data.append(go.Scatter(x=[row.min_value], y=[row.reclass],        
                    marker = dict(
                        size = 4,
                        color = 'cyan',
                        line = dict(
                            width = 1,
                            color = 'cyan'
                        )
                    ),
                ))
        if case_study.weather.temperature.method == "POLYNOMIAL":
            a0=case_study.weather.temperature.temperaturepolynomial.a0
            a1=case_study.weather.temperature.temperaturepolynomial.a1
            a2=case_study.weather.temperature.temperaturepolynomial.a2
            a3=case_study.weather.temperature.temperaturepolynomial.a3
            x1=case_study.weather.temperature.temperaturepolynomial.x1
            x2=case_study.weather.temperature.temperaturepolynomial.x2
            x3=case_study.weather.temperature.temperaturepolynomial.x3

            N = 100
            random_x = np.linspace(0, 100, 100)
            random_y0 = float(a0) + float(a1)*(random_x+float(x1))+float(a2)*(random_x+float(x2))**2

            # Create traces
            temp_data.append(go.Scatter(
                x = random_x,
                y = random_y0,
                mode = 'lines',
                line = dict(
                    width = 2,
                    color = 'cyan'
                )
            ))
        temp_graph=opy.plot({
            "data": temp_data,
            "layout": go.Layout(showlegend= False, 
                xaxis=dict(range=[-50, 50],showgrid=False, tickfont=dict(color='white'),title='Temperature (deg C)',titlefont=dict(color='white')), 
                yaxis=dict(range=[-0.1, 1.1], showgrid=False, tickfont=dict(color='white'),title='Reclass',titlefont=dict(color='white')), 
                width=300, height=200, 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=go.layout.Margin(
                    l=50,
                    r=10,
                    b=40,
                    t=20,
                    pad=4
                    ),
                ),
            }, auto_open=False, output_type='div', config={"displayModeBar": False}
        )
        context['temp_graph'] = temp_graph
            
    if case_study.weather.precipitation_on:
        if case_study.weather.precipitation.method == "RECLASS":
            for row in case_study.weather.precipitation.precipitationreclass_set.all():
                precip_data.append(go.Scatter(x=[row.min_value, row.max_value], y=[row.reclass, row.reclass],
                    marker = dict(
                        size = 10,
                        color = 'black',
                        line = dict(
                            width = 2,
                            color = 'cyan'
                        )
                    ),
                    line = dict(
                            width = 2,
                            color = 'cyan'
                    )
                ))
                precip_data.append(go.Scatter(x=[row.min_value], y=[row.reclass],        
                    marker = dict(
                        size = 10,
                        color = 'cyan',
                        line = dict(
                            width = 2,
                            color = 'cyan'
                        )
                    ),
                ))
        if case_study.weather.precipitation.method == "POLYNOMIAL":
            a0=case_study.weather.precipitation.precipitationpolynomial.a0
            a1=case_study.weather.precipitation.precipitationpolynomial.a1
            a2=case_study.weather.precipitation.precipitationpolynomial.a2
            a3=case_study.weather.precipitation.precipitationpolynomial.a3
            x1=case_study.weather.precipitation.precipitationpolynomial.x1
            x2=case_study.weather.precipitation.precipitationpolynomial.x2
            x3=case_study.weather.precipitation.precipitationpolynomial.x3

            N = 100
            random_x = np.linspace(0, 100, 100)
            random_y0 = float(a0) + float(a1)*(random_x+float(x1))+float(a2)*(random_x+float(x2))**2

            # Create traces
            precip_data.append(go.Scatter(
                x = random_x,
                y = random_y0,
                mode = 'lines',
                line = dict(
                    width = 2,
                    color = 'cyan'
                )
            ))
        precip_graph=opy.plot({
            "data": precip_data,
            "layout": go.Layout(showlegend= False, 
                xaxis=dict(range=[0, 100],showgrid=False, tickfont=dict(color='white'),title='Precipitation (mm)',titlefont=dict(color='white')), 
                yaxis=dict(range=[0, 1], showgrid=False, tickfont=dict(color='white'),title='Reclass',titlefont=dict(color='white')), 
                width=300, height=200, 
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=go.layout.Margin(
                    l=50,
                    r=10,
                    b=40,
                    t=20,
                    pad=4
                    ),
                ),
            }, auto_open=False, output_type='div', config={"displayModeBar": False}
        )
        context['precip_graph'] = precip_graph
    return render(request, 'pops/case_study_review.html', context)

def plotly_test(request):
    return render(request, 'pops/plotly_test.html',)

import plotly.offline as opy
import plotly.graph_objs as go

class Graph(TemplateView):
    template_name = 'pops/plotly_test.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)


        div=opy.plot({
            "data": [go.Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
            "layout": go.Layout(title="hello world")
        }, auto_open=False, output_type='div')


        context['graph'] = div

        return context

def case_study_edit(request,pk):
    '''
    Overview of case study creation form:

    If request is GET, create an empty instance of all forms, add to context dict, pass to
    the template.

    If request is POST, create instance of forms with request.POST (and request.FILES, if needed) 
    data. Check validity of required forms and save (with commit=False). Check for conditionally
    required forms, then check the validity of conditionally required forms and save (with commit=
    False). IF all required forms (including conditionally required forms) pass validation, 
    save forms AND set foreign keys, then redirect the user to a page detailing the case study. 
    IF any required form fails validation, pass the request.POST data (which now includes error 
    fields) back to the form template so that the user can correct any mistakes.
    '''
    custom_error = []
    
    #Initialize all of the forms
    case_study_form = CaseStudyForm(prefix="cs")
    host_form = HostForm(prefix="host")
    mortality_form = MortalityForm(prefix="mortality")
    pest_form = PestForm(prefix="pest")
    vector_form = VectorForm(prefix="vector")
    weather_form = WeatherForm(prefix="weather")
    wind_form = WindForm(prefix="wind")
    seasonality_form = SeasonalityForm(prefix="seasonality")
    lethal_temp_form = LethalTemperatureForm(prefix="lethal_temp")
    temperature_form = TemperatureForm(prefix="temp")
    precipitation_form = PrecipitationForm(prefix="precip")
    temperature_reclass_form = TemperatureReclassForm(prefix="temp_reclass")
    temperature_polynomial_form = TemperaturePolynomialForm(prefix="temp_polynomial")
    precipitation_polynomial_form = PrecipitationPolynomialForm(prefix="precip_polynomial")
    precipitation_reclass_formset = PrecipitationReclassFormSet(queryset=PrecipitationReclass.objects.none(), prefix="precip_reclass")
    temperature_reclass_formset = TemperatureReclassFormSet(queryset=TemperatureReclass.objects.none(), prefix="temp_reclass")
    #If the user has submitted the form
    if request.method == "POST":
        '''
        Create empty arrays to track models that need to be saved after all models pass validation.
        They are assigned to an array based on the Foreign Key that needs to be addded (e.g. mortality
        has a foreign key to host, so it would be added to host_success_models).
        '''
        host_success_models = []
        pest_success_models = []
        weather_success_models = []
        temperature_success_models = []
        precipitation_success_models = []
        '''
        Create instances of the forms populated with the request data 
        (i.e. the data entered by the user).
        
        Note: Doing this checks for errors and adds the errors to the form. This way
        if there are any errors in the forms, ALL errors get passed back to the user
        if any of the forms fail in the series of IF statements below.

        Note: Any form that contains a file field needs to be passed request.FILES
        in addition to request.POST.
        '''
        case_study_form = CaseStudyForm(request.POST, request.FILES, prefix="cs")
        host_form = HostForm(request.POST, request.FILES, prefix="host")
        pest_form = PestForm(request.POST, prefix="pest")
        weather_form = WeatherForm(request.POST, prefix="weather")
        mortality_form = MortalityForm(request.POST, request.FILES, prefix="mortality")
        vector_form = VectorForm(request.POST, prefix="vector")
        wind_form = WindForm(request.POST, prefix="wind")
        seasonality_form = SeasonalityForm(request.POST, prefix="seasonality")
        lethal_temp_form = LethalTemperatureForm(request.POST, prefix="lethal_temp")
        temperature_form = TemperatureForm(request.POST, prefix="temp")
        precipitation_form = PrecipitationForm(request.POST, prefix="precip")
        temperature_polynomial_form = TemperaturePolynomialForm(request.POST, prefix="temp_polynomial")
        precipitation_polynomial_form = PrecipitationPolynomialForm(request.POST, prefix="precip_polynomial")
        precipitation_reclass_formset = PrecipitationReclassFormSet(request.POST, prefix="precip_reclass")
        temperature_reclass_formset = TemperatureReclassFormSet(request.POST, prefix="temp_reclass")
        '''
        In the model schema: host, pest, and weather have foreign keys (or M2M) to case study. These
        forms are all required. All other forms are conditionally required based on selections in the
        main forms. Therefore, we want to check if the main 4 are valid, and get their data to see
        what other forms are required. We do this by saving an instance of the form, however, we
        set commit=False because we do NOT want to save it to the database YET. We only want to save
        the forms to the database if ALL forms are valid. After we check the validity of all the other
        forms, we can then save all the forms.

        Based on the data in the forms, we determine what other forms are required and check
        the validity of those forms (i.e. if host.mortality_on == True, then we need to check
        the validity of the Mortality form and save it (with commit=False) if it is
        valid. Otherwise we ignore it).

        Running .is_valid() cleans and validates the data using Django's default cleaning and 
        validation methods based on the field type. It also does any custom cleaning or validation
        in the clean method in forms.py. 

        We track whether any forms failed validation by setting success=False for any failed validation.
        '''
        if case_study_form.is_valid() and host_form.is_valid() and pest_form.is_valid() and weather_form.is_valid():
            new_case_study = case_study_form.save(commit=False)
            new_host = host_form.save(commit=False)
            new_pest = pest_form.save(commit=False)
            new_weather = weather_form.save(commit=False)

            success = True

            if new_host.mortality_on == True:
                mortality_form = MortalityForm(request.POST, request.FILES, prefix="mortality")
                if mortality_form.is_valid():
                    print("Mortality form is valid")
                    new_mortality = mortality_form.save(commit=False)
                    host_success_models.append(new_mortality)
                else:
                    success = False
                    custom_error.append("Error in mortality.")
                    print("Mortality form is INVALID")

            if new_pest.vector_born == True:
                vector_form = VectorForm(request.POST, prefix="vector")
                if vector_form.is_valid():
                    print("Vector form is valid")
                    new_vector = vector_form.save(commit=False)
                    pest_success_models.append(new_vector)
                else:
                    success = False
                    print("Vector form is INVALID")

            if new_weather.wind_on == True:
                wind_form = WindForm(request.POST, prefix="wind")
                if wind_form.is_valid():
                    print("Wind form is valid")
                    new_wind = wind_form.save(commit=False)
                    weather_success_models.append(new_wind)
                else:
                    success = False
                    print("Wind form is INVALID")

            if new_weather.seasonality_on == True:
                seasonality_form = SeasonalityForm(request.POST, prefix="seasonality")
                if seasonality_form.is_valid():
                    print("Seasonality form is valid")
                    new_seasonality = seasonality_form.save(commit=False)
                    weather_success_models.append(new_seasonality)
                else:
                    success = False
                    print("Seasonality form is INVALID")

            if new_weather.lethal_temp_on == True:
                lethal_temp_form = LethalTemperatureForm(request.POST, prefix="lethal_temp")
                if lethal_temp_form.is_valid():
                    print("Lethal temp form is valid")
                    new_lethal_temp = lethal_temp_form.save(commit=False)
                    weather_success_models.append(new_lethal_temp)
                else:
                    success = False
                    print("Lethal Temp form is INVALID")

            if new_weather.temp_on == True:
                temperature_form = TemperatureForm(request.POST, prefix="temp")
                if temperature_form.is_valid():
                    print("Temp form is valid")
                    new_temperature = temperature_form.save(commit=False)
                    weather_success_models.append(new_temperature)
                    if new_temperature.method == "RECLASS":
                        if temperature_reclass_formset.is_valid():
                            print("temp Reclass formset is valid")
                            instances = temperature_reclass_formset.save(commit=False)
                            for instance in instances:
                                temperature_success_models.append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Temp reclass formset form is INVALID")
                    if new_temperature.method == "POLYNOMIAL":
                        temperature_polynomial_form = TemperaturePolynomialForm(request.POST, prefix="temp_polynomial")
                        if temperature_polynomial_form.is_valid():
                            print("Temp Polynomial form is valid")
                            new_temperature_polynomial = temperature_polynomial_form.save(commit=False)
                            temperature_success_models.append(new_temperature_polynomial)
                        else:
                            success = False
                            print("Temp Polynomial form is INVALID")
                else:
                    success = False
                    print("Temp form is INVALID")

            if new_weather.precipitation_on == True:
                precipitation_form = PrecipitationForm(request.POST, prefix="precip")
                if precipitation_form.is_valid():
                    print("Precipitation form is valid")
                    new_precipitation = precipitation_form.save(commit=False)
                    weather_success_models.append(new_precipitation)
                    if new_precipitation.method == "RECLASS":
                        if precipitation_reclass_formset.is_valid():
                            print("Precip Reclass formset is valid")
                            print(precipitation_reclass_formset)
                            instances = precipitation_reclass_formset.save(commit=False)
                            for instance in instances:
                                precipitation_success_models.append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Precip reclass formset form is INVALID")
                    if new_precipitation.method == "POLYNOMIAL":
                        precipitation_polynomial_form = PrecipitationPolynomialForm(request.POST, prefix="precip_polynomial")
                        if precipitation_polynomial_form.is_valid():
                            print("precipitation Polynomial form is valid")
                            new_precipitation_polynomial = precipitation_polynomial_form.save(commit=False)
                            precipitation_success_models.append(new_precipitation_polynomial)
                        else:
                            success = False
                            print("Temp Polynomial form is INVALID")
                else:
                    success = False
                    print("Precipitation form is INVALID")
        else:
            success = False

        '''
        If all forms pass validation (i.e. success=True), then we can save all of the forms to the
        database.

        We also need to set the Foreign Key assignments. Host, Pest and Weather receive the
        Case Study FK. All other forms receive a FK based on host, pest, weather, temp or precip.
        These foreign keys are assigned in a loop and each model is saved to the Database.
        '''    
        if success:
            print("Success!")
            print(success)
            new_case_study.save()
            new_host.save(case_study=new_case_study)
            new_pest.save(case_study=new_case_study)
            new_weather.case_study = new_case_study
            new_weather.save()
            for model in host_success_models:
                model.host = new_host
                model.save()
            for model in pest_success_models:
                model.pest = new_pest
                model.save()
            for model in weather_success_models:
                model.weather = new_weather
                model.save()
            for model in temperature_success_models:
                model.temperature = new_temperature
                model.save()
            for model in precipitation_success_models:
                model.precipitation = new_precipitation
                model.save()
            #If successful, send the user to a page showing all of the case study details.
            return redirect('case_study_review', pk=new_case_study.pk)
        else:
            '''
            If any of the forms failed, create an error message and send the user
            back to the forms page with the errors.
            '''
            print("Something went wrong.")
            custom_error.append("Please correct the errors below:")
    else:
        print("Not a POST")
    #Context is a dictionary of data to pass to the template
    context = {
        'case_study_form': case_study_form,
        'host_form': host_form,
        'mortality_form': mortality_form,
        'pest_form': pest_form,
        'vector_form': vector_form,
        'weather_form': weather_form,
        'wind_form': wind_form,
        'seasonality_form': seasonality_form,
        'lethal_temp_form': lethal_temp_form,
        'temperature_form': temperature_form,
        'precipitation_form': precipitation_form,
        'temperature_reclass_form': temperature_reclass_form,
        'temperature_polynomial_form': temperature_polynomial_form,
        'precipitation_polynomial_form': precipitation_polynomial_form,
        'precipitation_reclass_formset': precipitation_reclass_formset,
        'temperature_reclass_formset': temperature_reclass_formset,
        'error_message': custom_error,
        }
    return render(request, 'pops/create_case_study.html', context)


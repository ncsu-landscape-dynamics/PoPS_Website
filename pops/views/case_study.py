from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from django.views.generic import ListView, DetailView, TemplateView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import ModelForm, modelform_factory
from django.http import HttpResponse, HttpResponseForbidden
from django.db.models import Q

import numpy as np

from ..models import *
from ..forms import *

from django.contrib.auth.mixins import LoginRequiredMixin


class CaseStudyReview(LoginRequiredMixin, TemplateView):
    login_url = "login"
    model = CaseStudy
    template_name = "pops/case_study_review.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(CaseStudyReview, self).get_context_data(**kwargs)
        case_study = CaseStudy.objects.select_related(
            "weather__wind",
            "weather__seasonality",
            "weather__lethaltemperature",
            "weather__temperature",
            "weather__temperature__temperaturepolynomial",
            "weather__precipitation",
            "weather__precipitation__precipitationpolynomial",
        ).get(pk=self.kwargs.get("pk"))
        hosts = Host.objects.select_related("mortality").filter(
            case_study__pk=self.kwargs.get("pk")
        )
        pests = (
            Pest.objects.select_related("vector")
            .filter(case_study__pk=self.kwargs.get("pk"))
            .select_related("pest_information")
        )

        # Create any data and add it to the context
        context["case_study"] = case_study
        context["hosts"] = hosts
        context["pests"] = pests
        return context


class NewCaseStudyView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "pops/create_case_study2.html"

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            permission = self.check_permissions(request, pk=pk)
            if not permission:
                return HttpResponseForbidden()
        my_forms, database_content = self.initialize_forms(request, pk=pk)
        required_models, success, optional_models = self.validate_forms(my_forms)
        if success:
            required_models = self.save_forms(
                request, required_models, success, optional_models
            )
            return redirect(
                "case_study_review", pk=required_models["new_case_study"].pk
            )
        else:
            my_forms["error_message"] = "Please correct the errors below:"
        context = {**my_forms, **database_content}
        return self.render_to_response(context)

    def check_permissions(self, request, pk):
        cs = get_object_or_404(CaseStudy, pk=pk)
        if cs.created_by == request.user:
            return True
        return

    def initialize_forms(self, request, pk=None):
        my_forms = {}
        original_datafiles = {}
        post_data = request.POST or None
        file_data = request.FILES or None
        cs = None
        all_plants_data = None
        host = None
        host_data = None
        mortality = None
        pest = None
        initial_infestation = None
        calibration_infestation = None
        validation_infestation = None
        vector = None
        prior_treatment = None
        weather = None
        wind = None
        seasonality = None
        lethal_temp = None
        temperature = None
        precipitation = None
        temperature_polynomial = None
        precipitation_polynomial = None
        temperature_reclass = None
        precipitation_reclass = None
        if pk:
            # Create any data and add it to the context
            cs = CaseStudy.objects.select_related(
                "weather__wind",
                "weather__seasonality",
                "weather__lethaltemperature",
                "weather__temperature",
                "weather__temperature__temperaturepolynomial",
                "weather__precipitation",
                "weather__precipitation__precipitationpolynomial",
            ).get(pk=pk)
            all_plants_data = cs.allplantsdata
            original_datafiles["all_plants_data"] = all_plants_data.user_file
            host = get_object_or_404(Host, case_study=cs)
            host_data = host.hostdata
            original_datafiles["host_data"] = host_data.user_file
            mortality = Mortality.objects.get_or_none(host=host)
            if mortality:
                original_datafiles["mortality_data"] = mortality.user_file
            pest = get_object_or_404(Pest, case_study=cs)
            initial_infestation = pest.initialinfestation
            original_datafiles["infestation_data"] = initial_infestation.user_file
            calibration_infestation = pest.calibrationinfestation
            original_datafiles["calibration_data"] = calibration_infestation.user_file
            validation_infestation = pest.validationinfestation
            original_datafiles["validation_data"] = validation_infestation.user_file
            vector = Vector.objects.get_or_none(pest=pest)
            prior_treatment = PriorTreatment.objects.get_or_none(pest=pest)
            if prior_treatment:
                original_datafiles["treatment_data"] = prior_treatment.user_file
            if vector:
                original_datafiles["vector_data"] = vector.user_file
            weather = cs.weather

            try:
                wind = cs.weather.wind
            except ObjectDoesNotExist:
                wind = None
            try:
                seasonality = cs.weather.seasonality
            except ObjectDoesNotExist:
                seasonality = None
            try:
                lethal_temp = cs.weather.lethaltemperature
            except ObjectDoesNotExist:
                lethal_temp = None
            try:
                temperature = cs.weather.temperature
            except ObjectDoesNotExist:
                temperature = None
            try:
                precipitation = cs.weather.precipitation
            except ObjectDoesNotExist:
                precipitation = None
            try:
                temperature_polynomial = cs.weather.temperature.temperaturepolynomial
            except ObjectDoesNotExist:
                temperature_polynomial = None
            try:
                precipitation_polynomial = (
                    cs.weather.precipitation.precipitationpolynomial
                )
            except ObjectDoesNotExist:
                precipitation_polynomial = None
            temperature_reclass = TemperatureReclass.objects.filter(
                temperature=temperature
            )
            precipitation_reclass = PrecipitationReclass.objects.filter(
                precipitation=precipitation
            )
            # TemperatureReclassFormSet = forms.modelformset_factory(TemperatureReclass, form=TemperatureReclassForm, min_num=2, validate_min=True, extra=1)
            # my_forms['temperature_reclass_formset'] = TemperatureReclassFormSet(post_data, queryset=temperature_reclass, prefix='temp_reclass')
            # PrecipitationReclassFormSet = forms.modelformset_factory(PrecipitationReclass, form=PrecipitationReclassForm, min_num=2, validate_min=True, extra=1)
            # my_forms['precipitation_reclass_formset'] = PrecipitationReclassFormSet(post_data, queryset=precipitation_reclass, prefix='precip_reclass')
            TemperatureReclassFormSet = forms.inlineformset_factory(
                Temperature,
                TemperatureReclass,
                form=TemperatureReclassForm,
                formset=BaseInlineReclassFormSet,
                min_num=2,
                validate_min=True,
                extra=1,
            )
            my_forms["temperature_reclass_formset"] = TemperatureReclassFormSet(
                post_data, instance=temperature, prefix="temp_reclass"
            )
            PrecipitationReclassFormSet = forms.inlineformset_factory(
                Precipitation,
                PrecipitationReclass,
                form=PrecipitationReclassForm,
                formset=BaseInlineReclassFormSet,
                min_num=2,
                validate_min=True,
                extra=1,
            )
            my_forms["precipitation_reclass_formset"] = PrecipitationReclassFormSet(
                post_data, instance=precipitation, prefix="precip_reclass"
            )
        else:
            TemperatureReclassFormSet = forms.modelformset_factory(
                TemperatureReclass,
                form=TemperatureReclassForm,
                formset=BaseReclassFormSet,
                can_delete=True,
                min_num=2,
                extra=1,
            )
            my_forms["temperature_reclass_formset"] = TemperatureReclassFormSet(
                post_data,
                queryset=TemperatureReclass.objects.none(),
                prefix="temp_reclass",
            )
            PrecipitationReclassFormSet = forms.modelformset_factory(
                PrecipitationReclass,
                form=PrecipitationReclassForm,
                formset=BaseReclassFormSet,
                can_delete=True,
                min_num=2,
                extra=1,
            )
            my_forms["precipitation_reclass_formset"] = PrecipitationReclassFormSet(
                post_data,
                queryset=PrecipitationReclass.objects.none(),
                prefix="precip_reclass",
            )

        my_forms["case_study_form"] = CaseStudyForm(
            post_data, file_data, instance=cs, prefix="cs"
        )
        my_forms["all_plants_data_form"] = AllPlantsDataForm(
            post_data, file_data, instance=all_plants_data, prefix="all_plants_data"
        )
        my_forms["host_form"] = HostForm(
            post_data, file_data, instance=host, prefix="host"
        )
        my_forms["host_data_form"] = HostDataForm(
            post_data, file_data, instance=host_data, prefix="host_data"
        )
        my_forms["mortality_form"] = MortalityForm(
            post_data, file_data, instance=mortality, prefix="mortality"
        )
        my_forms["pest_form"] = PestForm(
            post_data, file_data, instance=pest, prefix="pest"
        )
        my_forms["initial_infestation_form"] = InitialInfestationForm(
            post_data,
            file_data,
            instance=initial_infestation,
            prefix="initial_infestation",
        )
        my_forms["calibration_infestation_form"] = CalibrationInfestationForm(
            post_data,
            file_data,
            instance=calibration_infestation,
            prefix="calibration_infestation",
        )
        my_forms["validation_infestation_form"] = ValidationInfestationForm(
            post_data,
            file_data,
            instance=validation_infestation,
            prefix="validation_infestation",
        )
        my_forms["prior_treatment_form"] = PriorTreatmentForm(
            post_data, file_data, instance=prior_treatment, prefix="prior_treatment"
        )
        my_forms["vector_form"] = VectorForm(
            post_data, file_data, instance=vector, prefix="vector"
        )
        my_forms["weather_form"] = WeatherForm(
            post_data, instance=weather, prefix="weather"
        )
        my_forms["wind_form"] = WindForm(post_data, instance=wind, prefix="wind")
        my_forms["seasonality_form"] = SeasonalityForm(
            post_data, instance=seasonality, prefix="seasonality"
        )
        my_forms["lethal_temp_form"] = LethalTemperatureForm(
            post_data, instance=lethal_temp, prefix="lethal_temp"
        )
        my_forms["temperature_form"] = TemperatureForm(
            post_data, instance=temperature, prefix="temperature"
        )
        my_forms["precipitation_form"] = PrecipitationForm(
            post_data, instance=precipitation, prefix="precipitation"
        )
        my_forms["temperature_polynomial_form"] = TemperaturePolynomialForm(
            post_data, instance=temperature_polynomial, prefix="temperature_polynomial"
        )
        my_forms["precipitation_polynomial_form"] = PrecipitationPolynomialForm(
            post_data,
            instance=precipitation_polynomial,
            prefix="precipitation_polynomial",
        )
        return my_forms, original_datafiles

    def validate_forms(self, my_forms):
        required_models = {}
        optional_models = {}
        optional_models["case_study"] = []
        optional_models["host"] = []
        optional_models["pest"] = []
        optional_models["weather"] = []
        optional_models["temperature"] = []
        optional_models["precipitation"] = []
        success = True

        if (
            my_forms["case_study_form"].is_valid()
            and my_forms["host_form"].is_valid()
            and my_forms["pest_form"].is_valid()
            and my_forms["weather_form"].is_valid()
        ):
            print(
                "Case study, host and pest form are valid (but dependent forms may not be.)"
            )
            required_models["new_case_study"] = my_forms["case_study_form"].save(
                commit=False
            )
            required_models["new_host"] = my_forms["host_form"].save(commit=False)
            required_models["new_pest"] = my_forms["pest_form"].save(commit=False)
            if my_forms["host_data_form"].is_valid():
                required_models["new_host_data"] = my_forms["host_data_form"].save(
                    commit=False
                )
                optional_models["host"].append(required_models["new_host_data"])
            else:
                success = False
                print("Host data form failed.")
            if my_forms["all_plants_data_form"].is_valid():
                required_models["new_all_plants"] = my_forms[
                    "all_plants_data_form"
                ].save(commit=False)
                optional_models["case_study"].append(required_models["new_all_plants"])
            else:
                success = False
                print("All plant data form failed.")
            if my_forms["initial_infestation_form"].is_valid():
                required_models["new_initial_infestation"] = my_forms[
                    "initial_infestation_form"
                ].save(commit=False)
                optional_models["pest"].append(
                    required_models["new_initial_infestation"]
                )
            else:
                success = False
                print("Initial infestation form failed.")
            if my_forms["calibration_infestation_form"].is_valid():
                required_models["new_calibration_infestation"] = my_forms[
                    "calibration_infestation_form"
                ].save(commit=False)
                optional_models["pest"].append(
                    required_models["new_calibration_infestation"]
                )
            else:
                success = False
                print("New calibration infestation form failed.")
            if my_forms["validation_infestation_form"].is_valid():
                required_models["new_validation_infestation"] = my_forms[
                    "validation_infestation_form"
                ].save(commit=False)
                optional_models["pest"].append(
                    required_models["new_validation_infestation"]
                )
            else:
                success = False
                print("Validation infestation data form failed.")
            required_models["new_weather"] = my_forms["weather_form"].save(commit=False)
            if required_models["new_host"].mortality_on == True:
                if my_forms["mortality_form"].is_valid():
                    required_models["new_mortality"] = my_forms["mortality_form"].save(
                        commit=False
                    )
                    optional_models["host"].append(required_models["new_mortality"])
                else:
                    success = False
                    print("Mortality form failed.")
            if required_models["new_pest"].vector_born == True:
                if my_forms["vector_form"].is_valid():
                    required_models["new_vector"] = my_forms["vector_form"].save(
                        commit=False
                    )
                    optional_models["pest"].append(required_models["new_vector"])
                else:
                    success = False
                    print("Pest form failed.")
            if required_models["new_pest"].use_treatment == True:
                if my_forms["prior_treatment_form"].is_valid():
                    required_models["new_prior_treatment"] = my_forms[
                        "prior_treatment_form"
                    ].save(commit=False)
                    optional_models["pest"].append(
                        required_models["new_prior_treatment"]
                    )
                else:
                    success = False
                    print("Prior treatment form failed.")
            if required_models["new_weather"].wind_on == True:
                if my_forms["wind_form"].is_valid():
                    required_models["new_wind"] = my_forms["wind_form"].save(
                        commit=False
                    )
                    optional_models["weather"].append(required_models["new_wind"])
                else:
                    success = False
                    print("Wind form failed.")
            if required_models["new_weather"].seasonality_on == True:
                if my_forms["seasonality_form"].is_valid():
                    required_models["new_seasonality"] = my_forms[
                        "seasonality_form"
                    ].save(commit=False)
                    optional_models["weather"].append(
                        required_models["new_seasonality"]
                    )
                else:
                    success = False
                    print("Seasonality form failed.")
            if required_models["new_weather"].lethal_temp_on == True:
                if my_forms["lethal_temp_form"].is_valid():
                    required_models["new_lethal_temp"] = my_forms[
                        "lethal_temp_form"
                    ].save(commit=False)
                    optional_models["weather"].append(
                        required_models["new_lethal_temp"]
                    )
                else:
                    success = False
                    print("Lethal temp form failed.")
            if required_models["new_weather"].temp_on == True:
                if my_forms["temperature_form"].is_valid():
                    required_models["new_temperature"] = my_forms[
                        "temperature_form"
                    ].save(commit=False)
                    optional_models["weather"].append(
                        required_models["new_temperature"]
                    )
                    if required_models["new_temperature"].method == "POLYNOMIAL":
                        if my_forms["temperature_polynomial_form"].is_valid():
                            required_models["new_temperature_polynomial"] = my_forms[
                                "temperature_polynomial_form"
                            ].save(commit=False)
                            optional_models["temperature"].append(
                                required_models["new_temperature_polynomial"]
                            )
                        else:
                            success = False
                            print("Temperature polynomial form failed.")
                    if required_models["new_temperature"].method == "RECLASS":
                        if my_forms["temperature_reclass_formset"].is_valid():
                            print("temp Reclass formset is valid")
                            reclass_forms = my_forms[
                                "temperature_reclass_formset"
                            ].save(commit=False)
                            for obj in my_forms[
                                "temperature_reclass_formset"
                            ].deleted_objects:
                                obj.delete()
                            for instance in reclass_forms:
                                optional_models["temperature"].append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Temp reclass formset form is INVALID")
                            # print(my_forms['temperature_reclass_formset'])

                else:
                    success = False
                    print("Temperature form failed.")
            if required_models["new_weather"].precipitation_on == True:
                if my_forms["precipitation_form"].is_valid():
                    required_models["new_precipitation"] = my_forms[
                        "precipitation_form"
                    ].save(commit=False)
                    optional_models["weather"].append(
                        required_models["new_precipitation"]
                    )
                    if required_models["new_precipitation"].method == "POLYNOMIAL":
                        if my_forms["precipitation_polynomial_form"].is_valid():
                            required_models["new_precipitation_polynomial"] = my_forms[
                                "precipitation_polynomial_form"
                            ].save(commit=False)
                            optional_models["precipitation"].append(
                                required_models["new_precipitation_polynomial"]
                            )
                        else:
                            success = False
                            print("Precipitation polynomial form failed.")
                    if required_models["new_precipitation"].method == "RECLASS":
                        if my_forms["precipitation_reclass_formset"].is_valid():
                            print("precip Reclass formset is valid")
                            reclass_forms = my_forms[
                                "precipitation_reclass_formset"
                            ].save(commit=False)
                            for obj in my_forms[
                                "precipitation_reclass_formset"
                            ].deleted_objects:
                                obj.delete()
                            for instance in reclass_forms:
                                optional_models["precipitation"].append(instance)
                                print("instance stuff happened")
                                print(instance.min_value)
                        else:
                            success = False
                            print("Precip reclass formset form is INVALID")
                            print(my_forms["precipitation_reclass_formset"].errors)
                else:
                    success = False
                    print("Precipitation form failed.")
        else:
            print("VALIDATION FAILED")
            if my_forms["case_study_form"].is_valid():
                print("Main case study form is valid.")
            else:
                print("Main case study form is invalid.")
            if my_forms["host_form"].is_valid():
                print("Main host form is valid.")
            else:
                print("Main host form is invalid.")
            if my_forms["pest_form"].is_valid():
                print("Main pest form is valid.")
            else:
                print("Main pest form is invalid.")
                success = False

        return required_models, success, optional_models

    def save_forms(self, request, required_models, success, optional_models):
        required_models["new_case_study"].created_by = request.user
        required_models["new_case_study"].save()
        required_models["new_host"].case_study = required_models["new_case_study"]
        required_models["new_host"].save()
        required_models["new_pest"].case_study = required_models["new_case_study"]
        required_models["new_pest"].save()
        required_models["new_weather"].case_study = required_models["new_case_study"]
        required_models["new_weather"].save()
        for model in optional_models["case_study"]:
            model.case_study = required_models["new_case_study"]
            model.save()
        for model in optional_models["host"]:
            model.host = required_models["new_host"]
            model.save()
        for model in optional_models["pest"]:
            model.pest = required_models["new_pest"]
            model.save()
        for model in optional_models["weather"]:
            model.weather = required_models["new_weather"]
            model.save()
        for model in optional_models["temperature"]:
            model.temperature = required_models["new_temperature"]
            model.save()
        for model in optional_models["precipitation"]:
            model.precipitation = required_models["new_precipitation"]
            model.save()

        return required_models

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk:
            permission = self.check_permissions(request, pk=pk)
            if not permission:
                return HttpResponseForbidden()
        my_forms, database_content = self.initialize_forms(request, pk=pk)
        context = {**my_forms, **database_content}
        return self.render_to_response(context)
        # return self.post(request, *args, **kwargs)


class ExtendCaseStudyView(NewCaseStudyView):
    def save_forms(self, request, required_models, success):
        original_case_study = get_object_or_404(CaseStudy, pk=self.kwargs.get("pk"))
        required_models["new_case_study"].created_by = request.user
        required_models["new_case_study"].use_external_calibration = True
        required_models["new_case_study"].calibration = original_case_study
        required_models["new_case_study"].pk = None
        required_models["new_case_study"].save()
        required_models["new_host"].pk = None
        required_models["new_host"].case_study = required_models["new_case_study"]
        required_models["new_host"].save()
        return required_models

    def check_permissions(self, request, pk):
        cs = get_object_or_404(CaseStudy, pk=pk)
        if cs.created_by == request.user or cs.staff_approved == True:
            return True
        return


class ApprovedCaseStudyListView(ListView):

    model = CaseStudy
    context_object_name = "case_studies"
    # paginate_by = 10  # if pagination is desired
    template_name = "pops/my_account.html"

    def get_queryset(self):
        return CaseStudy.objects.filter(staff_approved=True).order_by("-date_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateCaseStudyStart(LoginRequiredMixin, TemplateView):
    login_url = "login"
    template_name = "pops/create_case_study_start.html"

    def post(self, request, **kwargs):
        case_study_id = request.POST.get("case_study_id")
        return redirect(reverse("case_study_edit", args=(case_study_id,)))


class ApprovedAndUserCaseStudyListView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    # paginate_by = 5  # if pagination is desired
    template_name = "pops/case_study_list.html"

    def get_queryset(self):
        return (
            CaseStudy.objects.prefetch_related("host_set", "pest_set__pest_information")
            .filter(Q(staff_approved=True) | Q(created_by=self.request.user))
            .order_by("-date_created")
        )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(ApprovedAndUserCaseStudyListView, self).get_context_data(
            **kwargs
        )
        case_studies = self.get_queryset()
        context["staff_approved_case_studies"] = case_studies.filter(
            staff_approved=True
        )
        context["user_case_studies"] = case_studies.filter(created_by=self.request.user)
        return context


class PestDetailView(DetailView):
    # login_url = 'login'
    model = PestInformation
    template_name = "pops/pest_details.html"
    context_object_name = "pest_information"

    def get_queryset(self):
        return PestInformation.objects.prefetch_related("pest_set__case_study")


class PestListView(TemplateView):
    # login_url = 'login'
    # paginate_by = 5  # if pagination is desired
    template_name = "pops/pest_list.html"

    def get_queryset(self):
        return PestInformation.objects.prefetch_related(
            "pest_set__case_study"
        ).order_by("-host_type", "common_name")

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(PestListView, self).get_context_data(**kwargs)
        pests = self.get_queryset()
        pests_without_case_studies = pests.distinct()
        # pests_with_case_studies=pests.filter(pest__case_study__staff_approved=True).distinct()
        # pests_without_case_studies=pests.exclude(pest__case_study__staff_approved=True).distinct()
        # context['pests_with_case_studies'] = pests_with_case_studies.filter(staff_approved = True)
        context["pests_without_case_studies"] = pests_without_case_studies.filter(
            staff_approved=True
        )
        return context

    # def get_queryset(self):
    #     return CaseStudy.objects.filter(Q(staff_approved = True ) | Q(created_by = self.request.user))


def case_study_submitted(request):
    return render(
        request,
        "pops/case_study_submitted.html",
    )


class CaseStudyDetailView(LoginRequiredMixin, DetailView):
    login_url = "login"
    model = CaseStudy
    template_name = "pops/case_study_details.html"
    context_object_name = "case_study"

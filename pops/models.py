from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.postgres.fields import ArrayField
import os

from users.models import CustomUser

# Django automatically creates a primary key for each model and we are not overwriting this default behavior in any of our models.
class CaseStudy(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, on_delete = models.SET_NULL)
    name = models.CharField(verbose_name = _("case study name"), max_length = 150, blank=True, help_text="Give your case study a descriptive name.")
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    number_of_pests = models.PositiveSmallIntegerField(verbose_name = _("number of pests"), help_text="How many pests are in your model system?", blank=True, default = 1, validators = [MinValueValidator(1), MaxValueValidator(10)])
    number_of_hosts = models.PositiveSmallIntegerField(verbose_name = _("number of hosts"), help_text="How many hosts are in your model system?", blank=True, default = 1, validators = [MinValueValidator(1), MaxValueValidator(10)])
    # all_plants = models.FilePathField(verbose_name = _("all plants"), path=settings.FILE_PATH_FIELD_DIRECTORY, match=None, recursive=False, max_length=200, null = True)
    start_year = models.PositiveSmallIntegerField(verbose_name = _("start year"), help_text="The first year of the simulation.", blank=True, default = 2012, validators = [MinValueValidator(1900), MaxValueValidator(2200)])
    end_year = models.PositiveSmallIntegerField(verbose_name = _("end year"), help_text="The last year of the simulation.", blank=True, default = 2016, validators = [MinValueValidator(1900), MaxValueValidator(2200)])
    # directory_name =os.path.join(settings.FILE_PATH_FIELD_DIRECTORY, CaseStudy.name)
    #infestation_data = models.FileField(verbose_name = _("infestation data"), upload_to=settings.FILE_PATH_FIELD_DIRECTORY, max_length=100)
    # treatment_data = models.FileField(verbose_name =  _("previous treatments data"), upload_to = settings.FILE_PATH_FIELD_DIRECTORY, max_length=100)
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    TIME_STEP_CHOICES = ((MONTH, 'Month'), (WEEK, 'Week'), (DAY, 'Day'))
    time_step = models.CharField(verbose_name = _("time step"), default = "Month", max_length = 50, choices = TIME_STEP_CHOICES, help_text='Select a time step for your simulation:')

    class Meta:
        verbose_name = _("case study")
        verbose_name_plural = _("case studies")

    def __str__(self):
        return self.name

class Host(models.Model):

    case_study = models.ManyToManyField(CaseStudy, verbose_name = _("case study"))
    name = models.CharField(verbose_name = _("host common name"), help_text="What is the host's common name?", max_length = 150, blank=True)
    score = models.DecimalField(verbose_name = _("score"), help_text="Host score is a value between 0 and 1. 0 has no effect while 1 has maximum effect.", blank=True, max_digits = 5, decimal_places = 2, default = 1, validators = [MinValueValidator(0), MaxValueValidator(1)])
    mortality_on = models.BooleanField(verbose_name = _("mortality"), help_text="Does the host experience mortality as a result of the pest/pathogen?", blank=True)
    # host_data = models.FilePathField(verbose_name = _("host data"), path=settings.FILE_PATH_FIELD_DIRECTORY, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("host")
        verbose_name_plural = _("hosts")

    def __str__(self):
        return self.name

class Mortality(models.Model):

    host = models.OneToOneField(Host, verbose_name = _("host"), on_delete = models.CASCADE, primary_key=True)
    user_input = models.BooleanField(verbose_name = _("user inputs the mortality rate and time lag?"), help_text="Sample help text.", default = False, blank=True)
    rate = models.DecimalField(verbose_name = _("mortality rate"), help_text="Sample help text.", max_digits = 3, decimal_places = 2, blank=True, null=True, default = 0, validators = [MinValueValidator(0), MaxValueValidator(1)])
    rate_standard_deviation = models.DecimalField(verbose_name = _("mortality rate standard deviation"), help_text="Sample help text.", max_digits = 3, decimal_places = 2, blank=True, null=True)
    time_lag = models.PositiveSmallIntegerField(verbose_name = _("mortality time lag"), help_text="Sample help text.", blank=True, null=True, default = 2, validators = [MinValueValidator(1), MaxValueValidator(10)])
    time_lag_standard_deviation = models.DecimalField(verbose_name = _("mortality time lag standard deviation"), help_text="Sample help text.", max_digits = 4, decimal_places = 2, blank=True, null=True)

    class Meta:
        verbose_name = _("mortality")
        verbose_name_plural = _("mortalities")

    def __str__(self):
        return self.rate

class Creation(models.Model):

    host = models.ForeignKey(Host, verbose_name = _("host"), on_delete = models.CASCADE)

    class Meta:
        verbose_name = _("creation of host map")
        verbose_name_plural = _("creation of host maps")

    def __str__(self):
        return self.name

class PestInformation(models.Model):

    common_name = models.CharField(verbose_name = _("pest common name"), max_length = 150)
    scientific_name = models.CharField(verbose_name = _("pest scientific name"), help_text="Sample help text.", max_length = 150)
    about = models.TextField(verbose_name = _("about the pest"), help_text="Sample help text.", )
    risks = models.TextField(verbose_name = _("risks associated with the pest"), help_text="Sample help text.", )
    management_activity = models.TextField(verbose_name = _("management activities to control the pest"), help_text="Sample help text.", )
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    date_updated = models.DateTimeField(verbose_name = _("date updated"), auto_now = True, auto_now_add = False)

    class Meta:
        verbose_name = _("pest information")
        verbose_name_plural = _("pest informations")

    def __str__(self):
        return self.common_name

class Pest(models.Model):

    name = models.CharField(verbose_name = _("pest common name"), help_text="Sample help text.", max_length = 150, blank=True)
    case_study = models.ManyToManyField(CaseStudy, verbose_name = _("case study"))
    pest_information = models.ForeignKey(PestInformation, verbose_name = _("pest information"), help_text="Sample help text.", null=True, on_delete = models.SET_NULL)
    staff_approved = models.BooleanField(verbose_name = _("approved by staff"), help_text="Sample help text.", default = False)
    vector_born = models.BooleanField(verbose_name = _("vector born"), help_text="Sample help text.", default = False)
    MODEL_CHOICES = (
        ("SI", "Susceptible Infected"),
        ("SID", "Susceptible Infected Diseased"),
        ("SEID", "Susceptible Exposed Infected Diseased"),
    )
    model_type = models.CharField(verbose_name = _("model type"), help_text="Sample help text.", max_length = 20,
                    choices = MODEL_CHOICES,
                    default = "SI", blank=True)
    DISPERSAL_CHOICES = (
        ("CAUCHY", "Cauchy"),
        ("DOUBLE SCALE CAUCHY", "Double Scale Cauchy"),
        ("EXPONENTIAL", "Exponential"),
        ("DOUBLE SCALE EXPONENTIAL", "Double Scale Exponential")
    )
    dispersal_type = models.CharField(verbose_name = _("dispersal type"), help_text="Sample help text.", max_length = 70,
                    choices = DISPERSAL_CHOICES,
                    default = "CAUCHY", blank=True)

    class Meta:
        verbose_name = _("pest")
        verbose_name_plural = _("pests")

    def __str__(self):
        return self.name

class Vector(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    common_name = models.CharField(verbose_name = _("vector common name"), help_text="Sample help text.", max_length = 150, blank=True)
    scientific_name = models.CharField(verbose_name = _("vector scientific name"), help_text="Sample help text.", max_length = 150, blank=True)
    vector_to_host_transmission_rate = models.DecimalField(verbose_name = _("vector to host transmission rate"), help_text="Sample help text.", max_digits = 3, decimal_places = 2, blank=True, null = True)
    vector_to_host_transmission_rate_standard_deviation = models.DecimalField(verbose_name = _("vector to host transmission rate standard deviation"), help_text="Sample help text.", max_digits = 3, decimal_places = 2, blank=True, null=True)
    host_to_vector_transmission_rate = models.DecimalField(verbose_name = _("host to vector transmission rate"), help_text="Sample help text.", max_digits = 3, decimal_places = 2, blank=True, null = True)
    host_to_vector_transmission_rate_standard_deviation = models.DecimalField(verbose_name = _("host to vector transmission rate standard deviation"), help_text="Sample help text.", max_digits = 3, decimal_places = 2, blank=True, null=True)

    class Meta:
        verbose_name = _("vector")
        verbose_name_plural = _("vectors")

    def __str__(self):
        return self.common_name

class ShortDistance(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    scale = models.DecimalField(verbose_name = _("short distance scale"), max_digits = 5, decimal_places = 1)
    scale_standard_deviation = models.DecimalField(verbose_name = _("short distance scale standard deviation"), max_digits = 5, decimal_places = 1)
    percent_short_distance = models.DecimalField(verbose_name = _("percentage of dispersal that is short distance"), default = 1, max_digits = 3, decimal_places = 2)

    class Meta:
        verbose_name = _("short distance dispersal")
        verbose_name_plural = _("short distance dispersals")

    def __str__(self):
        return self.scale

class LongDistance(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    scale = models.DecimalField(verbose_name = _("long distance scale"), max_digits = 5, decimal_places = 1)
    scale_standard_deviation = models.DecimalField(verbose_name = _("long distance scale standard deviation"), max_digits = 5, decimal_places = 1)

    class Meta:
        verbose_name = _("long distance dispersal")
        verbose_name_plural = _("long distance dispersals")

    def __str__(self):
        return self.scale

class CrypticToInfected(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    rate = models.DecimalField(verbose_name = _("cryptic to infected rate"), max_digits = 3, decimal_places = 2)
    rate_standard_deviation = models.DecimalField(verbose_name = _("cryptic to infected standard deviation"), max_digits = 3, decimal_places = 2)

    class Meta:
        verbose_name = _("cryptic to infected")
        verbose_name_plural = _("cryptic to infecteds")

    def __str__(self):
        return self.rate

class InfectedToDiseased(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    rate = models.DecimalField(verbose_name = _("infected to diseased rate"), max_digits = 3, decimal_places = 2)
    rate_standard_deviation = models.DecimalField(verbose_name = _("infected to diseased standard deviation"), max_digits = 3, decimal_places = 2)

    class Meta:
        verbose_name = _("infected to diseased")
        verbose_name_plural = _("infected to diseaseds")

    def __str__(self):
        return self.rate

class Weather(models.Model):

    case_study = models.OneToOneField(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE, primary_key=True)
    wind_on = models.BooleanField(verbose_name = _("use wind"), help_text="Sample help text.", default = False)
    seasonality_on = models.BooleanField(verbose_name = _("use seasonality"), help_text="Sample help text.", default = False)
    lethal_temp_on = models.BooleanField(verbose_name = _("use lethal temp"), help_text="Sample help text.", default = False)
    temp_on = models.BooleanField(verbose_name = _("use temp"), help_text="Sample help text.", default = False)
    precipitation_on = models.BooleanField(verbose_name = _("use precipitation"), help_text="Sample help text.", default = False)

    class Meta:
        verbose_name = _("weather")
        verbose_name_plural = _("weathers")

    def __str__(self):
        return self.wind_on

class Wind(models.Model):

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    DIRECTION_CHOICES = (
        ("NONE", "None"),
        ("N", "North"),
        ("NE", "Northeast"),
        ("E", "East"),
        ("SE", "Southeast"),
        ("S", "South"),
        ("SW", "Southwest"),
        ("W", "West"),
        ("NW", "Northwest"),
    )
    wind_direction = models.CharField(verbose_name = _("wind direction"), help_text="Sample help text.", 
                    max_length = 30,
                    choices = DIRECTION_CHOICES,
                    default = "NONE", blank = False)
    KAPPA_CHOICES = (
            (1, "1"),
            (2, "2"),
            (3, "3"),
            (4, "4"),
            (5, "5"),
            (6, "6"),
            (7, "7"),
            (8, "8"),
            (9, "9"),
            (10, "10"),
            (11, "11"),
            (12, "12"),
        )

    kappa = models.PositiveSmallIntegerField(verbose_name = _("wind strenth (kappa)"), help_text="Sample help text.", choices = KAPPA_CHOICES, default = 1, blank = False, validators = [MinValueValidator(1), MaxValueValidator(12)])

    class Meta:
        verbose_name = _("wind")
        verbose_name_plural = _("winds")

    def __str__(self):
        return self.wind_direction

class Seasonality(models.Model):
    MONTH = (
            (1, "January"),
            (2, "February"),
            (3, "March"),
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December"),
        )
    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    first_month = models.PositiveSmallIntegerField(verbose_name = _("first month of season"), help_text="Sample help text.", choices = MONTH, default = 1, blank=False, validators = [MinValueValidator(1), MaxValueValidator(12)])
    last_month = models.PositiveSmallIntegerField(verbose_name = _("last month of season"), help_text="Sample help text.", choices = MONTH, default = 12, blank=False, validators = [MinValueValidator(1), MaxValueValidator(12)])

    class Meta:
        verbose_name = _("seasonality")
        verbose_name_plural = _("seasonalities")

    def __str__(self):
        return self.first_month

class LethalTemperature(models.Model):
    MONTH = (
            (1, "January"),
            (2, "February"),
            (3, "March"),
            (4, "April"),
            (5, "May"),
            (6, "June"),
            (7, "July"),
            (8, "August"),
            (9, "September"),
            (10, "October"),
            (11, "November"),
            (12, "December"),
        )

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    month = models.PositiveSmallIntegerField(verbose_name = _("month in which lethal temperature occurs"), help_text="Sample help text.", choices = MONTH, default = 1, blank=False)
    value = models.DecimalField(verbose_name = _("lethal temperature"), help_text="Sample help text.", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(-50), MaxValueValidator(50)])
    # lethal_temperature_data = models.FilePathField(verbose_name = _("lethal temperature data"), path=None, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("lethal temperature")
        verbose_name_plural = _("lethal temperatures")

    def __str__(self):
        return self.value

class Temperature(models.Model):

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    METHOD_CHOICES = (
        ("RECLASS", "Reclass"),
        ("POLYNOMIAL", "Polynomial"),
    )
    method = models.CharField(verbose_name = _("temperature coefficient creation method"), help_text="Sample help text.", max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "RECLASS", blank = False)
    # temperature_data = models.FilePathField(verbose_name = _("temperature data"), path=None, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("temperature")
        verbose_name_plural = _("temperatures")

    def __str__(self):
        return self.method

class Precipitation(models.Model):

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    METHOD_CHOICES = (
        ("RECLASS", "Reclass"),
        ("POLYNOMIAL", "Polynomial"),
    )
    method = models.CharField(verbose_name = _("precipitation coefficient creation method"), help_text="Sample help text.", max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "RECLASS", blank = False)
    # precipitation_data = models.FilePathField(verbose_name = _("precipitation data"), path=None, match=None, recursive=True, max_length=100)

    class Meta:
        verbose_name = _("precipitation")
        verbose_name_plural = _("precipitations")

    def __str__(self):
        return self.method

class TemperatureReclass(models.Model):

    temperature = models.OneToOneField(Temperature, verbose_name = _("temperature"), on_delete = models.CASCADE, primary_key=True)
    threshold = models.DecimalField(verbose_name = _("temperature threshold"), max_digits = 5, decimal_places = 2, blank = True, validators = [MinValueValidator(-50), MaxValueValidator(50)])
    # matrix = ArrayField(
    #     ArrayField(
    #         models.DecimalField(max_digits = 4, decimal_places = 2),
    #         size=3,
    #     ),
    # )

    class Meta:
        verbose_name = _("temperature reclass")
        verbose_name_plural = _("temperature reclasses")

    def __str__(self):
        return self.threshold

class PrecipitationReclass(models.Model):

    precipitation = models.ForeignKey(Precipitation, verbose_name = _("precipitation"), on_delete = models.CASCADE)
    min_value = models.DecimalField(verbose_name = _("min"), help_text="Sample help text.", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    max_value = models.DecimalField(verbose_name = _("max"), help_text="Sample help text.", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    reclass = models.DecimalField(verbose_name = _("reclass"), help_text="Sample help text.", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(1)])

    class Meta:
        verbose_name = _("precipitation reclass")
        verbose_name_plural = _("precipitation reclasses")

    def __str__(self):
        return self.reclass


class TemperaturePolynomial(models.Model):

    temperature = models.OneToOneField(Temperature, verbose_name = _("temperature"), on_delete = models.CASCADE, primary_key=True)
    DEGREE_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
    )
    degree = models.PositiveSmallIntegerField(verbose_name = _("polynomial degree"), help_text="Sample help text.", 
                    choices = DEGREE_CHOICES, default = 1, blank = False)
    a0 = models.DecimalField(verbose_name = _("a0"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a1 = models.DecimalField(verbose_name = _("a1"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a2 = models.DecimalField(verbose_name = _("a2"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a3 = models.DecimalField(verbose_name = _("a3"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    x1 = models.DecimalField(verbose_name = _("x1"), help_text="Sample help text.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x2 = models.DecimalField(verbose_name = _("x2"), help_text="Sample help text.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x3 = models.DecimalField(verbose_name = _("x3"), help_text="Sample help text.", max_digits = 5, decimal_places = 2, blank = True, null = True)

    class Meta:
        verbose_name = _("temperature polynomial")
        verbose_name_plural = _("temperature polynomials")

    def __str__(self):
        return self.a0

class PrecipitationPolynomial(models.Model):

    precipitation = models.OneToOneField(Precipitation, verbose_name = _("precipitation"), on_delete = models.CASCADE, primary_key=True)
    DEGREE_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
    )
    degree = models.PositiveSmallIntegerField(verbose_name = _("polynomial degree"), help_text="Sample help text.", 
                    choices = DEGREE_CHOICES, default = 1, blank = False)
    a0 = models.DecimalField(verbose_name = _("a0"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a1 = models.DecimalField(verbose_name = _("a1"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a2 = models.DecimalField(verbose_name = _("a2"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a3 = models.DecimalField(verbose_name = _("a3"), help_text="Sample help text.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    x1 = models.DecimalField(verbose_name = _("x1"), help_text="Sample help text.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x2 = models.DecimalField(verbose_name = _("x2"), help_text="Sample help text.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x3 = models.DecimalField(verbose_name = _("x3"), help_text="Sample help text.", max_digits = 5, decimal_places = 2, blank = True, null = True)

    class Meta:
        verbose_name = _("precipitation polynomial")
        verbose_name_plural = _("precipitation polynomials")

    def __str__(self):
        return self.a0

class Treatment(models.Model):

    year = models.PositiveSmallIntegerField(verbose_name = _("treatment year"), validators = [MinValueValidator(1900), MaxValueValidator(2200)])
    #treatment_file = models.FileField(verbose_name = _("treatment raster for that year"), upload_to=settings.FILE_PATH_FIELD_DIRECTORY, max_length = 200)

    class Meta:
        verbose_name = _("treatment")
        verbose_name_plural = _("treatments")

    # def __str__(self):
    #     return self.name


class Session(models.Model):

    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    name = models.CharField(verbose_name = _("session name"), max_length=150)

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")

    def __str__(self):
        return self.name

class Run(models.Model):

    session = models.ForeignKey(Session, verbose_name = _("session id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("run name"), max_length = 150)
    random_seed = models.PositiveIntegerField(verbose_name = _("random seed"), default = None, null = True, validators = [MinValueValidator(1)])

    class Meta:
        verbose_name = _("run")
        verbose_name_plural = _("runs")

    def __str__(self):
        return self.name

class InputChange(models.Model):

    run = models.ForeignKey(Run, verbose_name = _("run id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("parameter name"), max_length = 150)
    value = models.DecimalField(verbose_name = _("parameter value"), max_digits = 5, decimal_places = 2)

    class Meta:
        verbose_name = _("input change")
        verbose_name_plural = _("input changes")

    def __str__(self):
        return self.name

class Output(models.Model):

    run = models.ForeignKey(Run, verbose_name = _("run id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("output variable name"), max_length = 150)
    # data = MatrixField(verbose_name = _("output data"), datatype = 'float')

    class Meta:
        verbose_name = _("output")
        verbose_name_plural = _("outputs")

    def __str__(self):
        return self.name

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.core.exceptions import ObjectDoesNotExist 
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage
import os

from users.models import CustomUser

class MyManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

def all_plants_directory(instance, filename):
    return 'case_studies/{0}/all_plants/{1}'.format(instance.case_study.id, filename)

def host_directory(instance, filename):
    return 'case_studies/{0}/hosts/{1}/host_data/{2}'.format(instance.host.case_study.id, instance.host.id, filename)

def mortality_directory(instance, filename):
    return 'case_studies/{0}/hosts/{1}/mortality/{2}'.format(instance.host.case_study.id, instance.host.id, filename)

def initial_infestation_directory(instance, filename):
    return 'case_studies/{0}/pests/{1}/initial_infestation/{2}'.format(instance.pest.case_study.id, instance.pest.id, filename)

def validation_infestation_directory(instance, filename):
    return 'case_studies/{0}/pests/{1}/validation_infestation/{2}'.format(instance.pest.case_study.id, instance.pest.id, filename)

def calibration_infestation_directory(instance, filename):
    return 'case_studies/{0}/pests/{1}/calibration_infestation/{2}'.format(instance.pest.case_study.id, instance.pest.id, filename)

def vector_directory(instance, filename):
    return 'case_studies/{0}/pests/{1}/vector/{2}'.format(instance.pest.case_study.id, instance.pest.id, filename)

def treatment_directory(instance, filename):
    return 'case_studies/{0}/pests/{1}/prior_treatment/{2}'.format(instance.pest.case_study.id, instance.pest.id, filename)

def temperature_directory(instance, filename):
    return 'case_studies/{0}/temperature_data/{1}'.format(instance.weather.case_study.id, filename)

def precipitation_directory(instance, filename):
    return 'case_studies/{0}/precipitation_data/{1}'.format(instance.weather.case_study.id, filename)

def lethal_temperature_directory(instance, filename):
    return 'case_studies/{0}/lethal_temperature_data/{1}'.format(instance.weather.case_study.id, filename)


# Django automatically creates a primary key for each model and we are not overwriting this default behavior in any of our models.
class CaseStudy(models.Model):

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, on_delete = models.SET_NULL)
    name = models.CharField(verbose_name = _("case study name"), max_length = 150, blank=True, help_text="Give your case study a descriptive name.")
    description = models.TextField(verbose_name = _("case study description"), max_length = 300, blank=True, null=True, help_text="Give your case study a description.")
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    number_of_pests = models.PositiveSmallIntegerField(verbose_name = _("number of pests"), help_text="How many pests are in your model system?", blank=True, default = 1, validators = [MinValueValidator(1), MaxValueValidator(10)])
    number_of_hosts = models.PositiveSmallIntegerField(verbose_name = _("number of hosts"), help_text="How many hosts are in your model system?", blank=True, default = 1, validators = [MinValueValidator(1), MaxValueValidator(10)])
    start_year = models.PositiveSmallIntegerField(verbose_name = _("first calibration year"), help_text="The first year that you have pest occurence data for calibration.", blank=True, default = 2012, validators = [MinValueValidator(1900), MaxValueValidator(2200)])
    end_year = models.PositiveSmallIntegerField(verbose_name = _("final calibration year"), help_text="The last year that you have pest occurence data for calibration.", blank=True, default = 2018, validators = [MinValueValidator(1900), MaxValueValidator(2200)])
    future_years = models.PositiveSmallIntegerField(verbose_name = _("final model year"), help_text="The last year that you want to run the PoPS model (this is in the future).", blank=True, default = 2023, validators = [MinValueValidator(2018), MaxValueValidator(2200)])
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    TIME_STEP_CHOICES = ((MONTH, 'Month'), (WEEK, 'Week'), (DAY, 'Day'))
    time_step = models.CharField(verbose_name = _("time step"), default = "Month", max_length = 50, choices = TIME_STEP_CHOICES, help_text='Select a time step for your simulation:')
    staff_approved = models.BooleanField(verbose_name = _("approved by staff"), help_text="Sample help text.", default = False)
    STATUS_CHOICES = (
        ("NO START", "Not started"),
        ("IN PROGRESS", "In progress"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Successful"),
        ("EXTERNAL", "Non-self"),
    )
    calibration_status = models.CharField(verbose_name = _("calibration status"), help_text="What type of model do you want to use?", max_length = 20,
                    choices = STATUS_CHOICES,
                    default = "NO START", blank=True)
    use_external_calibration = models.BooleanField(verbose_name = _("use another case study's calibration?"), help_text="Sample help text.", default = False)
    calibration = models.ForeignKey("self", verbose_name = _("calibrated case study"), null=True, blank=True, on_delete = models.SET_NULL)
    model_api = models.CharField(verbose_name = _("model api url"), max_length = 250, null = True, blank=True, help_text="Link to the model api for this case study.")

    objects = MyManager()

    class Meta:
        verbose_name = _("case study")
        verbose_name_plural = _("case studies")

    def __str__(self):
        return self.name

    def get_string_fields(self):
        # list of some excluded fields
        excluded_fields = ['']

        # getting all fields that available in `Client` model,
        # but not in `excluded_fields`
        field_names = [field.name for field in CaseStudy._meta.get_fields() 
                       if field.name not in excluded_fields]
        values = []
        for field_name in field_names:
            pass
            # get specific value from instanced object.
            # and outputing as `string` value.
            #values.append('%s' % getattr(self, field_name))

        # joining all string values.
        return field_names

class HistoricData(models.Model):

    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study id"), on_delete = models.CASCADE)
    year = models.PositiveIntegerField(verbose_name = _("year"), default = 2015, null = True, validators = [MinValueValidator(1900)])
    data = models.JSONField(null = True)
    infected_area = models.DecimalField(verbose_name = _("infected_area (m^2)"), help_text="Overall infected area from the run.", blank=True, max_digits = 16, decimal_places = 2, default = 1, validators = [MinValueValidator(0)])
    number_infected = models.IntegerField(verbose_name = _("number_infected"), default = 0, null = True, validators = [MinValueValidator(0)])

    class Meta:
        verbose_name = _("historic data")
        verbose_name_plural = _("historic datas")
    
    def __str__(self):
        return str(self.pk)

class MapBoxParameters(models.Model):

    case_study = models.OneToOneField(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE, primary_key=True)
    longitude = models.DecimalField(verbose_name = _("longitude"), help_text="Longitude of the center of the case study", blank=True, max_digits = 17, decimal_places = 14, default = -75.89533170441632, validators = [MinValueValidator(-180), MaxValueValidator(180)])
    latitude = models.DecimalField(verbose_name = _("latitude"), help_text="Latitude of the center of the case study", blank=True, max_digits = 17, decimal_places = 14, default = 40.2039152196177, validators = [MinValueValidator(-90), MaxValueValidator(90)])
    zoom = models.PositiveSmallIntegerField(verbose_name = _("mapbox zoom level"), help_text="The zoom level of MapBox.", blank=True, default = 7, validators = [MinValueValidator(0), MaxValueValidator(16)])

    objects = MyManager()

    class Meta:
        verbose_name = _("map box parameter")
        verbose_name_plural = _("map box parameters")

    def __str__(self):
        return str(self.pk)

class AllPlantsData(models.Model):

    case_study = models.OneToOneField(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE, primary_key=True)
    user_file = models.FileField(verbose_name = _("all plant data"), help_text="Upload your total plants data as a raster file. This could be all the plants in a cell or all cells could have the value of the maximum number of hosts foound in any cell in your study area.",upload_to=all_plants_directory, max_length=100, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("all_plant")
        verbose_name_plural = _("all_plants")

    def __str__(self):
        return str(self.pk)

class Host(models.Model):

    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study"), on_delete=models.CASCADE)
    name = models.CharField(verbose_name = _("host common name"), help_text="What is the host's common name?", max_length = 150, blank=True)
    score = models.DecimalField(verbose_name = _("score"), help_text="Host score is a value between 0 and 1. 0 has no effect while 1 has maximum effect. This is for generalist pests with differing host preferences and pathogens with differing host competencies.", blank=True, max_digits = 5, decimal_places = 2, default = 1, validators = [MinValueValidator(0), MaxValueValidator(1)])
    mortality_on = models.BooleanField(verbose_name = _("mortality"), help_text="Does the host experience mortality as a result of the pest/pathogen?", blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("host")
        verbose_name_plural = _("hosts")

    def __str__(self):
        return self.name

class HostData(models.Model):

    host = models.OneToOneField(Host, verbose_name = _("host"), on_delete = models.CASCADE, primary_key=True)
    user_file = models.FileField(verbose_name = _("host data"), help_text="Upload your host data as a raster file.", upload_to=host_directory, max_length=100, blank=True)
    host_map = models.JSONField(null = True)

    objects = MyManager()

    class Meta:
        verbose_name = _("host_data")
        verbose_name_plural = _("hosts_data")

    def __str__(self):
        return str(self.pk)
        
class Mortality(models.Model):

    host = models.OneToOneField(Host, verbose_name = _("host"), on_delete = models.CASCADE, primary_key=True)
    METHOD_CHOICES = (
        ("DATA_FILE", "PoPS estimates mortality rate and time lag from user data"),
        ("USER", "User provides mortality rate and time lag"),
    )
    method = models.CharField(verbose_name = _("mortality rate method"), help_text="Choose a method to determine mortality rate and time lag.", max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "DATA_FILE", blank = False)    
    user_file = models.FileField(verbose_name = _("mortality data"), upload_to=mortality_directory, max_length=100, help_text="A single raster file with number of trees that experienced mortality as a result of the pest/pathogen that year (each layer is a year)", null = True, blank=True)
    rate = models.DecimalField(verbose_name = _("mortality rate (fraction)"), help_text="What percentage of hosts experience mortality each year from the pest or pathogen?", max_digits = 3, decimal_places = 2, blank=True, null=True, default = 0, validators = [MinValueValidator(0), MaxValueValidator(1)])
    time_lag = models.PositiveSmallIntegerField(verbose_name = _("mortality time lag (years)"), help_text="How long after initial infection/infestation (in years) before mortality occurs on average?", blank=True, null=True, default = 2, validators = [MinValueValidator(1), MaxValueValidator(10)])

    objects = MyManager()

    class Meta:
        verbose_name = _("mortality")
        verbose_name_plural = _("mortalities")

    def __str__(self):
        return str(self.pk)

class MortalityRate(models.Model):

    mortality = models.ForeignKey(Mortality, verbose_name = _("mortality"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("mortality rate value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("mortality rate probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("mortality rate")
        verbose_name_plural = _("mortality rates")

    def __str__(self):
        return str(self.pk)

class MortalityTimeLag(models.Model):

    mortality = models.ForeignKey(Mortality, verbose_name = _("mortality"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("mortality time lag value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("mortality time lag probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("mortality time lag")
        verbose_name_plural = _("mortality time lags")

    def __str__(self):
        return str(self.pk)

class Creation(models.Model):

    host = models.ForeignKey(Host, verbose_name = _("host"), on_delete = models.CASCADE)

    class Meta:
        verbose_name = _("creation of host map")
        verbose_name_plural = _("creation of host maps")

    def __str__(self):
        return str(self.pk)

class PestInformation(models.Model):

    common_name = models.CharField(verbose_name = _("pest common name"), max_length = 150)
    scientific_name = models.CharField(verbose_name = _("pest scientific name"), help_text="Sample help text.", max_length = 150)
    about = models.TextField(verbose_name = _("about the pest"), help_text="Sample help text.", )
    risks = models.TextField(verbose_name = _("risks associated with the pest"), help_text="Sample help text.", )
    management_activity = models.TextField(verbose_name = _("management activities to control the pest"), help_text="Sample help text.", )
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    date_updated = models.DateTimeField(verbose_name = _("date updated"), auto_now = True, auto_now_add = False)
    staff_approved = models.BooleanField(verbose_name = _("approved by staff"), help_text="Sample help text.", default = False)
    invasive = models.BooleanField(verbose_name = _("invasive"), help_text="Is the organism invasive in the US?", default = True)
    HOST_CHOICES = (
        ("ANIMAL", "Animal"),
        ("PLANT", "Plant"),
    )
    host_type = models.CharField(verbose_name = _("host type"), help_text="Choose what system type this pest/pathogen infects.", max_length = 30,
                    choices = HOST_CHOICES,
                    default = "PLANT", blank = False)     
    ORGANISM_CHOICES = (
        ("PEST", "Pest (e.g. insect)"),
        ("PATHOGEN", "Pathogen (e.g. disease)"),
    )
    organism_type = models.CharField(verbose_name = _("organism type"), help_text="Choose whether this is a pest or pathogen.", max_length = 30,
                    choices = ORGANISM_CHOICES,
                    default = "PEST", blank = False) 
    arrival_year = models.PositiveSmallIntegerField(verbose_name = _("first year found in US"), help_text="The first year that it was identified in the US.", blank=True, null=True, default = None, validators = [MinValueValidator(1700), MaxValueValidator(2100)])
    arrival_location = models.CharField(verbose_name = _("first location found in US (State)"), max_length = 150,blank=True, null=True, default = None)
    thumbnail = models.FileField(verbose_name = "Small thumbnail image of pest/pathogen", help_text="Upload thumbnail image of pest/pathogen (58x58 px crop to 0.8in square at 72ppi).",upload_to="pest_images", max_length=100, blank=True, null=True)
    large_image = models.FileField(verbose_name = "Large image of pest/pathogen", help_text="Upload image of pest/pathogen (crop to 2in square at 72ppi).",upload_to="pest_images", max_length=100, blank=True, null=True)
    spread_image = models.FileField(verbose_name = "Image or GIF of forecast", help_text="Upload image or gif of pest/pathogen ( at 72ppi).",upload_to="pest_images", max_length=100, blank=True, null=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("pest information")
        verbose_name_plural = _("pest informations")

    def __str__(self):
        return self.common_name

class Pest(models.Model):

    pest_information = models.ForeignKey(PestInformation, verbose_name = _("pest information"), help_text="Sample help text.", null=True, blank=True, on_delete = models.SET_NULL)
    name = models.CharField(verbose_name = _("pest common name"), help_text="What is the common name of the pest/pathogen?", max_length = 150, blank=True, null=True)
    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study"), on_delete=models.CASCADE)
    use_treatment = models.BooleanField(verbose_name = _("prior treatments"), help_text="Has management occurred during the time of initial infection/infestation?", default = False)
    vector_born = models.BooleanField(verbose_name = _("vector born"), help_text="Is the disease spread by a vector (e.g. an insect)?", default = False)
    MODEL_CHOICES = (
        ("SI", "Susceptible Infected"),
        ("SID", "Susceptible Infected Diseased"),
        ("SEID", "Susceptible Exposed Infected Diseased"),
    )
    model_type = models.CharField(verbose_name = _("model type"), help_text="What type of model do you want to use?", max_length = 20,
                    choices = MODEL_CHOICES,
                    default = "SI", blank=True)
    DISPERSAL_CHOICES = (
        ("CAUCHY", "Cauchy"),
        ("DOUBLE SCALE CAUCHY", "Double Scale Cauchy"),
        ("EXPONENTIAL", "Exponential"),
        ("DOUBLE SCALE EXPONENTIAL", "Double Scale Exponential")
    )
    natural_dispersal_type = models.CharField(verbose_name = _("natural dispersal type"), help_text="", max_length = 70,
                    choices = DISPERSAL_CHOICES,
                    default = "CAUCHY", blank=True)
    anthropogenic_dispersal_type = models.CharField(verbose_name = _("anthropogenic dispersal type"), help_text="", max_length = 70,
                    choices = DISPERSAL_CHOICES,
                    default = "CAUCHY", blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("pest")
        verbose_name_plural = _("pests")

    def __str__(self):
        if self.name == '':
            string = self.pest_information.common_name
        else:
            string = self.name
        return string

class InitialInfestation(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    user_file = models.FileField(verbose_name = _("initial infestation data"), help_text="Upload your initial infestation/infection data as a raster file (1 file with a layer for each year). At least 3 years are needed for calibration and validation ", blank=True, upload_to=initial_infestation_directory, max_length=100)

    objects = MyManager()
 
    class Meta:
        verbose_name = _("initial_infestation_data")
        verbose_name_plural = _("initial_infestation_datas")

    def __str__(self):
        return str(self.pk)

class CalibrationInfestation(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    user_file = models.FileField(verbose_name = _("calibration infestation data"), help_text="Upload your calibration infestation/infection data as a raster file (1 file with a layer for each year). At least 3 years are needed for calibration and validation ", blank=True, upload_to=validation_infestation_directory, max_length=100)

    objects = MyManager()

    class Meta:
        verbose_name = _("calibration_infestation_data")
        verbose_name_plural = _("calibration_infestation_datas")

    def __str__(self):
        return str(self.pk)

class ValidationInfestation(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    user_file = models.FileField(verbose_name = _("validation infestation data"), help_text="Upload your validation infestation/infection data as a raster file (1 file with a layer for each year). At least 3 years are needed for calibration and validation ", blank=True, upload_to=calibration_infestation_directory, max_length=100)

    objects = MyManager()

    class Meta:
        verbose_name = _("validation_infestation_data")
        verbose_name_plural = _("validation_infestation_datas")

    def __str__(self):
        return str(self.pk)

class PriorTreatment(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    user_file = models.FileField(verbose_name =  _("prior treatments data"), help_text="Upload the raster file for management actions. 1 file with a layer for each year.", upload_to = treatment_directory, max_length=100, null=True, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("prior_treatment")
        verbose_name_plural = _("prior_treatments")

    def __str__(self):
        return self.pest

class PriorTreatmentYear(models.Model):

    prior_treatment = models.ForeignKey(PriorTreatment, verbose_name = _("prior treatment"), on_delete = models.CASCADE)
    year = models.PositiveSmallIntegerField(verbose_name = _("prior treatment year"), validators = [MinValueValidator(1900), MaxValueValidator(2200)])

    objects = MyManager()

    class Meta:
        verbose_name = _("prior treatment year")
        verbose_name_plural = _("prior treatment years")

    def __str__(self):
        return self.year

class Vector(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    common_name = models.CharField(verbose_name = _("vector common name"), help_text="What is the common name of the vector?", max_length = 150, blank=True)
    scientific_name = models.CharField(verbose_name = _("vector scientific name"), help_text="What is the scientific name of the vector?", max_length = 150, blank=True)
    user_file = models.FileField(verbose_name = _("vector data"), help_text="Upload your vector data as a raster file.",upload_to=vector_directory, max_length=100, null = True, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("vector")
        verbose_name_plural = _("vectors")

    def __str__(self):
        return self.common_name

class VectorHostTransmissionRate(models.Model):

    vector = models.ForeignKey(Vector, verbose_name = _("vector"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("vector to host transmission rate value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("vector to host transmission rate probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("vector to host transmission rate")
        verbose_name_plural = _("vector to host transmission rates")

    def __str__(self):
        return str(self.pk)

class HostVectorTransmissionRate(models.Model):

    vector = models.ForeignKey(Vector, verbose_name = _("vector"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("host to vector transmission rate value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("host to vector transmission rate probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("host to vector transmission rate")
        verbose_name_plural = _("host to vector transmission rates")

    def __str__(self):
        return str(self.pk)

class VectorReproductiveRate(models.Model):

    vector = models.ForeignKey(Vector, verbose_name = _("vector"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("vector reproductive rate value"), max_digits = 5, decimal_places = 1, blank=True)
    probability = models.DecimalField(verbose_name = _("vector reproductive rate probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("vector reproductive rate")
        verbose_name_plural = _("vector reproductive rates")

    def __str__(self):
        return str(self.pk)

class VectorNaturalDistance(models.Model):

    vector = models.ForeignKey(Vector, verbose_name = _("vector"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("vector natural distance scale value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("vector natural distance scale probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("vector natural distance dispersal")
        verbose_name_plural = _("vector natural distance dispersals")

    def __str__(self):
        return str(self.pk)

class ReproductiveRate(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("reproductive rate value"), max_digits = 5, decimal_places = 1, blank=True)
    probability = models.DecimalField(verbose_name = _("reproductive rate probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("reproductive rate")
        verbose_name_plural = _("reproductive rates")

    def __str__(self):
        return str(self.pk)

class PercentNaturalDistance(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("percent natural distance scale value"), max_digits = 5, decimal_places = 2, blank=True)
    probability = models.DecimalField(verbose_name = _("percent natural distance scale probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("natural distance dispersal percentage")
        verbose_name_plural = _("natural distance dispersal percentages")

    def __str__(self):
        return str(self.pk)

class NaturalDistance(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("natural distance scale value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("natural distance scale probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("natural distance dispersal")
        verbose_name_plural = _("natural distance dispersals")

    def __str__(self):
        return str(self.pk)

class AnthropogenicDistance(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("anthropogenic distance scale value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("anthropogenic distance scale probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("anthropogenic distance dispersal")
        verbose_name_plural = _("anthropogenic distance dispersals")

    def __str__(self):
        return str(self.pk)

class AnthropogenicDirection(models.Model):

    pest = models.OneToOneField(Pest, verbose_name = _("pest"), on_delete = models.CASCADE, primary_key=True)
    DIRECTION_CHOICES = (
        ("N", "North"),
        ("NE", "Northeast"),
        ("E", "East"),
        ("SE", "Southeast"),
        ("S", "South"),
        ("SW", "Southwest"),
        ("W", "West"),
        ("NW", "Northwest"),
    )
    direction = models.CharField(verbose_name = _("anthropogenic direction"), help_text="What is the predominate anthropogenic direction in your study area?", 
                    max_length = 30,
                    choices = DIRECTION_CHOICES,
                    default = "N", blank = False)
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

    kappa = models.PositiveSmallIntegerField(verbose_name = _("anthropogenic direction strenth (kappa)"), help_text="What is the average anthropogenic strength in your study area? 0 is no effect and 12 is very strong directional movement", choices = KAPPA_CHOICES, default = 1, blank = False, validators = [MinValueValidator(1), MaxValueValidator(12)])

    objects = MyManager()

    class Meta:
        verbose_name = _("anthropogenic direction")
        verbose_name_plural = _("anthropogenic directions")

    def __str__(self):
        return str(self.pk)

class CrypticToInfected(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("cryptic to infected value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("cryptic to infected  probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("cryptic to infected")
        verbose_name_plural = _("cryptic to infecteds")

    def __str__(self):
        return str(self.pk)

class InfectedToDiseased(models.Model):

    pest = models.ForeignKey(Pest, verbose_name = _("pest"), on_delete = models.CASCADE)
    value = models.DecimalField(verbose_name = _("infected to diseased value"), max_digits = 5, decimal_places = 0, blank=True)
    probability = models.DecimalField(verbose_name = _("infected to diseased  probability"), max_digits = 5, decimal_places = 2, blank=True)

    objects = MyManager()

    class Meta:
        verbose_name = _("infected to diseased")
        verbose_name_plural = _("infected to diseaseds")

    def __str__(self):
        return str(self.pk)

class Weather(models.Model):

    case_study = models.OneToOneField(CaseStudy, verbose_name = _("case study"), on_delete = models.CASCADE, primary_key=True)
    wind_on = models.BooleanField(verbose_name = _("wind"), help_text="Does wind strongly affect the spread of your pest/pathogen and do you have a predominate wind direction and strength?", default = False)
    seasonality_on = models.BooleanField(verbose_name = _("seasonality"), help_text="Does your pest/pathogen not spread during part of the year?", default = False)
    lethal_temp_on = models.BooleanField(verbose_name = _("lethal temperature"), help_text="Does your pest/pathogen experience mortality due to extreme temperature conditions?", default = False)
    temp_on = models.BooleanField(verbose_name = _("temperature"), help_text="Does temperature affect the reproduction and survival of your pest/pathogen?", default = False)
    precipitation_on = models.BooleanField(verbose_name = _("precipitation"), help_text="Does precipitation affect the reproduction and survival of your pest/pathogen?", default = False)

    objects = MyManager()

    class Meta:
        verbose_name = _("weather")
        verbose_name_plural = _("weathers")

    def __str__(self):
        return str(self.pk)

class Wind(models.Model):

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    DIRECTION_CHOICES = (
        ("N", "North"),
        ("NE", "Northeast"),
        ("E", "East"),
        ("SE", "Southeast"),
        ("S", "South"),
        ("SW", "Southwest"),
        ("W", "West"),
        ("NW", "Northwest"),
    )
    wind_direction = models.CharField(verbose_name = _("wind direction"), help_text="What is the predominate wind direction in your study area?", 
                    max_length = 30,
                    choices = DIRECTION_CHOICES,
                    default = "N", blank = False)
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

    kappa = models.PositiveSmallIntegerField(verbose_name = _("wind strenth (kappa)"), help_text="What is the average wind strength in your study area? 0 is no effect and 12 is very strong directional movement", choices = KAPPA_CHOICES, default = 1, blank = False, validators = [MinValueValidator(1), MaxValueValidator(12)])

    objects = MyManager()

    class Meta:
        verbose_name = _("wind")
        verbose_name_plural = _("winds")

    def __str__(self):
        return str(self.pk)


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
    first_month = models.PositiveSmallIntegerField(verbose_name = _("first month of season"), help_text="What is the first month your pest/pathogen spreads during the year?", choices = MONTH, default = 1, blank=False, validators = [MinValueValidator(1), MaxValueValidator(12)])
    last_month = models.PositiveSmallIntegerField(verbose_name = _("last month of season"), help_text="What is the last month your pest/pathogen spreads during the year?", choices = MONTH, default = 12, blank=False, validators = [MinValueValidator(1), MaxValueValidator(12)])

    objects = MyManager()

    class Meta:
        verbose_name = _("seasonality")
        verbose_name_plural = _("seasonalities")

    def __str__(self):
        return "Seasonality"

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
    LETHAL_TYPE = (
            ('COLD', "Cold"),
            ('HOT', "Hot"),
        )

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    lethal_type = models.CharField(verbose_name = _("lethal temperature type"), help_text="Is your pest killed by hot or cold temperatures?", choices = LETHAL_TYPE, max_length = 4, default = "COLD", blank=False)
    month = models.PositiveSmallIntegerField(verbose_name = _("month in which lethal temperature occurs"), help_text="What month does your lethal temperature occur?", choices = MONTH, default = 1, blank=False)
    value = models.DecimalField(verbose_name = _("lethal temperature"), help_text="What is the lethal temperature at which pest/pathogen mortality occurs?", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(-50), MaxValueValidator(50)])
    lethal_temperature_data = models.FileField(verbose_name = _("lethal temperature data"), help_text="Upload your letah temperature data as a raster file (1 file with a layer for each year).", upload_to=lethal_temperature_directory, max_length=100, null = True)

    objects = MyManager()

    class Meta:
        verbose_name = _("lethal temperature")
        verbose_name_plural = _("lethal temperatures")

    def __str__(self):
        return "Lethal_temp"

class Temperature(models.Model):

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    METHOD_CHOICES = (
        ("RECLASS", "Reclass"),
        ("POLYNOMIAL", "Polynomial"),
    )
    method = models.CharField(verbose_name = _("temperature coefficient creation method"), help_text="Choose a method to transform temperature into a coefficient used by the model. Temperature values are transformed into a value between 0 and 1.", max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "RECLASS", blank = False)
    temperature_data = models.FileField(verbose_name = _("temperature data"), help_text="Upload your temperature data as a raster file (1 file with a layer for each timestep).", upload_to=temperature_directory, max_length=100, null = True)

    objects = MyManager()

    class Meta:
        verbose_name = _("temperature")
        verbose_name_plural = _("temperatures")

    def __str__(self):
        return 'Temperature'

class Precipitation(models.Model):

    weather = models.OneToOneField(Weather, verbose_name = _("weather"), on_delete = models.CASCADE, primary_key=True)
    METHOD_CHOICES = (
        ("RECLASS", "Reclass"),
        ("POLYNOMIAL", "Polynomial"),
    )
    method = models.CharField(verbose_name = _("precipitation coefficient creation method"), help_text="Choose a method to transform precipitation into a coefficient used by the model. Precipitation values are transformed into a value between 0 and 1.", max_length = 30,
                    choices = METHOD_CHOICES,
                    default = "RECLASS", blank = False)
    precipitation_data = models.FileField(verbose_name = _("precipitation data"), help_text="Upload your precipitation data as a raster file (1 file with a layer for each timestep).", upload_to=precipitation_directory, max_length=100, null = True)

    objects = MyManager()

    class Meta:
        verbose_name = _("precipitation")
        verbose_name_plural = _("precipitations")

    def __str__(self):
        return 'Precipitation'

class TemperatureReclass(models.Model):

    temperature = models.ForeignKey(Temperature, verbose_name = _("temperature"), on_delete = models.CASCADE)
    min_value = models.DecimalField(verbose_name = _("min"), help_text="Minimum temperature (in degrees Celsius) to reclass from.", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(-50), MaxValueValidator(100)])
    max_value = models.DecimalField(verbose_name = _("max"), help_text="Maximum temperature (in degrees Celsius) to reclass from.", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(-50), MaxValueValidator(100)])
    reclass = models.DecimalField(verbose_name = _("reclass"), help_text="Reclass value (between 0 and 1).", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(1)])

    objects = MyManager()

    class Meta:
        verbose_name = _("temperature reclass")
        verbose_name_plural = _("temperature reclasses")
        ordering = ['min_value']

    def __str__(self):
        return 'TemperatureReclass'

class PrecipitationReclass(models.Model):

    precipitation = models.ForeignKey(Precipitation, verbose_name = _("precipitation"), on_delete = models.CASCADE)
    min_value = models.DecimalField(verbose_name = _("min"), help_text="Minimum precipitation (in millimeters) to reclass from.", max_digits = 6, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    max_value = models.DecimalField(verbose_name = _("max"), help_text="Maximum precipitation (in millimeters) to reclass from.", max_digits = 6, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    reclass = models.DecimalField(verbose_name = _("reclass"), help_text="Reclass value (between 0 and 1).", max_digits = 4, decimal_places = 2, blank=True, validators = [MinValueValidator(0), MaxValueValidator(1)])

    objects = MyManager()

    class Meta:
        verbose_name = _("precipitation reclass")
        verbose_name_plural = _("precipitation reclasses")
        ordering = ['min_value']

    def __str__(self):
        return 'PrecipitationReclass'


class TemperaturePolynomial(models.Model):

    temperature = models.OneToOneField(Temperature, verbose_name = _("temperature"), on_delete = models.CASCADE, primary_key=True)
    DEGREE_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
    )
    degree = models.PositiveSmallIntegerField(verbose_name = _("polynomial degree"), help_text="Select the degree of your polynomial function.", 
                    choices = DEGREE_CHOICES, default = 1, blank = False)
    a0 = models.DecimalField(verbose_name = _("a0"), help_text="value of a0 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a1 = models.DecimalField(verbose_name = _("a1"), help_text="value of a1 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a2 = models.DecimalField(verbose_name = _("a2"), help_text="value of a2 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a3 = models.DecimalField(verbose_name = _("a3"), help_text="value of a3 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    x1 = models.DecimalField(verbose_name = _("x1"), help_text="value of x1 in your polynomial transformation.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x2 = models.DecimalField(verbose_name = _("x2"), help_text="value of x2 in your polynomial transformation.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x3 = models.DecimalField(verbose_name = _("x3"), help_text="value of x3 in your polynomial transformation.", max_digits = 5, decimal_places = 2, blank = True, null = True)

    objects = MyManager()

    class Meta:
        verbose_name = _("temperature polynomial")
        verbose_name_plural = _("temperature polynomials")

    def __str__(self):
        return 'Temperature Polynomial'

class PrecipitationPolynomial(models.Model):

    precipitation = models.OneToOneField(Precipitation, verbose_name = _("precipitation"), on_delete = models.CASCADE, primary_key=True)
    DEGREE_CHOICES = (
        (1, "One"),
        (2, "Two"),
        (3, "Three"),
    )
    degree = models.PositiveSmallIntegerField(verbose_name = _("polynomial degree"), help_text="Select the degree of your polynomial function.", 
                    choices = DEGREE_CHOICES, default = 1, blank = False)
    a0 = models.DecimalField(verbose_name = _("a0"), help_text="value of a0 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a1 = models.DecimalField(verbose_name = _("a1"), help_text="value of a1 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a2 = models.DecimalField(verbose_name = _("a2"), help_text="value of a2 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    a3 = models.DecimalField(verbose_name = _("a3"), help_text="value of a3 in your polynomial transformation.", max_digits = 8, decimal_places = 5, blank = True, null = True)
    x1 = models.DecimalField(verbose_name = _("x1"), help_text="value of x1 in your polynomial transformation.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x2 = models.DecimalField(verbose_name = _("x2"), help_text="value of x2 in your polynomial transformation.", max_digits = 5, decimal_places = 2, blank = True, null = True)
    x3 = models.DecimalField(verbose_name = _("x3"), help_text="value of x3 in your polynomial transformation.", max_digits = 5, decimal_places = 2, blank = True, null = True)

    objects = MyManager()

    class Meta:
        verbose_name = _("precipitation polynomial")
        verbose_name_plural = _("precipitation polynomials")

    def __str__(self):
        return 'Precipitation Polynomial'

class Session(models.Model):

    case_study = models.ForeignKey(CaseStudy, verbose_name = _("case study"), help_text="Select a case study for this session.", on_delete = models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name = _('created by'), editable = False,
        null = True, on_delete = models.SET_NULL)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    name = models.CharField(verbose_name = _("session name"), max_length=150, help_text="Give your session a descriptive name.")
    description = models.TextField(verbose_name = _("session description"), max_length = 300, blank=True, null=True, help_text="Give your session a description.")
    reproductive_rate = models.DecimalField(verbose_name = _("reproductive rate"), help_text="Reproductive rate of pest/pathogen", max_digits = 6, decimal_places = 2, blank=True, null=True, default = 0)
    distance_scale = models.DecimalField(verbose_name = _("distance scale"), max_digits = 5, decimal_places = 1)
    final_year = models.PositiveIntegerField(verbose_name = _("final run year"), default = 2021, null = True, validators = [MinValueValidator(2018)])
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
    management_month = models.PositiveSmallIntegerField(verbose_name = _("month management takes place"), help_text="What month does management take place?", choices = MONTH, default = 7, blank=False, validators = [MinValueValidator(1), MaxValueValidator(12)])
    WEATHER_CHOICES = (
        ("BAD", "Poor spread conditions"),
        ("AVERAGE", "Average spread conditions"),
        ("GOOD", "Optimal spread conditions"),
    )
    weather = models.CharField(verbose_name = _("weather"), help_text="", max_length = 20,
                    choices = WEATHER_CHOICES,
                    default = "AVERAGE", blank=True)
    default_run = models.OneToOneField('Run', verbose_name = _("default run"), help_text="Default no management run for this session and default run_collection parameters.", on_delete = models.CASCADE, blank=True, null = True)
    max_value = models.PositiveSmallIntegerField(verbose_name = _("maximum value within a cell in default run"), help_text="Maximum value of number of infected in a cell for final year of the default run", default = 0, null = True, blank=True, validators = [MinValueValidator(0), MaxValueValidator(100)])
    public = models.BooleanField(verbose_name = _("public"), help_text="Is the session sharing set to public (any user can view and edit the session)?", default = False)

    class Meta:
        verbose_name = _("session")
        verbose_name_plural = _("sessions")

    def __str__(self):
        return self.name

class RunCollection(models.Model):

    session = models.ForeignKey(Session, verbose_name = _("session id"), on_delete = models.CASCADE)
    name = models.CharField(verbose_name = _("run name"), default="Default_name", max_length = 45)
    description = models.TextField(verbose_name = _("run description"), default="Give your run a description.", max_length = 300, blank=True, null=True, help_text="Give your run a description.")
    random_seed = models.PositiveIntegerField(verbose_name = _("random seed"), default = 33, null = True, validators = [MinValueValidator(1)])
    tangible_landscape = models.BooleanField(verbose_name = _("tangible landscape"), help_text="Use tangible landscape for management?", default = False)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN PROGRESS", "In progress"),
        ("READING DATA", "Reading data"),
        ("WAITING FOR TL", "Waiting for Tangible Landscape"),
        ("RUNNING MODEL", "Running model"),
        ("WRITING DATA", "Writing data"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Successful"),
    )
    status = models.CharField(verbose_name = _("run status"), help_text="", max_length = 20,
                    choices = STATUS_CHOICES,
                    default = "PENDING", blank=True)
    budget = models.PositiveIntegerField(verbose_name = _("budget"), default = 30000000, null = True, validators = [MinValueValidator(1)])
    default = models.BooleanField(verbose_name = _("default run collection"), help_text="Is this the default run collection for this session?", default = False)

    class Meta:
        verbose_name = _("run collection")
        verbose_name_plural = _("run collections")

    def __str__(self):
        return self.name

class Run(models.Model):

    run_collection = models.ForeignKey(RunCollection, verbose_name = _("run collection id"), on_delete = models.CASCADE)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("IN PROGRESS", "In progress"),
        ("READING DATA", "Reading data"),
        ("WAITING FOR TL", "Waiting for Tangible Landscape"),
        ("RUNNING MODEL", "Running model"),
        ("WRITING DATA", "Writing data"),
        ("FAILED", "Failed"),
        ("SUCCESS", "Successful"),
    )
    status = models.CharField(verbose_name = _("run status"), help_text="", max_length = 20,
                    choices = STATUS_CHOICES,
                    default = "PENDING", blank=True)
    management_polygons = models.JSONField(null = True, blank = True)
    management_cost = models.DecimalField(verbose_name = _("management cost"), max_digits = 16, decimal_places = 2, blank=True, null=True, default = 0)
    management_area = models.DecimalField(verbose_name = _("management area"), max_digits = 16, decimal_places = 2, blank=True, null=True, default = 0)
    logging = models.TextField(verbose_name = _("error logs for backend"), max_length = 300, blank=True, null=True, help_text="For checking error logs for backend model runs")
    time_taken = models.DecimalField(verbose_name = _("time taken"), max_digits = 5, decimal_places = 1, blank=True, null=True)
    steering_year = models.PositiveIntegerField(verbose_name = _("steering year"), default = None, null = True, blank= True, validators = [MinValueValidator(2018)])

    class Meta:
        verbose_name = _("run")
        verbose_name_plural = _("runs")

    def __str__(self):
        return str(self.pk)

class Output(models.Model):

    run = models.ForeignKey(Run, verbose_name = _("run id"), on_delete = models.CASCADE)
    date_created = models.DateTimeField(verbose_name = _("date created"), auto_now = False, auto_now_add = True)
    number_infected = models.IntegerField(verbose_name = _("number_infected"), default = 0, null = True, validators = [MinValueValidator(0)])
    infected_area = models.DecimalField(verbose_name = _("infected_area (m^2)"), help_text="Overall infected area from the run.", blank=True, max_digits = 16, decimal_places = 2, default = 1, validators = [MinValueValidator(0)])
    year = models.PositiveIntegerField(verbose_name = _("year"), default = 2020, null = True, validators = [MinValueValidator(2018)])
    single_spread_map = models.JSONField(null = True)
    probability_map = models.JSONField(null = True)
    susceptible_map = models.JSONField(null = True)
    escape_probability = models.DecimalField(verbose_name = _("probability of escape"), help_text="Probability that the pest/pathogen escapes quarantine or other boundary.", blank=True, max_digits = 6, decimal_places = 2, default = 1, validators = [MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        verbose_name = _("output")
        verbose_name_plural = _("outputs")

    def __str__(self):
        return str(self.pk)

class SpreadRate(models.Model):

    output = models.OneToOneField(Output, verbose_name = _("output"), on_delete = models.CASCADE, primary_key = True)
    west_rate = models.DecimalField(verbose_name = _("westerly spread rate"), help_text="Spread rate in westerly direction", blank=True, null=True, max_digits = 16, decimal_places = 2)
    east_rate = models.DecimalField(verbose_name = _("easterly spread rate"), help_text="Spread rate in easterly direction", blank=True, null=True, max_digits = 16, decimal_places = 2)
    north_rate = models.DecimalField(verbose_name = _("northerly spread rate"), help_text="Spread rate in northerly direction", blank=True, null=True, max_digits = 16, decimal_places = 2)
    south_rate = models.DecimalField(verbose_name = _("southerly spread rate"), help_text="Spread rate in southerly direction", blank=True, null=True, max_digits = 16, decimal_places = 2)

    class Meta:
        verbose_name = _("spread rate")
        verbose_name_plural = _("spread rates")

    def __str__(self):
        return str(self.output)

class DistanceToBoundary(models.Model):

    output = models.OneToOneField(Output, verbose_name = _("output"), on_delete = models.CASCADE, primary_key = True)
    west_distance = models.DecimalField(verbose_name = _("westerly distance to boundary"), help_text="Spread rate in westerly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])
    east_distance = models.DecimalField(verbose_name = _("easterly distance to boundary"), help_text="Spread rate in easterly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])
    north_distance = models.DecimalField(verbose_name = _("northerly distance to boundary"), help_text="Spread rate in northerly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])
    south_distance = models.DecimalField(verbose_name = _("southerly distance to boundary"), help_text="Spread rate in southerly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])

    class Meta:
        verbose_name = _("distance to boundary")
        verbose_name_plural = _("distance to boundarys")

    def __str__(self):
        return str(self.output)

class TimeToBoundary(models.Model):

    output = models.OneToOneField(Output, verbose_name = _("output"), on_delete = models.CASCADE, primary_key = True)
    west_time = models.DecimalField(verbose_name = _("westerly time to boundary"), help_text="Spread rate in westerly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])
    east_time = models.DecimalField(verbose_name = _("easterly time to boundary"), help_text="Spread rate in easterly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])
    north_time = models.DecimalField(verbose_name = _("northerly time to boundary"), help_text="Spread rate in northerly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])
    south_time = models.DecimalField(verbose_name = _("southerly time to boundary"), help_text="Spread rate in southerly direction", blank=True, null=True, max_digits = 6, decimal_places = 2, validators = [MinValueValidator(0)])

    class Meta:
        verbose_name = _("time to boundary")
        verbose_name_plural = _("time to boundarys")

    def __str__(self):
        return str(self.output)

class AllowedUsers(models.Model):

    session = models.ForeignKey(Session, verbose_name = _("session id"), on_delete = models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name = _('user id'), on_delete = models.CASCADE)

    class Meta:
        verbose_name = _("allowed user")
        verbose_name_plural = _("allowed users")

    def __str__(self):
        return str(self.pk)
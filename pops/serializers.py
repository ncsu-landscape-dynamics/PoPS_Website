# from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import *


class TemperaturePolynomialSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperaturePolynomial
        fields = ["degree", "a0", "a1", "a2", "a3", "x1", "x2", "x3"]


class PrecipitationPolynomialSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecipitationPolynomial
        fields = ["degree", "a0", "a1", "a2", "a3", "x1", "x2", "x3"]


class TemperatureReclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperatureReclass
        fields = ["min_value", "max_value", "reclass"]


class PrecipitationReclassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrecipitationReclass
        fields = ["min_value", "max_value", "reclass"]


class PrecipitationSerializer(serializers.ModelSerializer):
    precipitationreclass_set = PrecipitationReclassSerializer(many=True)
    precipitationpolynomial = PrecipitationPolynomialSerializer()

    class Meta:
        model = Precipitation
        fields = [
            "method",
            "precipitationreclass_set",
            "precipitationpolynomial",
            "precipitation_data",
        ]


class TemperatureSerializer(serializers.ModelSerializer):
    temperaturereclass_set = TemperatureReclassSerializer(many=True)
    temperaturepolynomial = TemperaturePolynomialSerializer()

    class Meta:
        model = Temperature
        fields = [
            "method",
            "temperaturereclass_set",
            "temperaturepolynomial",
            "temperature_data",
        ]


class LethalTemperatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = LethalTemperature
        fields = ("lethal_type", "month", "value", "lethal_temperature_data")


class SeasonalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Seasonality
        fields = ("first_month", "last_month")


class WindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wind
        fields = ("wind_direction", "kappa")


class TemperatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"


class WeatherSerializer(serializers.ModelSerializer):
    wind = WindSerializer()
    seasonality = SeasonalitySerializer()
    lethaltemperature = LethalTemperatureSerializer()
    temperature = TemperatureSerializer()
    precipitation = PrecipitationSerializer()

    class Meta:
        model = Weather
        fields = (
            "pk",
            "wind_on",
            "seasonality_on",
            "lethal_temp_on",
            "temp_on",
            "precipitation_on",
            "wind",
            "seasonality",
            "lethaltemperature",
            "temperature",
            "precipitation",
        )


class MortalityRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortalityRate
        fields = ["value", "probability"]


class MortalityTimeLagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortalityTimeLag
        fields = ["value", "probability"]


class MortalitySerializer(serializers.ModelSerializer):

    mortalityrate_set = MortalityRateSerializer(many=True)
    mortalitytimelag_set = MortalityTimeLagSerializer(many=True)

    class Meta:
        model = Mortality
        fields = [
            "method",
            "user_file",
            "rate",
            "time_lag",
            "mortalityrate_set",
            "mortalitytimelag_set",
        ]


class QuarantineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quarantine
        fields = ["name", "date", "polygon"]


class QuarantineLinkSerializer(serializers.ModelSerializer):

    quarantine = QuarantineSerializer()

    class Meta:
        model = QuarantineLink
        fields = ["quarantine"]


class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = ["means", "covariance_matrix"]


class LatencyPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = LatencyPeriod
        fields = ["minimum", "maximum"]


class AnthropogenicDirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnthropogenicDirection
        fields = ["direction", "kappa"]


class PestInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PestInformation
        fields = ["common_name"]


class VectorHostTransmissionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VectorHostTransmissionRate
        fields = ["value", "probability"]


class HostVectorTransmissionRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostVectorTransmissionRate
        fields = ["value", "probability"]


class VectorPestInformationSerializer(serializers.ModelSerializer):

    vectorhosttransmissionrate_set = VectorHostTransmissionRateSerializer(many=True)
    hostvectortransmissionrate_set = HostVectorTransmissionRateSerializer(many=True)

    class Meta:
        model = VectorPestInformation
        fields = [
            "vector",
            "vectorhosttransmissionrate_set",
            "hostvectortransmissionrate_set",
        ]


class PriorTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorTreatment
        fields = ["user_file", "date"]


class InfestationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Infestation
        fields = ["user_file"]


class HostLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostLocation
        fields = ["raster_map", "json_map", "meta_data", "date"]


class HostMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostMovement
        fields = ["date", "number_of_units", "to_location", "from_location"]


class HostInformationSerializer(serializers.ModelSerializer):

    hostlocation_set = HostLocationSerializer(many=True)
    hostmovement_set = HostMovementSerializer(many=True)

    class Meta:
        model = HostInformation
        fields = ["name", "hostlocation_set", "hostmovement_set"]


class ClippedHostLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClippedHostLocation
        fields = ["raster_map", "json_map", "date"]


class ClippedHostMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClippedHostMovement
        fields = ["movement_file", "date"]


class PestHostInteractionSerializer(serializers.ModelSerializer):

    clippedhostlocation = ClippedHostLocationSerializer()
    clippedhostmovement = ClippedHostMovementSerializer()
    mortality = MortalitySerializer()

    class Meta:
        model = PestHostInteraction
        fields = [
            "pest",
            "host",
            "competency",
            "susceptibility",
            "mortality_on",
            "clippedhostlocation",
            "clippedhostmovement",
            "mortality",
        ]


class PestSerializer(serializers.ModelSerializer):

    # vectorpestinformation_set = VectorPestInformationSerializer(many=True)
    infestation = InfestationSerializer()
    priortreatment = PriorTreatmentSerializer()
    latencyperiod = LatencyPeriodSerializer()
    anthropogenicdirection = AnthropogenicDirectionSerializer()
    parameters = ParametersSerializer()
    quarantinelink_set = QuarantineLinkSerializer(many=True)
    pesthostinteraction_set = PestHostInteractionSerializer(many=True)
    weather = WeatherSerializer()

    class Meta:
        model = Pest
        fields = [
            "pk",
            "use_treatment",
            "vector_born",
            "model_type",
            "natural_dispersal_type",
            "anthropogenic_dispersal_type",
            "use_quarantine",
            # "vectorpestinformation_set",
            "infestation",
            "priortreatment",
            "latencyperiod",
            "anthropogenicdirection",
            "parameters",
            "pesthostinteraction_set",
            "quarantinelink_set",
            "weather",
        ]


class AllPopulationsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllPopulationsData
        fields = ["user_file"]


class MapBoxParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapBoxParameters
        fields = ["longitude", "latitude", "zoom"]


class CaseStudySerializer(serializers.ModelSerializer):
    allpopulationsdata = AllPopulationsDataSerializer()
    mapboxparameters = MapBoxParametersSerializer()
    pest_set = PestSerializer(many=True)

    class Meta:
        model = CaseStudy
        fields = [
            "name",
            "description",
            "number_of_pests",
            "number_of_hosts",
            "time_step_unit",
            "time_step_n",
            "first_calibration_date",
            "last_calibration_date",
            "first_forecast_date",
            "last_forecast_date",
            "staff_approved",
            "calibration_status",
            "use_external_calibration",
            "calibration",
            "output_frequency_unit",
            "output_frequency_n",
            "use_movements",
            "start_exposed",
            "use_spread_rate",
            "r_data",
            "advanced_network_file",
            "allpopulationsdata",
            "mapboxparameters",
            "pest_set",
        ]


class SpreadRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpreadRate
        fields = ["west_rate", "east_rate", "north_rate", "south_rate"]


class DistanceToBoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceToBoundary
        fields = ["west_distance", "east_distance", "north_distance", "south_distance"]


class TimeToBoundarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeToBoundary
        fields = ["west_time", "east_time", "north_time", "south_time"]


class OutputSerializer(serializers.ModelSerializer):
    spreadrate = SpreadRateSerializer()
    distancetoboundary = DistanceToBoundarySerializer()
    timetoboundary = TimeToBoundarySerializer()

    class Meta:
        model = Output
        fields = [
            "pk",
            "pest",
            "run",
            "number_infected",
            "infected_area",
            "year",
            "min_spread_map",
            "max_spread_map",
            "mean_spread_map",
            "median_spread_map",
            "probability_map",
            "standard_deviation_map",
            "escape_probability",
            "spreadrate",
            "distancetoboundary",
            "timetoboundary",
        ]

    def create(self, validated_data):
        spreadrate_data = validated_data.pop("spreadrate")
        distancetoboundary_data = validated_data.pop("distancetoboundary")
        timetoboundary_data = validated_data.pop("timetoboundary")
        output = Output.objects.create(**validated_data)
        SpreadRate.objects.create(output=output, **spreadrate_data)
        DistanceToBoundary.objects.create(output=output, **distancetoboundary_data)
        TimeToBoundary.objects.create(output=output, **timetoboundary_data)
        return output


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"


class RunSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        exclude = ["management_polygons"]


class RunCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunCollection
        fields = "__all__"


class TemperatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperature
        fields = "__all__"


class LethalTemperatureDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = LethalTemperature
        fields = "__all__"


class PrecipitationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Precipitation
        fields = "__all__"


class SessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"

    runcollection_count = serializers.SerializerMethodField()
    most_recent_runcollection = serializers.SerializerMethodField()
    runcollection_set = RunCollectionSerializer(many=True)
    # second_most_recent_runcollection = serializers.SerializerMethodField()

    def get_runcollection_count(self, obj):
        return obj.runcollection_set.count()

    def get_most_recent_runcollection(self, obj):
        if obj.runcollection_set.exists():
            return obj.runcollection_set.order_by("-pk")[0].pk
        else:
            return "null"

    def get_second_most_recent_runcollection(self, obj):
        if obj.runcollection_set.exists():
            if obj.runcollection_set.count() > 1:
                return obj.runcollection_set.order_by("-pk")[1].pk
            else:
                return obj.runcollection_set.order_by("-pk")[0].pk
        else:
            return "null"


class SessionModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"

    runcollection_count = serializers.SerializerMethodField()
    most_recent_runcollection = serializers.SerializerMethodField()
    # second_most_recent_runcollection = serializers.SerializerMethodField()

    def get_runcollection_count(self, obj):
        return obj.runcollection_set.count()

    def get_most_recent_runcollection(self, obj):
        if obj.runcollection_set.exists():
            return obj.runcollection_set.order_by("-pk")[0].pk
        else:
            return "null"

    def get_second_most_recent_runcollection(self, obj):
        if obj.runcollection_set.exists():
            if obj.runcollection_set.count() > 1:
                return obj.runcollection_set.order_by("-pk")[1].pk
            else:
                return obj.runcollection_set.order_by("-pk")[0].pk
        else:
            return "null"


class RunCollectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunCollection
        fields = "__all__"

    run_set = RunSerializer(many=True)
    second_most_recent_run = serializers.SerializerMethodField()

    def get_second_most_recent_run(self, obj):
        if obj.run_set.exists():
            if obj.run_set.count() > 1:
                return obj.run_set.order_by("-pk")[1].pk
            else:
                return obj.run_set.order_by("-pk")[0].pk
        else:
            return "null"


class RunCollectionModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RunCollection
        fields = "__all__"

    second_most_recent_run = serializers.SerializerMethodField()

    def get_second_most_recent_run(self, obj):
        if obj.run_set.exists():
            if obj.run_set.count() > 1:
                return obj.run_set.order_by("-pk")[1].pk
            else:
                return obj.run_set.order_by("-pk")[0].pk
        else:
            return "null"


class OutputPKSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = [
            "pk",
            "number_infected",
            "infected_area",
            "year",
            "escape_probability",
            "spreadrate",
            "distancetoboundary",
            "timetoboundary",
        ]


class RunDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"

    output_initial_year = serializers.SerializerMethodField()
    output_set = OutputPKSerializer(many=True)

    def get_output_initial_year(self, obj):
        if obj.output_set.exists():
            return obj.output_set.order_by("pk")[0].pk
        else:
            return "null"


class RunModelWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = "__all__"

    output_initial_year = serializers.SerializerMethodField()

    def get_output_initial_year(self, obj):
        if obj.output_set.exists():
            return obj.output_set.order_by("pk")[0].pk
        else:
            return "null"


class RunRDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Run
        fields = ["r_data"]

class OutputSpreadMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        fields = ["median_spread_map"]

class CaseStudyRDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = ["r_data"]

class CaseStudyAdvancedNetworkFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseStudy
        fields = ["advanced_network_file"]

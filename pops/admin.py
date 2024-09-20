from django.contrib import admin

from .models import *


class PestInline(admin.TabularInline):
    model = Pest
    extra = 0
    show_change_link = True


class HistoricDataInline(admin.TabularInline):
    model = HistoricData
    extra = 0
    show_change_link = True


class MapBoxParametersInline(admin.TabularInline):
    model = MapBoxParameters
    extra = 0
    show_change_link = True


class AllPopulationsDataInline(admin.TabularInline):
    model = AllPopulationsData
    extra = 0
    show_change_link = True


class MortalityRateInline(admin.TabularInline):
    model = MortalityRate
    extra = 0
    show_change_link = True


class MortalityTimeLagInline(admin.TabularInline):
    model = MortalityTimeLag
    extra = 0
    show_change_link = True


class VectorHostTransmissionRateInline(admin.TabularInline):
    model = VectorHostTransmissionRate
    extra = 0
    show_change_link = True


class HostVectorTransmissionRateInline(admin.TabularInline):
    model = HostVectorTransmissionRate
    extra = 0
    show_change_link = True


class VectorPestInformationAdmin(admin.ModelAdmin):
    list_display = ("disease", "vector")
    inlines = [VectorHostTransmissionRateInline, HostVectorTransmissionRateInline]
    list_per_page = 30


class PestLocationInline(admin.TabularInline):
    model = PestLocation
    extra = 0
    show_change_link = True


class PestTreatmentInline(admin.TabularInline):
    model = PestTreatment
    extra = 0
    show_change_link = True


class QuarantineInline(admin.TabularInline):
    model = Quarantine
    extra = 0
    show_change_link = True


class PestPesticideInline(admin.TabularInline):
    model = PestPesticideLink
    extra = 0
    show_change_link = True


class PestInformationAdmin(admin.ModelAdmin):
    list_display = ("common_name", "scientific_name", "date_created", "staff_approved")
    inlines = [
        PestLocationInline,
        PestTreatmentInline,
        QuarantineInline,
        PestPesticideInline,
    ]
    list_per_page = 30


class WeatherInline(admin.TabularInline):
    model = Weather
    extra = 0
    show_change_link = True


class CaseStudyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "session_count",
        "created_by",
        "date_created",
        "calibration_status",
    )
    inlines = [
        MapBoxParametersInline,
        AllPopulationsDataInline,
        HistoricDataInline,
        PestInline,
    ]
    # inlines = [
    #     HostInline, PestInline, AllPlantsDataInline, HistoricDataInline, MapBoxParametersInline, WeatherInline
    # ]
    search_fields = [
        "name",
        "created_by__username",
        "created_by__first_name",
        "created_by__last_name",
        "pest__name",
    ]
    list_select_related = ("created_by",)
    list_filter = ("staff_approved",)
    list_per_page = 30

    def session_count(self, obj):
        return obj.session_set.count()

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        return super(CaseStudyAdmin, self).save_model(request, obj, form, change)


class MortalityInline(admin.TabularInline):
    model = Mortality
    extra = 0
    show_change_link = True


class ClippedHostLocationInline(admin.TabularInline):
    model = ClippedHostLocation
    extra = 0
    show_change_link = True


class ClippedHostMovementInline(admin.TabularInline):
    model = ClippedHostMovement
    extra = 0
    show_change_link = True


class HostLocationInline(admin.TabularInline):
    model = HostLocation
    extra = 0
    show_change_link = True


class HostMovementInline(admin.TabularInline):
    model = HostMovement
    extra = 0
    show_change_link = True


class HostInformationAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")
    inlines = [HostLocationInline, HostMovementInline]
    list_per_page = 30


class PestHostInteractionAdmin(admin.ModelAdmin):
    list_display = ("pest", "host", "competency", "susceptibility")
    inlines = [ClippedHostLocationInline, ClippedHostMovementInline, MortalityInline]
    list_per_page = 30


class MortalityAdmin(admin.ModelAdmin):
    list_display = ("pk", "host", "method", "rate")
    inlines = [MortalityRateInline, MortalityTimeLagInline]
    list_per_page = 30


class VectorPestInformationInline(admin.TabularInline):
    model = VectorPestInformation
    fk_name = "disease"
    extra = 0
    show_change_link = True


class PestHostInteractionInline(admin.TabularInline):
    model = PestHostInteraction
    extra = 0
    show_change_link = True


class PriorTreatmentInline(admin.TabularInline):
    model = PriorTreatment
    extra = 0
    show_change_link = True


class InfestationInline(admin.TabularInline):
    model = Infestation
    extra = 0
    show_change_link = True


class QuarantineLinkInline(admin.TabularInline):
    model = QuarantineLink
    extra = 0
    show_change_link = True


class LatencyPeriodInline(admin.TabularInline):
    model = LatencyPeriod
    extra = 0
    show_change_link = True


class AnthropogenicDirectionInline(admin.TabularInline):
    model = AnthropogenicDirection
    extra = 0
    show_change_link = True


class ParametersInline(admin.TabularInline):
    model = Parameters
    extra = 0
    show_change_link = True


class PestAdmin(admin.ModelAdmin):
    list_display = ("__str__", "pest_information", "case_study")
    inlines = [
        VectorPestInformationInline,
        PestHostInteractionInline,
        PriorTreatmentInline,
        InfestationInline,
        QuarantineLinkInline,
        LatencyPeriodInline,
        AnthropogenicDirectionInline,
        ParametersInline,
        WeatherInline,
    ]
    list_per_page = 30


# class PriorTreatmentAdmin(admin.ModelAdmin):
#     inlines = [
#         PriorTreatmentYearInline
#     ]

# class VectorAdmin(admin.ModelAdmin):
#     inlines = [
#         VectorHostTransmissionRateInline, HostVectorTransmissionRateInline, VectorNaturalDistanceInline, VectorReproductiveRateInline
#     ]


class TemperatureReclassAdmin(admin.ModelAdmin):
    list_display = ("__str__", "min_value", "max_value", "reclass")


class PrecipitationReclassAdmin(admin.ModelAdmin):
    list_display = ("__str__", "min_value", "max_value", "reclass")


class TemperatureReclassInline(admin.TabularInline):
    model = TemperatureReclass
    extra = 0
    show_change_link = True


class TemperaturePolynomialInline(admin.TabularInline):
    model = TemperaturePolynomial
    extra = 0
    show_change_link = True


class TemperatureAdmin(admin.ModelAdmin):
    inlines = [TemperatureReclassInline, TemperaturePolynomialInline]


class PrecipitationReclassInline(admin.TabularInline):
    model = PrecipitationReclass
    extra = 0
    show_change_link = True


class PrecipitationPolynomialInline(admin.TabularInline):
    model = PrecipitationPolynomial
    extra = 0
    show_change_link = True


class PrecipitationAdmin(admin.ModelAdmin):
    inlines = [PrecipitationReclassInline, PrecipitationPolynomialInline]


class WindInline(admin.TabularInline):
    model = Wind
    extra = 0
    show_change_link = True


class SeasonalityInline(admin.TabularInline):
    model = Seasonality
    extra = 0
    show_change_link = True


class TemperatureInline(admin.TabularInline):
    model = Temperature
    extra = 0
    show_change_link = True


class PrecipitationInline(admin.TabularInline):
    model = Precipitation
    extra = 0
    show_change_link = True


class LethalTemperatureInline(admin.TabularInline):
    model = LethalTemperature
    extra = 0
    show_change_link = True


class WeatherAdmin(admin.ModelAdmin):
    inlines = [
        WindInline,
        LethalTemperatureInline,
        SeasonalityInline,
        TemperatureInline,
        PrecipitationInline,
    ]
    list_per_page = 30


class RunCollectionInline(admin.TabularInline):
    model = RunCollection
    extra = 0
    show_change_link = True


class AllowedUsersInline(admin.TabularInline):
    model = AllowedUsers
    extra = 0
    show_change_link = True


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "run_collection_count",
        "created_by",
        "case_study",
        "date_created",
    )
    search_fields = [
        "name",
        "created_by__username",
        "created_by__first_name",
        "created_by__last_name",
        "case_study__name",
    ]
    list_select_related = ("created_by", "case_study")
    list_filter = ["public", "case_study"]
    list_per_page = 30
    inlines = [RunCollectionInline, AllowedUsersInline]

    def run_collection_count(self, obj):
        return obj.runcollection_set.count()

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

        return super(SessionAdmin, self).save_model(request, obj, form, change)


class RunInline(admin.TabularInline):
    model = Run
    extra = 0
    show_change_link = True


class RunCollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "session", "date_created", "status", "tangible_landscape")
    inlines = [
        RunInline,
    ]
    list_per_page = 30


class OutputInline(admin.TabularInline):
    model = Output
    extra = 0
    show_change_link = True


class RunAdmin(admin.ModelAdmin):
    list_display = ("run_collection", "steering_year", "date_created", "status")
    inlines = [
        OutputInline,
    ]
    list_per_page = 30


class AllowedUsersAdmin(admin.ModelAdmin):
    list_display = ("user", "session")
    list_per_page = 30


class SpreadRateInline(admin.TabularInline):
    model = SpreadRate
    show_change_link = True
    extra = 0


class DistanceToBoundaryInline(admin.TabularInline):
    model = DistanceToBoundary
    show_change_link = True
    extra = 0


class TimeToBoundaryInline(admin.TabularInline):
    model = TimeToBoundary
    show_change_link = True
    extra = 0


class OutputAdmin(admin.ModelAdmin):
    list_display = ("run", "year", "date_created", "number_infected")
    exclude = [
        "min_spread_map",
        "max_spread_map",
        "median_spread_map",
        "probability_map",
        "susceptible_map",
    ]
    inlines = [SpreadRateInline, DistanceToBoundaryInline, TimeToBoundaryInline]


admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(HistoricData)
admin.site.register(MapBoxParameters)
admin.site.register(AllPopulationsData)
admin.site.register(PestInformation, PestInformationAdmin)
admin.site.register(Pest, PestAdmin)
admin.site.register(Pesticide)
admin.site.register(PestPesticideLink)

admin.site.register(Weather, WeatherAdmin)
admin.site.register(Wind)
admin.site.register(Seasonality)
admin.site.register(LethalTemperature)
admin.site.register(Temperature, TemperatureAdmin)
admin.site.register(Precipitation, PrecipitationAdmin)
admin.site.register(TemperatureReclass)
admin.site.register(TemperaturePolynomial)
admin.site.register(PrecipitationReclass)
admin.site.register(PrecipitationPolynomial)

admin.site.register(HostInformation, HostInformationAdmin)
admin.site.register(PestHostInteraction, PestHostInteractionAdmin)
admin.site.register(HostLocation)
admin.site.register(ClippedHostLocation)
admin.site.register(HostMovement)
admin.site.register(ClippedHostMovement)

admin.site.register(Mortality, MortalityAdmin)
admin.site.register(MortalityRate)
admin.site.register(MortalityTimeLag)
admin.site.register(VectorPestInformation, VectorPestInformationAdmin)
admin.site.register(VectorHostTransmissionRate)
admin.site.register(HostVectorTransmissionRate)

admin.site.register(Infestation)
admin.site.register(PriorTreatment)
admin.site.register(Parameters)
admin.site.register(PlottingDistanceScale)
admin.site.register(PlottingReproductiveRate)
admin.site.register(AnthropogenicDirection)
admin.site.register(LatencyPeriod)
admin.site.register(Quarantine)
admin.site.register(QuarantineLink)

admin.site.register(PestLocation)
admin.site.register(PestTreatment)

admin.site.register(Session, SessionAdmin)
admin.site.register(Run, RunAdmin)
admin.site.register(RunCollection, RunCollectionAdmin)
admin.site.register(Output, OutputAdmin)
admin.site.register(SpreadRate)
admin.site.register(DistanceToBoundary)
admin.site.register(TimeToBoundary)

admin.site.register(AllowedUsers)

from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Prefetch


from ..models import *
from ..serializers import *


class CaseStudyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows case studies to be viewed or edited.
    """
    # queryset = CaseStudy.objects.prefetch_related(
    #     Prefetch('host_set', queryset=Host.objects.select_related('mortality','hostdata')),
    #     Prefetch('pest_set',queryset=Pest.objects.prefetch_related('infectedtodiseased_set',
    #     'cryptictoinfected_set','anthropogenicdistance_set','naturaldistance_set','percentnaturaldistance_set'
    #     ).select_related('vector','initialinfestation','priortreatment')),
    #     Prefetch('weather__temperature__temperaturereclass_set'),
    #     Prefetch('weather__precipitation__precipitationreclass_set')).select_related(
    #         'created_by','allplantsdata','weather__wind','weather__seasonality',
    #         'weather__lethaltemperature','weather__temperature','weather__temperature__temperaturepolynomial',
    #         'weather__precipitation', 'weather__precipitation__precipitationpolynomial').all()
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudySerializer
    permission_classes = (permissions.AllowAny,)

class RunViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = Run.objects.prefetch_related().all()
    serializer_class = RunSerializer
    permission_classes = (permissions.AllowAny,)

class RunCollectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows run collections to be viewed or edited.
    """
    queryset = RunCollection.objects.prefetch_related().all()
    serializer_class = RunCollectionSerializer
    permission_classes = (permissions.AllowAny,)


class RunCollectionDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows run collections to be viewed or edited.
    """
    queryset = RunCollection.objects.prefetch_related("run_set").all()
    serializer_class = RunCollectionDetailSerializer
    permission_classes = (permissions.AllowAny,)

class RunCollectionModelWriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows run collections to be viewed or edited.
    """
    queryset = RunCollection.objects.all()
    serializer_class = RunCollectionModelWriteSerializer
    permission_classes = (permissions.AllowAny,)

class OutputViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Output.objects.prefetch_related().all()
    serializer_class = OutputSerializer
    permission_classes = (permissions.AllowAny,)

class TemperatureDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Temperature.objects.prefetch_related().all()
    serializer_class = TemperatureDataSerializer
    permission_classes = (permissions.AllowAny,)

class LethalTemperatureDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = LethalTemperature.objects.prefetch_related().all()
    serializer_class = LethalTemperatureDataSerializer
    permission_classes = (permissions.AllowAny,)

class PrecipitationDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Precipitation.objects.prefetch_related().all()
    serializer_class = PrecipitationDataSerializer
    permission_classes = (permissions.AllowAny,)

class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows output to be viewed or edited.
    """
    queryset = Session.objects.prefetch_related().all()
    serializer_class = SessionSerializer
    permission_classes = (permissions.AllowAny,)


class SessionModelWriteViewSet(viewsets.ModelViewSet):

    queryset = Session.objects.all()
    serializer_class = SessionModelWriteSerializer
    permission_classes = (permissions.AllowAny,)


class SessionDetailViewSet(viewsets.ModelViewSet):

    queryset = Session.objects.prefetch_related('runcollection_set').all()
    serializer_class = SessionDetailSerializer
    permission_classes = (permissions.AllowAny,)

class RunModelWriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = Run.objects.all()
    serializer_class = RunModelWriteSerializer
    permission_classes = (permissions.AllowAny,)


class RunDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = Run.objects.prefetch_related("output_set").all()
    serializer_class = RunDetailSerializer
    permission_classes = (permissions.AllowAny,)


class RunRDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = Run.objects.all()
    serializer_class = RunRDataSerializer
    permission_classes = (permissions.AllowAny,)

class OutputSpreadMapViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = Output.objects.all()
    serializer_class = OutputSpreadMapSerializer
    permission_classes = (permissions.AllowAny,)

class CaseStudyRDataViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudyRDataSerializer
    permission_classes = (permissions.AllowAny,)

class CaseStudyAdvancedNetworkFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows runs to be viewed or edited.
    """
    queryset = CaseStudy.objects.all()
    serializer_class = CaseStudyAdvancedNetworkFileSerializer
    permission_classes = (permissions.AllowAny,)

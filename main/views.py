from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Mahalla, Sector, Person, Xonadon, Problem
from django.db.models import Count, Q
from drf_spectacular.utils import extend_schema
from django.core.exceptions import ObjectDoesNotExist
from .serializers import (
    MahallaInfoSerializer, 
    MainStatsSerializer, 
    SectorInfoSerializer,
    XonadonSerializer,
    MahallaIdSerializer,
    PersonSerializer,
    RaisInfoSerializer,
    DetailedXonadonSerializer,
)


# Create your views here.


class MainStatsAPI(APIView):
    @extend_schema(
        request=MainStatsSerializer,
        responses=MainStatsSerializer
    )
    def get(self, request):
        mahalla_count = Mahalla.objects.count()
        population_count = Person.objects.count()
        households_with_problems = 0
        households_without_problems = 0
        all_households = Xonadon.objects.all()
        for household in all_households:
            # household hal_qilish_holati
            organishlar = household.organish.all()
            if len(organishlar) != 0:                
                have_not_finshed_organish = False
                for organish in organishlar:
                    if organish.hal_qilish_holati in ["Boshlanmagan", "Davom etayapti"]:
                        have_not_finshed_organish = True
                        break
                if have_not_finshed_organish:
                    households_with_problems += 1
                else:
                    households_without_problems += 1
        data = {
            "mahalla_count" : mahalla_count, 
            "population_count" : population_count,
            "households_with_problems" : households_with_problems,
            "households_without_problems" : households_without_problems,
            }
    
        ser = MainStatsSerializer(data=data)
        if ser.is_valid():
            return Response(ser.data)
        else:
            return Response(ser.errors)



class ProblemsStatsAPI(APIView):

    def get(self, request, mahalla_pk=None):
        list_problems = [problem_obj for problem_obj in Problem.objects.all()]
        #main
        dict_organish_main_count = {}
        dict_organish_main_percentage = {}
        sum_organish_main_count = 0
        
        #finished
        dict_organish_finished_count = {}
        dict_organish_finished_percentage = {}
        sum_organish_finished_count = 0
        
        #not_finished
        dict_organish_not_finished_count = {}
        dict_organish_not_finished_percentage = {}
        sum_organish_not_finished_count = 0

        #main stats
        for problem_obj in list_problems:
            if mahalla_pk:
                organish_count = problem_obj.organish.filter(xonadon__mahalla__id=mahalla_pk).count()
                finished_organish_count = problem_obj.organish.filter(hal_qilish_holati="Yakunlangan", xonadon__mahalla__id=mahalla_pk).count()
                not_finished_organish_count = problem_obj.organish.filter(hal_qilish_holati="Davom etayapti", xonadon__mahalla__id=mahalla_pk).count()
            else:
                organish_count = problem_obj.organish.count()
                finished_organish_count = problem_obj.organish.filter(hal_qilish_holati="Yakunlangan").count()
                not_finished_organish_count = problem_obj.organish.filter(hal_qilish_holati="Davom etayapti").count()

            dict_organish_main_count[problem_obj] = organish_count
            dict_organish_finished_count[problem_obj] = finished_organish_count
            dict_organish_not_finished_count[problem_obj] = not_finished_organish_count
            
            sum_organish_main_count += organish_count
            sum_organish_finished_count += finished_organish_count
            sum_organish_not_finished_count += not_finished_organish_count


        for problem, count in dict_organish_main_count.items():
            percentage = 100 * (count/sum_organish_main_count)
            dict_organish_main_percentage[problem.text] = percentage

        for problem, count in dict_organish_finished_count.items():
            percentage = 100 * (count/sum_organish_finished_count)
            dict_organish_finished_percentage[problem.text] = percentage

        for problem, count in dict_organish_not_finished_count.items():
            percentage = 100 * (count/sum_organish_not_finished_count)
            dict_organish_not_finished_percentage[problem.text] = percentage

        response_dict = {
            "all_problems" : dict_organish_main_percentage,
            "finished_problems" : dict_organish_finished_percentage,
            "not_finished_problems" : dict_organish_not_finished_percentage,
        }    
        
        return Response(response_dict)



class SectorInfo(APIView):
    @extend_schema(
        request=SectorInfoSerializer,
        responses=SectorInfoSerializer
    )
    def get(self, request, number):
        try:
            sector_obj = Sector.objects.get(number=number)
            serializer = SectorInfoSerializer(instance=sector_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response("There is no sector under this id!", status=status.HTTP_400_BAD_REQUEST)


class MahallaInfo(RetrieveAPIView):
    queryset = Mahalla.objects.all()
    serializer_class = MahallaInfoSerializer


class MahallaRaisInfo(APIView):
    @extend_schema(
        request=RaisInfoSerializer,
        responses=RaisInfoSerializer
    )
    def get(self, request, pk):
        try:
            mahalla_object = Mahalla.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(
                data={
                    "error": f"Mahalla object does not exist under id {pk}"
                },
                status=status.HTTP_404_NOT_FOUND
            )
        if hasattr(mahalla_object, "rais"):
            rais_object = mahalla_object.rais
            serializer = RaisInfoSerializer(instance=rais_object)
            return Response(
                data=serializer.data, 
                status=status.HTTP_200_OK
            )
        return Response(
            data={
                "error":f"Mahalla object (id:{pk}) does not have rais object"
            },
            status=status.HTTP_404_NOT_FOUND
        )        


class PopulationList(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class MahallaPopulationList(ListAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @extend_schema(request=MahallaIdSerializer)
    def get(self, request, pk, *args, **kwargs):     
        try:
            Mahalla.objects.get(pk=pk)
        except:
            return Response("There is no mahalla under this id!", status=status.HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(household__mahalla__pk=pk)
        return super().get(request, *args, **kwargs)


class XonadonList(ListAPIView):
    queryset = Xonadon.objects.all()
    serializer_class = XonadonSerializer


class MahallaXonadonList(ListAPIView):
    queryset = Xonadon.objects.all()
    serializer_class = XonadonSerializer

    @extend_schema(request=MahallaIdSerializer)
    def get(self, request, pk, *args, **kwargs):     
        try:
            Mahalla.objects.get(pk=pk)
        except:
            return Response("There is no mahalla under this id!", status=status.HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(mahalla__pk=pk)
        return super().get(request, *args, **kwargs)
    

class ProblemFreeXonadonList(ListAPIView):
    queryset = Xonadon.objects.all()
    serializer_class = DetailedXonadonSerializer

    @extend_schema(request=MahallaIdSerializer)
    def get(self, request, pk, *args, **kwargs):     
        try:
            Mahalla.objects.get(pk=pk)
        except:
            return Response("There is no mahalla under this id!", status=status.HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.annotate(num_b=Count('organish')).filter(num_b=0, mahalla__pk=pk)
        return super().get(request, *args, **kwargs)
    

class InspectedXonadonList(ListAPIView):
    queryset = Xonadon.objects.all()
    serializer_class = DetailedXonadonSerializer

    @extend_schema(request=MahallaIdSerializer)
    def get(self, request, pk, *args, **kwargs):     
        try:
            Mahalla.objects.get(pk=pk)
        except:
            return Response("There is no mahalla under this id!", status=status.HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(mahalla__pk=pk)
        self.queryset = self.queryset.annotate(num_b=Count('organish')).filter(~Q(num_b=0))

        return super().get(request, *args, **kwargs)


class InspectedCleanXonadonList(ListAPIView):
    queryset = Xonadon.objects.all()
    serializer_class = DetailedXonadonSerializer

    @extend_schema(request=MahallaIdSerializer)
    def get(self, request, pk, *args, **kwargs):     
        try:
            Mahalla.objects.get(pk=pk)
        except:
            return Response("There is no mahalla under this id!", status=status.HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(
                mahalla__pk=pk
            ).filter(
                organish__hal_qilish_holati='Yakunlangan'
            ).distinct()
        return super().get(request, *args, **kwargs)
    

class InspectedWithProblemXonadonList(ListAPIView):
    queryset = Xonadon.objects.all()
    serializer_class = DetailedXonadonSerializer

    @extend_schema(request=MahallaIdSerializer)
    def get(self, request, pk, *args, **kwargs):     
        try:
            Mahalla.objects.get(pk=pk)
        except:
            return Response("There is no mahalla under this id!", status=status.HTTP_400_BAD_REQUEST)
        self.queryset = self.queryset.filter(
                mahalla__pk=pk
            ).filter(
                organish__hal_qilish_holati='Davom etayapti'
            ).distinct()
        return super().get(request, *args, **kwargs)
from django.urls import path
from .views import (
    SectorInfo, 
    MainStatsAPI, 
    ProblemsStatsAPI, 
    MahallaInfo, 
    XonadonList,
    MahallaXonadonList,
    PopulationList,
    MahallaPopulationList,
    MahallaRaisInfo,
    ProblemFreeXonadonList,
    InspectedXonadonList,
    InspectedCleanXonadonList,
    InspectedWithProblemXonadonList
)


urlpatterns = [
    path('api/v1/main/sector/<number>', SectorInfo.as_view(), name='sector-info'),
    path('api/v1/main/main-stats', MainStatsAPI.as_view(), name='main-stats'),
    path('api/v1/main/problem-stats', ProblemsStatsAPI.as_view(), name='problem-stats'),
    path('api/v1/main/problem-stats-mahalla/<mahalla_pk>', ProblemsStatsAPI.as_view(), name="problem-stats-mahalla"),
    path('api/v1/main/mahalla/<int:pk>', MahallaInfo.as_view(), name='mahalla-info'),
    path('api/v1/main/mahalla-rais/<int:pk>', MahallaRaisInfo.as_view(), name='mahalla-info'),
    path('api/v1/main/population-list/', PopulationList.as_view(), name='population-list'),
    path('api/v1/main/population-list/mahalla/<int:pk>', MahallaPopulationList.as_view(), name='population-mahalla-list'),
    path('api/v1/main/xonadon-list/', XonadonList.as_view(), name='xonadon-list'),
    path('api/v1/main/xonadon-list/mahalla/<int:pk>', MahallaXonadonList.as_view(), name='xonadon-mahalla-list'),
    path('api/v1/main/problem-free-xonadon-list/mahalla/<int:pk>', ProblemFreeXonadonList.as_view()),
    path('api/v1/main/all-inspected-xonadon-list/mahalla/<int:pk>', InspectedXonadonList.as_view()),
    path('api/v1/main/clean-inspected-xonadon-list/mahalla/<int:pk>', InspectedCleanXonadonList.as_view()),
    path('api/v1/main/inspected-with-problem-xonadon-list/mahalla/<int:pk>', InspectedWithProblemXonadonList.as_view()),

]

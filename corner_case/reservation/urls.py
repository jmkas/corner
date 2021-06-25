from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "reservation"
urlpatterns = [
    path('rooms/', views.RoomView.as_view(), name='rooms_view'),
    path('', views.ReservationListView.as_view(), name='reservation_list_view'),
    path('<int:pk>', views.ReservationDetailView.as_view(), name='reservation_detail_view'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

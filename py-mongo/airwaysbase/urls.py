from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^airplanes/$', views.airplanes_list, name="airplanes_list"),
    url(r'^flights/$', views.flights_list, name="flights_list"),
    url(r'^airports/$', views.airports_list, name="airports_list"),
    url(r'^flights/new/?$', views.create_flight, name="create_flight"),
    url(r'^flights/(?P<flight_id>.*)/update/?$', views.update_flight, name="update_flight"),
    url(r'^flights/(?P<flight_id>.*)/delete/?$', views.delete_flight, name="delete_flight"),
    url(r'^flights/(?P<flight_id>.*)', views.view_flight, name="view_flight"),
]

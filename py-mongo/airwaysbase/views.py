from datetime import datetime
from pymongo.database import DBRef
from django.core.urlresolvers import reverse
from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import NewFlightForm, SearchForm
from .db_manager import DB
from .custom_models import *

# Create your views here.

db = DB()


def index(request):
    stats = {
        'flights_from_airport': Stat.flights_from_airport(),
        'flights_to_airport': Stat.flights_to_airport(),
        'flights_per_aircraft': Stat.flights_per_aircraft(),
        'most_cancellation_airports': Stat.most_cancellation_airports()
    }
    flights = Flight.get_list(10)

    return render(request, 'airwaysbase/index.html', {
        'response': {
            'stats': stats,
            'flights_list_limited': flights
        }
    })


def flights_list(request):
    return render(request, 'airwaysbase/flight/list.html', {
        'response': {
            'flights': Flight.get_list()
        }
    })


def view_flight(request, flight_id):
    flight_data = Flight\
        .get_by_id(flight_id)\
        .to_dict()

    return render(request, 'airwaysbase/flight/details.html', {
        'response': {
            'data': flight_data
        }
    })


def create_flight(request):
    if request.method == 'GET':
        form = NewFlightForm()
        return render(request, 'airwaysbase/flight/create.html', {
            'form': form
        })

    if request.method == 'POST':
        form = NewFlightForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_flight = Flight(data, from_form=True)
            new_flight.save()
            return HttpResponseRedirect('/')


def delete_flight(request, flight_id):
    Flight.delete_by_id(flight_id)
    return HttpResponseRedirect('/')


def update_flight(request, flight_id):
    flight = Flight.get_by_id(flight_id)
    errors = None
    if request.method == 'POST':
        form = NewFlightForm(request.POST)
        if form.is_valid():
            updated_data = form.cleaned_data
            flight.update(updated_data)
            redirect_url = reverse('view_flight', kwargs={'flight_id': flight.id})
            return redirect(redirect_url)
        else:
            errors = 'Please, fill form fields correctly!'

    return render(request, 'airwaysbase/flight/update.html', {
        'airports': Airport.get_list(),
        'airplanes': Aircraft.get_list(),
        'form': NewFlightForm(flight.to_form_data()),
        'errors': errors
    })


def airplanes_list(request):
    return render(request, 'airwaysbase/airplane/list.html', {'response': {
        'airplanes_list': Aircraft.get_list()
    }})


def airports_list(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return render(request, 'airwaysbase/airport/list.html', {'response': {
                'airports_list': Airport.search(data['search']),
                'form': form
            }})
    form = SearchForm()
    return render(request, 'airwaysbase/airport/list.html', {'response': {
        'airports_list': Airport.get_list(),
        'form': form
    }})
# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import holidays


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()

        # Check if it's a public holiday
        is_holiday = isPublicHoliday(datetime.strptime(data['reservation_date'], '%Y-%m-%d').date())

        if exist == False and not is_holiday:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
            return HttpResponse("{'success': 'Reservation made successfully'}", content_type='application/json')
        elif is_holiday:
            return HttpResponse("{'error': 'Selected date is a public holiday'}", content_type='application/json')
        else:
            return HttpResponse("{'error': 'Slot already booked'}", content_type='application/json')

    date = request.GET.get('date', datetime.today().date())

    # Check if the selected date is a public holiday
    is_selected_date_holiday = isPublicHoliday(datetime.strptime(date, '%Y-%m-%d').date())
    if is_selected_date_holiday:
        return HttpResponse("{'error': 'Selected date is a public holiday'}", content_type='application/json')

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')

def isPublicHoliday(selectedDate):
    US_holidays = holidays.UnitedStates(years=selectedDate.year)
    # nigeria_holidays = holidays.Nigeria(years=selectedDate.year)

    if selectedDate in US_holidays:
        holiday_name = US_holidays.get(selectedDate)
        print(f"{selectedDate} is a public holiday ({holiday_name})")
        return True
    else:
        print(f"{selectedDate} is not a public holiday")
        return False
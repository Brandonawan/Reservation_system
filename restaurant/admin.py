from django.contrib import admin

# Register your models here.
from .models import Menu
from .models import Booking


@admin.register(Menu)
class Menu(admin.ModelAdmin):
    list_display = ('name', 'price', 'menu_item_description')
@admin.register(Booking)
class Booking(admin.ModelAdmin):
    list_display = ('first_name', 'reservation_date', 'reservation_slot')
from django.contrib import admin
from .models import CarMake, CarModel


class CarModelInline(admin.StackedInline):
    model = CarModel
    fields = ('name', 'dealer_id','car_type','year')
    extra = 1

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'dealer_id','car_type','year')

class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'description')

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

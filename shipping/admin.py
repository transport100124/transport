from django.contrib import admin

from .models import Manufacturer, Kind, Replica, Driver, Automobile, Waybill, Application, Movement, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Manufacturer)
admin.site.register(Kind)
admin.site.register(Replica)
admin.site.register(Driver)
admin.site.register(Automobile)
admin.site.register(Waybill)
admin.site.register(Application)
admin.site.register(Movement)
admin.site.register(News)

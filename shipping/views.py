from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Manufacturer, Kind, Replica, Driver, Automobile, Waybill, Application, Movement, News
# Подключение форм
from .forms import ManufacturerForm, KindForm, ReplicaForm, DriverForm, AutomobileForm, WaybillForm, ApplicationForm, MovementForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        return render(request, "index.html")            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def manufacturer_index(request):
    try:
        manufacturer = Manufacturer.objects.all().order_by('title')
        return render(request, "manufacturer/index.html", {"manufacturer": manufacturer,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def manufacturer_create(request):
    try:
        if request.method == "POST":
            manufacturer = Manufacturer()
            manufacturer.title = request.POST.get("title")
            manufacturerform = ManufacturerForm(request.POST)
            if manufacturerform.is_valid():
                manufacturer.save()
                return HttpResponseRedirect(reverse('manufacturer_index'))
            else:
                return render(request, "manufacturer/create.html", {"form": manufacturerform})
        else:        
            manufacturerform = ManufacturerForm()
            return render(request, "manufacturer/create.html", {"form": manufacturerform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def manufacturer_edit(request, id):
    try:
        manufacturer = Manufacturer.objects.get(id=id)
        if request.method == "POST":
            manufacturer.title = request.POST.get("title")
            manufacturerform = ManufacturerForm(request.POST)
            if manufacturerform.is_valid():
                manufacturer.save()
                return HttpResponseRedirect(reverse('manufacturer_index'))
            else:
                return render(request, "manufacturer/edit.html", {"form": manufacturerform})
        else:
            # Загрузка начальных данных
            manufacturerform = ManufacturerForm(initial={'title': manufacturer.title, })
            return render(request, "manufacturer/edit.html", {"form": manufacturerform})
    except Manufacturer.DoesNotExist:
        return HttpResponseNotFound("<h2>Manufacturer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def manufacturer_delete(request, id):
    try:
        manufacturer = Manufacturer.objects.get(id=id)
        manufacturer.delete()
        return HttpResponseRedirect(reverse('manufacturer_index'))
    except Manufacturer.DoesNotExist:
        return HttpResponseNotFound("<h2>Manufacturer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def manufacturer_read(request, id):
    try:
        manufacturer = Manufacturer.objects.get(id=id) 
        return render(request, "manufacturer/read.html", {"manufacturer": manufacturer})
    except Manufacturer.DoesNotExist:
        return HttpResponseNotFound("<h2>Manufacturer not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def kind_index(request):
    try:
        kind = Kind.objects.all().order_by('title')
        return render(request, "kind/index.html", {"kind": kind,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def kind_create(request):
    try:
        if request.method == "POST":
            kind = Kind()
            kind.title = request.POST.get("title")
            kindform = KindForm(request.POST)
            if kindform.is_valid():
                kind.save()
                return HttpResponseRedirect(reverse('kind_index'))
            else:
                return render(request, "kind/create.html", {"form": kindform})
        else:        
            kindform = KindForm()
            return render(request, "kind/create.html", {"form": kindform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def kind_edit(request, id):
    try:
        kind = Kind.objects.get(id=id)
        if request.method == "POST":
            kind.title = request.POST.get("title")
            kindform = KindForm(request.POST)
            if kindform.is_valid():
                kind.save()
                return HttpResponseRedirect(reverse('kind_index'))
            else:
                return render(request, "kind/edit.html", {"form": kindform})
        else:
            # Загрузка начальных данных
            kindform = KindForm(initial={'title': kind.title, })
            return render(request, "kind/edit.html", {"form": kindform})
    except Kind.DoesNotExist:
        return HttpResponseNotFound("<h2>Kind not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def kind_delete(request, id):
    try:
        kind = Kind.objects.get(id=id)
        kind.delete()
        return HttpResponseRedirect(reverse('kind_index'))
    except Kind.DoesNotExist:
        return HttpResponseNotFound("<h2>Kind not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def kind_read(request, id):
    try:
        kind = Kind.objects.get(id=id) 
        return render(request, "kind/read.html", {"kind": kind})
    except Kind.DoesNotExist:
        return HttpResponseNotFound("<h2>Kind not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def replica_index(request):
    try:
        replica = Replica.objects.all().order_by('title')
        return render(request, "replica/index.html", {"replica": replica,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def replica_create(request):
    try:
        if request.method == "POST":
            replica = Replica()
            replica.manufacturer = Manufacturer.objects.filter(id=request.POST.get("manufacturer")).first()
            replica.kind = Kind.objects.filter(id=request.POST.get("kind")).first()
            replica.title = request.POST.get("title")
            replica.capacity = request.POST.get("capacity")
            replicaform = ReplicaForm(request.POST)
            if replicaform.is_valid():
                replica.save()
                return HttpResponseRedirect(reverse('replica_index'))
            else:
                return render(request, "replica/create.html", {"form": replicaform})
        else:        
            replicaform = ReplicaForm()
            return render(request, "replica/create.html", {"form": replicaform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def replica_edit(request, id):
    try:
        replica = Replica.objects.get(id=id)
        if request.method == "POST":
            replica.manufacturer = Manufacturer.objects.filter(id=request.POST.get("manufacturer")).first()
            replica.kind = Kind.objects.filter(id=request.POST.get("kind")).first()
            replica.title = request.POST.get("title")
            replica.capacity = request.POST.get("capacity")
            replicaform = ReplicaForm(request.POST)
            if replicaform.is_valid():
                replica.save()
                return HttpResponseRedirect(reverse('replica_index'))
            else:
                return render(request, "replica/edit.html", {"form": replicaform})
        else:
            # Загрузка начальных данных
            replicaform = ReplicaForm(initial={'manufacturer': replica.manufacturer, 'kind': replica.kind, 'title': replica.title, 'capacity': replica.capacity, })
            return render(request, "replica/edit.html", {"form": replicaform})
    except Replica.DoesNotExist:
        return HttpResponseNotFound("<h2>Replica not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def replica_delete(request, id):
    try:
        replica = Replica.objects.get(id=id)
        replica.delete()
        return HttpResponseRedirect(reverse('replica_index'))
    except Replica.DoesNotExist:
        return HttpResponseNotFound("<h2>Replica not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def replica_read(request, id):
    try:
        replica = Replica.objects.get(id=id) 
        return render(request, "replica/read.html", {"replica": replica})
    except Replica.DoesNotExist:
        return HttpResponseNotFound("<h2>Replica not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def driver_index(request):
    try:
        driver = Driver.objects.all().order_by('full_name')
        return render(request, "driver/index.html", {"driver": driver,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def driver_create(request):
    try:
        if request.method == "POST":
            driver = Driver()
            driver.full_name = request.POST.get("full_name")
            driver.birthday = request.POST.get("birthday")
            driver.phone = request.POST.get("phone")
            driver.category = request.POST.get("category")
            driverform = DriverForm(request.POST)
            if driverform.is_valid():
                driver.save()
                return HttpResponseRedirect(reverse('driver_index'))
            else:
                return render(request, "driver/create.html", {"form": driverform})
        else:        
            driverform = DriverForm(initial={ 'birthday': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "driver/create.html", {"form": driverform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def driver_edit(request, id):
    try:
        driver = Driver.objects.get(id=id)
        if request.method == "POST":
            driver.full_name = request.POST.get("full_name")
            driver.birthday = request.POST.get("birthday")
            driver.phone = request.POST.get("phone")
            driver.category = request.POST.get("category")
            driverform = DriverForm(request.POST)
            if driverform.is_valid():
                driver.save()
                return HttpResponseRedirect(reverse('driver_index'))
            else:
                return render(request, "driver/edit.html", {"form": driverform})
        else:
            # Загрузка начальных данных
            driverform = DriverForm(initial={'full_name': driver.full_name, 'birthday': driver.birthday.strftime('%Y-%m-%d'), 'phone': driver.phone, 'category': driver.category, })
            return render(request, "driver/edit.html", {"form": driverform})
    except Driver.DoesNotExist:
        return HttpResponseNotFound("<h2>Driver not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def driver_delete(request, id):
    try:
        driver = Driver.objects.get(id=id)
        driver.delete()
        return HttpResponseRedirect(reverse('driver_index'))
    except Driver.DoesNotExist:
        return HttpResponseNotFound("<h2>Driver not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def driver_read(request, id):
    try:
        driver = Driver.objects.get(id=id) 
        return render(request, "driver/read.html", {"driver": driver})
    except Driver.DoesNotExist:
        return HttpResponseNotFound("<h2>Driver not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def automobile_index(request):
    try:
        automobile = Automobile.objects.all().order_by('reg_number')
        return render(request, "automobile/index.html", {"automobile": automobile,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def automobile_create(request):
    try:
        if request.method == "POST":
            automobile = Automobile()
            automobile.replica = Replica.objects.filter(id=request.POST.get("replica")).first()
            automobile.yr = request.POST.get("yr")
            automobile.reg_number = request.POST.get("reg_number")
            automobile.driver = Driver.objects.filter(id=request.POST.get("driver")).first()
            automobileform = AutomobileForm(request.POST)
            if automobileform.is_valid():
                automobile.save()
                return HttpResponseRedirect(reverse('automobile_index'))
            else:
                return render(request, "automobile/create.html", {"form": automobileform})
        else:        
            automobileform = AutomobileForm(initial={'yr': datetime.now().year, })
            return render(request, "automobile/create.html", {"form": automobileform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def automobile_edit(request, id):
    try:
        automobile = Automobile.objects.get(id=id)
        if request.method == "POST":
            automobile.replica = Replica.objects.filter(id=request.POST.get("replica")).first()
            automobile.yr = request.POST.get("yr")
            automobile.reg_number = request.POST.get("reg_number")
            automobile.driver = Driver.objects.filter(id=request.POST.get("driver")).first()
            automobileform = AutomobileForm(request.POST)
            if automobileform.is_valid():
                automobile.save()
                return HttpResponseRedirect(reverse('automobile_index'))
            else:
                return render(request, "automobile/edit.html", {"form": automobileform})
        else:
            # Загрузка начальных данных
            automobileform = AutomobileForm(initial={'replica': automobile.replica, 'yr': automobile.yr, 'reg_number': automobile.reg_number, 'driver': automobile.driver, })
            return render(request, "automobile/edit.html", {"form": automobileform})
    except Automobile.DoesNotExist:
        return HttpResponseNotFound("<h2>Automobile not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def automobile_delete(request, id):
    try:
        automobile = Automobile.objects.get(id=id)
        automobile.delete()
        return HttpResponseRedirect(reverse('automobile_index'))
    except Automobile.DoesNotExist:
        return HttpResponseNotFound("<h2>Automobile not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def automobile_read(request, id):
    try:
        automobile = Automobile.objects.get(id=id) 
        return render(request, "automobile/read.html", {"automobile": automobile})
    except Automobile.DoesNotExist:
        return HttpResponseNotFound("<h2>Automobile not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def waybill_index(request):
    try:
        waybill = Waybill.objects.all().order_by('datew', 'numb')
        return render(request, "waybill/index.html", {"waybill": waybill,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def waybill_create(request):
    try:
        if request.method == "POST":
            waybill = Waybill()
            waybill.datew = request.POST.get("datew")
            waybill.numb = request.POST.get("numb")
            waybill.automobile = Automobile.objects.filter(id=request.POST.get("automobile")).first()
            waybill.start = request.POST.get("start")
            waybill.finish = request.POST.get("finish")
            waybill.whence = request.POST.get("whence")
            waybill.where = request.POST.get("where")
            waybill.details = request.POST.get("details")
            waybillform = WaybillForm(request.POST)
            if waybillform.is_valid():
                waybill.save()
                return HttpResponseRedirect(reverse('waybill_index'))
            else:
                return render(request, "waybill/create.html", {"form": waybillform})
        else:        
            waybillform = WaybillForm(initial={'datew': datetime.now().strftime('%Y-%m-%d'), 'start': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'finish': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "waybill/create.html", {"form": waybillform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def waybill_edit(request, id):
    try:
        waybill = Waybill.objects.get(id=id)
        if request.method == "POST":
            waybill.datew = request.POST.get("datew")
            waybill.numb = request.POST.get("numb")
            waybill.automobile = Automobile.objects.filter(id=request.POST.get("automobile")).first()
            waybill.start = request.POST.get("start")
            waybill.finish = request.POST.get("finish")
            waybill.whence = request.POST.get("whence")
            waybill.where = request.POST.get("where")
            waybill.details = request.POST.get("details")
            waybillform = WaybillForm(request.POST)
            if waybillform.is_valid():
                waybill.save()
                return HttpResponseRedirect(reverse('waybill_index'))
            else:
                return render(request, "waybill/edit.html", {"form": waybillform})
        else:
            # Загрузка начальных данных
            waybillform = WaybillForm(initial={'datew': waybill.datew.strftime('%Y-%m-%d'), 'numb': waybill.numb, 'automobile': waybill.automobile, 'start': waybill.start.strftime('%Y-%m-%d %H:%M:%S'), 'finish': waybill.finish.strftime('%Y-%m-%d %H:%M:%S'), 'whence': waybill.whence, 'where': waybill.where, 'details': waybill.details, })
            return render(request, "waybill/edit.html", {"form": waybillform})
    except Waybill.DoesNotExist:
        return HttpResponseNotFound("<h2>Waybill not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def waybill_delete(request, id):
    try:
        waybill = Waybill.objects.get(id=id)
        waybill.delete()
        return HttpResponseRedirect(reverse('waybill_index'))
    except Waybill.DoesNotExist:
        return HttpResponseNotFound("<h2>Waybill not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def waybill_read(request, id):
    try:
        waybill = Waybill.objects.get(id=id) 
        return render(request, "waybill/read.html", {"waybill": waybill})
    except Waybill.DoesNotExist:
        return HttpResponseNotFound("<h2>Waybill not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def application_index(request):
    try:
        application = Application.objects.all().order_by('datea')
        return render(request, "application/index.html", {"application": application})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список 
@login_required
def application_list(request):
    try:
        #print(request.user.id)
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        application = Application.objects.filter(user_id=request.user.id).order_by('-datea')
        return render(request, "application/list.html", {"application": application, 'first_name': first_name, 'last_name': last_name, 'email': email})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
#@group_required("Managers")
def application_create(request):
    try:
        if request.method == "POST":
            application = Application()
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            application.user_id = request.user.id
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_list'))
            else:
                return render(request, "application/create.html", {"form": applicationform})
        else:        
            applicationform = ApplicationForm()
            return render(request, "application/create.html", {"form": applicationform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def application_edit(request, id):
    try:
        application = Application.objects.get(id=id) 
        if request.method == "POST":
            application.title = request.POST.get("title")
            application.details = request.POST.get("details")
            applicationform = ApplicationForm(request.POST)
            if applicationform.is_valid():
                application.save()
                return HttpResponseRedirect(reverse('application_index'))
            else:
                return render(request, "application/edit.html", {"form": applicationform})
        else:
            # Загрузка начальных данных
            applicationform = ApplicationForm(initial={'title': application.title, 'details': application.details, })
            return render(request, "application/edit.html", {"form": applicationform})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def application_delete(request, id):
    try:
        application = Application.objects.get(id=id)
        application.delete()
        return HttpResponseRedirect(reverse('application_index'))
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def application_read(request, id):
    try:
        application = Application.objects.get(id=id)
        movement = Movement.objects.filter(application_id=id).order_by('-datem')
        return render(request, "application/read.html", {"application": application, "movement": movement})
    except Application.DoesNotExist:
        return HttpResponseNotFound("<h2>Application not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def movement_index(request, application_id):
    try:
        movement = Movement.objects.filter(application_id=application_id).order_by('-datem')
        app = Application.objects.get(id=application_id)
        #movement = Movement.objects.all().order_by('-orders', '-datem')
        return render(request, "movement/index.html", {"movement": movement, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def movement_create(request, application_id):
    try:
        app = Application.objects.get(id=application_id)
        if request.method == "POST":
            movement = Movement()
            movement.application_id = application_id
            movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/create.html", {"form": movementform})
        else:
            movementform = MovementForm(initial={ 'datem': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "movement/create.html", {"form": movementform, "application_id": application_id, "app": app})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def movement_edit(request, id, application_id):
    app = Application.objects.get(id=application_id)
    try:
        movement = Movement.objects.get(id=id) 
        if request.method == "POST":
            #movement.datem = datetime.now()
            movement.status = request.POST.get("status")
            movement.details = request.POST.get("details")
            movementform = MovementForm(request.POST)
            if movementform.is_valid():
                movement.save()
                return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
            else:
                return render(request, "application/edit.html", {"form": movementform})
        else:
            # Загрузка начальных данных
            movementform = MovementForm(initial={'application': movement.application, 'datem': movement.datem.strftime('%Y-%m-%d'), 'status': movement.status, 'details': movement.details,  })
            return render(request, "movement/edit.html", {"form": movementform, "application_id": application_id, "app": app})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def movement_delete(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id)
        movement.delete()
        return HttpResponseRedirect(reverse('movement_index', args=(application_id,)))
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
def movement_read(request, id, application_id):
    try:
        movement = Movement.objects.get(id=id) 
        return render(request, "movement/read.html", {"movement": movement, "application_id": application_id})
    except Movement.DoesNotExist:
        return HttpResponseNotFound("<h2>Movement not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                news_search = request.POST.get("news_search")
                #print(news_search)                
                if news_search != '':
                    news = news.filter(Q(title__contains = news_search) | Q(details__contains = news_search)).all()                
                return render(request, "news/list.html", {"news": news, "news_search": news_search, })    
            else:          
                return render(request, "news/list.html", {"news": news})                 
        else:
            return render(request, "news/list.html", {"news": news}) 
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']   
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################    

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user
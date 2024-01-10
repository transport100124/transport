from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput
from .models import Manufacturer, Kind, Replica, Driver, Automobile, Waybill, Application, Movement, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Производитель автомобиля 
class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('manufacturer_title'),            
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Тип автомобиля 
class KindForm(forms.ModelForm):
    class Meta:
        model = Kind
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('kind_title'),            
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Модель автомобиля 
class ReplicaForm(forms.ModelForm):
    class Meta:
        model = Replica
        fields = ['manufacturer', 'kind', 'title', 'capacity',]
        widgets = {
            'manufacturer': forms.Select(attrs={'class': 'chosen'}),
            'kind': forms.Select(attrs={'class': 'chosen'}),
            'title': TextInput(attrs={"size":"100"}),            
            'capacity': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'manufacturer': _('manufacturer_title'),            
            'kind': _('kind_title'),            
        }
    ## Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Водитель 
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['full_name', 'birthday', 'phone', 'category',]
        widgets = {
            'full_name': TextInput(attrs={"size":"100"}),
            'birthday': DateInput(attrs={"type":"date"}),
            'phone': TextInput(attrs={"size":"60", "type":"tel", "pattern": "+7-[0-9]{3}-[0-9]{3}-[0-9]{4}"}),
            'category': TextInput(attrs={"size":"80"}),
        }
    # Метод-валидатор для поля birthday
    def clean_birthday(self):        
        if isinstance(self.cleaned_data['birthday'], datetime.date) == True:
            data = self.cleaned_data['birthday']
            # Проверка даты рождения не моложе 18 лет
            if data > timezone.now() - relativedelta(years=18):
                raise forms.ValidationError(_('Minimum age 18 years old'))
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Автомобиль 
class AutomobileForm(forms.ModelForm):
    class Meta:
        model = Automobile
        fields = ['replica', 'yr', 'reg_number', 'driver',]
        widgets = {
            'replica': forms.Select(attrs={'class': 'chosen'}),
            'yr': NumberInput(attrs={"size":"10", "min": "1900", "max": "2030", "step": "1"}),            
            'reg_number': TextInput(attrs={"size":"50"}),            
            'driver': forms.Select(attrs={'class': 'chosen'}),           
        }
        labels = {
            'replica': _('replica'),            
            'driver': _('driver'),            
        }

# Путевой лист 
class WaybillForm(forms.ModelForm):
    class Meta:
        model = Waybill
        fields = ['datew', 'numb', 'automobile', 'start', 'finish', 'whence', 'where', 'details',]
        widgets = {
            'datew': DateTimeInput(format='%d/%m/%Y'),
            'numb': NumberInput(attrs={"size":"10", "min": "1", "max": "10000", "step": "1"}),   
            'automobile': forms.Select(attrs={'class': 'chosen'}),
            'start': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'finish': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'whence': TextInput(attrs={"size":"100"}),            
            'where': TextInput(attrs={"size":"100"}),            
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),          
        }
        labels = {
            'automobile': _('automobile'),            
        }
    # Метод-валидатор для поля datew
    def clean_datew(self):        
        if isinstance(self.cleaned_data['datew'], datetime.date) == True:
            data = self.cleaned_data['datew']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data  
    # Метод-валидатор для поля start
    def clean_start(self):        
        if isinstance(self.cleaned_data['start'], datetime.date) == True:
            data = self.cleaned_data['start']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data  
    # Метод-валидатор для поля finish
    def clean_finish(self):        
        if isinstance(self.cleaned_data['finish'], datetime.date) == True:
            data = self.cleaned_data['finish']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data  

# Заявки
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('title', 'details')
        widgets = {
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),            
        }        

# Движение заявки
class MovementForm(forms.ModelForm):
    class Meta:
        model = Movement
        fields = ('datem', 'status', 'details')
        widgets = {
            'datem': DateInput(attrs={"type":"date", "readonly":"readonly"}),
            'status': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),
        }

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime.date) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

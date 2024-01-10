from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.

# Производитель автомобиля
class  Manufacturer(models.Model):
    title = models.CharField(_('manufacturer_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'manufacturer'
    def __str__(self):
        # Вывод в тег Select 
        return "{}".format(self.title)

# Тип кузова автомобиля
class  Kind(models.Model):
    title = models.CharField(_('kind_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'kind'
    def __str__(self):
        # Вывод в тег Select
        return "{}".format(self.title)

# Модель автомобиля
class  Replica(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, related_name='replica_manufacturer', on_delete=models.CASCADE)
    kind = models.ForeignKey(Kind, related_name='replica_kind', on_delete=models.CASCADE)
    title = models.CharField(_('replica_title'), max_length=128, unique=True)
    capacity = models.CharField(_('capacity'), max_length=128)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'replica'
    def __str__(self):
        # Вывод в тег Select
        #return "{} {} {}".format(self.manufacturer, self.kind, self.title)
        return "{}".format(self.title)

# Водитель 
class Driver(models.Model):
    full_name = models.CharField(_('full_name'), max_length=128)
    birthday = models.DateTimeField(_('birthday'))
    phone = models.CharField(_('phone'), max_length=64)
    category = models.CharField(_('category'), max_length=128)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'driver'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['full_name']),
        ]
        # Сортировка по умолчанию
        ordering = ['full_name']
    def __str__(self):
        # Вывод в тег Select 
        return "{}".format(self.full_name)

# Автомобиль
class  Automobile(models.Model):
    replica = models.ForeignKey(Replica, related_name='automobile_replica', on_delete=models.CASCADE)
    yr = models.IntegerField(_('yr'))  
    reg_number = models.CharField(_('reg_number'), max_length=64, unique=True)
    driver = models.ForeignKey(Driver, related_name='automobile_driver', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'automobile'
    def __str__(self):
        # Вывод в тег Select 
        return "{} {}".format(self.replica, self.reg_number)

# Путевой лист 
class Waybill(models.Model):
    datew = models.DateTimeField(_('datew'))
    numb = models.IntegerField(_('numb'))     
    automobile = models.ForeignKey(Automobile, related_name='waybill_automobile', on_delete=models.CASCADE)
    start = models.DateTimeField(_('start'))
    finish = models.DateTimeField(_('finish'))
    whence = models.CharField(_('whence'), max_length=255)
    where = models.CharField(_('where'), max_length=255)
    details = models.TextField(_('waybill_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'waybill'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datew']),
        ]
        # Сортировка по умолчанию
        ordering = ['datew']
    def __str__(self):
        # Вывод в тег Select 
        return "{} {}".format(self.datew.strftime('%d.%m.%Y'), self.numb)

## Водители к путевому листу
#class  WaybillDriver(models.Model):
#    waybill = models.ForeignKey(Waybill, related_name='waybil_driver_waybill', on_delete=models.CASCADE)
#    driver = models.ForeignKey(Driver, related_name='waybil_driver_driver', on_delete=models.CASCADE)
#    class Meta:
#        # Параметры модели
#        # Переопределение имени таблицы
#        db_table = 'waybil_driver'
#    def __str__(self):
#        # Вывод в тег Select 
#        return "{} {}".format(self.waybill, self.driver)

# Заявка клиента
class Application(models.Model):
    datea = models.DateTimeField(_('datea'), auto_now_add=True)
    user = models.ForeignKey(User, related_name='application_user', on_delete=models.CASCADE)
    title = models.CharField(_('application_title'), max_length=255)
    details = models.TextField(_('application_details'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'application'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['datea']),
            models.Index(fields=['user']),
        ]
        # Сортировка по умолчанию
        ordering = ['datea']
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datea.strftime('%d.%m.%Y'), self.user, self.title)

# Рассмотрение заявки клиента
class Movement(models.Model):
    application = models.ForeignKey(Application, related_name='movement_application', on_delete=models.CASCADE)
    datem = models.DateTimeField(_('datem'))
    status = models.CharField(_('movement_status'), max_length=128)
    details = models.TextField(_('movement_details'), blank=True, null=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'movement'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['application']),
            models.Index(fields=['datem']),
        ]
        # Сортировка по умолчанию
        ordering = ['datem']        
    def __str__(self):
        # Вывод в тег Select
        return "{} ({}): {}".format(self.datem.strftime('%d.%m.%Y'), self.application, self.status)

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']

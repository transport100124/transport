"""
URL configuration for transport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings 
from django.conf.urls.static import static 
from django.conf.urls import include

from shipping import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('', views.index),
    path('index/', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    #path('report/index/', views.report_index, name='report_index'),
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    
    path('manufacturer/index/', views.manufacturer_index, name='manufacturer_index'),
    path('manufacturer/create/', views.manufacturer_create, name='manufacturer_create'),
    path('manufacturer/edit/<int:id>/', views.manufacturer_edit, name='manufacturer_edit'),
    path('manufacturer/delete/<int:id>/', views.manufacturer_delete, name='manufacturer_delete'),
    path('manufacturer/read/<int:id>/', views.manufacturer_read, name='manufacturer_read'),

    path('kind/index/', views.kind_index, name='kind_index'),
    path('kind/create/', views.kind_create, name='kind_create'),
    path('kind/edit/<int:id>/', views.kind_edit, name='kind_edit'),
    path('kind/delete/<int:id>/', views.kind_delete, name='kind_delete'),
    path('kind/read/<int:id>/', views.kind_read, name='kind_read'),

    path('replica/index/', views.replica_index, name='replica_index'),
    path('replica/create/', views.replica_create, name='replica_create'),
    path('replica/edit/<int:id>/', views.replica_edit, name='replica_edit'),
    path('replica/delete/<int:id>/', views.replica_delete, name='replica_delete'),
    path('replica/read/<int:id>/', views.replica_read, name='replica_read'),

    path('driver/index/', views.driver_index, name='driver_index'),
    path('driver/create/', views.driver_create, name='driver_create'),
    path('driver/edit/<int:id>/', views.driver_edit, name='driver_edit'),
    path('driver/delete/<int:id>/', views.driver_delete, name='driver_delete'),
    path('driver/read/<int:id>/', views.driver_read, name='driver_read'),
    
    path('automobile/index/', views.automobile_index, name='automobile_index'),
    path('automobile/create/', views.automobile_create, name='automobile_create'),
    path('automobile/edit/<int:id>/', views.automobile_edit, name='automobile_edit'),
    path('automobile/delete/<int:id>/', views.automobile_delete, name='automobile_delete'),
    path('automobile/read/<int:id>/', views.automobile_read, name='automobile_read'),

    path('waybill/index/', views.waybill_index, name='waybill_index'),
    path('waybill/create/', views.waybill_create, name='waybill_create'),
    path('waybill/edit/<int:id>/', views.waybill_edit, name='waybill_edit'),
    path('waybill/delete/<int:id>/', views.waybill_delete, name='waybill_delete'),
    path('waybill/read/<int:id>/', views.waybill_read, name='waybill_read'),

    path('application/index/', views.application_index, name='application_index'),
    path('application/list/', views.application_list, name='application_list'),
    path('application/create/', views.application_create, name='application_create'),
    path('application/edit/<int:id>/', views.application_edit, name='application_edit'),
    path('application/delete/<int:id>/', views.application_delete, name='application_delete'),
    path('application/read/<int:id>/', views.application_read, name='application_read'),

    path('movement/index/<int:application_id>/', views.movement_index, name='movement_index'),
    path('movement/create/<int:application_id>/', views.movement_create, name='movement_create'),
    path('movement/edit/<int:id>/<int:application_id>/', views.movement_edit, name='movement_edit'),
    path('movement/delete/<int:id>/<int:application_id>/', views.movement_delete, name='movement_delete'),
    path('movement/read/<int:id>/<int:application_id>/', views.movement_read, name='movement_read'),

    path('news/index/', views.news_index, name='news_index'),
    path('news/list/', views.news_list, name='news_list'),
    path('news/create/', views.news_create, name='news_create'),
    path('news/edit/<int:id>/', views.news_edit, name='news_edit'),
    path('news/delete/<int:id>/', views.news_delete, name='news_delete'),
    path('news/read/<int:id>/', views.news_read, name='news_read'),

    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('settings/account/', views.UserUpdateView.as_view(), name='my_account'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


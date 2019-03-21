"""SpringCenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, re_path
from django.views.static import serve

from SpringCenter import settings
from app01.views import  admin_login,get_geetest,admin_register,\
    admin_index,admin_today_income,admin_index,admin_userinfor,admin_logout
from stark.service.stark import StarkSite
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #后台路径
    path('stark/', StarkSite.urls),
    #前台路径
    path('admin_index/', admin_index),
    path('admin_userinfor/', admin_userinfor),
    path('admin_login/', admin_login),
    path('admin_logout/', admin_logout),
    path('pc-geetest/register/', get_geetest),
    path('admin_register/', admin_register),
    #应用路径
    path('admin_index/', admin_index),
    path('admin_house/', views.admin_house),
    path('admin_addhouse/', views.admin_addhouse),
    path('admin_delhouse/', views.admin_delhouse),
    path('admin_edithouse/', views.admin_edithouse),
    path('admin_bath/', views.admin_bath),
    path('admin_addbath/', views.admin_addbath),
    path('admin_delbath/', views.admin_delbath),
    path('admin_editbath/', views.admin_editbath),
    path('admin_expensive/', views.admin_expensive),
    path('admin_addexpense/', views.admin_addexpense),
    path('admin_editexpen/', views.admin_editexpen),
    path('admin_delexpen/', views.admin_delexpen),
    path('admin_income/', views.admin_income),
    path('admin_delincome/', views.admin_delincome),
    path('admin_day_income/', views.admin_day_income),
    path('admin_echart_income/', views.admin_echart_income),
    path('admin_store/', views.admin_store),
    path('admin_addstore/', views.admin_addstore),
    path('admin_delstore/', views.admin_delstore),
    path('admin_editstore/', views.admin_editstore),
    path('admin_other/', views.admin_other),
    path('admin_addother/', views.admin_addother),
    path('admin_editother/', views.admin_editother),
    path('admin_delsother/', views.admin_delsother),

    path('admin_today_income/', admin_today_income),
    # media相关的路由设置
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
]


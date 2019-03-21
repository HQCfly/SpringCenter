from stark.service.stark import StarkSite,ModelStark

from .models import *
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.http import JsonResponse

from django.shortcuts import HttpResponse, redirect, render


#用户信息
class UserInforConfig(ModelStark):

    list_display = ["id","username","avatar","email","create_time"]


StarkSite.register(UserInfor,UserInforConfig)

#洗浴相关
class bathAccountConfig(ModelStark):
    list_display= ["id","num_bath","num_brand","num_back","remark_bath","day_bath","price_bath"]
    search_fields = ["num_bath", "num_brand", "price_bath","day_bath"]
    list_filter = ["num_brand", "day_bath"]

StarkSite.register(bathAccount,bathAccountConfig)
# StarkSite.register(Role)


StarkSite.register(coupleAccount)


#住房相关

class cataHouseConfig(ModelStark):

    list_display = ["id","house_name"]


StarkSite.register(cataHouse,cataHouseConfig)

class houseAccountConfig(ModelStark):

    list_display = ["id","name","sex","identity","num_house","day_house","price_house","day_time","remark_house","cata_house"]
    search_fields = ["name", "num_house", "price_house"]
    list_filter = ["num_house","name"]


StarkSite.register(houseAccount,houseAccountConfig)



#电费相关

StarkSite.register(electricityAccount)

#收入相关
class incomeAccountConfig(ModelStark):
    list_display = ["id","day_income","total_bath",
                    "total_house","total_store",
                    "total_bath_house","total_pay","total_income","remark_income"]
    list_display_links = ["id"]

StarkSite.register(incomeAccount,incomeAccountConfig)




#角色相关
class RoleConfig(ModelStark):
    list_display= ["id","title"]
    list_display_links = ["title"]


StarkSite.register(Role,RoleConfig)



#权限相关

class PermissionConfig(ModelStark):
    list_display= ["id","title","url","action","group"]
    list_display_links = ["title"]

StarkSite.register(Permission,PermissionConfig)

class PermissionGroupConfig(ModelStark):
    list_display = ["id","title"]
    list_display_links = ["title"]
StarkSite.register(PermissionGroup,PermissionGroupConfig)










#





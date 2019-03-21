from django.contrib import admin

# Register your models here.
from app01 import models

admin.site.register(models.houseAccount)
admin.site.register(models.bathAccount)
admin.site.register(models.cataHouse)
admin.site.register(models.electricityAccount)
admin.site.register(models.expenseAccount)
admin.site.register(models.incomeAccount)
admin.site.register(models.otherAccount)
admin.site.register(models.storeAccount)
admin.site.register(models.UserInfor)
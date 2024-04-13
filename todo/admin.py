from django.contrib import admin
from .models import Todo,Client,Image,Account

# Register your models here.
admin.site.register(Todo)
admin.site.register(Account)
admin.site.register(Client)
admin.site.register(Image)
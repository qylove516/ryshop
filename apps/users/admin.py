from django.contrib import admin
from users.models import UserProfile


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


admin.site.register(UserProfile, UserAdmin)

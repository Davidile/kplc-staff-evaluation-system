from typing import Any
from django.contrib import admin
from django.contrib import messages
from .models import PerformanceReview,Department,Announcement
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(DefaultUserAdmin):
    list_per_page = 4  # Number of users per page in admin list view

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class PerfornceReviewAdmin(admin.ModelAdmin):
    list_display=('user','review_date','calculate_total_score')
    list_per_page = 2
    list_max_show_all = 2
    def save_model(self,request, obj, form, change):
        if not obj.can_review():
            messages.set_level(request, messages.ERROR)
            messages.error(request,"User has been reviewd in the last 120 days.")
            return
        super().save_model(request,obj,form,change)
# Register your models here.
admin.site.register(PerformanceReview,PerfornceReviewAdmin)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head', 'created_at', 'updated_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'created_by', 'created_at', 'updated_at', 'is_active')
    list_filter = ('department', 'is_active')

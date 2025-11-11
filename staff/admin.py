from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StaffMember

@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "subject_taught", "is_active", "order")
    list_editable = ("is_active", "order")
    search_fields = ("name", "subject_taught")
    list_filter = ("is_active",)

    class Meta:
        model = StaffMember
        verbose_name = "Teacher/Staff"
        verbose_name_plural = "Teachers/Staffs"
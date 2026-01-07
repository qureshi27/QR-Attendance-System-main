from django.contrib import admin

# Register your models here.

from .models import Student, Section, Year, Branch, AttendanceLog


class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'ip_address', 'timestamp', 'session_id')
    list_filter = ('timestamp', 'student__s_branch', 'student__s_year')
    search_fields = ('student__s_roll', 'student__s_fname', 'student__s_lname', 'ip_address')
    readonly_fields = ('timestamp',)


admin.site.register(Student)
admin.site.register(Section)
admin.site.register(Year)
admin.site.register(Branch)
admin.site.register(AttendanceLog, AttendanceLogAdmin)

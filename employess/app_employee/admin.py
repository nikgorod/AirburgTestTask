from django.contrib import admin
from .models import Employee, Department, User


class UserAdmin(admin.ModelAdmin):
    pass


class EmployeesInLine(admin.TabularInline):
    model = Employee
    extra = 1


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'work_date_start', 'department', 'employee_director')
    fields = ('user', 'phone', 'work_date_start', 'position', 'salary', 'department', 'employee_director')
    readonly_fields = ('work_date_start', )
    ordering = ('work_date_start', 'user')
    list_filter = ('department', )
    inlines = [EmployeesInLine]

    def get_actions(self, request):
        actions = super(self.__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'employees_num')
    fields = ('name', 'description', 'employees_num')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(User, UserAdmin)
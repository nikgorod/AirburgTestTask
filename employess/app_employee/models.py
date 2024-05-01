from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist


class Department(models.Model):
    name = models.CharField(max_length=150, verbose_name='название отдела')
    description = models.TextField(verbose_name='описание', blank=False)
    employees_num = models.PositiveIntegerField(verbose_name='кол-во сотрудников', default=0)

    def increment_employees_num(self):
        department = Department.objects.get(name=self.name)
        department.employees_num += 1
        department.save()

    def decrement_employees_num(self):
        department = Department.objects.get(name=self.name)
        department.employees_num -= 1
        department.save()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'отдел'
        verbose_name_plural = 'отделы'


class User(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=150, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    middle_name = models.CharField(_('middle_name'), max_length=150, blank=False)

    def get_full_name(self):
        full_name = '%s %s %s' % (self.last_name, self.first_name, self.middle_name)
        return full_name.strip()

    def __str__(self):

        return self.get_full_name()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Employee(models.Model):
    phone_number_regex = RegexValidator(regex=r'\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}')

    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, related_name='employee_auth')
    phone = models.CharField(
        validators=[phone_number_regex], max_length=18, unique=True, blank=False, verbose_name='телефон'
    )
    work_date_start = models.DateField(verbose_name='дата начала работы', auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employee_department',
                                   verbose_name='отдел')
    position = models.CharField(max_length=100, blank=False, verbose_name='должность')
    salary = models.FloatField(verbose_name='зарплата', default=0)
    employee_director = models.ForeignKey("Employee", on_delete=models.PROTECT,
                                          verbose_name='руководитель', related_name='director', null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            employee = Employee.objects.get(phone=self.phone)
        except ObjectDoesNotExist:
            department = Department.objects.get(name=self.department.name)
            department.increment_employees_num()
        super().save()

    def delete(self, using=None, keep_parents=False):
        department = Department.objects.get(name=self.department.name)
        department.decrement_employees_num()
        super().delete()

    def __str__(self):
        return f"{self.user}"

    class Meta:

        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'

from rest_framework.serializers import ModelSerializer, SlugRelatedField, HyperlinkedRelatedField
from rest_framework import serializers
from app_employee.models import Employee, Department, User
from django.core.validators import RegexValidator


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'username', 'email')


class EmployeeSerializer(ModelSerializer):

    phone = RegexValidator(regex=r'\+7\s\(\d{3}\)\s\d{3}-\d{2}-\d{2}')

    department = SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ('id', 'user', 'phone', 'work_date_start',
                  'department', 'position', 'salary',
                  'employee_director')


class DepartmentSerializer(ModelSerializer):

    class Meta:
        model = Department
        fields = ('name', 'description', 'employees_num')

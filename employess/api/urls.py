from django.urls import path
from .views import (
    EmployeeListAPIView,
    UserListAPIView,
    UserDetail,
    EmployeeDetail,
    DepartmentDetail,
    DepartmentListApiView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger
schema_view = get_schema_view(
   openapi.Info(
      title="ILoveDjango",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('employees/', EmployeeListAPIView.as_view(), name='employees_list'),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name='employee_detail'),
    path('users/', UserListAPIView.as_view(), name='users_list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user_detail'),
    path('departments/', DepartmentListApiView.as_view(), name='departments_list'),
    path('departments/<int:pk>/', DepartmentDetail.as_view(), name='department_detail')
]

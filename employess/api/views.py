from django.http import JsonResponse, Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import EmployeeSerializer, UserSerializer, DepartmentSerializer
from app_employee.models import Employee, Department, User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import action


class BaseListApiView(APIView):
    model = None
    serializer = None

    def get(self, request):
        queryset = self.model.objects.all()
        return JsonResponse(self.serializer(queryset, many=True).data, safe=False)

    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class EmployeeListAPIView(BaseListApiView):
    model = Employee
    serializer = EmployeeSerializer
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['user', 'phone', 'department', 'position', 'salary', 'employee_director'],
                                  properties=
                                  {'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='пользователь'),
                                   'phone': openapi.Schema(type=openapi.TYPE_STRING, description='телефон'),
                                   'department': openapi.Schema(type=openapi.TYPE_INTEGER, description='id отдела'),
                                   'position': openapi.Schema(type=openapi.TYPE_STRING, description='должность'),
                                   'salary': openapi.Schema(type=openapi.TYPE_NUMBER, description='зарплата'),
                                   'employee_director': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                       description='руководитель')}
                                  )

    @swagger_auto_schema(method='POST', request_body=request_body)
    @action(methods=['post'], detail=False, )
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(BaseListApiView):
    model = User
    serializer = UserSerializer


class DepartmentListApiView(BaseListApiView):
    model = Department
    serializer = DepartmentSerializer

    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'description'],
                                  properties=
                                  {
                                      'name': openapi.Schema(type=openapi.TYPE_STRING, description='название отдела'),
                                      'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'), }
                                  )

    @swagger_auto_schema(method='POST', request_body=request_body)
    @action(methods=['post'], detail=False, )
    def post(self, request):
        serializer = self.serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BaseDetailView(APIView):
    model = None
    serializer = None

    def get_object(self, pk):
        try:
            instance = self.model.objects.get(pk=pk)
            return instance
        except self.model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        instance = self.get_object(pk)
        serializer_context = {
            'request': request,
        }
        return JsonResponse(self.serializer(instance, context=serializer_context).data, safe=False)

    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDetail(BaseDetailView):
    model = User
    serializer = UserSerializer


class EmployeeDetail(BaseDetailView):
    model = Employee
    serializer = EmployeeSerializer
    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'description'],
                                  properties=
                                  {
                                      'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='пользователь'),
                                      'phone': openapi.Schema(type=openapi.TYPE_STRING, description='телефон'),
                                      'department': openapi.Schema(type=openapi.TYPE_INTEGER, description='id отдела'),
                                      'position': openapi.Schema(type=openapi.TYPE_STRING, description='должность'),
                                      'salary': openapi.Schema(type=openapi.TYPE_NUMBER, description='зарплата'),
                                      'employee_director': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                                          description='руководитель')}
                                  )

    @swagger_auto_schema(method='PUT', request_body=request_body)
    @action(methods=['put'], detail=False, )
    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class DepartmentDetail(BaseDetailView):
    model = Department
    serializer = DepartmentSerializer

    request_body = openapi.Schema(type=openapi.TYPE_OBJECT,
                                  required=['name', 'description'],
                                  properties=
                                  {
                                      'name': openapi.Schema(type=openapi.TYPE_STRING, description='название отдела'),
                                      'description': openapi.Schema(type=openapi.TYPE_STRING, description='описание'), }
                                  )

    @swagger_auto_schema(method='PUT', request_body=request_body)
    @action(methods=['put'], detail=False, )
    def put(self, request, pk):
        instance = self.get_object(pk)
        serializer = self.serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

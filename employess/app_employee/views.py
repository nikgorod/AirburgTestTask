from django.shortcuts import render


def main_view(request):
    return render(request, 'app_employee/index.html')

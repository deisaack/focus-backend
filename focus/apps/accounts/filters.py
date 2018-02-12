from django_filters import rest_framework as filters
from .models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        fields = (
            'id', 'employee_no', 'id_no', 'phone', 'gender', 'phone_verified'
        )
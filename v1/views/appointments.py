from django.shortcuts import render
from django.db.models import Q
from django.views import View
from datetime import datetime
from v1.models import Appointments


class AppointmentsView(View):
    template_name = 'appointments.html'

    @classmethod
    def get(cls, request):
        search_query = request.GET.get('search', '').strip()
        appointments = Appointments.objects.select_related('created_by')

        if search_query:
            appointments = cls.filter_appointments(appointments, search_query)

        context = {
            'appointments': appointments,
            'search_query': search_query,
        }
        return render(request, cls.template_name, context)

    @classmethod
    def filter_appointments(cls, appointments, search_query):
        try:
            date_query = datetime.strptime(search_query, '%Y-%m-%d').date()
            return appointments.filter(scheduling__date=date_query)
        except ValueError:
            return appointments.filter(
                Q(created_by__file_name__icontains=search_query) |
                Q(registration_id__icontains=str(search_query))
            )


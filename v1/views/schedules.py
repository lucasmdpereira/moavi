from datetime import datetime, timedelta
from v1.models import Appointments
from django.views import View
from django.shortcuts import render
from collections import defaultdict


TEN_MINUTES_INTERVALS_IN_A_DAY = 144
MINUTES_PER_HOUR = 60
HOURS_PER_DAY = 24
INTERVAL_IN_MINUTES = 10
TIME_DIVISOR_FOR_LABELS = 6


class SchedulesView(View):
    template_name = 'schedules.html'

    def get(self, request, *args, **kwargs):
        date_filter = request.GET.get('date', datetime.today().date().isoformat())
        selected_date = datetime.strptime(date_filter, '%Y-%m-%d')
        end_date = selected_date + timedelta(days=1)

        appointments = Appointments.objects.filter(scheduling__range=(selected_date, end_date)).order_by('registration_id', 'scheduling')

        employees_schedule = defaultdict(lambda: [0] * TEN_MINUTES_INTERVALS_IN_A_DAY)

        for appointment in appointments:
            registration_id = appointment.registration_id
            time_index = (appointment.scheduling.hour * MINUTES_PER_HOUR + appointment.scheduling.minute) // INTERVAL_IN_MINUTES

            current_value = employees_schedule[registration_id][time_index - 1] if time_index > 0 else 0
            new_value = 1 - current_value

            for i in range(time_index, TEN_MINUTES_INTERVALS_IN_A_DAY):
                employees_schedule[registration_id][i] = new_value

        general_list = [sum(x[i] for x in employees_schedule.values()) for i in range(TEN_MINUTES_INTERVALS_IN_A_DAY)]

        labels = [f'{i // TIME_DIVISOR_FOR_LABELS:02}:{(i % TIME_DIVISOR_FOR_LABELS) * INTERVAL_IN_MINUTES:02}' for i in range(TEN_MINUTES_INTERVALS_IN_A_DAY)]

        return render(request, self.template_name, {'labels': labels, 'data': general_list, 'date': selected_date})

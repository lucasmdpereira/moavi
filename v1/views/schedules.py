from collections import defaultdict
from datetime import datetime, timedelta
from v1.models import Appointments
from django.views import View
from django.shortcuts import render
import pytz
from collections import defaultdict

TEN_MINUTES_INTERVALS_IN_A_DAY = 144


class SchedulesView(View):
    template_name = 'schedules.html'

    def get(self, request, *args, **kwargs):
        date_filter = request.GET.get('date', datetime.today().date().isoformat())
        local_timezone = pytz.timezone('UTC')
        selected_date = local_timezone.localize(datetime.strptime(date_filter, '%Y-%m-%d'))
        end_date = selected_date + timedelta(days=1)

        appointments = Appointments.objects.filter(scheduling__range=(selected_date, end_date))

        intervals = defaultdict(int)
        for appointment in appointments:
            adjusted_time = appointment.scheduling
            interval = (adjusted_time.hour * 60 + adjusted_time.minute) // 10
            intervals[interval] += 1

        labels = []
        data = []
        for i in range(TEN_MINUTES_INTERVALS_IN_A_DAY):
            hour = i // 6
            minute = (i % 6) * 10
            labels.append(f'{hour:02}:{minute:02}')
            data.append(intervals[i])

        return render(request, self.template_name, {'labels': labels, 'data': data, 'date': selected_date})

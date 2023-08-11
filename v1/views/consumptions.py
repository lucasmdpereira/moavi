import csv
from datetime import datetime
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.http import HttpResponse
from io import TextIOWrapper
from v1.models import Consumptions, Appointments
import pytz


HEADER_LINES = 1
NUMBER_OF_COLUMNS = 3


class ConsumptionsView(ListView):
    model = Consumptions
    template_name = 'consumptions.html'
    context_object_name = 'consumptions'

    @classmethod
    def get_queryset(cls):
        return Consumptions.objects.all()

    @classmethod
    def post(cls, request):
        validation_errors = []

        if 'file' not in request.FILES:
            validation_errors.append("Nenhum arquivo enviado.")

        if not validation_errors:
            csv_file = request.FILES['file']
            csv_file_str = csv_file.read().decode('utf-8')
            rows = csv_file_str.splitlines()

            for row_number, row in enumerate(rows[HEADER_LINES:], start=HEADER_LINES):
                row_data = row.split(";")
                if len(row_data) != NUMBER_OF_COLUMNS:
                    validation_errors.append(f"Linha {row_number}: Formato inválido.")
                    continue

                registration_id, date_str, time_str = row_data

                if not registration_id.isdigit():
                    validation_errors.append(f"Linha {row_number}: Matrícula inválida.")

                try:
                    scheduling = cls.create_datetime(date_str, time_str)
                except ValueError:
                    validation_errors.append(f"Linha {row_number}: Data ou hora inválida.")
                    continue

                if not validation_errors:
                    consumption, *_ = Consumptions.objects.get_or_create(
                        file_name=csv_file.name,
                        appointments_entries=len(rows) - HEADER_LINES,
                        imported_by=request.user
                    )

                    Appointments.objects.get_or_create(
                        registration_id=registration_id,
                        scheduling=scheduling,
                        created_by=consumption
                    )
        if validation_errors:
            return render(
                request,
                'consumptions.html',
                {'validation_errors': validation_errors, 'consumptions': Consumptions.objects.all()}
            )

        return redirect('consumptions')

    @classmethod
    def create_datetime(cls, date_str, time_str):
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        time_obj = datetime.strptime(time_str, '%H:%M').time()
        utc_datetime = datetime.combine(date_obj, time_obj)

        return utc_datetime.replace(tzinfo=pytz.utc)

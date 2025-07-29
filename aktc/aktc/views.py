

import datetime
from django.shortcuts import render  # , HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from aktcUI.models import WeekDaysSchedule


# views.py
from django.views.generic import TemplateView


class FrontendAppView(TemplateView):
    template_name = "index.html"


@csrf_exempt
def get_departure_dates_choices(request):
    print("departure date loading")
    if request.method == 'POST':
        print("Post request accepted", request)
        selected_date = request.POST.get('date')
        print("Post request accepted", selected_date)
        # object_selected_date = datetime.datetime.strptime(selected_date)
        selected_date_data = WeekDaysSchedule.objects.filter(
            start_or_only_date=selected_date).first()
        if selected_date_data:
            scheduled_times_for_day = list()
            for depart_time in selected_date_data.daily_schedule.time.all():
                scheduled_times_for_day.append(dict(hour=depart_time.hour,
                                                    minute=depart_time.minute,
                                                    meridian=depart_time.meridian))

            print("selected_date_data", selected_date_data)
            slots = {
                "start_or_only_date": selected_date_data.start_or_only_date,
                "daily_schedule": scheduled_times_for_day
            }
        else:
            slots = {
                "start_or_only_date": None,
                "daily_schedule": None
            }
        datetime.time(hour=1, minute=20)
        print("slots", slots)

        return JsonResponse(slots)


def confirm_passenger_arrival(request):
    context = {
        'hero': 'he is the hero of the day'
    }
    return render(request, 'admin/confirm_passenger.html', context)
# return render(request, 'admin/confirm_passenger.html', {})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import locationData, pollutant_data, activityHistory
from django.http import JsonResponse


@login_required
def home_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    return render(request, 'home.html')


def activityLog_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    act_history = activityHistory.objects.select_related(
        'user').all()

    return render(request, 'activity_log.html', {'activity_log': act_history})


def analysis_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    dropdown_options = locationData.objects \
        .values_list('site_id', 'site_name') \
        .order_by('site_name')


# get the requeest from the fetch in javascript
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        selected_location = request.GET.get('location', '').strip()
        mindate = request.GET.get('mindate', "%Y-%m-%d").strip()
        maxdate = request.GET.get('maxdate', "%Y-%m-%d").strip()

        fields = ['date', 'site_id', 'aqi', 'so2',
                  'co', 'o3', 'nox', 'pm25', 'pm10']
        if selected_location and selected_location != 'Select Location':
            pollutant_values_show = pollutant_data.objects \
                .filter(site_id=selected_location)
        else:
            pollutant_values_show = pollutant_data.objects

        records = pollutant_values_show.filter(date__range=[mindate, maxdate]).order_by('date').values(
            *fields)

        serializable_data = [
            {key: (str(val) if val is not None else '')
             for key, val in item.items()}
            for item in records
        ]

        return JsonResponse({'success': True, 'data': serializable_data})

    context = {
        'location_options': dropdown_options,

    }

    return render(request, 'analysis.html', context)


def data_management_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    dropdown_options = locationData.objects \
        .values_list('site_id', 'site_name') \
        .order_by('site_name')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_location = request.GET.get('location', '')

        fields = ['date', 'site_id', 'aqi', 'so2',
                  'co', 'o3', 'nox', 'pm25', 'pm10']
        if selected_location and selected_location != 'Select Location':
            pollutant_values_show = pollutant_data.objects \
                .filter(site_id=selected_location)
        else:
            pollutant_values_show = pollutant_data.objects

        records = pollutant_values_show.order_by('date').values(
            *fields)[:100]

        serializable_data = [
            {key: (str(val) if val is not None else '')
             for key, val in item.items()}
            for item in records
        ]

        return JsonResponse({'success': True, 'data': serializable_data})

    context = {
        'location_options': dropdown_options,

    }

    return render(request, 'data_management.html', context)


def report_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    return render(request, 'reports.html')


def settings_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    return render(request, 'settings.html')


def support_view(request):
    if not request.user.is_authenticated:

        return redirect('/')

    return render(request, 'support.html')

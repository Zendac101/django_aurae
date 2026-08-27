from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import locationData, pollutant_data
from django.http import JsonResponse


@login_required
def home_view(request):
    if not request.user.is_authenticated:

        return redirect('/accounts/registerUser')

    return render(request, 'home.html')


def analysis_view(request):
    if not request.user.is_authenticated:

        return redirect('/accounts/registerUser')

    dropdown_options = locationData.objects.using('sensor_data_db') \
        .values_list('site_id', 'site_name') \
        .order_by('site_name')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':

        selected_location = request.GET.get('location', '')
        fields = ['date', 'time', 'site_id', 'aqi',
                  'status', 'so2', 'co', 'o3', 'no', 'no2', 'nox']
        if selected_location and selected_location != 'Select Location':
            pollutant_values_show = pollutant_data.objects.using('sensor_data_db') \
                .filter(site_id=selected_location).values_list('date', 'time', 'site_id', 'aqi', 'status', 'so2', 'co', 'o3', 'no2', 'nox', 'no') \
                .order_by('date', 'time')
        else:
            pollutant_values_show = pollutant_data.objects.using('sensor_data_db') \
                .values_list('date', 'time', 'site_id', 'aqi', 'status', 'so2', 'co', 'o3', 'no2', 'nox', 'no') \
                .order_by('date', 'time')[:100]

        records = pollutant_values_show.values(
            *fields).order_by('date', 'time')[:100]
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

        return redirect('/accounts/registerUser')

    dropdown_options = locationData.objects.using('sensor_data_db') \
        .values_list('site_id', 'site_name') \
        .order_by('site_name')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        selected_location = request.GET.get('location', '')

        if selected_location and selected_location != 'Select Location':
            pollutant_values_show = pollutant_data.objects.using('sensor_data_db') \
                .filter(site_id=selected_location).values_list('date', 'time', 'site_id', 'aqi', 'status', 'so2', 'co', 'o3', 'no2', 'nox', 'no') \
                .order_by('date', 'time')

        else:
            pollutant_values_show = pollutant_data.objects.using('sensor_data_db') \
                .values_list('date', 'time', 'site_id', 'aqi', 'status', 'so2', 'co', 'o3', 'no2', 'nox', 'no') \
                .order_by('date', 'time')[:100]

        serializable_data = [list(row) for row in pollutant_values_show]

        return JsonResponse({'success': True, 'data': serializable_data})

    context = {
        'location_options': dropdown_options,

    }

    return render(request, 'data_management.html', context)


def report_view(request):
    if not request.user.is_authenticated:

        return redirect('/accounts/registerUser')

    return render(request, 'reports.html')


def settings_view(request):
    if not request.user.is_authenticated:

        return redirect('/accounts/registerUser')

    return render(request, 'settings.html')


def support_view(request):
    if not request.user.is_authenticated:

        return redirect('/accounts/registerUser')

    return render(request, 'support.html')

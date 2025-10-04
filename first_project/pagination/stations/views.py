from django.shortcuts import render, redirect
from django.urls import reverse
import csv
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))

def detect_delimiter(file_path):
    with open(file_path, encoding='utf-8') as f:
        sample = f.read(1024)
        if ';' in sample:
            return ';'
        elif ',' in sample:
            return ','
        return ','


import csv
from django.shortcuts import render
from django.conf import settings


def bus_stations(request):
    # Читаем CSV-файл
    with open(settings.BUS_STATION_CSV, encoding='utf-8') as f:
        delimiter = detect_delimiter(settings.BUS_STATION_CSV)
        reader = csv.DictReader(f, delimiter=delimiter)
        stations = list(reader)

    # Параметры пагинации
    page_size = 10
    page = request.GET.get('page', 1)

    try:
        page = int(page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    start = (page - 1) * page_size
    end = start + page_size

    current_stations = stations[start:end]

    has_previous = page > 1
    has_next = end < len(stations)

    prev_page = page - 1 if has_previous else None
    next_page = page + 1 if has_next else None

    context = {
        'bus_stations': current_stations,
        'current_page': page,
        'prev_page': prev_page,
        'next_page': next_page,
        'has_previous': has_previous,
        'has_next': has_next,
    }

    return render(request, 'stations/myindex.html', context)
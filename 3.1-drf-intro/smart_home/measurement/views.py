from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer

@api_view(['GET', 'POST'])
def sensors_list(request):
    if request.method == 'GET':
        sensors = Sensor.objects.all()
        serializer = SensorSerializer(sensors, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SensorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def sensor_update(request, pk):
    try:
        sensor = Sensor.objects.get(pk=pk)
    except Sensor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SensorSerializer(sensor, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def sensor_detail(request, pk):
    try:
        sensor = Sensor.objects.prefetch_related('measurements').get(pk=pk)
    except Sensor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SensorDetailSerializer(sensor)
    return Response(serializer.data)


@api_view(['POST'])
def add_measurement(request):
    sensor_id = request.data.get('sensor')
    temperature = request.data.get('temperature')
    image = request.FILES.get('image', None)

    try:
        sensor = Sensor.objects.get(id=sensor_id)
    except Sensor.DoesNotExist:
        return Response({'error': 'Sensor not found'}, status=status.HTTP_404_NOT_FOUND)

    measurement = Measurement(sensor=sensor, temperature=temperature)
    if image:
        measurement.image = image
    measurement.save()

    return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)

from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать в Smart Home API! Используйте /api/sensors/ и /api/measurements/")
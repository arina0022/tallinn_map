from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import folium
from folium.plugins import HeatMap
from .models import SlipperyPoint

@csrf_exempt
def map_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        lat = data.get("lat")
        lon = data.get("lon")
        slipperiness = data.get("slipperiness", 5)

        marker = SlipperyPoint.objects.create(latitude=lat, longitude=lon, slipperiness=slipperiness)

        return JsonResponse({"status": "success", "id": marker.id})

    markers = list(SlipperyPoint.objects.values("latitude", "longitude", "slipperiness"))


    return render(request, 'map.html', {'markers': json.dumps(markers)})

@csrf_exempt
def ready_map(request):
    map = folium.Map(location=[59.4300, 24.7536], tiles="Cartodb Positron", zoom_start=12)
    
    heatmap_data = list(SlipperyPoint.objects.values_list('latitude', 'longitude', 'slipperiness'))

    if heatmap_data:
        HeatMap(heatmap_data).add_to(map)

    mapready_html = map._repr_html_()
    return render(request, 'map_ready.html',{'mapready_html': mapready_html})


@csrf_exempt
def ready_map_hour(request):
    selected_hour = request.GET.get('hour', None)
    
    map = folium.Map(location=[59.4300, 24.7536], tiles="Cartodb Positron", zoom_start=12)

    all_data = list(SlipperyPoint.objects.values_list('latitude', 'longitude', 'slipperiness', 'timestamp'))

    heatmap_data = []
    available_hours = set()

    for lat, lon, weight, timestamp in all_data:
        record_hour = timestamp.strftime('%H')

        available_hours.add(record_hour)

        if selected_hour is None or selected_hour == record_hour:
            heatmap_data.append([float(lat), float(lon), float(weight)])

    if heatmap_data:
        HeatMap(heatmap_data).add_to(map)

    mapready_html = map._repr_html_()

    return render(request, 'map_ready_hour.html', {
        'mapready_html': mapready_html,
        'available_hours': sorted(available_hours),
        'selected_hour': selected_hour
    })
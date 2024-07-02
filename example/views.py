from rest_framework.response import Response
from django.http import FileResponse
from rest_framework.decorators import api_view
import requests
from  example.serializers import VisitorName


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def get_coordinate(request, ip: str):
    url = "https://get.geojs.io/v1/ip/geo/{ip}.json"
    formatted_url = url.format(ip=ip)
    response = requests.get(formatted_url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        # Handle error: Request failed (non-200 status code)
        return {"error": f"Request failed with status code: {response.status_code}"}


def weather(request, lat: str, log: str):

    url = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={log}&current=temperature"
    formatted_url = url.format(lat=lat, log=log)
    response = requests.get(formatted_url)
    data = response.json()
    return data


@api_view(["GET"])
def getInfo(request):
    info = {"name": "Smart Monday", "Slack": "@smartPYJ"}
    return Response(info)
    

@api_view(["GET"])
def getData(request):
    serializer = VisitorName(data=request.GET)
    if serializer.is_valid():
        visitor_name = (serializer.validated_data['visitor_name']).strip('"') 
        ip = get_client_ip(request)
        coordinate = get_coordinate(request, ip)
        city = coordinate["city"]
        lat, log = coordinate["latitude"], coordinate["longitude"]
        temp = weather(request, lat, log)
        temperature = temp["current"]["temperature"]

        return Response(
            {
                "client_ip": ip,
                "location": city,
                "greeting": f"Hello, {visitor_name}! the temperature is {temperature} degree Celcius in {city}",
            }
        )
    else:
        return Response(serializer.errors)

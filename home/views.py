from django.shortcuts import render, HttpResponse
import json
import requests
import math
 # Create your views here.
def index(request):
    if "location" in request.GET:
        city= request.GET.get('location')
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=8257c3245fe46476bbb73f8920f1418e"
        x= requests.get(url)
        y=x.json()
        context={
            'City': f"{y['name']}",
            'Temp': f"{math.trunc(y['main']['temp']-273.15)}°C",
            'icon': f"{y['weather'][0]['icon']}",
            'Pressure': f"Pressure: {y['main']['pressure']} mb",
            'Humidity': f"Humidity: {y['main']['humidity']}%",
            'weather_condition': f"{y['weather'][0]['description']}".capitalize(),

        }
        return render(request, 'home.html', context)



    return render(request, 'home.html')
    #return HttpResponse("Hi Richa")
# Create your views here.


# Create your views here.
from django.shortcuts import render

from aiohttp import ClientSession

from datetime import datetime


async def get(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            return await response.json()


async def home(request):
    city: str = request.POST.get('search') if request.POST else "Samarqand"
    api_key: str = "af82ad5966541eca3cfa0d349ff10587"  # https://openweathermap.org/
    url: str = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    response = await get(url=url.format(city, api_key))
    if response.get('message') == 'city not found':
        return render(request=request, template_name='index.html', context={'message': 'notfound'})
    date = datetime.now()
    weather: dict = {
        'city': city,
        'temp': int(response['main']['temp']),
        'temp_min': int(response['main']['temp_min']),
        'temp_max': int(response['main']['temp_max']),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
        'date': date.strftime('%A'),
    }
    context: dict = {
        'weather': weather
    }
    return render(request=request, template_name='index.html', context=context)

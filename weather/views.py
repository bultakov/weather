from django.shortcuts import render

from aiohttp import ClientSession


async def get(url: str) -> dict:
    async with ClientSession() as session:
        async with session.get(url=url) as response:
            return await response.json()


async def home(request):
    city: str = "Samarqand"
    if request.POST:
        city: str = request.POST.get('search')
    api_key: str = "af82ad5966541eca3cfa0d349ff10587"  # https://openweathermap.org/
    url: str = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric"
    response = await get(url=url.format(city, api_key))
    weather: dict = {
        'city': city,
        'temperature': response['main']['temp'],
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }
    context: dict = {
        'weather': weather
    }
    return render(request=request, template_name='index.html', context=context)

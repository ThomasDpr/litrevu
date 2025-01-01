import pytz
from django.utils.timezone import activate


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone = request.session.get('django_timezone', 'Europe/Paris')
        try:
            activate(pytz.timezone(timezone))
        except pytz.UnknownTimeZoneError:
            activate(pytz.timezone('UTC'))

        request.session['django_timezone'] = timezone  
        response = self.get_response(request)
        return response

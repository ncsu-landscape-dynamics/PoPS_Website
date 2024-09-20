from django.conf import settings  # import the settings file


def mapbox_key(request):
    return {"MAPBOX_KEY": settings.MAPBOX_KEY}


# def mapbox_dashboard_style(request):
#     return {"MAPBOX_DASHBOARD_STYLE": settings.MAPBOX_DASHBOARD_STYLE}
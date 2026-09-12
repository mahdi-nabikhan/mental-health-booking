from django.contrib import admin
from django.urls import path, include


app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        'api/v1/accounts/',
        include('booking.api.v1.urls')
    ),
]
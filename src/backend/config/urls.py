from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts API
    path(
        'api/v1/accounts/',
        include('accounts.api.v1.urls'),
    ),
    path(
            'api/v1/booking/',
            include('booking.api.v1.urls'),
        ),
    
    path(
        'api/v1/blog/',
        include('blog.api.v1.urls')
        ),
    
    path(
        "api/v1/faq/",
        include("faq.api.v1.urls")
        ),
    



    # Swagger
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
]
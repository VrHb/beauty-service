from django.urls import include, path

urlpatterns = [
    path("", include("saloonapp.urls")),
    path("", include('django.contrib.auth.urls')),
]

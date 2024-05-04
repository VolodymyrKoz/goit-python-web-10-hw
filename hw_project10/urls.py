from django.contrib import admin
from django.urls import path, include
from quotes.views import AddQuoteView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("quotes.urls")),
    path("users/", include("users.urls")),
    path('add_quote/', AddQuoteView.as_view(), name='add_quote'),
]

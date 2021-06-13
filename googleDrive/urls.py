from django.urls import path
from .views import *

urlpatterns = [
    path('api/login', login),
    path('api/list', list),
    path('api/search', filename_search),
    path('api/download', download),
    path('api/upload', upload),
    path('api/logout', logout),
]

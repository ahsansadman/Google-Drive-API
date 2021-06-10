from django.urls import path
from .views import *

urlpatterns = [
    path('api/login', login),
    path('api/list/<str:token>', list),
    path('api/filename/<str:filename>/<str:token>', filename_search),
    path('api/download/<str:filename>/<str:file_id>', download),
    path('api/upload', upload),
    path('api/logout', logout),
]

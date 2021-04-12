from django.urls import path

from . import views

app_name = 'crudgenerics'

urlpatterns = [
    path('speakers', views.SpeakerDisplayCreate.as_view()),
    path('speakers/<int:pk>', views.SpeakerUpdateDelete.as_view()),
    #url(r'^\?view=(?P<vtype>instructor|course|room)$', 'index', name='index'),
]
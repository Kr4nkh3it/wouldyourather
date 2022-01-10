from django.urls import path

from . import views

app_name = 'wyrapp'
urlpatterns = [
    path('',views.index,name='index'),
    path('<int:question_id>/',views.choose,name='choose'),
    path('<int:question_id>/results/',views.results,name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote')
]

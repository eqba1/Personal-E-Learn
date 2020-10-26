from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('subjects/',
        views.SubjectListView.as_view(),
        name='subject_list'),
    path('subjects/<pk>/',
        views.SubjcetDetailView.as_view(),
        name='subject_detail'),
]
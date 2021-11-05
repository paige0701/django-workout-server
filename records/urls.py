from django.urls import path
from records import views

urlpatterns = [
    path('', views.RecordListView.as_view()),
    path('<slug:pk>/', views.RecordDetailView.as_view())
]

from django.urls import path
from . import views


app_name = 'services'


urlpatterns = [
	# post views
    path("", views.ServiceListView.as_view(), name="list-service"),
    path('create-service/', views.ServiceCreateView.as_view(), name='create-service'),
    path('update-service/<int:pk>', views.ServiceUpdateView.as_view(), name='update-service'),
    path('service/<int:pk>', views.ServiceDetailView.as_view(), name='detail-service'),
]

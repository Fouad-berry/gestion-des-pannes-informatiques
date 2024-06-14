from django.urls import path
from . import views


app_name = 'directions'


urlpatterns = [
	# post views
	path('create-direction/', views.DirectionCreateView.as_view(), name='create-direction'),
    path('direction/update/<int:pk>', views.DirectionUpdateView.as_view(), name='update-direction'),
    path('delete-direction/<int:pk>', views.DirectionDeleteView.as_view(), name='delete-direction'),
    path('direction/<int:pk>', views.DirectionDetailView.as_view(), name='detail-direction'),
    path("", views.DirectionListView.as_view(), name="list-direction"),
]

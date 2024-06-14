from django.urls import path
from . import views


app_name = 'pannes'

# path("panne/<int:pk>", views.PanneDetailView.as_view(), name="panne-detail"),
urlpatterns = [
	# post views
    path("all-panne/", views.PanneListView.as_view(), name="all-panne"),
    path('delete-panne/<int:pk>', views.PanneDeleteView.as_view(), name='delete-panne'),
    path('done-panne/<int:pk>', views.PanneDoneView.as_view(), name='done-panne'),
    path("pannes/", views.AllPAnnesView.as_view(), name="pannes"),
    path("observation/<int:pk>", views.PanneObservationView.as_view(), name="oservation-panne")

]

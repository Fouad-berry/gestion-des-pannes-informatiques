from django.urls import path
from . import views

app_name = 'materiels'

urlpatterns = [
	# post views
    path('create-materiel/', views.MaterielCreateView.as_view(), name='create-materiel'),
    path('update-materiel/<int:pk>', views.MaterielUpdateView.as_view(), name='update-materiel'),
    path('delete-materiel/<int:pk>', views.MaterielDeleteView.as_view(), name='delete-materiel'),
    path('', views.MaterielListView.as_view(), name='list-materiel'),
    path('materiels/', views.MaterielAllView.as_view(), name="materiel_list"),
    path("materiel/<int:pk>", views.MaterielDetailView.as_view(), name="detail-materiel")

    
]
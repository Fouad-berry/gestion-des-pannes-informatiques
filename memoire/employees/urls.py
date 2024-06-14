from django.urls import path
from . import views

app_name = 'employees'

urlpatterns = [
	# post views
    path('register/', views.EmployeeCreateView.as_view(), name='register'),
    path('update-user/', views.UserUpdateView.as_view(), name='update-user'),
    path('delete-employee/<int:pk>', views.EmployeeDeleteView.as_view(), name='delete-employee'),
    path('list-employee/', views.EmployeeListView.as_view(), name='list-employee'),

    path("services/direction/", views.GetServicesView.as_view(), name="services"),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('', views.IndexView.as_view(), name='index'),
    path('a-propos/', views.AproposView.as_view(), name='a-propos'),
    path('contact-us/', views.ContactView.as_view(), name='contact-us'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('user-profile/', views.UserProfileView.as_view(), name='user-profile'),
]
from django.urls import path
from . import views


app_name = "tickets"


urlpatterns = [
	# post views
    path("create-ticket/", views.TicketCreateView.as_view(), name="create-ticket"),
    path("delete-ticket/<int:pk>", views.TicketDeleteView.as_view(), name="delete-ticket"),
    path("all-ticket/", views.TicketListView.as_view(), name="all-ticket"),
    path("ticket/<int:pk>", views.TicketDetailView.as_view(), name="detail-ticket"),
    path("user-ticket/", views.TicketUserListView.as_view(), name="user-ticket"),

]

from django.urls import path, include
from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="helpdesk/dashboard"),
    path("members/", views.memberPage, name="helpdesk/members"),
    path("tickets/", views.getSupportTickets, name="helpdesk/tickets"),
    path("ticket/<int:ticketId>/", views.getTicketDetails, name="helpdesk/ticket"),
    path("ajax/validate_username/",views.hardware_details),
    path('tech-logs/', views.getTechnicalLogs, name="technical-logs"),
    path('isapprove/<str:tag>', views.checkstatus, name="checkstatus"),
]
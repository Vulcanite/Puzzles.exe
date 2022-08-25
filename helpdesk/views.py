from django.shortcuts import render
from employee.models import RequestTable
from .windows_config import get_config
from django.http import JsonResponse

status_colors = {"OPENED": "primary", "APPROVED":"", "REJECTED":"danger"}

def dashboard(request):
    return render(request, "helpdesk/dashboard.html")

def memberPage(request):
    return render(request, "helpdesk/member.html")

def deleteUser(request):
    pass

def addUser(request):
    pass

def editUser(request):
    pass

def getSupportTickets(request):
    logs = RequestTable.objects.all()
    for log in logs:
        if log.status == "OPENED":
            log.color = "bg-primary"
        elif log.status == "APPROVED":
            log.color = "bg-success"
        else:
            log.color = "bg-danger"
    return render(request, "helpdesk/tickets.html", {'logs': logs})

def requestApproval(request):
    pass

def getTicketDetails(request, ticketId):
    log = RequestTable.objects.get(id=ticketId)
    return render(request, "helpdesk/ticketDetails.html", {"log":log})

def hardware_details(request):
    data = get_config()
    print(data)
    return JsonResponse(data)
     

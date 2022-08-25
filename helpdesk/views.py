from django.shortcuts import render
from employee.models import RequestTable
from .windows_config import get_config
from django.http import JsonResponse

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
    return render(request, "helpdesk/tickets.html", {'logs': logs})

def requestApproval(request):
    pass

def getTicketDetails(request, ticketId):
    log = RequestTable.objects.get(id=ticketId)
    print(log.description)
    return render(request, "helpdesk/ticketDetails.html", {"log":log})

def hardware_details(request):
    data = get_config()
    print(data)
    return JsonResponse(data)
     

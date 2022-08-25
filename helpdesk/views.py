from django.shortcuts import render
from employee.models import RequestTable

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
    logs = RequestTable.objects.all()
    for i in logs:
        if i.id==ticketId:
            log = i
        # print(type(i.id))
        # print(type(ticketId))
        # log = RequestTable.objects.get(i.id)
    print(log.description)
    print(str(ticketId))
    # log = RequestTable.objects.get(RequestTable.id==str(ticketId))
    # print(log)
    return render(request, "helpdesk/ticketDetails.html", {"log":log})
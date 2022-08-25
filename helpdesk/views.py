from django.shortcuts import render

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
    return render(request, "helpdesk/tickets.html", {})

def requestApproval(request):
    pass

def allotTechnician(request):
    pass

def getTicketDetails(request, ticketId):
    return render(request, "helpdesk/ticketDetails.html", {"ticketId":ticketId})
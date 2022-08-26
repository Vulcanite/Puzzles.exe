from django.shortcuts import render
from employee.models import RequestTable
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from deepdiff import DeepDiff
from employee.models import RequestTable
from helpdesk.models import hardware_details

status_colors = {"OPENED": "primary", "APPROVED":"", "REJECTED":"danger"}

def dashboard(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    object = hardware_details.objects.get(emp_ip_address = ip)
    open_requests = RequestTable.objects.filter(status='OPENED').count()
    approved_requests = RequestTable.objects.filter(status='APPROVED').count()
    return render(request, "helpdesk/dashboard.html", {"open_requests":open_requests, "approved_requests":approved_requests, "details":object.emp_pc_config})

def memberPage(request):
    return render(request, "helpdesk/member.html")

def deleteUser(request):
    pass

def addUser(request):
    pass

def editUser(request):
    pass

def getTechnicalLogs(request):
    log = dict()
    return render(request, "helpdesk/technical-logs.html")

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

@csrf_exempt
def checkstatus(request,tag):
    if request.method == 'POST':
        print('worked',tag)
        ticket_id = request.session["ticketId"]
        obj = RequestTable.objects.get(id=ticket_id)
        obj.status = tag
        obj.save()
        return HttpResponse("Success!")

def getTicketDetails(request, ticketId):
    if request.method == 'POST':
        print('worked',request.data)
    request.session["ticketId"] = ticketId
    log = RequestTable.objects.get(id=ticketId)
    if log.status == "OPENED":
        log.color = "bg-primary"
    elif log.status == "APPROVED":
        log.color = "bg-success"
    else:
        log.color = "bg-danger"
    return render(request, "helpdesk/ticketDetails.html", {"log":log})

def diff(old_config, new_config):
    return DeepDiff(old_config, new_config, ignore_order=True)
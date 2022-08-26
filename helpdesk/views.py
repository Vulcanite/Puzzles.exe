from django.shortcuts import render
from employee.models import RequestTable
from .windows_config import get_config
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
status_colors = {"OPENED": "primary", "APPROVED":"", "REJECTED":"danger"}

def dashboard(request):
    open_requests = RequestTable.objects.filter(status='OPENED').count()
    approved_requests = RequestTable.objects.filter(status='APPROVED').count()
    return render(request, "helpdesk/dashboard.html", {"open_requests":open_requests, "approved_requests":approved_requests})

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



@csrf_exempt
def checkstatus(request):
    if request.method == 'POST':
        print('worked',request.data)
        return HttpResponse("hiii")

def getTicketDetails(request, ticketId):
    if request.method == 'POST':
        print('worked',request.data)

    log = RequestTable.objects.get(id=ticketId)
    if log.status == "OPENED":
        log.color = "bg-primary"
    elif log.status == "APPROVED":
        log.color = "bg-success"
    else:
        log.color = "bg-danger"
    return render(request, "helpdesk/ticketDetails.html", {"log":log})

def hardware_details(request):
    data = get_config()
    print(data)
    return JsonResponse(data)


def save_hardware_to_db(request):
    try:
        save_request = hardware_details(emp_fname= request.POST.get('titleInput'),
                                    emp_pc_config = request.POST.get('inputTag'),
                                    emp_ip_address = request.POST.get('descInput'))
        save_request.save()
        return HttpResponse("Config Successfully Saved!!!")
    except:
        return HttpResponse("Config Saved Failed!!!")
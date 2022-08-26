from webbrowser import get
from django.shortcuts import render

from employee.models import RequestTable
from helpdesk.models import hardware_details

def dashboard(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    try:
        object = hardware_details.objects.filter(emp_ip_address = ip)
        return render(request, "employee/dashboard.html", {"details" : object.emp_pc_config})
    except:
        return render(request, "employee/dashboard.html")

def supportRequest(request):
    return render(request, "employee/support-form.html")

def addRequest(request):
    if request.method == 'POST':
        save_request = RequestTable(title = request.POST.get('titleInput'),
                                request_tags = request.POST.get('inputTag'),
                                description = request.POST.get('descInput'),
                                created_by = request.user)
        save_request.save()
    return render(request, "employee/support-form.html")

def fetchConfiguration(request):
    pass

def deleteRequest(request):
    pass

def editRequest(request):
    pass

def logs(request):
    tickets = RequestTable.objects.filter(created_by = request.user)
    for log in tickets:
        if log.status == "OPENED":
            log.color = "bg-primary"
        elif log.status == "APPROVED":
            log.color = "bg-success"
        else:
            log.color = "bg-danger"
    return render(request,"employee/logs.html", {"logs": tickets})
from django.shortcuts import render

from employee.models import RequestTable

def dashboard(request):
    return render(request, "employee/dashboard.html")

def supportRequest(request):
    return render(request, "employee/support-form.html")

def addRequest(request):
    if request.method == 'POST':
        save_request = RequestTable(title = request.POST.get('titleInput'),
                                request_tags = request.POST.get('inputTag'),
                                description = request.POST.get('descInput'))
        save_request.save()
    return render(request, "employee/support-form.html")

def fetchConfiguration(request):
    pass

def deleteRequest(request):
    pass

def editRequest(request):
    pass
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from helpdesk.models import hardware_details

@api_view(['POST',])
def save_hardware_to_db(request):
	if request.method == 'POST':
		data = request.POST.get('data')
		print(data)
		try:
			objects = hardware_details.objects.filter(emp_ip_address = data["IPAddress"])
			if objects == None:
				save_config = hardware_details(emp_pc_config = data, emp_ip_address = data["IPAddress"])
				save_config.save()
			return Response(data, status=status.HTTP_200_OK)
		except:
			return Response(data, status=status.HTTP_404_OK)
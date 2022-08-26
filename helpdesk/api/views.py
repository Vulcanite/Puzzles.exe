from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from helpdesk.models import hardware_details

@api_view(['POST',])
def save_hardware_to_db(request):
	if request.method == 'POST':
		data = request.data
		print(data)
		save_config = hardware_details.objects.filter(emp_ip_address = data["IPAddress"])
		if len(save_config) == 0:
			save_config = hardware_details(emp_pc_config = data, emp_ip_address = data["IPAddress"])
			save_config.save()
			return Response(data, status=status.HTTP_200_OK)
		else:
			save_config = hardware_details.objects.get(emp_ip_address = data["IPAddress"])
			save_config.emp_pc_config = data
			save_config.save()
			return Response(data, status=status.HTTP_200_OK)
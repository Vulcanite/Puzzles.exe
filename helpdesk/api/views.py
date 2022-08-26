from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from helpdesk.models import hardware_details

@api_view(['POST',])
def save_hardware_to_db(request):
	if request.method == 'POST':
		data = request.data
		try:
			save_request = hardware_details(emp_fname= "Amish" ,
										emp_pc_config = data,
										emp_ip_address = data["Private IP Address:"])
			save_request.save()
			return Response(data,status=status.HTTP_200_OK)
		except:
			return Response(data,status=status.HTTP_200_OK)
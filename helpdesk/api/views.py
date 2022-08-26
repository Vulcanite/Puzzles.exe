from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST',])
def save_hardware_to_db(request):
	if request.method == 'POST':
		data = request.data['data']
		return Response(data,status=status.HTTP_200_OK)
from django.urls import path
from .views import init_player, walker, send_data

urlpatterns = [
	path('', init_player, name='init'),
	path('walker/', walker, name='walker'),
	path('data/', send_data, name='data'),
]

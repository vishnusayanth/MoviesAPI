from .serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken


# Class based view to retrieve the token after successful registration
class RegisterView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    permission_classes = []
    authentication_classes = []

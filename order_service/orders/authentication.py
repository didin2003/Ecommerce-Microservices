from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed


class CustomJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

   
        user_id = validated_token.get("user_id")

        if not user_id:
            raise AuthenticationFailed("Invalid token - user_id missing")

        # dummy user object (microservice style)
        class User:
            def __init__(self, id):
                self.id = id
                self.is_authenticated = True

        return (User(user_id), validated_token)
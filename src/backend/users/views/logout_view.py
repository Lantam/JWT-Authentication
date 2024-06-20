from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken as SimpleJWTRefreshToken

from refresh_tokens.utils import get_refresh_token_object_from_db_by_user_id


class LogoutAPIView(APIView):

    def post(self, request):
        user_id = request.COOKIES.get('user_id')
        if user_id:
            print('user_id found')
            refresh_token_object = get_refresh_token_object_from_db_by_user_id(user_id)
            if refresh_token_object:
                self.blacklist_refresh_token(refresh_token_object.token)
                self.delete_refresh_token_from_db(refresh_token_object)
            else:
                print('could not get refresh token object')
        else:
            print('could not get user_id')

        response = Response()
        response.delete_cookie('access_token')
        # response.delete_cookie('user_id')

        return response

    def blacklist_refresh_token(self, refresh_token):
        try:
            SimpleJWTRefreshToken(refresh_token).blacklist()
            print('blacklisted Refreshtoken')
        except Exception as e:
            print(f'Error blacklisting refresh token: {e}')

    def delete_refresh_token_from_db(self, refresh_token_object):
        try:
            refresh_token_object.delete()
            print('Refresh token deleted')
        except Exception as e:
            print(f'An error occurred while deleting refresh token: {e}')

from django.contrib.auth.backends import BaseBackend
from .models import Users



#### this file is created to Custom the authentication backend as i created a new Class named Users which donesnot inherit from
# the Class User of the django 
## the default authenticate method was validating the user name and password 
# here i used the email and the password 

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Users.objects.get(Email=email)
            if user.Password == password :
                return user


        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None

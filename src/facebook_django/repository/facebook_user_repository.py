from facebook_django.repository.facebook_repository import FaceBookRepository
import urllib
from django.http import HttpRequest
from httplib import HTTP
import json


class FacebookUserRepository(FaceBookRepository):
   
    
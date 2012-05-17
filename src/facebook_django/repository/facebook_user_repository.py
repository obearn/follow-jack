from facebook_django.repository.facebook_repository import FaceBookRepository
import urllib
from django.http import HttpRequest
from httplib import HTTP
import json
from facebook_django.model.facebook_objects import FaceBookUserCoordinates


class FacebookUserRepository(FaceBookRepository):
   
    def find_friends(self, user):
        friends_param = {"access_token": user.access_token}
        friends_url = "/%s/friends" % user.id
        friends = self._do_request("GET", friends_url, friends_param)
        
        print "User %s friends :%s" % (user.id, friends)
        user_friends = json.loads(friends)
        user_friend_list = []
        for user_data in user_friends["data"]:
            user_friend_list.append(FaceBookUserCoordinates(user_data["id"]))
            
        return user_friend_list   
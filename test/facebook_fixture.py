import urllib
import httplib
import json
from facebook_django.model.facebook_objects import FaceBookObject, FaceBookUser,\
    FaceBookLink
from facebook_django.myeworld.views import FacebookExceptionFactory
from facebook_django.repository.facebook_repository import FaceBookRepository

    
class TestUser(FaceBookObject):

    def __init__(self, id, login_url, access_token, password=None):
        self.id = id
        self.login_url = login_url
        self.access_token = access_token
        self.friends = []
        self.password = password
    
    def __eq__(self, other):
        if hasattr(other, "id") and other.id == self.id:
            return True
        return False
    
    def __hash__(self):
        return self.id
    
class FaceBookFixture(FaceBookRepository):
    
    def __init__(self, app_id, client_secret):
        self._client_secret = client_secret
        self._app_id = app_id
        self._app_token = None
        self._persistent_users = {}
        self.init_token()
   
    def init_token(self):
        app_login_args = dict(client_id=self._app_id,
                  client_secret=self._client_secret,
                  grant_type="client_credentials")
        app_login_url = "https://graph.facebook.com/oauth/access_token?%s"
    
        login_request = urllib.urlopen(app_login_url % urllib.urlencode(app_login_args))
        app_token_response = login_request.read()
    
#        print "Received token %s" % app_token_response
        
        self._app_token = app_token_response.rsplit("=")[1]
    
    def list_test_users(self):
        test_users_uri = "%s/accounts/test-users" % self._app_id
                             
        get_users_response = self._do_request(FaceBookRepository.GET, test_users_uri, dict(access_token=self._app_token))
        user_credentials = json.loads(get_users_response)
        
        user_list = []
        
        for user_data in user_credentials["data"]:
            user_list.append(TestUser(user_data["id"], user_data["login_url"],
                                      user_data["access_token"]))
            
        return user_list
    
    def add_user(self, permissions="read_stream", user_key=None):
        add_user_params = dict(access_token=self._app_token,
                        installed = "true",
                        permissions=permissions)
        app_url = "%s/accounts/test-users" % self._app_id
        
        data = self._do_request("POST", app_url, add_user_params)
        user_credential = json.loads(data)
        
        test_user = TestUser(user_credential["id"], user_credential["login_url"],
                         user_credential["access_token"], user_credential["password"])
        
        if user_key is not None:
            self._persistent_users[user_key] = test_user
            
        return test_user
    
    def delete_user(self, test_user):
        delete_user_params = dict(access_token=self._app_token)
        app_url = "/%s" % test_user.id

        data = self._do_request("DELETE", app_url, delete_user_params)        
        return data.lower() == "true"
        
    def create_friends(self, test_user, new_friend):
        user_friend_request_params = {"access_token": test_user.access_token}
        user_friend_request_url = "/%s/friends/%s" % (test_user.id, new_friend.id)
        add_friend_result = self._do_request("POST", user_friend_request_url, user_friend_request_params)
                
        user_friend_validation_params = {"access_token": new_friend.access_token}
        user_friend_request_validation_url = "/%s/friends/%s" % (new_friend.id, test_user.id)
        validate_friend_result = self._do_request("POST",
                                  user_friend_request_validation_url, user_friend_validation_params)
                
        return validate_friend_result
    
    def publish_link(self):
        raise Exception("Not Implemented")
    
    def delete_all_users(self):
        user_list = self.list_test_users()
        
        return_value = True
        
        for test_user in user_list:
            return_value = self.delete_user(test_user)
            if return_value is False:
                break
            
        return return_value

    def find_friends(self, user):
        friends_param = {"access_token": user.access_token}
        friends_url = "/%s/friends" % user.id
        friends = self._do_request("GET", friends_url, friends_param)
        
        print "User %s friends :%s" % (user.id, friends)
        user_friends = json.loads(friends)
        user_friend_list = []
        for user_data in user_friends["data"]:
            user_friend_list.append(FaceBookUser(user_data["id"], user_data["name"]))
            
        return user_friend_list
    
    def create_link(self, user, name, url, picture, caption, description, message):
        create_link_params = {'access_token': user.access_token,
                              'name': name,
                              'link': url,
                              'picture': picture,
                              'caption': caption,
                              'description': description,
                              'message': message}
        
        link_url = "/%s/links" % user.id
        link_json = self._do_request("POST", link_url, create_link_params)
        
        link_dict = json.loads(link_json)
        
        if "error" in link_dict:
            raise FacebookExceptionFactory.createException(link_dict)
        
        
        return FaceBookLink(link_dict["id"])

    def create_comment(self, link, user, comment):
        create_link_params = {'access_token': user.access_token,
                              'message': comment}
        
        link_url = "/%s/comments" % link.id
        link_json = self._do_request("POST", link_url, create_link_params)
        
        link_dict = json.loads(link_json)
        
        if "error" in link_dict:
            raise FacebookExceptionFactory.createException(link_dict)
        
        
        return "151669121567304_1288680"
    
    def find_object(self, user, object_id):
        links_param = {"access_token": user.access_token}
        links_url = "%s" % object_id.split("_")[1]
        user_object_json = self._do_request("GET", links_url, links_param)
        user_object_dict = json.loads(user_object_json)
        print "User %s object %s :%s" % (user.id, object_id, user_object_dict)
        return user_object_dict
    
#    get_users_url = "https://graph.facebook.com/10150125414350721/accounts/test-users?%s" % urllib.urlencode(dict(access_token=))
#    get_users_request = urllib.urlopen(get_users_url)
#    get_user_response = get_users_request.read()
#    
#    user_credentials = json.load(StringIO(data))
#    print user_credentials
#    
#    user_details_request = urllib.urlopen("https://graph.facebook.com/%s/home&access_token=%s" % (user_credentials["id"], user_credentials["access_token"]))
#    print user_details_request.read()
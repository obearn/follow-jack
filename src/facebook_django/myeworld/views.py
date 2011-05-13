# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template.context import RequestContext
from django.utils.safestring import mark_safe
from facebook_django.model.facebook_objects import FaceBookLink,\
    FaceBookUserCoordinates
from facebook_django.myeworld.utils import GenericTree
import json
import urllib



class FaceBookAuthenticationException(Exception):
    pass

class UnknownFacebookException(Exception):
    pass

class FacebookExceptionFactory():
    EXCEPTION_MAP = {'OAuthException': FaceBookAuthenticationException}
    
    @classmethod
    def createException(cls, json_error_dict):
        if "error" in json_error_dict:
            error_desc = json_error_dict["error"]
            if "message" in error_desc and "type" in error_desc:
                expection_type = error_desc["type"]
                if expection_type in cls.EXCEPTION_MAP:
                    return  cls.EXCEPTION_MAP[expection_type](error_desc["message"])
            else:
                return Exception("Invalid facebook error message, message/type key not found %s" % json_error_dict)
        else:
            return Exception("Invalid facebook error message, error key not found %s" % json_error_dict)
      
def console(request):
    current_user = None
    console_data = None
    console = ""
    if "profile" in request.session:
        current_user = request.session["profile"]
        
        if "console" in request.POST:
            console = request.POST["console"]
            access_token = request.session["access_token"]
            json_dict = get_json_dict(console, access_token)
            console_data = GenericTree(id="console_data").format(json_dict)
        
    return render_to_response("console.html", {'current_user': current_user,
                                               "console": console,
                                                "fb_data": mark_safe(console_data)},
                                                 context_instance=RequestContext(request))

def fql(request):
    current_user = None
    console_data = None
    console = ""
    if "profile" in request.session:
        current_user = request.session["profile"]
        
        if "console" in request.POST:
            console = request.POST["console"]
            access_token = request.session["access_token"]
            json_dict = get_fql_dict(console, access_token)
            console_data = GenericTree(id="console_data").format(json_dict)
        
    return render_to_response("fql.html", {'current_user': current_user,
                                               "console": console,
                                                "fb_data": mark_safe(console_data)},
                                                 context_instance=RequestContext(request))
    
def user_links(request, user_id):
    graph_api = "%s/links" % user_id
    access_token = request.session["access_token"]
    json_dict = get_json_dict(graph_api, access_token)
    
    links = []
    for link_data in json_dict["data"]:
        links.append(FaceBookLink(link_data["id"], link_data["from"]["name"],
                                   link_data.get("name","Unknown"),
                                   link=link_data.get("link", "Unknown"),
                                   created_time=link_data.get("created_time", "Unknown")))
    
    if "profile" in request.session:
        current_user = request.session["profile"]
    
    #FIXME add facebook url in facebook object
    return render_to_response("links.html", {"links": links, 'current_user': current_user,
                                             "access_token": access_token})

def get_json_dict(grah_api, token):
    if "?" in grah_api:
        request_uri = grah_api + "&%s" % token
    else:
        request_uri = grah_api + "?%s" % token
        
    grah_api_url = "https://graph.facebook.com/%s" 
    grah_api_request = urllib.urlopen(grah_api_url % request_uri)
    json_data = grah_api_request.read()
    json_dict = json.loads(json_data)
    if "error" in json_dict:
        raise FacebookExceptionFactory.createException(json_dict)
    return json_dict

def get_fql_dict(fql_request, token):
    fql_params = dict(query=fql_request)   
    fql_url = "https://api.facebook.com/method/fql.query?%s&%s" % (urllib.urlencode(fql_params), token)
    grah_api_request = urllib.urlopen(fql_url)
    json_data = grah_api_request.read()
    json_dict = json.loads(json_data)
    if "error" in json_dict:
        raise FacebookExceptionFactory.createException(json_dict)
    return json_dict

def index(request):  
    if "profile" in request.session:
        current_user = request.session["profile"]
        access_token = request.session["access_token"]
        json_dict = get_json_dict("me/friends", access_token)
        
        user_friends = []
        for user_data in json_dict["data"]:
            user_friends.append(FaceBookUserCoordinates(user_data["id"], user_data["name"]))
    
        return render_to_response("index.html", {'current_user': current_user, "user_friends": user_friends}, context_instance=RequestContext(request))
    else:
        return redirect("/myeworld/login")
    
FACEBOOK_APP_ID = "10150125414350721"
FACEBOOK_APP_SECRET = "745e73889c2f4829832d4a8c36f9499c"
def login(request):
    validation_code = None
    if "code" in request.GET:
        validation_code = request.GET["code"]
        absolute_uri = request.build_absolute_uri()
        redirect_uri = absolute_uri.split("?")[0]
        args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=redirect_uri)
        args["client_secret"] = FACEBOOK_APP_SECRET
        args["code"] = validation_code
    
        token_request_url = "https://graph.facebook.com/oauth/access_token?%s"
        token_request = urllib.urlopen(token_request_url % urllib.urlencode(args))
        response = token_request.read()
        
        profile = json.load(urllib.urlopen(
            "https://graph.facebook.com/me?%s" % response))

        request.session["profile"] = profile
        request.session["access_token"] = response
        return redirect("/myeworld/")
    else:
        absolute_uri = request.build_absolute_uri()
        redirect_uri = absolute_uri.split("?")[0]
        args = dict(client_id=FACEBOOK_APP_ID, redirect_uri=redirect_uri)
        return redirect(
            "https://www.facebook.com/dialog/oauth?" +
            urllib.urlencode(args))
        
def logout(request):
     if "profile" in request.session:
         request.session.pop("profile")
     
     return redirect("/myeworld/")
    
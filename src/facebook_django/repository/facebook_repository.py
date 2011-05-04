'''
Created on 2 mai 2011

@author: obearn
'''
import urllib
import httplib

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
      

class FaceBookRepository(object):
    
    GET  = 'GET'
    POST = 'POST'
    
    FACEBOOK_GRAPH_SERVER = "graph.facebook.com"
    FACEBOOK_GRAPH_URL    = "https://%s" % FACEBOOK_GRAPH_SERVER
    
    def __init__(self, debug_level=0):
        self._debug_level = debug_level
        
    def _do_request(self, mode, uri, params):
        data = None
        
        if mode == FaceBookRepository.GET:
            get_url = "%s/%s?%s" % \
                            (FaceBookRepository.FACEBOOK_GRAPH_URL, uri, urllib.urlencode(params))
            
            get_request = urllib.urlopen(get_url)
            
            data = get_request.read()
        else:
            conn = httplib.HTTPSConnection(FaceBookRepository.FACEBOOK_GRAPH_SERVER)
            conn.request(mode, uri, urllib.urlencode(params) if params is not None else None)
            
            response = conn.getresponse()
            data = response.read()
            
            conn.close()
        
        return data
    
    
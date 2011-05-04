from facebook_django.repository.facebook_repository import FaceBookRepository
import json
from facebook_django.model.facebook_objects import FaceBookLink

class FaceBookLinkRepository(FaceBookRepository):
    
    def find_links(self, user):
        links_param = {"access_token": user.access_token}
        links_url = "/%s/links" % user.id
        user_links_json = self._do_request("GET", links_url, links_param)
        user_links_dict = json.loads(user_links_json)
        links = []
        for link in user_links_dict["data"]:
            facebook_link = self._create_facebook_link(link)
            links.append(facebook_link)
        
        return links
    
    #TODO Refactor facebookobject creation
    def _extract_json_field(self, json_dict, *fields):
        if len(fields) == 1:
            field = fields[0]
            return json_dict[field] if field in json_dict else None
        elif len(fields) > 1:
            field = fields[0]
            return self._extract_json_field(json_dict[field], *fields[1:]) if field in json_dict else None 
        return None
    
    #TODO Refactor facebookobject creation
    def _create_facebook_link(self, link):
        facebook_link = FaceBookLink(
                              link['id'], 
                              link['from']['id'],
                              link['name'], 
                              link['link'],
                              link['picture'],
                              self._extract_json_field(link, 'caption'),
                              self._extract_json_field(link, 'description'),
                              link['message'],
                              created_time = self._extract_json_field(link, 'created_time'),
                              comments = self._extract_json_field(link, 'comments', 'data'))
        
        return facebook_link
    
    def find_link(self, user, id):
        links_param = {"access_token": user.access_token}
        links_url = "%s" % id
        user_links_json = self._do_request("GET", links_url, links_param)
        link = json.loads(user_links_json)
        
        facebook_link = self._create_facebook_link(link)
                
        return facebook_link
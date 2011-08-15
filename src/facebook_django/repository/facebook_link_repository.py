from facebook_django.model.facebook_objects import FaceBookLink,\
    FaceBookListFactory
from facebook_django.repository.facebook_repository import FaceBookRepository
import json

class FaceBookLinkRepository(FaceBookRepository):
    
    def find_links(self, user):
        links_param = {"access_token": user.access_token}
        links_url = "/%s/links" % user.id
        user_links_json = self._do_request("GET", links_url, links_param)
        links = FaceBookListFactory.loads(json.dumps(user_links_json), FaceBookLink)
        return links
    
    def find_link(self, user, id):
        link_param = {"access_token": user.access_token}
        link_url = "%s" % id
        user_links_json = self._do_request("GET", link_url, link_param)
        facebook_link = FaceBookLink.loads(user_links_json)
        return facebook_link
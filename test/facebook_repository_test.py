from unittest import TestCase
from django.test.simple import DjangoTestSuiteRunner
import json
from facebook_django.model.facebook_objects import FaceBookLink, FaceBookComment,\
    FaceBookObject, FaceBookBase, FaceBookUserCoordinates
import re
from facebook_django.repository.facebook_repository import FaceBookRepository
from types import StringType
import datetime
from date_utils import utc

test_runner = DjangoTestSuiteRunner()
test_runner.setup_test_environment()
test_runner.setup_databases()

#class FaceBookLinkRepositoryTest(TestCase):
#    
#    def test_create_link_from_json_dict(self):
#        dict = {u'picture': u'http://www.iana.org/_img/icann-logo-micro.png', u'from': {u'name': u'Helen Ambccbhechci Baowitz', u'id': u'100002332853839'}, u'name': u'IANA \u2014 Example domains', u'comments': {u'data': [{u'created_time': u'2011-05-02T20:27:36+0000', u'message': u'My 2 cents', u'from': {u'name': u'Jennifer Ambbifiachjh Dingleberg', u'id': u'100002296913808'}, u'id': u'164289640297819_1645251'}]}, u'link': u'http://www.example.com/article.html', u'created_time': u'2011-05-02T20:27:29+0000', u'message': u'User Message', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v1/yD/r/aS8ecmYRys0.gif', u'id': u'164289640297819', u'description': u'As described in RFC 2606, \twe maintain a number of domains such as EXAMPLE.COM and EXAMPLE.ORG \tfor documentation purposes. These domains may be used as illustrative \texamples in documents without prior coordination with us. They are  \tnot available for registration.'}
#        
#        fb_link_repos = FaceBookLinkRepository()
#        fb_link = fb_link_repos._create_facebook_link(dict)
#        
#        self.assertTrue(fb_link.comments is not None)
        

json_dict = {"id":"190575504321662",
             "from": {"name":"Elizabeth Ambdbhhjefcf Wisemansky","id":"100002428805636"},
             "message":"User Message",
             "picture":"http:\/\/www.iana.org\/_img\/icann-logo-micro.png",
             "link":"http:\/\/www.iana.org\/domains\/example\/",
             "name":"IANA \u2014 Example domains",
             "description":"As described in RFC 2606, \twe maintain a number of domains such as EXAMPLE.COM and EXAMPLE.ORG \tfor documentation purposes. These domains may be used as illustrative \texamples in documents without prior coordination with us. They are  \tnot available for registration.",
             "icon":"http:\/\/static.ak.fbcdn.net\/rsrc.php\/v1\/yD\/r\/aS8ecmYRys0.gif",
             "created_time":"2011-05-11T21:49:39+0000",
             "comments": {"data":[{"id":"190575504321662_2453948","from":{"name":"Lisa Ambdeceheeid Martinazziman","id":"100002453585594"},"message":"My 2 cents","created_time":"2011-05-11T21:49:40+0000"}]}}

class FaceBookRepositoryTest(TestCase):
 
    def test_decode_link_id(self):       
        test_dict = {"id":"161660850563710"}
        
        facebook_link = FaceBookLink.loads(json.dumps(test_dict))
        
        self.assertTrue(isinstance(facebook_link, FaceBookLink), facebook_link)
        self.assertTrue(isinstance(facebook_link, FaceBookObject), facebook_link)
        self.assertEqual(facebook_link.id, test_dict["id"])
        
    
    def test_decode_simple_unicode_field(self):
        test_dict = {"id":"190575504321662",
             "message":"User Message"}
        
        facebook_link = FaceBookLink.loads(json.dumps(test_dict))
        
        message = facebook_link.message
        self.assertTrue(message is not None, "Property message not set")
        self.assertTrue(isinstance(message, unicode), "Found %s::%s" % (type(message), str))
        self.assertEqual(facebook_link.message, test_dict["message"])
    
    def test_decode_simple_date_field(self):
        test_dict = {"id":"190575504321662",
                     "created_time":"2011-05-11T21:49:39+0000"}
        
        facebook_link = FaceBookLink.loads(json.dumps(test_dict))
        
        created_time = facebook_link.created_time
        #TODO assert field
        self.assertTrue(created_time is not None, "Property message not set")
        self.assertTrue(isinstance(created_time, datetime.datetime))
        self.assertEqual(datetime.datetime(2011, 5, 11, 21, 49, 39, tzinfo=utc), created_time)
                     
    def test_decode_mapped_field(self):
        test_dict = {"id":"190575504321662",
                     "from": {"name":"Elizabeth Ambdbhhjefcf Wisemansky","id":"100002428805636"}}
        
        facebook_link = FaceBookLink.loads(json.dumps(test_dict))
        
        facebook_user_coord = facebook_link.from_user
        self.assertTrue(facebook_user_coord is not None, "Property facebook_user_coord not set")
        
        #TODO refactor assert facebookusercoord from dict
        self.assertTrue(isinstance(facebook_user_coord, FaceBookUserCoordinates), "Expected %s, Found %s" % (FaceBookUserCoordinates, type(facebook_user_coord)))
        self.assertEqual(facebook_user_coord.id, test_dict["from"]["id"])
        self.assertEqual(facebook_user_coord.name, test_dict["from"]["name"])
        
    def test_decode_list_field(self):
        test_dict = {"id":"190575504321662",
             "comments": {"data":[{"id":"190575504321662_2453948","from":{"name":"Lisa Ambdeceheeid Martinazziman","id":"100002453585594"},"message":"My 2 cents","created_time":"2011-05-11T21:49:40+0000"}]}}

        facebook_link = FaceBookLink.loads(json.dumps(test_dict))
        comments = facebook_link.comments
        
        #TODO refactor add assertInstanceOf
        self.assertTrue(comments is not None)
        self.assertTrue(isinstance(comments, list))
        self.assertEqual(len(comments), 1)
        comment = comments[0]
        self.assertTrue(isinstance(comment, FaceBookComment))
        self.assertEqual(test_dict["comments"]["data"][0]["id"], comment.id)
        self.assertEqual(test_dict["comments"]["data"][0]["message"], comment.message)
        #TODO refactor assert facebookusercoord from dict
        facebook_user_coord_dict = test_dict["comments"]["data"][0]["from"]
        
        self.assertTrue(isinstance(comment.from_user, FaceBookUserCoordinates), "Expected %s, Found %s" % (FaceBookUserCoordinates, type(comment.from_user)))
        self.assertEqual(comment.from_user.id, facebook_user_coord_dict["id"])
        self.assertEqual(comment.from_user.name, facebook_user_coord_dict["name"])
        
        
    #TODO def test_decode_empty_list_field(self):
    #TODO def test_decode_multiple_items_list_field(self): ??
    
class FaceBookJSONEncodeTest(TestCase):
    def test_id_field(self):
        link  = FaceBookLink(0)
        
        self.assertTrue(isinstance(link, FaceBookObject))
        self.assertTrue(isinstance(link, FaceBookLink))
        
        self.assertEqual(link.json(), '{"id": %s}' % link.id)
        
    def test_simple_argument(self):
        link  = FaceBookLink(0)
        link.link = "link_url"
        
        self.assertEqual(link.json(), '{"link": "%s", "id": 0}' % link.link)
        
    def test_facebook_field(self):
        link  = FaceBookLink(0)
        link.from_user = FaceBookUserCoordinates(7)
        link.from_user.name = "Adam"
        
        json_link = link.json()
        
        self.assertTrue(re.search('"from_user": {.*}', json_link), json_link)
        self.assertTrue(re.search('"id": %s' % link.from_user.id, json_link), json_link)
        
    def test_list_fb_object_field(self):
        link  = FaceBookLink(0)
        comment_253 = FaceBookComment(253)
        comment_253.message = "comment_253"
        link.comments = [comment_253, ]
        
        json_link = link.json()
        
        self.assertTrue(re.search('"comments": \[.*\]', json_link), json_link)
        for comment in link.comments:
            self.assertTrue(re.search('"message": "%s"' % comment.message, json_link), json_link)
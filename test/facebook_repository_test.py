from unittest import TestCase
from facebook_django.repository.facebook_link_repository import FaceBookLinkRepository

class FaceBookLinkRepositoryTest(TestCase):
    
    def test_create_link_from_json_dict(self):
        dict = {u'picture': u'http://www.iana.org/_img/icann-logo-micro.png', u'from': {u'name': u'Helen Ambccbhechci Baowitz', u'id': u'100002332853839'}, u'name': u'IANA \u2014 Example domains', u'comments': {u'data': [{u'created_time': u'2011-05-02T20:27:36+0000', u'message': u'My 2 cents', u'from': {u'name': u'Jennifer Ambbifiachjh Dingleberg', u'id': u'100002296913808'}, u'id': u'164289640297819_1645251'}]}, u'link': u'http://www.example.com/article.html', u'created_time': u'2011-05-02T20:27:29+0000', u'message': u'User Message', u'icon': u'http://static.ak.fbcdn.net/rsrc.php/v1/yD/r/aS8ecmYRys0.gif', u'id': u'164289640297819', u'description': u'As described in RFC 2606, \twe maintain a number of domains such as EXAMPLE.COM and EXAMPLE.ORG \tfor documentation purposes. These domains may be used as illustrative \texamples in documents without prior coordination with us. They are  \tnot available for registration.'}
        
        fb_link_repos = FaceBookLinkRepository()
        fb_link = fb_link_repos._create_facebook_link(dict)
        
        self.assertTrue(fb_link.comments is not None)
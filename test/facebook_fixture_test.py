from unittest import TestCase, TestSuite
from facebook_fixture import FaceBookFixture, TestUser, FaceBookUserCoordinates
import unittest
from facebook_django.repository.facebook_link_repository import FaceBookLinkRepository

APP_ID = "10150125414350721"
CLIENT_SECRET = "745e73889c2f4829832d4a8c36f9499c"

class FacebookFixtureUserManagementTest(TestCase):
    
    def setUp(self):
        self._facebook_fixture = FaceBookFixture(APP_ID, CLIENT_SECRET)
    
    def tearDown(self):
        self._facebook_fixture.delete_all_users()
        
    def test_add_user(self):
        #SUT
        test_user = self._facebook_fixture.add_user()
              
        #Assertions
        self.assertTrue(isinstance(test_user, TestUser))
        
        list_users = self._facebook_fixture.list_users()
        self.assertTrue(list_users is not None and len(list_users) > 0)
        for test_user in list_users:
            self.assertTrue(isinstance(test_user, TestUser))
        
    def test_delete_all_users(self):
        #Fixture
        self._facebook_fixture.add_user()
        self._facebook_fixture.add_user()
        self._facebook_fixture.add_user()
        
        #SUT
        return_value = self._facebook_fixture.delete_all_users()
        
        #Assertions
        self.assertTrue(return_value is True)
        list_users = self._facebook_fixture.list_users()
        self.assertTrue(list_users is not None and len(list_users) == 0)
        
    def test_delete_user(self):
        #Fixture
        self._facebook_fixture.delete_all_users()
        user1 = self._facebook_fixture.add_user()
        user2 = self._facebook_fixture.add_user()
        user3 = self._facebook_fixture.add_user()
        
        #SUT
        return_value = self._facebook_fixture.delete_user(user2)
        
        #Assertions
        self.assertTrue(return_value is True)
        list_users = self._facebook_fixture.list_users()
        self.assertEqual(len(list_users), 2)
        self.assertTrue(user1 in list_users)
        self.assertTrue(user2 not in list_users)
        self.assertTrue(user3 in list_users)
        
    def test_create_friends(self):
        #Fixture
        user1 = self._facebook_fixture.add_user()
        user2 = self._facebook_fixture.add_user()
        
        #SUT
        return_value = self._facebook_fixture.create_friends(user1, user2)
        
        #Assertions
        self.assertTrue(return_value)
        
    def test_find_friends(self):
        #Fixture
        user1 = self._facebook_fixture.add_user()
        user2 = self._facebook_fixture.add_user()
        self._facebook_fixture.create_friends(user1, user2)
        
        #SUT
        user_friends = self._facebook_fixture.find_friends(user1)  
        
        #Assertions
        self.assertTrue(user_friends is not None)
        self.assertEqual(len(user_friends), 1)
        
        user_friend = user_friends[0]
        self.assertTrue(isinstance(user_friend, FaceBookUserCoordinates))
        self.assertEqual(user2.id, user_friend.id)

class FixtureFixtureLinkManagementTest(TestCase):
    
    def setUp(self):
        self._facebook_fixture = FaceBookFixture(APP_ID, CLIENT_SECRET)
        self._link_user    = self._facebook_fixture.add_user(permissions='read_stream,share_item', user_key="link_user")
        self._friend_user = self._facebook_fixture.add_user(user_key="friend_user")
        self._facebook_fixture.create_friends(self._link_user, self._friend_user)
        self._facebook_link_repository = FaceBookLinkRepository()
        
    def tearDown(self):
        self._facebook_fixture.delete_all_users()
        
    def _create_test_link(self):
        facebook_link = self._facebook_fixture.create_link(self._link_user,
                                           'Article Title',
                                           'http://www.example.com/article.html',
                                           'http://www.example.com/article-thumbnail.jpg',
                                           'Caption for the link',
                                           'Longer description of the link',
                                           'User Message')
        return facebook_link
    
    def test_create_link(self):        
        #SUT
        facebook_link = self._create_test_link()
        
        #Assertions
        user_links = self._facebook_link_repository.find_links(self._link_user)
        self.assertTrue(facebook_link in user_links)
                
    def test_create_comment(self):
        #Fixture
        facebook_link = self._create_test_link()
        
        #SUT
        comment_id = self._facebook_fixture.create_comment(facebook_link, self._friend_user, "My 2 cents")
        
        #Assertions
        updated_link = self._facebook_link_repository.find_link(self._link_user, facebook_link.id)
        
        self.assertTrue(comment_id in [comment.id for comment in updated_link.comments],
                         "Comment %s not found in %s" % (comment_id, updated_link.comments))
        
        
        
if __name__ == '__main__':
    test_suite = TestSuite([FixtureFixtureLinkManagementTest("test_create_comment")])
    unittest.TextTestRunner(verbosity=2).run(test_suite)

#    
#    
#    
#    
#    owner_token_url_args = dict(client_id="obearn@yahoo.fr", client_secret=pw, grant_type="client_credentials")
#    owner_token_url = "https://graph.facebook.com/oauth/access_token?%s"
#    owner_token_request = urllib.urlopen(owner_token_url % urllib.urlencode(owner_token_url_args))
#    owner_token = owner_token_request.read()
#    
#    print "Owner token %s" % owner_token
    

    

    
#    
#    insight_request = urllib.urlopen("https://graph.facebook.com/test/insights?access_token=%s" % app_token.split("=")[1])
#    insight_response = insight_request.read()
#    
#    print "Insights : \n%s" % insight_response
#    
    
#    add_user_params = dict(access_token=app_token.rsplit("=")[1],
#                           installed = "true",
#                           permissions="read_stream")
#    
#    app_url = "10150125414350721/accounts/test-users"
#    print app_url
#    import httplib
#    conn = httplib.HTTPSConnection("graph.facebook.com")
#    conn.debuglevel = 9
#    conn.request("POST", app_url, urllib.urlencode(add_user_params))
#    response = conn.getresponse()
#    print response.status
#    data = response.read()  
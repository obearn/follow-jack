from unittest import TestCase
from facebook_django.model.facebook_objects import FaceBookUserCoordinates

class FaceBookUserRepositoryTest(TestCase):

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
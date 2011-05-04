from __future__ import with_statement
import json
from facebook_django.myeworld.models import MyContent
from facebook_django.myeworld.filter import Filter
import pprint
from unittest import TestCase

class VideoFilterTest(TestCase):
    
    def load_data(self, file_name):
        return json.load(file_name)
    
    def setUp(self):
        self._filter = Filter()
        
    def test_filter_youtube(self):
        self.print_json("resources/test/statuses.json")
        statuses = self.load_data("resources/test/statuses.txt")
        
        expected_content = MyContent()
        expected_content.content = "test"
        expected_content.user    = 576279899

        contents = self._filter.filter(statuses)
        
        self.asserTrue(expected_content in contents)

    def print_json(self, file_name):
        with open(file_name, "r") as file:
            statuses = self.load_data(file)
            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(statuses)

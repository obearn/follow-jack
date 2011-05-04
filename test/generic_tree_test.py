from unittest import TestCase, TestLoader, TestSuite
from facebook_django.myeworld.utils import GenericTree
import unittest

class GenericTreeTest(TestCase):

    def setUp(self):
        self._generic_tree = GenericTree()
    
    def test_json_root_None(self):
        json_root = {"root": None}
        json_tree = self._generic_tree.format(json_root)
        self.assertEqual(json_tree, "<ul><li>root</li></ul>")
        
     
    def test_json_root_leafs(self):
        json_leaf_value = {"leaf1": "value1", "leaf2": "value2"}
        json_tree = self._generic_tree.format(json_leaf_value)
        self.assertEqual(json_tree, "<ul><li>leaf1: value1</li><li>leaf2: value2</li></ul>")
        
    
    def test_json_root_child(self):
        json_child_value = {"parent": {"child": "value",}}
        json_tree = self._generic_tree.format(json_child_value)
        self.assertEqual(json_tree, "<ul><li>parent<ul><li>child: value</li></ul></li></ul>")
     
    
    def test_json_grand_child(self):
        json_grand_child_value = {"grandpa": {"parent": {"child": "thechild"}}}
        json_tree = self._generic_tree.format(json_grand_child_value)
        self.assertEqual(json_tree, "<ul><li>grandpa" \
                                    "<ul><li>parent" \
                                    "<ul><li>child: thechild</li></ul>" \
                                    "</li></ul>" \
                                    "</li></ul>")
    
    def test_json_child_list(self):
        json_child_list = {"parent": [{"id": "1213213213", "name": "child1"}, {"id": "1213213214", "name":"child2"}, ]}
        json_tree = self._generic_tree.format(json_child_list)
        expected = "<ul><li>parent" \
                        "<ul>" \
                            "<li>1213213213" \
                                "<ul><li>name: child1</li></ul>" \
                            "</li>" \
                            "<li>1213213214" \
                                "<ul><li>name: child2</li></ul>" \
                            "</li>" \
                        "</ul>" \
                    "</li></ul>"
                                    
        self.assertEqual(json_tree, expected, "\n%s\n%s" %(json_tree, expected))
    
    def test_json_complex_child_list(self):
        json_child_list = {"parent": [{"id": "child_id", "att1": "value1", "att2": "value2"}, ]}
        json_tree = self._generic_tree.format(json_child_list)
        expected = "<ul><li>parent" \
                    "<ul><li>child_id" \
                    "<ul>" \
                    "<li>att2: value2</li>" \
                    "<li>att1: value1</li>" \
                    "</ul>" \
                    "</li></ul>" \
                    "</li></ul>"
        self.assertEqual(json_tree, expected, "\n%s\n%s" %(json_tree, expected))
        
    def test_format_id(self):
        id = "myid"
        generict_tree = GenericTree(id)
        
        json_tree = generict_tree.format({"root": None})
        
        expected_result = '<ul id="%s"><li>root</li></ul>' % id
        self.assertEqual(json_tree, expected_result)
        
if __name__ == '__main__':
    suite = TestSuite([GenericTreeTest("test_json_child_list"), ])
    unittest.TextTestRunner(verbosity=2).run(suite)
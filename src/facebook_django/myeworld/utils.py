from pprint import pprint
class GenericTree(object):
    
    def __init__(self, id=None):
        self._id = id
        
    def format(self, json_dict):
        if self._id is not None:
            html_tree = '<ul id="%s">' % self._id
        else:
            html_tree = "<ul>"
            
        for key, value in json_dict.items():
            html_tree += self.format_item({key: value})
        return html_tree + "</ul>"
    
    def format_item(self, item):
        html_tree = ""
        for key, value in item.items():
            if value is not None:
                if isinstance(value, list):
                    html_tree += "<li>%s<ul>" % key
                    html_tree += "".join("<li>%s<ul>%s</ul></li>" % (list_item.pop("id"), self.format_item(list_item)) for list_item in value)
                    html_tree += "</ul></li>"
                elif isinstance(value, dict):
                    html_tree += "<li>%s<ul>%s</ul></li>" % (key, self.format_item(value))
                else:
                    html_tree += "<li>%s: %s</li>" % (key, value)
            else:
                html_tree = "<li>%s</li>" % key
        return html_tree


import simplejson
import json
from facebook_django.repository.facebook_user_repository import FacebookUserRepository
import datetime
from dateutil.parser import parse

class FaceBookAttr(object):
    def __init__(self, type, json_field=None):
        self.type = type
        self.json_field = json_field

    def set_value(self, obj, name, value):
        if issubclass(self.type, FaceBookObject):
            value_object = self.type.load_dict(value)
            setattr(obj, name, value_object)
        else:
            #TODO do we support literals as values
            setattr(obj, name, value)
            
class FaceBookDateAttr(FaceBookAttr):
    def __init__(self):
        super(FaceBookDateAttr, self).__init__(datetime.datetime)
        
    def set_value(self, obj, name, value):
        datetime_value = parse(str(value))
        setattr(obj, name, datetime_value)
        
class ListOf(FaceBookAttr):
    
    def set_value(self, obj, name, value):
        if isinstance(value, dict):
            data = value["data"]
        elif isinstance(value, list):
            data = value
        else:
            raise Exception("Unsupported type for ListOf attribute data : %s" % type(value))
        list_value = []
        for object_dict in data:
            item = self.type.load_dict(object_dict)
            list_value.append(item)
        setattr(obj, name, list_value)
        
class FaceBookBase(type):
    """
    Metaclass for all facebook objects.
    """
    def __new__(cls, name, bases, attrs):
        setattr(cls, "json_field_mapping",  {})
        
        for obj_name, obj in attrs.items():
            if isinstance(obj, FaceBookAttr):
                if obj.json_field is not None:
                    cls.json_field_mapping[obj.json_field] = obj_name
            
        return type.__new__(cls, name, bases, attrs)
    
    def add_json_field_mapping(self):
       pass
    
class FaceBookEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, FaceBookObject):
            print "encode facebookobject %s\n" % obj.__class__
            return obj.__dict__
        print "encode object %s" % type(obj)
        return simplejson.JSONEncoder.default(self, obj)

class FaceBookObject(object):
    __metaclass__ = FaceBookBase
    
    def __init__(self, id):
        super(FaceBookObject, self).__init__()
        self.id = id

    def __eq__(self, other):
        if hasattr(other, "id") and other.id == self.id:
            return True
        return False
    
    def __hash__(self):
        return self.id
    
    def json(self):
        return simplejson.dumps(self, cls=FaceBookEncoder)

    def __getattritbute__(self, name):
        print "looking for %s" % name 
        
    @classmethod
    def loads(cls, data_string):
        json_dict = json.loads(data_string)
        return cls.load_dict(json_dict)
        
    @classmethod
    def load_dict(cls, object_dict):
        id = None
        if "id" in object_dict:
            id = object_dict.pop("id")
        
        facebook_object =  cls(id)
        
        for key, value in object_dict.items():
            if not hasattr(facebook_object, key):
                field_mapping = cls.json_field_mapping.get(key)
                if field_mapping is not None:
                    key = field_mapping
                else:
                    #TODO log warning
                    continue
            
            class_field = getattr(cls, key)
            if isinstance(class_field, FaceBookAttr):
                class_field.set_value(facebook_object, key, value)
            else:
                #TODO do we support literals as values
                raise Exception("%s.%s is not a facebook field" % (str(cls), key))
            
        return facebook_object
    
class FaceBookUserCoordinates(FaceBookObject):   
    name = FaceBookAttr(str)
    
    def __init__(self, id):
        super(FaceBookUserCoordinates, self).__init__(id)
        

class FaceBookComment(FaceBookObject):
    created_time = FaceBookDateAttr()
    message = FaceBookAttr(str)
    from_user = FaceBookAttr(FaceBookUserCoordinates, json_field="from")
          
class FaceBookPaging(FaceBookObject):
    next = FaceBookAttr(str)
    previouse = FaceBookAttr(str)
     
class FaceBookListFactory():
    
    @classmethod
    def loads(cls, data_string, item_type):
        face_book_list_type = type("FaceBookList%s" % item_type, (FaceBookList, ), {"data":ListOf(item_type)})
        return face_book_list_type.loads(data_string)
    
class FaceBookList(FaceBookObject):
    paging = FaceBookAttr(FaceBookPaging)
    
class FaceBookLink(FaceBookObject):
#    name = models.CharField(max_length=200)
#    link = models.CharField(max_length=200)
#    picture = models.CharField(max_length=200)
#    caption = models.CharField(max_length=200)
#    description = models.CharField(max_length=200)
#    message = models.CharField(max_length=200)
#    created_time = models.DateField(max_length=200)
    
#    name = None
    link = FaceBookAttr(str)
    message = FaceBookAttr(str)
    from_user = FaceBookAttr(FaceBookUserCoordinates, json_field="from")
    comments = ListOf(FaceBookComment)
#    picture = None
#    caption = None
#    description = None
    created_time = FaceBookDateAttr()
    
    
    def __init__(self, id, from_user=None, name=None, link=None,
                 picture=None, caption=None, description=None, message=None,
                 created_time=None, comments=None):
        super(FaceBookLink, self).__init__(id)
        
#        self.name           = name
#        self.from_user      = from_user
#        self.link           = link
#        self.picture        = picture
#        self.caption        = caption
#        self.description    = description
#        self.message        = message
#        self.created_time   = created_time
#        self.comments       = comments
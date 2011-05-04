class FaceBookObject(object):
    
    def __init__(self, id):
        self.id = id

    def __eq__(self, other):
        if hasattr(other, "id") and other.id == self.id:
            return True
        return False
    
    def __hash__(self):
        return self.id
           
class FaceBookUser(FaceBookObject):
        
    def __init__(self, id, name):
        super(FaceBookUser, self).__init__(id)
        self.name = name
        
class FaceBookLink(FaceBookObject):
    
    def __init__(self, id, from_user=None, name=None, link=None,
                 picture=None, caption=None, description=None, message=None,
                 created_time=None, comments=None):
        super(FaceBookLink, self).__init__(id)
        self.name           = name
        self.from_user      = from_user
        self.link           = link
        self.picture        = picture
        self.caption        = caption
        self.description    = description
        self.message        = message
        self.created_time   = created_time
        self.comments       = comments
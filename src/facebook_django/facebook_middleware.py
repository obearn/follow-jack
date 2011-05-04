from django.shortcuts import redirect
from facebook_django.myeworld.views import FaceBookAuthenticationException

class FaceBookAuthenticationMiddleWare(object):
	
	def process_exception(self, request, exception):
		if isinstance(exception, FaceBookAuthenticationException):
			if "profile" in request.session:
				request.session.pop("profile")
			return redirect("/myeworld/login")
	
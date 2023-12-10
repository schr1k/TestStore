from django.http import HttpResponse


def index(request):
    return HttpResponse("Add /admin into url to administrate database")

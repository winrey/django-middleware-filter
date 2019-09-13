from django.http import HttpResponse

def default_view(request):
    return HttpResponse("This is just a test view")
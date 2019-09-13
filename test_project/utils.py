from django.http import HttpResponse

def append(response, content):
    return HttpResponse(response.content.decode("utf-8") + content)
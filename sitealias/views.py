from django.http import HttpResponse

def my_view(request):
    return HttpResponse(b'Test Response')
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, "index.html", {})

@csrf_exempt
def test(request):
    l=request.POST.get('names')
    print l
    return HttpResponse("")


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time


# Create your views here.
@csrf_exempt
def upload(request):
    if request.method == "GET":
        return render(request, "upload/index.html")
    else:
        print(request.FILES.keys())
        for key in request.FILES.keys():
            file = request.FILES.get(key, None)
            if file:
                with open("a.bin", "wb") as a:
                    for chunk in file.chunks():
                        a.write(chunk)
        return render(request, "upload/index.html")

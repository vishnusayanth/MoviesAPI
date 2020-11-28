from django.http import JsonResponse
from app.models import RequestCounter


# Returns a response containing the number of requests processed by this API
def request_count(request):
    return JsonResponse({'requests': RequestCounter.objects.first().value})


# Resets the count of requests in the db by deleting the current object.
# New object will be created upon receiving a new request
def reset_request_count(request):
    RequestCounter.objects.all().delete()
    return JsonResponse({'message': 'request count reset successfully'})

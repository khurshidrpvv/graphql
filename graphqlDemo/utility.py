from django.core.cache import cache
from django.shortcuts import redirect

def celarCache(request):
  cache.clear()
  return redirect('graphql/')
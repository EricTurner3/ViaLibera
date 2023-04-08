from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Vehicle

# Create your views here.
@login_required
def index(request):
    vehicles = Vehicle.objects.all()
    paginator = Paginator(vehicles, 10) # 10 vehicles per page


    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Page from the theme 
    return render(request, 'index.html', {'page_obj': page_obj})
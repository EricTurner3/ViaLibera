from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core import serializers

from .models import Vehicle, SpecificationCategory, Specification, VehicleSpecification

# Create your views here.
@login_required
def index(request):
    vehicles = Vehicle.objects.all()
    paginator = Paginator(vehicles, 10) # 10 vehicles per page


    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Page from the theme 
    return render(request, 'index.html', {'page_obj': page_obj})

@login_required
def vehicle_detail_view(request, primary_key):
    vehicle = get_object_or_404(Vehicle, pk=primary_key)
    spec_cat = SpecificationCategory.objects.all().order_by("order")
    specs = VehicleSpecification.objects.all().prefetch_related("specification", "specification__category")
    return render(request, 'vehicle_detail.html', context={'vehicle': vehicle, 'categories': spec_cat, 'specs': specs})
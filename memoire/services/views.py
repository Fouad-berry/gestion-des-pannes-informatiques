from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.generic import CreateView, DeleteView, UpdateView, View, ListView, DetailView
from users.models import Service, Direction
from .forms import ServiceForm
import json
# Create your views here.


class ServiceListView(View):
    template_name="services/list.html"
    form_class= ServiceForm
    services = Service.objects.all()
    
    def get(self, request, *args, **kwargs):
        id = Service.objects.all().last().id
        return render(request, self.template_name, {"services":self.services, "form": self.form_class(), "id": id})
    

class ServiceUpdateView(UpdateView):
    model = Service
    form_class=ServiceForm
    
    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        direction_service = request.POST.get('direction_service')
        direction_service = Direction.objects.get(id=direction_service)
        service = Service.objects.get(pk=kwargs['pk'])
        if service:
            service = Service(code=code, nom=nom, direction_service=direction_service)
            service.save()
            data = {
                "message": "SUCCESS",
            }
        else:
            data = {
                "message": "ERROR",
            }
        return JsonResponse(data=data, status=200)
class ServiceCreateView(CreateView):
    model = Service
    form_class=ServiceForm
    template_name="directions/create.html"

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        direction_service = request.POST.get('direction_service')
        direction_service = Direction.objects.get(id=direction_service)
        if Service.objects.filter(code=code).exists():
            return HttpResponse('Error: A direction with the same name already exists.')

        service = Service(code=code, nom=nom, direction_service=direction_service)
        service.save()
        data= {
            "message" : "SUCCESS",
        }
        return JsonResponse(data, status=200)
    
class ServiceDetailView(DetailView):
    model = Service
    template_name = "tickets/detail.html"
    
    def get(self, request, *args, **kwargs):
        id=request.GET.get("id")
        service=Service.objects.get(pk=int(id))
        response_data = {
            "id" : service.id,
            "code" : service.code,
            "nom" : service.nom,
            "direction_service" : service.direction_service.id,
        }
        return JsonResponse(response_data)

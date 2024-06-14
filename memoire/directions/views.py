from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.views.generic import CreateView, DeleteView, UpdateView, View, ListView, DetailView
from users.models import Direction
from .forms import DirectionForm
# Create your views here.


class DirectionCreateView(CreateView):
    model = Direction
    form_class=DirectionForm
    template_name="directions/create.html"

    def post(self, request, *args, **kwargs):
        code = request.POST.get('code')
        nom = request.POST.get('nom')
        if Direction.objects.filter(nom=nom).exists():
            return HttpResponse('Error: A direction with the same name already exists.')

        direction = Direction(code=code, nom=nom)
        direction.save()
        return JsonResponse({"message": "Success"}, status=200)

class DirectionUpdateView(UpdateView):
    model = Direction
    form_class=DirectionForm
    success_url=reverse_lazy("directions:list-direction")


    # def get_object(self, queryset=None):
    #     # Retrieve the direction object based on the provided 'pk' URL parameter
    #     return Direction.objects.get(pk=self.kwargs['pk'])

    # def get(self, request, *args, **kwargs):
    #     direction = self.get_object()
    #     response_data = {
    #         'code': direction.code,
    #         'nom': direction.nom,
    #     }
    #     return JsonResponse(response_data)


class DirectionDeleteView(DeleteView):
    model = Direction
    template_name="directions/confirm_delete.html"
    success_url=reverse_lazy("directions:list-direction")


class DirectionDetailView(DetailView):
    model = Direction
    template_name = "directions/detail.html"
    
    def get(self, request, *args, **kwargs):
        direction=Direction.objects.get(pk=kwargs['pk'])
        response_data = {
            "id" : direction.pk,
            "nom" : direction.nom,
            "code" : direction.code,
        }
        return JsonResponse(response_data, status=200)


class DirectionListView(View):
    template_name="directions/list.html"
    form_class= DirectionForm
    directions = Direction.objects.all()
    
    def get(self, request, *args, **kwargs):
        direction = request.GET.get("direction_id")
        # if direction is not None:
        #     direction = Direction.objects.get(pk=direction)
        return render(request, self.template_name, {"directions":self.directions, "direction": direction, "form": self.form_class()})

    # def post(self, request, *args, **kwargs):
    #     direction = request.POST.get("id")
    #     nom = request.POST.get("nom")
    #     code = request.POST.get("code")
    #     try:
    #         direction = Direction.objects.get(pk=direction)
    #         if direction:
    #             if nom != None :
    #                 direction.nom = nom
    #                 direction.save()
    #             elif code != None:
    #                 direction.code = code
    #                 direction.save()
    #             elif nom != None and code != None:
    #                 direction.nom = nom
    #                 direction.code = code
    #                 direction.save()
    #         else:
    #             direction = Direction(nom=nom, code=code)
    #             direction.save()
    #     except:
    #         messages = "error in your code"
    #     return render(request, self.template_name, {"directions":self.directions})

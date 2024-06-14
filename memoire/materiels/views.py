from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from users.models import Materiel, Employee
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView
from .forms import MaterielForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
# Create your views here.

class MaterielCreateView(View):
    model = Materiel
    form_class=MaterielForm

    def get(self, request, *args, **kwargs):
        return redirect("materiels:list-materiel")
    
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST, request.FILES)
        try:
            last_id=Materiel.objects.last().id  + 1
        except :
            last_id=1
        nom = request.POST.get('nom')
        materiel = Materiel.objects.filter(nom=nom).first()
        if materiel:
            materiel.marque = request.POST.get('marque')
            materiel.modele = request.POST.get('modele')
            materiel.type = request.POST.get('type')
            materiel.annee_mise_en_service = request.POST.get('annee_mise_en_service')
            materiel.etat_fonctionnement = request.POST.get('etat_fonctionnement')
            materiel.utilisateur = request.POST.get('utilisateur')
        else:
            nom = request.POST.get('nom')
            marque = request.POST.get('marque')
            modele = request.POST.get('modele')
            type = request.POST.get('type')
            image = request.POST.get('image')
            annee_mise_en_service = request.POST.get('annee_mise_en_service')
            etat_fonctionnement = request.POST.get('etat_fonctionnement')
            utilisateur = request.POST.get('utilisateur')
            if utilisateur == "":
                materiel = Materiel(nom=nom, marque=marque, modele=modele, type=type, annee_mise_en_service=annee_mise_en_service, etat_fonctionnement=etat_fonctionnement, image=image)
            else :
                utilisateur=Employee.objects.get(id=utilisateur)
                materiel = Materiel(nom=nom, marque=marque, modele=modele, type=type, annee_mise_en_service=annee_mise_en_service, etat_fonctionnement=etat_fonctionnement, utilisateur=utilisateur, image=image)
        materiel.save()
        data = {
            "message" : "bueno",
            "last_id" : last_id
        }
        return JsonResponse(data, status=200)
    

class MaterielUpdateView(UpdateView):
    model = Materiel
    template_name = "employees/create.html"
    form_class=MaterielForm
    success_url=reverse_lazy('materiels:list-materiel')


class MaterielDeleteView(DeleteView):
    model = Materiel
    success_url=reverse_lazy('materiels:list-materiel')


class MaterielAllView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        materiels = Materiel.objects.all().values()
        context={
            "materiels":list(materiels),
        }
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return 
        return JsonResponse(context, status=200)


class MaterielListView(LoginRequiredMixin, TemplateView):
    form_class=MaterielForm
    template_name = 'materiels/list.html'
    
    def get(self, request, *args, **kwargs):
        materiels = Materiel.objects.all()
        form=self.form_class() 
        return render(request, self.template_name, {"form":form, 'materiels':materiels})

class MaterielDetailView(View):
    
    def get(self, request, *args, **kwargs):
        materiel=Materiel.objects.get(pk=kwargs['pk'])
        if materiel.utilisateur is not None:
            response_data = {
                "id" : materiel.pk,
                "nom" : materiel.nom,
                "marque" : materiel.marque,
                "modele" : materiel.modele,
                "type" : materiel.type,
                "annee_mise_en_service" : materiel.annee_mise_en_service,
                "etat_fonctionnement" : materiel.etat_fonctionnement,
                "utilisateur" : materiel.utilisateur.id
            }
        else:
            response_data = {
                "id" : materiel.pk,
                "nom" : materiel.nom,
                "marque" : materiel.marque,
                "modele" : materiel.modele,
                "type" : materiel.type,
                "annee_mise_en_service" : materiel.annee_mise_en_service,
                "etat_fonctionnement" : materiel.etat_fonctionnement
            }
        return JsonResponse(response_data, status=200)
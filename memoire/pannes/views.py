from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView, View, ListView, DetailView
from users.models import Panne, Employee, Commentaire
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from commentaires.forms import CommentaireForm
# Create your views here.


class AllPAnnesView(LoginRequiredMixin, View):
    pannes = Panne.objects.all().values('id', 'ticket__materiel__nom', 'created_at', 'agent__user__username', 'etat')
    agents = Employee.objects.filter(direction_employee__code="DSI").values('id', 'user__username')

    def get(self, request, *args, **kwargs):
        data = {
            "pannes" : list(self.pannes),
            "agents" : list(self.agents)
        }

        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            json_data = serializers.serialize('json', data['pannes'])
            return JsonResponse(json_data, safe=False, status=200)
        return JsonResponse(data, status=200)


class PanneListView(LoginRequiredMixin, View):
    template_name = "pannes/allpannes.html"

    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.is_superuser:
            pannes = Panne.objects.all()
            agents = Employee.objects.filter(direction_employee__code="DSI")
            context ={"pannes":pannes, "agents": agents}
        else:
            agent=Employee.objects.get(user=user)
            pannes = Panne.objects.filter(agent=agent)
            context ={"pannes":pannes}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        agent = request.POST.get("agent")
        id = request.POST.get("panneId")
        agent=Employee.objects.get(id=agent)
        if agent != None and id != None:
            panne = Panne.objects.get(pk=id)
            panne.agent = agent
            panne.save()

            data= {
                "message" : "SUCCESS",
                "agent" : agent.user.username
            } 
        else:
            # Handle form errors or invalid data
            data= {
                "message" : "ERROR",
            } 
            return JsonResponse(data, status=403)
        return JsonResponse(data, status=200)


class PanneAgentsListView(LoginRequiredMixin, View):
    template_name = "pannes/allpannes.html"

    def get(self, request, *args, **kwargs):
        pannes = Panne.objects.filter(agent=request.user)
        return render(request, self.template_name, {"pannes":pannes})
  
  
class PanneDeleteView(DeleteView):
    model = Panne
    template_name = "pannes/confirm_delete.html"
    success_url = reverse_lazy("pannes:all-panne")


class PanneDoneView(View):

    def get(self, request, *args, **kwargs):
        panne = Panne.objects.filter(pk=kwargs['pk']).first()
        panne.etat = 'termine'
        panne.save()
        # return redirect(reverse("pannes:all-panne"))
        data={'message':'succes'}
        return JsonResponse(data, status=200)
    

class PanneObservationView(View):
    
    def post(self, request, *args, **kwargs):
        panne = Panne.objects.filter(pk=kwargs['pk']).first()
        panne.observation = request.POST.get('observation')
        panne.save()
        data = {}
        if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            data={'panne': panne}
            return data
        return JsonResponse(data, status=200)
    

class PanneDetailView(DetailView):
    model = Panne
    template_name = 'tickets/detail.html'
    context_object_name="panne"

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        connected_comments = Commentaire.objects.filter(panne=self.get_object())
        number_of_comments = connected_comments.count()
        data['comments'] = connected_comments
        data['no_of_comments'] = number_of_comments
        data['comment_form'] = CommentaireForm()
        return data    
    
    def post(self , request , *args , **kwargs):
        if self.request.method == 'POST':
            print('-------------------------------------------------------------------------------Reached here')
            comment_form = CommentaireForm(self.request.POST)
            if comment_form.is_valid():
                content = comment_form.cleaned_data['content']
                try:
                    parent = comment_form.cleaned_data['parent']
                except:
                    parent=None


            new_comment = Commentaire(content=content , employee = Employee.objects.get(username=self.request.user.username)  , panne=self.get_object() , parent=parent)
            new_comment.save()
            return redirect(self.request.path_info)
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView, DeleteView, UpdateView, View, ListView, DetailView
from users.models import Panne, Employee, Ticket, Materiel
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TicketForm

# Create your views here.
class TicketCreateView(LoginRequiredMixin, View):
    form_class=TicketForm

    def get(self, request, *args, **kwargs):
        form=self.form_class(initial={'user':request.user})
        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data:
                materiel = form.cleaned_data['materiel']
                description = form.cleaned_data['description']
                priorite = form.cleaned_data['priorite']
                reference  = request.POST.get("reference")
                ticket = Ticket.objects.filter(reference=reference).first()
                if ticket:
                    materiel = Materiel.objects.get(pk=request.POST.get("materiel"))  
                    ticket.materiel = materiel
                    ticket.priorite = priorite
                    ticket.description = description
                    ticket.save()
                else :
                    user=request.user
                    user = Employee.objects.get(user=user)
                    materiel = Materiel.objects.filter(nom=materiel).first()
                    try:
                        last_id=Ticket.objects.last().id  + 1
                    except :
                        last_id=1
                    reference = "%s-%s"%(materiel, last_id)
                    while Ticket.objects.filter(reference=reference).exists():
                        last_id += 1
                        reference = "%s-%s" % (materiel, last_id)
                    ticket=Ticket(materiel=materiel, description=description, reference=reference, plaignant=user, priorite=priorite)
                    ticket.save()
                    panne = Panne(ticket=ticket)
                    panne.save()
        else:
            # Handle form errors or invalid data
            return HttpResponse("Error")
        
        return HttpResponse("Success")
    

class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "tickets/alltickets.html"
    context_object_name="tickets"


class TicketUserListView(LoginRequiredMixin, View):
    template_name="tickets/userstickets.html"
    form_class = TicketForm()

    def get(self, request, *args, **kwargs):
        if request.user is not None:
            user = Employee.objects.filter(user=request.user).first()
            ticketss = Ticket.objects.filter(plaignant=user)
            tickets = []
            for ticket in ticketss:
                panne = Panne.objects.filter(ticket=ticket).first()
                if panne:
                    panne = {
                        "id": panne.pk,
                        "reference": panne.ticket.reference,
                        "materiel": panne.ticket.materiel,
                        "date": panne.ticket.created_at,
                        "etat": panne.etat,
                        "date": panne.created_at
                    }
                    tickets.append(panne)
        return render(
            request, 
            self.template_name, 
            {"tickets":tickets, "form":self.form_class}
        )

    
class TicketDetailView(DetailView):
    model = Ticket
    template_name = "tickets/detail.html"
    
    def get(self, request, *args, **kwargs):
        id=request.GET.get("id")
        ticket=Ticket.objects.get(pk=int(id))
        response_data = {
            "id" : ticket.pk,
            "reference" : ticket.reference,
            "materiel" : ticket.materiel.id,
            "priorite" : ticket.priorite,
            "description" : ticket.description,
            "date" : ticket.created_at
        }
        return JsonResponse(response_data)

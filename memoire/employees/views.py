from django.contrib.auth import authenticate, login, logout, mixins, models, decorators
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.http import JsonResponse
from django.views.generic import DeleteView, UpdateView, View, ListView
from users.models import Employee, Ticket, Panne, Direction, Materiel, Notification, Service
from tickets.forms import TicketForm
from .forms import EmployeeForm, ContactForm
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
# from datetime import datetime, timedelta
# import calendar
from django.db.models import Count
from django.db.models.functions import ExtractMonth

# Create your views here.

#Fonction qui permet d'ajouter un utilisateur a un groupe 


class GetServicesView(View):

    def get(self, request, *args, **kwargs):
        direction_id = request.GET.get('direction_id')
        services = Service.objects.filter(direction_service_id=direction_id).values('id', 'nom')
        return JsonResponse({'services': list(services)})


class EmployeeCreateView(View):
    model = Employee
    template_name = "users/register.html"
    form_class=EmployeeForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form':self.form_class})
    
    def post(self, request, *args, **kwargs):
        context = {'form':self.form_class}
        form=self.form_class(request.POST)

        if form.is_valid():
            try:
                user=models.User.objects.create(username=request.POST.get('username'), email=request.POST.get('email'), first_name=request.POST.get('first_name'), last_name=request.POST.get('last_name'))
                user.set_password(request.POST.get('password'))
                user.save()
                direction=Direction.objects.get(pk=request.POST.get('direction_employee'))
                service = Service.objects.get(pk=request.POST.get('service_employee'))
                employee=Employee.objects.create(user=user, bureau=request.POST.get('bureau'), poste=request.POST.get('poste'), direction_employee=direction, adresse=request.POST.get('adresse'), contact=request.POST.get('contact'), service_employee=service)
                employee.save()
                
                if direction.code == "DSI":
                    group = models.Group.objects.get(name='Agents')
                    group.user_set.add(user)
                
                if employee:
                    login(request, user)
                    return redirect("employees:index")
                context['valides'] = "Employé créé avec succès"
            except:
                context['invalides'] = "Votre email ou immatriculation existe deja dans la base"
        else:
            context['invalides'] = form.errors
        return render(request, self.template_name, context=context)
    

class EmployeeUpdateView(View):
    model = Employee
    template_name = "employees/create.html"
    form_class=EmployeeForm
    success_url=reverse_lazy('employees:index')


class EmployeeDeleteView(DeleteView):
    model = Employee


class LogoutView(mixins.LoginRequiredMixin, View):
    template_name="users/login.html"

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name)


class LoginView(View):
    template_name="users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user:
            redirect(reverse("employees:logout"))
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        messages = []

        try:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)    
                return redirect(reverse_lazy('employees:index'))
            else:
                messages.append("Invalid username  or password")
        except Exception as e:
            messages.append("An error occurred during authentication: {}".format(str(e)))
        return render(request, self.template_name, {"messages": messages})


class IndexView(View):
    template_name="index.html"

    def get(self, request, *args, **kwargs):
        user=request.user
        if not user.is_authenticated or not Employee.objects.filter(user=user).exists():
            form = TicketForm(materiel=Materiel.objects.filter(utilisateur=None))
        else:
            employee=Employee.objects.get(user=user.id)
            form = TicketForm(materiel=Materiel.objects.filter(utilisateur=employee)) 

        return render(request, self.template_name, {'form':form})
    
    def post(self, request, *args, **kwargs):
        user=request.user
        form=TicketForm(request.POST)
        context = {'form':form}

        if user:
            try:
                user = Employee.objects.get(user=user)
            except:
                context['invalides'] = "Cet employe n'existe pas"
        else:
            return redirect(reverse_lazy('employees:login'))

        if form.is_valid():
            materiel = form.cleaned_data['materiel']
            description = form.cleaned_data['description']
            priorite = form.cleaned_data['priorite']
            materiel = Materiel.objects.get(nom=materiel)
            if materiel is None:
            # Handle invalid materiel selection
                context['valides'] = 'Invalid materiel selection.'
            else:
                try:
                    last_id = Ticket.objects.last().id + 1
                except:
                    last_id = 1
                reference = "%s-%s" % (materiel.nom, last_id)
                while Ticket.objects.filter(reference=reference).exists():
                    last_id += 1
                    reference = "%s-%s" % (materiel.nom, last_id)
                try:
                    ticket = Ticket(materiel=materiel, description=description, reference=reference, plaignant=user,
                                priorite=priorite)
                    ticket.save()
                    
                    panne = Panne(ticket=ticket)
                    panne.save()

                    valides = "Nous avons recu votre message, Veuillez patienter qu'un agent vienne prendre en charge votre probleme. Merci!"
                    if valides:
                        context['valides'] = valides
                except ValueError:
                    context['invalides'] = "Cet utilisateur n'a pas le droit de creer un ticket"
                except:
                    context['invalides'] = "Ce ticket ne peut pas etre enregistre"
        else:
            context['invalides'] = form.errors

        return render(request, self.template_name, context)


class EmployeeListView(ListView):
    model = Employee
    template_name = "users/allusers.html"
    context_object_name = "employees"

class ProfileView(View):
    template_name="profile.html"
    
    def get(self, request, *args, **kwargs):
        nb_tot_pannes = Panne.objects.all().count()
        nb_tot_agents = Employee.objects.filter(direction_employee__code="DSI").count()
        nb_tot_termine = Panne.objects.filter(etat="termine").count()
        nb_users = Employee.objects.all().count()
        pannes = Panne.objects.all()
        materiels = Materiel.objects.all()
        mes_pannes = []
        for materiel in materiels:
            nbr_panne_regle=0
            nbr_panne = Ticket.objects.filter(materiel=materiel).count()
            tickets = Ticket.objects.filter(materiel=materiel)
            for ticket in tickets:
                if Panne.objects.filter(etat='termine', ticket=ticket):
                    nbr_panne_regle += 1
                else:
                    nbr_panne_regle = nbr_panne_regle
            try:
                ticket = Ticket.objects.filter(materiel=materiel).last().created_at 
            except:
                ticket = "Aucune panne"
            panne = {
                "materiel_id" : materiel.id,
                "nbr_panne": nbr_panne,
                "nbr_panne_regle" : nbr_panne_regle,
                "materiel_nom" : materiel.nom,
                "derniere_panne" : ticket
            }
            mes_pannes.append(panne)
        
        pannes_par_mois = Panne.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(
            etat_count=Count('etat')
        ).values('month', 'etat_count')

        # Créer une liste pour stocker les données de chaque mois
        data = []
        for mois in pannes_par_mois:
            mois_label = mois['month']
            # mois_name = calendar.month.name(mois_label)
            data.append({
                'mois': mois_label,
                # 'mois_name' : mois_name,
                'total_pannes': mois['etat_count'],
                'pannes_resolues': Panne.objects.filter(created_at__month=mois['month'], etat='termine').count()
            })
            
        user = request.user  
        if not user.is_authenticated:
            return redirect('employees:login')

        if isinstance(user, AnonymousUser):
            # Rediriger ou gérer le cas où l'utilisateur n'est pas authentifié
            return redirect('employees:login')

        if user.is_authenticated:
            notifications = Notification.objects.filter(recipient=user)[:3]
            try:
                employee = Employee.objects.get(user=user)
                context = {
                    'notifcations':notifications,
                    'nb_tot_pannes' : nb_tot_pannes,
                    'nb_tot_agents' : nb_tot_agents,
                    'nb_tot_termine' : nb_tot_termine,
                    'nb_users' : nb_users,
                    "pannes" : pannes,
                    "user": user,
                    "employee": employee,
                    "mes_pannes" : mes_pannes,
                    'data' : data
                }
            except Employee.DoesNotExist:
                context = {
                    'notifcations':notifications,
                    'nb_tot_pannes' : nb_tot_pannes,
                    'nb_tot_agents' : nb_tot_agents,
                    'nb_tot_termine' : nb_tot_termine,
                    'nb_users' : nb_users,
                    "pannes" : pannes,
                    "user": user,
                    "mes_pannes" : mes_pannes,
                    'data' : data
                }            
        else:
            return redirect("employees:login")
        return render(request, self.template_name, context)
    

class UserProfileView(View):
    form_class=EmployeeForm()
    template_name = "users/user.html"

    def get(self, request, *args, **kwargs):
        directions = Direction.objects.all()
        services = Service.objects.all()
        user = request.user
        if not user.is_authenticated:
            return redirect('employees:login')
        try:
            employee = Employee.objects.get(user=user)
            context = {
                "user": user,
                "employee": employee,
                "directions": directions,
                "services": services
            }
        except Employee.DoesNotExist:
            context = {
                "user": user,
                "directions": directions,
                "services": services
            }
        return render(request, self.template_name, context)


class UserUpdateView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        current_user = models.User.objects.get(id=user.id)
        is_password_valid = current_user.check_password(request.POST.get('password'))

        if is_password_valid:
            try:
                employee = Employee.objects.get(user=current_user.id)
                current_user.first_name = request.POST.get('first_name')
                current_user.last_name = request.POST.get('last_name')
                current_user.email = request.POST.get('email')
                employee.adresse = request.POST.get('adresse')
                employee.contact = request.POST.get('contact')
                
                if request.POST.get('direction_employee') is None:
                    employee.direction_employee = None
                else:
                    employee.direction = Direction.objects.get(id=request.POST.get('direction_employee'))

                if request.POST.get('service_employee') is None:
                    employee.service_employee = None
                else:
                    employee.service = Service.objects.get(id=request.POST.get('service_employee'))

                current_user.save()
                employee.save()
                
                messages.success(request, "Vous avez modifié vos informations avec succès !")
            except Employee.DoesNotExist:
                current_user.first_name = request.POST.get('first_name')
                current_user.last_name = request.POST.get('last_name')
                current_user.email = request.POST.get('email')
                current_user.save()
                
                messages.success(request, "Vous avez modifié vos informations avec succès !")
        else:
            messages.error(request, "Mot de passe incorrect ! Votre opération a échoué")

        return redirect(reverse_lazy("employees:user-profile"))
    

class AproposView(View):
    template_name="users/a-propos.html"

    def get(self, request, *args, **kwargs):
        return  render(request, self.template_name)
    

class ContactView(View):
    template_name="users/contact.html"
    form_class=ContactForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form':self.form_class()})
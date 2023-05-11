from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Project, Ticket, TicketCategory, Response
from django.contrib import messages
from .forms import NewUserForm, TicketForm
from django.utils import timezone
from django.db.models import Q


def loginPage(request):
    page = 'login'
    next = ''

    if request.user.is_authenticated:
        return redirect('home')

    if request.GET:
        next = request.GET['next']

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            login(request, user)
            if next == '':
                return redirect('home')
            else:
                return redirect(next)
        except:
            messages.error(
                request, "Incorrect email address or password. Please try again.")

    context = {"page": page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # use Django's built-in validation
            pass

    context = {"form": form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='/login')
def home(request):
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    projects = Project.objects.all()
    tickets = Ticket.objects.filter(Q(title__icontains=query) | Q(
        description__icontains=query) | Q(project__name__icontains=query) | Q(id__icontains=query))
    ticket_responses = Response.objects.filter(ticket__title__icontains=query)
    user = request.user.name.split(" ")[0]

    context = {
        'projects': projects,
        'tickets': tickets,
        'ticket_responses': ticket_responses,
        'user': user,
    }
    return render(request, 'base/index.html', context)


@login_required(login_url='/login')
def createTicket(request):
    form = TicketForm()
    project_managers = User.objects.filter(role='Project Manager')

    if request.method == 'POST':
        project_name = request.POST.get('project')
        project, created = Project.objects.get_or_create(name=project_name)
        project.started = timezone.now()

        Ticket.objects.create(
            owner=request.user,
            project=project,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            category=TicketCategory.objects.get(
                id=request.POST.get('category')),
            project_manager=User.objects.get(
                id=request.POST.get('project_manager')),
        )
        return redirect('home')

    context = {'form': form, 'project_managers': project_managers}
    return render(request, 'base/create-ticket.html', context)


@login_required(redirect_field_name='next', login_url='/login')
def viewTicket(request, pk):
    ticket = Ticket.objects.get(id=pk)
    form = TicketForm(instance=ticket)
    responses = ticket.response_set.all()

    if request.user.role == "DPM":
        form = TicketForm(instance=ticket,
                          is_project_manager=True)

    if request.method == 'POST':
        ticket.status = request.POST.get('status')
        ticket.save()
        ticket_response = Response.objects.create(
            user=request.user,
            ticket=ticket,
            body=request.POST.get('body')
        )
        return redirect('view-ticket', pk=ticket.id)

    context = {'ticket': ticket, 'responses': responses, 'form': form}
    return render(request, 'base/view-ticket.html', context)

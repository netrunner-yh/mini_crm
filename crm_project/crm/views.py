from django import forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .models import Ticket, User, Comment
from .forms import UserRegistrationForm, TicketForm, CommentForm


@staff_member_required(login_url='login')
def create_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('user_roles')
    else:
        form = UserRegistrationForm()
    return render(request, 'crm/create_user.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ticket_list')
        else:
            return render(request, 'crm/login.html', {'error': 'Неверное имя пользователя или пароль.'})
    return render(request, 'crm/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def create_ticket(request):
    user_role = request.user.role

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.responsible_person = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        if user_role == 'operator':
            form = TicketForm(initial={
                'responsible_person': request.user,
                'status': 'Открыт'
            })
            form.fields['responsible_person'].widget = forms.HiddenInput()
            form.fields['status'].widget = forms.HiddenInput()
        else:
            form = TicketForm()

    return render(request, 'crm/create_ticket.html', {'form': form})


def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    user_role = request.user.role

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            if user_role == 'operator':
                form.fields['responsible_person'].disabled = True
                form.fields['status'].disabled = True
            form.save()
            return redirect('ticket_detail', ticket_id=ticket_id)
    else:
        if user_role == 'operator':
            form = TicketForm(instance=ticket, initial={
                'responsible_person': ticket.responsible_person,
                'status': ticket.status
            })
            form.fields['responsible_person'].widget = forms.HiddenInput()
            form.fields['status'].widget = forms.HiddenInput()
        else:
            form = TicketForm(instance=ticket)

    return render(request, 'crm/edit_ticket.html', {'form': form, 'ticket': ticket})


@login_required(login_url='login')
def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-id')
    return render(request, 'crm/ticket_list.html', {'tickets': tickets})


def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.ticket = ticket
            comment.author = request.user
            comment.save()
            return redirect('ticket_detail', ticket_id=ticket_id)
    else:
        comment_form = CommentForm()
    return render(request, 'crm/ticket_detail.html', {'ticket': ticket, 'comment_form': comment_form})


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', ticket_id=comment.ticket.id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'crm/edit_comment.html', {'form': form, 'comment': comment})


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    ticket_id = comment.ticket.id
    comment.delete()
    return redirect('ticket_detail', ticket_id=ticket_id)


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def user_roles(request):
    users = User.objects.all()
    return render(request, 'crm/user_roles.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser, login_url='login')
def update_role(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        role = request.POST['role']
        user.role = role
        user.save()
        return redirect('user_roles')
    return render(request, 'crm/user_roles.html', {'user': user})


def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('user_roles')

    return render(request, 'crm/user_roles.html', {'user': user})


def search_tickets(request):
    query = request.GET.get('query')
    tickets = []

    if query:
        tickets = Ticket.objects.filter(
            Q(account_number__icontains=query) |
            Q(full_name__icontains=query) |
            Q(phone_number__icontains=query)
        )

    return render(request, 'crm/search_tickets.html', {'query': query, 'tickets': tickets})

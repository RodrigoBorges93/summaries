from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Summary
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.messages.views import SuccessMessageMixin

# index page
def home(request):
    return render(request, 'main/index.html')


# signup page
def cadastro(request):
  if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
          user = form.save()
          user.save()
          username = form.cleaned_data.get('username')
          raw_password = form.cleaned_data.get('password1')
          user = authenticate(request, username=username, password=raw_password)
          if user is not None:
            login(request, user)
            messages.success(request, "Usuário criado com sucesso!")
          
          return redirect('home')
  else:
    form = SignUpForm()
  return render(request, 'main/cadastro.html', {'form': form})


# logout function
def logout_view(request):
  logout(request)
  return redirect('home')

#login page
def logging(request):
  return render (request, "registration/login.html")

# Page with a form to create summaries
class Summarycreate(CreateView):
  model = Summary
  fields = ['subject', 'summary']

  def form_valid(self, form):
    obj = form.save(commit=False)
    obj.user = self.request.user
    obj.user_id = self.request.user.id 
    obj.save()
    return redirect ('summary_list')

# Page that will show all of the user's summaries, ordered by subject, in this page you can search an specific keyword
class Summary_lista(ListView):
  model = Summary
  paginate_by = 10

  def get_queryset(self):
    if Summary.objects.all():
      query = self.request.GET.get('q')
      if query:
        queryset = Summary.objects.filter(Q(user_id = self.request.user.id)&(
        Q(subject__icontains = query)|
        Q(summary__icontains = query))).order_by('subject')

      else:
        queryset = Summary.objects.filter(user_id = self.request.user.id).order_by('subject')
      return queryset


# Page to edit an existing summary
class Summaryedit(UpdateView):
  model = Summary
  fields = ['subject', 'summary']

  def get_queryset(self):
    base_qs = super(Summaryedit, self).get_queryset()
    return base_qs.filter(user_id = self.request.user.id)

  def get_success_url(self):
    return reverse ('summary_list')


# Page to delete an existing summary
class Summarydelete(DeleteView):
  model = Summary

  def get_queryset(self):
    base_qs = super(Summarydelete, self).get_queryset()
    return base_qs.filter(user_id = self.request.user.id)

  def get_success_url(self):
    return reverse ('summary_list')

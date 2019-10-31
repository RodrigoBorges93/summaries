from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from main import views
from django.contrib.auth.views import LoginView

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  url(r'^$', views.home, name='home'),
  url(r'^cadastro/', views.cadastro, name = 'cadastro'),
  path('login/', LoginView.as_view(), name="login"),
  url(r'^logout/', views.logout_view, name = 'logout'),
  url(r'^create_summary/', views.Summarycreate.as_view(), name = 'create_summary'),
  url(r'^all_summaries/', views.Summary_lista.as_view(), name = 'summary_list'),
  path(r'edit_summary/<int:pk>', views.Summaryedit.as_view(), name = 'summary_edit'),
  path(r'delete_summary/<int:pk>', views.Summarydelete.as_view(), name = 'summary_delete'),
]

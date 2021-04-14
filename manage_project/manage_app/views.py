from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from . import models
from django.views.generic.edit import FormView
# Create your views here.

from manage_app.models import Code
from . import forms
from manage_app.forms import NewUserForm

# Create your views here.

def index(request):
    code_list=Code.objects.order_by('user')
    date_dict={'access_records':code_list} #mapping to templates/index.html <div>
    
    return render(request,'manage_app/index.html',context=date_dict)

    return render(request,'first_app/user.html',context=user_dict)
def form_name_view(request):
    form=forms.FormName()
    if request.method=='POST':
        form=forms.FormName(request.POST)
        if form.is_valid():
            print("validation IS SUCCESS")
            print("User="+form.cleaned_data['user'])
            print("Code="+form.cleaned_data['code'])
            print("Validate="+form.cleaned_data['validate'])
            print("mac_address="+form.cleaned_data['mac_address'])
    return render(request,'manage_app/form_page.html',{'form':form})

def addUser(request):
    form = NewUserForm()
    #print("form="+form)
    if request.method == "POST":
        form= NewUserForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print("ERROR FORM INVALID")
    return render(request,'manage_app/form_page.html',{'form':form})

def generate(request):
    return ""

class CodeListView(ListView):
    print("CodeListView")
    context_object_name='code'
    model= models.Code
    template_name='manage_app/code_list.html'

class CodeDetailView(DetailView):
    
    context_object_name='code_detail'
    model=models.Code
    template_name='manage_app/code_detail.html'

class CodeCreateView(CreateView):
    fields=('user','code','validate','mac_address')
    model=models.Code
    success_url= reverse_lazy("manage_app:list")
class CodeUpdateView(UpdateView):
    fields =('user','code','validate','mac_address')
    model=models.Code
    template_name="manage_app/form_page.html"
    success_url= reverse_lazy("manage_app:list")
class CodeDeleteView(DeleteView):
    model=models.Code
    success_url= reverse_lazy("manage_app:list")

class IndexView(TemplateView):
    template_name='manage_app/index.html'
    model=models.Code
    
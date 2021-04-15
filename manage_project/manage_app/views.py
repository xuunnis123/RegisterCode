from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import View,TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from . import models
from django.views.generic.edit import FormView

from manage_app.models import Code
from . import forms
from manage_app.forms import NewUserForm
from rsa_company_gen import encode_rsa


def index(request):
    code_list=Code.objects.order_by('user')
    date_dict={'access_records':code_list} #mapping to templates/index.html <div>
    
    return render(request,'manage_app/index.html',context=date_dict)

def generate(request,mac_address,datetime):
    datetime=request.POST.get('validate')
    mac_address=request.POST.get('mac_address')
    print("Generate")
    date=datetime.split("-")
    datetime=date[0]+date[1]+date[2]
    content=datetime+mac_address
    encode={"code",encode_rsa(content,mac_address)}

def CodeGen(request):
    if request.method == "POST":
        datetime=request.POST.get('validate')
        mac_address=request.POST.get('mac_address')
        date=datetime.split("-")
        datetime=date[0]+date[1]+date[2]
        content=datetime+mac_address
        print(request.POST.objects.get(pk=pk))
        encode={"code",encode_rsa(content,mac_address)}
        print(encode)
        return render(request,"",encode)

class CodeGenView(CreateView):
    print("CodeGenView")
    fields=('user','validate','mac_address')
    model=models.Code
    template_name='manage_app/code_gen.html'
    #success_url= reverse_lazy("manage_app:create")
    
    def get_success_url(self):
   
        print("test=",self.get_object().id)
        return reverse_lazy('update',kwargs={'pk': self.get_object().id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    def generate(self,request):
        datetime=request.POST.get('validate')
        mac_address=equest.POST.get('mac_address')
        print("datetrime:",datetrime)
        date=datetime.split("-")
        datetime=date[0]+date[1]+date[2]
        content=datetime+mac_address
        encode={"code",encode_rsa(content,mac_address)}
        print(encode)

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
    template_name="manage_app/code_form.html"
    success_url= reverse_lazy("manage_app:list")
class CodeDeleteView(DeleteView):
    model=models.Code
    success_url= reverse_lazy("manage_app:list")

class IndexView(TemplateView):
    template_name='manage_app/index.html'
    model=models.Code
    
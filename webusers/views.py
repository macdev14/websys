from django.forms.utils import ErrorList
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from django import forms
from django.forms import ModelForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
import json



class UserForm(forms.ModelForm):
    fields = [
        "name",
        "email",
        "identity",
        "country",
        "state",
        "city",
        'street',
        "number"
    ]
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = User
        fields = '__all__'


from django.contrib.auth.views import (
    PasswordChangeView,
)

class CustomPassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPassword, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class UpdatePassword(PasswordChangeView):
    form_class = CustomPassword
    success_url = '/'
    template_name = 'webusers/update_password.html'
   

class UserUpdateView(UpdateView):
    model = User
   
    form_class = UserForm
    template_name_suffix = '_update_form'
    success_url ="/"
    def get_object(self):
        return User.objects.get(pk=self.request.user.id) # or request.POST
    


class RegisterForm(forms.ModelForm):
    address = forms.CharField(widget = forms.HiddenInput(), required = False)
    password = forms.CharField(widget=forms.PasswordInput)
    reference = forms.CharField(required=False)
    date_joined = forms.CharField(widget = forms.HiddenInput(), required = False)
    username = forms.CharField(widget = forms.HiddenInput(), required = False)
    password = forms.CharField(widget = forms.HiddenInput(), required = False)
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
    class Meta:
        model = User
        fields = '__all__'




def register(request):
    
    if  request.method == 'POST':
        
        try:
            userform = UserForm(request.POST)
            errors = userform.errors.as_json()
            errors = json.loads(errors)
            for message in errors:
               
                messages.add_message(request, messages.INFO, message + ': '+ errors[message][0]['message'])
            if not errors:
               
                username, email, password, number, identity, street, country = request.POST['name'], request.POST['email'], request.POST['password'], request.POST['number'], request.POST['identity'], request.POST['street'], request.POST['country']
                try:
                    user = User.objects.create_user(username=userform['email'].data, email=userform['email'].data, password=userform['password'].data, number=userform['number'].data)
                    user.name=userform['name'].data
                    user.identity=userform['identity'].data 
                    user.street=userform['street'].data
                    user.country=userform['country'].data
                    user.state=userform['state'].data
              
                    user.save()
                    login(request, user)
                    return redirect('index')
                except IntegrityError as e:
                   
                    messages.add_message(request, messages.INFO, 'Conta já existente.')
                
        except Exception as e:
           
            messages.add_message(request, messages.INFO, 'Erro ao cadastrar.')
            pass
        

    userform = UserForm(request.POST or None)
    return render(request, "register.html", { 'userform': userform })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["email"]
        password = request.POST["password"]
      
        user = authenticate(request, username=username, password=password)
        

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            messages.add_message(request, messages.INFO, 'Senha e/ou email inválido.')
    return redirect("index")
    

def logout_view(request):
    logout(request)
    return redirect("index")

def index(request):
    return render(request, "index.html")

def delete_account(request):
    current_user = request.user
    userid = current_user.id
    user = User.objects.get(pk=userid)
    user.delete()
    messages.success(request, 'Perfil removido com sucesso.')
    return redirect('index')



def mydata(request):
    current_user = request.user
    userid = current_user.id
    
    user = None
    if not userid:
        return redirect('index')
    if User.objects.filter(pk=userid).exists():
     
        user = User.objects.get(pk=userid)
    if request.method =='POST':
        form = UserForm(request.POST, instance=user)
       
        errors = form.errors.as_json()
        errors = json.loads(errors)
        for message in errors:
          
            messages.add_message(request, messages.INFO, message + ': '+ errors[message][0]['message'])
        
        
        if form.is_valid() and user:
            user.set_password(form['password'].data)
           
            try:
                user.save()
               
                form.save()
            except IntegrityError as e:
            
                messages.add_message(request, messages.INFO, 'Nome / Senha existentes.')
           
            
            
      
           
            userauth = authenticate(request, username=form['email'].data, password='1234')
          
            if userauth:
                login(request, userauth)
                messages.success(request, 'Perfil atualizado com sucesso.')
            else:
                return redirect('index')

           
    
    form = UserForm(instance=user)
    return render(request, "profile.html", { 'userform': form })


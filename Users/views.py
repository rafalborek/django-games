from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.views.generic.edit import UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .forms import UserFormLogin, UserFormRegister, UserFormUpdate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from games.models import GomokuOnline, BridgeOnline




# Create your views here.

def logout_view(request):

    logout(request)
    return redirect('mainPage:index')

class UserProfileView(View):
    pass

class UserRegisterView(View):

    form_class = UserFormRegister
    template_name = 'Users/registration_form.html'
    
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form' : form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            
            user = form.save(commit=False)
            # cleaned (normalized) data
            
            username  = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('mainPage:index')
                
        return render(request,self.template_name,{'form' : form})   
    
    
class UserLoginView(View):

    form_class = UserFormLogin
    template_name = 'Users/login_form.html'
    
    def get(self,request):
        form = self.form_class(None)
        return render(request,self.template_name,{'form' : form})
    
    def post(self,request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            
            username  = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('mainPage:index')
                
        return render(request,self.template_name,{'form' : form})   
    
class UserUpdateView(UpdateView):

    
    form_class = UserFormUpdate
    #model = User
    #fields = ['username','email']
    template_name = 'Users/edit_profile_form.html'
    success_url = reverse_lazy('mainPage:index')
    
    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)
    
class UserDeleteView(DeleteView):

    model = User
    success_url = reverse_lazy('mainPage:index')
    
    

class StatisticsView(View):
 
    def get(self,request):

        u = GomokuOnline.objects.filter(user=self.request.user)
        if u.exists():
            u = get_object_or_404(GomokuOnline,user=self.request.user)
        else:
            u=None
        u2 = BridgeOnline.objects.filter(user=self.request.user)
        if u2.exists():
            u2 = get_object_or_404(BridgeOnline,user=self.request.user)
        else:
            u2=None
        
                
        return render(request, 'Users/statistics.html', {"u": u, "u2": u2})
    
    
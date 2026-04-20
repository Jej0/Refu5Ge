from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm

@login_required
def modifier_profil(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
         form.save()
         return redirect('modifier_profil') # Remplace 'profil' par 'modifier_profil'
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'todo/modifier_profil.html', {'form': form})
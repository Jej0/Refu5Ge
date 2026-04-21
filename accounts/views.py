from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .forms import CustomUserCreationForm, UserUpdateForm
from .models import EmailVerifToken
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save(commit=False)
            user.is_active = False  # compte desactiver jusqua verif email
            user.save()

            tok = EmailVerifToken.objects.create(user=user)
            link = request.build_absolute_uri(
                reverse('accounts:verif_email', args=[str(tok.token)]))
            
            obj = "Verifier votre email"
            message = f"""

Bonjour {user.username},

Cliquez sur ce lien pour verifier votre email, expire dans 24 heures.

{link}
"""
            send_mail(obj,message, settings.DEFAULT_FROM_EMAIL ,[user.email], fail_silently=False)

            messages.success(request, "Un email à été envoyé pour verifer votre compte")
            return redirect('accounts:login')
        
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/register.html', {'form': form})



def verif_email(request,token):
    tok = get_object_or_404(EmailVerifToken, token=token)

    if tok.is_expired():
        messages.error(request, 'Lien expiré')
        tok.delete()
        return redirect('accounts:register')
    
    user = tok.user
    user.is_active = True
    user.save()

    tok.delete()

    messages.success(request, 'Votre email a bien été verifié')
    return redirect('accounts:login')


@login_required
def profil(request):
    return render(request, 'login/profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('accounts:profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'login/edit_profile.html', {'form': form})
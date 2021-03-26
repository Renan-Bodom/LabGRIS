from django.shortcuts import render, redirect
from django.contrib import messages
import sys
from LabGRis.pyrebase_settings import db, auth
from LabGRis.decorators import clear_session

#@validate_session
def users(request):
    return render(request,'users/users.html')

def login(request):
    return render(request, 'users/login.html')


def valida_senha(request):
    email = request.POST.get('txtUserEmail', '')
    senha = request.POST.get('txtUserPassword', '')
    try:

        sign_user = auth.sign_in_with_email_and_password(email, senha)
        sign_user = auth.refresh(sign_user['refreshToken'])

        userLab = db.child("users").child(sign_user['userId']).get()

        request.session['idToken'] = sign_user['idToken']
        request.session['userEmail'] = email
        request.session['userId'] = sign_user['userId']
        request.session['nomeUsuario'] = userLab.val()['nome']
        request.session['perfilUsuario'] = userLab.val()['perfil']


    except:
        print("Entrou AQUI")
        clear_session(request)
        print(sys.exc_info()[1])
        messages.error(request, "Usuário ou senha inválidos!")
        return redirect('/usuario/entrar/')

    return redirect('/')
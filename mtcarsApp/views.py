from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Cliente, Carro
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import requests
import json

def welcome_view(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "paginas/welcome.html")

def cadastro_view(request):

    if request.user.is_authenticated:
        return redirect("home")
   
    if request.method == "POST":
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirma-password")
        
        if password != confirm_password:
            print("sao diferentes ")
            return render(request, "cadastro/cadastro.html", {
                "nome": nome, 
                "sobrenome": sobrenome, 
                "email": email, 
                "erroSenha": True
            })
            
        url_lambda = "https://95ibb4hx42.execute-api.us-east-1.amazonaws.com/dev/assinaTopicoEmailCliente"
        
        payload = {
            "cliente_email": email
        }
        
        try:
            response = requests.post(url_lambda, json=payload)
            if response.status_code == 200:
                mensagem = response.json()
                status_code = mensagem["statusCode"]
                if status_code == 201:
                    Cliente.objects.create_user(nome=nome, 
                                                sobrenome=sobrenome,
                                                email=email, username=email, 
                                                password=password, 
                                                email_confirmado=False)
                    return render(request, "cadastro/confirmacao_email.html", {"cliente_email": email})
                else:
                    return render(request, "cadastro/cadastro.html", {"nome": nome, 
                                                                      "sobrenome": sobrenome, 
                                                                      "email_cadastrado": True})
            else:
                return HttpResponse(f"Erro ao processar a assinatura SNS: {response.text}", status=500)
        
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Erro ao tentar se conectar ao servidor SNS: {str(e)}", status=500)
    
    return render(request, "cadastro/cadastro.html")


def verifica_validacao_email_view(request, cliente_email):
   
    if request.user.is_authenticated:
        return redirect("home")
    
    url_lambda = "https://mxxq4obo28.execute-api.us-east-1.amazonaws.com/dev/validacaoEmailAssinante"
    payload = {
        "cliente_email": cliente_email
    }
    
    try:
        response = requests.post(url_lambda, json=payload)
        if response.status_code == 200:
            mensagem = response.json()
            status_code = mensagem["statusCode"]
            if status_code == 200:
                cliente = Cliente.objects.get(email=cliente_email)
                cliente.email_confirmado = True
                cliente.save()
                login(request, cliente)
                return redirect("home")
            
            else:
                return redirect("login")
                
    except requests.exceptions.RequestException as e:
        return HttpResponse(f"Erro ao tentar se conectar ao servidor SNS: {str(e)}", status=500)
                        
    return redirect("login")

def login_view(request):
    
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            verifica_validacao_email_view(request, email)
            if user.email_confirmado:
                login(request, user)
                return redirect("home")
            else:
                return render(request, 'cadastro/login.html', {"aviso_confirmacao_email": True})
        else:
            return render(request, 'cadastro/login.html', {"erro_credencial": True})
        
    return render(request, 'cadastro/login.html')


def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="/login")
def home_view(request):
  
    carros_db = Carro.objects.all()
    modelo_selecionado = None
    
    if request.method == 'POST':
        modelo = request.POST.get("modelo")
        ano = request.POST.get("ano")
        modelo_selecionado = modelo
        
        url_lambda = "https://qlqyqghubh.execute-api.us-east-1.amazonaws.com/dev/consultaInventario"
        
        payload = {
            "modelo": modelo, 
            "ano": ano
        }
        
        try:
            response = requests.post(url_lambda, json=payload)
            
            if response.status_code == 200:
                carro = response.json()
                status_code = carro['statusCode']
                if status_code == 200: 
                    user = request.user 
                    cliente = {
                        "id": user.id, 
                        "nome": user.nome, 
                        "sobrenome": user.sobrenome, 
                        "email": user.email
                    }
             
                    return render(request, 'paginas/home.html', {'carro': carro, 
                                                     'cliente': cliente, 
                                                     'carros': carros_db,          
                                                     'modelo_selecionado': modelo_selecionado})
        
                else:
                    erro = carro['body']['message']
                    return render(request, 'paginas/home.html', {'carros': carros_db, 
                                                     'cliente': request.user,
                                                     'erro': erro, 
                                                     'modelo_selecionado': modelo_selecionado})
            
            else:
                print(f"Erro na requisição para a Lambda: {response.status_code}")
                return render(request, 'paginas/home.html', {
                    'erro': "Erro ao comunicar com o servidor. Tente novamente mais tarde.",
                    'carros': carros_db,
                    'modelo_selecionado': modelo_selecionado
                })
        
        except requests.exceptions.RequestException as err:
            print(f"Erro ao chamar API: {err}")
            return render(request, 'paginas/home.html', {'erro': 'Erro ao se conectar ao servidor. Tente novamente mais tarde.',
                                    'cliente': request.user, 
                                    'carros': carros_db, 
                                    'modelo_selecionado': modelo_selecionado})
        
    return render(request, 'paginas/home.html', {'cliente': request.user, 
                                                 'carros': carros_db, 
                                                 'modelo_selecionado': modelo_selecionado})
    
    
    
@login_required(login_url="/login")
def reservar_view(request, carro_id):
    
    url = "https://kizvt207ed.execute-api.us-east-1.amazonaws.com/dev/reservaCarro"
    
    payload = {
            "carro_id": carro_id,
            "cliente_id": request.user.id 
    }
       
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            mensagem = response.json()
            status_code = mensagem['statusCode']
            if status_code == 200:
                return render(request, "paginas/carro_reservado.html")
            else:
                return redirect("home")
            
        else:
            print(f"Erro na requisição para a Lambda: {response.status_code}")
            return redirect("home")
            
    except requests.exceptions.RequestException as e: 
        print(f'Erro de conexão: {str(e)}')
        return redirect('home')
    

@login_required(login_url="/login")
def notificar_quando_chegar_view(request, carro_id):
    
    url = "https://6bfoky82cc.execute-api.us-east-1.amazonaws.com/dev/salvaClientesInteressados"
    
    payload = {
        "carro_id": carro_id, 
        "cliente_id": request.user.id
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            mensagem = response.json()
            status_code = mensagem['statusCode']
            if status_code == 200:
                return HttpResponse("Cliente interessado com sucesso!")
            else:
                 return HttpResponse("Não foi possivel notificar cliente!")
             
        else:
            print(f"Erro na requisição para a Lambda: {response.status_code}")
            return redirect("home")
            
            
    except requests.exceptions.RequestException as e: 
        print(f'Erro de conexão: {str(e)}')
        return redirect('home')
    

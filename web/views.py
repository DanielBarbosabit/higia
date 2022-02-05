from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import time
from time import time as timer
from web.models import *
from django.http import HttpResponse, JsonResponse, FileResponse
import random
from django.contrib.auth.models import User
from django.contrib import auth, messages
import datetime
from django.contrib.auth.models import User
from django.db import connection
import json
from numpy import random as rd
import os, shutil

#libs for pdf
from borb.pdf.document import Document
from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.forms.text_field import TextField
from borb.pdf.canvas.color.color import HexColor
from decimal import Decimal

from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf.canvas.layout.shape.shape import Shape
from borb.pdf.page.page_size import PageSize
import typing

import csv
# from web.model_forms import Governanca_clientes
from django.forms import ModelForm


#login e cadastro de usuários
def index(request):

    return render(request, 'inicial.html')

def login(request):
    # """Realiza o login de uma pessoa no sistema"""
    try:
        if request.method == 'POST':
            email = request.POST['email'].strip()
            senha = request.POST['senha'].strip()
            if email == '' and senha == '':
                messages.error(request,'Os campos email e senha não podem ficar em branco')
                return redirect('/index/')
            elif email == '':
                messages.error(request,'O campos email não pode ficar em branco')
                return redirect('/index/')
            elif senha == '':
                messages.error(request,'O campos senha não pode ficar em branco')
                return redirect('/index/')
            if User.objects.filter(email=email).exists():
                print('print 1')
                nome = User.objects.filter(email=email).values_list('username', flat=True).get()
                print('nome: ', nome)
                print('print 2')
                user = auth.authenticate(request, username=nome, password=senha)
                print('print 3')
                if user is not None:
                    print('print 4')
                    auth.login(request, user)
                    return redirect('pacientes')
                else:
                    messages.error(request, 'Erro de autenticação! Crie uma nova conta')
                    return redirect('/index/')
            else:
                messages.error(request,'Usuário/Senha inválidos')
                return redirect('/index/')
    except:
        messages.error(request, 'Erro de autenticação! Crie uma nova conta')
        return redirect('/index/')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cadastro(request):
    return render(request, 'cadastro.html')

def cria_cadastro(request):
    """Cadastra uma nova pessoa no sistema """
    if request.method == 'POST':
        nome = request.POST['nome'].strip()
        email = request.POST['email'].strip()
        senha = request.POST['password'].strip()
        senha2 = request.POST['password2'].strip()
        if not nome:
            messages.error(request,'O campo nome não pode ficar em branco')
            return redirect('cadastro')
        if not email:
            messages.error(request,'O campo email não pode ficar em branco')
            return redirect('cadastro')
        if senha != senha2:
            messages.error(request, 'As senhas não são iguais')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Usuário já cadastrado')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request,'Usuário já cadastrado')
            return redirect('cadastro')

        if email == 'daniel_herbert_barbosa@hotmail.com' or email == 'diogom382@gmail.com' or email == 'admindispenser@gmail.com':
            user = User.objects.create_user(username=nome, email=email, password=senha, is_superuser=True)
            user.save()
            messages.error(request, 'Usuário cadastrado com sucesso!')

        else:
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()
            messages.error(request, 'Usuário cadastrado com sucesso!')

        usuarios = list(User.objects.all())

        # Essa lista de usuários é a tabela criada sem utilização do Django para linkar
        # todos dados dos pacientes com seus respectivos médicos/esteticistas
        usuarios_plataforma = Governanca_clientes.objects.count()

        # Verifica se a tabela de usuários está vazia e caso esteja, chama a função para carregar
        # todos os usuários da auth users para ela
        if usuarios_plataforma != len(usuarios):
            carrega_usuarios_governanca_clientes()

        try:
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            print('nome: ', nome)
            print('print 2')
            user = auth.authenticate(request, username=nome, password=senha)

            if user is not None:
                print('print 4')
                auth.login(request, user)
                return redirect('pacientes')

        except:
            return redirect('index')

@login_required(login_url='login')
def dashboard(request):
    if request.user.is_active:
        usuario = json.dumps(request.user.username.split(" ")[0])
        #return render(request, '_menu_estetica.html', {'usuario': usuario})
        return render(request, 'dashboard.html')
    else:
        return render(request, '/index/')

@login_required(login_url='login')
def pacientes(request):
    if request.user.is_active:

        # carrega clientes da plataforma
        id_cliente_fk = busca_id_cliente(request)
        pacientes_list = busca_pacientes(id_cliente_fk)

        error_atendimento = json.dumps(False)

        return render(request, 'pacientes.html', {'pacientes': pacientes_list,
                                                  'error_atendimento': error_atendimento})


def busca_pacientes(id_cliente_fk):
    pacientes = Pacientes.objects.filter(id_cliente_fk=id_cliente_fk)

    paciente_list = []
    pacientes_list = []

    for paciente in pacientes:
        paciente_list.append(paciente.id)
        paciente_list.append(paciente.nome)
        paciente_list.append(paciente.email)
        paciente_list.append(paciente.contato_1)

        pacientes_list.append(paciente_list)
        paciente_list = []

    pacientes_list = json.dumps(pacientes_list)

    return pacientes_list


def busca_id_cliente(request):
    """
    :param request: recebe a requisição para saber quem é o usuário
    :return: Retorna a chave estrangeira do usuário para vinculá-lo em cada uma das tabelas
    """
    email_cliente = request.user.email
    cliente = Governanca_clientes.objects.get(email=email_cliente)
    id_cliente_fk = cliente.id_cliente_pk

    return id_cliente_fk

@login_required(login_url='login')
def adicionar_paciente(request):
    if request.user.is_active:
        if request.POST:
            id_cliente_fk = busca_id_cliente(request)

            nome_paciente = request.POST.get('nome_paciente')
            contato_1 = request.POST.get('contato_1')
            contato_2 = request.POST.get('contato_2')
            email = request.POST.get('email')
            cpf = request.POST.get('cpf')
            rg = request.POST.get('rg')
            profissao = request.POST.get('profissao')
            data_nascimento = request.POST.get('data_nascimento')
            endereco = request.POST.get('endereco')
            numero_endereco = request.POST.get('numero_endereco')
            cidade = request.POST.get('cidade')
            estado = request.POST.get('estado')
            cep = request.POST.get('cep')
            sexo = request.POST.get('sexo')

            #Verifica se existe algum paciente desse usuário com os mesmos valores de RG e CPF
            pacientes_existentes = Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).values()
            campo_duplicado = []
            for paciente in pacientes_existentes:
                if rg == paciente['rg']:
                    campo_duplicado.append('RG')
                elif cpf == paciente['cpf']:
                    campo_duplicado.append('CPF')

                if len(campo_duplicado) > 0:
                    paciente_list = []

                    paciente_list.append(None)
                    paciente_list.append(nome_paciente)
                    paciente_list.append(email)
                    paciente_list.append(contato_1)
                    paciente_list.append(contato_2)
                    paciente_list.append(cpf)
                    paciente_list.append(rg)
                    paciente_list.append(profissao)
                    paciente_list.append(data_nascimento)
                    paciente_list.append(sexo)
                    paciente_list.append(endereco)
                    paciente_list.append(numero_endereco)
                    paciente_list.append(cidade)
                    paciente_list.append(estado)
                    paciente_list.append(cep)

                    paciente_list = json.dumps(paciente_list)
                    campo_duplicado = json.dumps(campo_duplicado)

                    return render(request, 'editar_pacientes.html', {'paciente': paciente_list,
                                                                     'campo_duplicado': campo_duplicado})

            if contato_1 == "":
                contato_1 = None
            if contato_2 == "":
                contato_2 = None
            if email == "":
                email = None
            if cpf == "":
                cpf = None
            if rg == "":
                rg = None
            if profissao == "":
                profissao = None
            if endereco == "":
                endereco = None
            if numero_endereco == "":
                numero_endereco = None
            if cidade == "":
                cidade = None
            if estado == "":
                estado = None
            if endereco == "":
                endereco = None
            if cep == "":
                cep = None
            if sexo == "":
                sexo = None

            now = datetime.datetime.now()
            data_criacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" +\
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" +\
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

            inclusao_pacientes = Pacientes(nome = nome_paciente,
                                            contato_1 = contato_1,
                                            contato_2 = contato_2,
                                            email = email,
                                            cpf = cpf,
                                            rg = rg,
                                            endereco = endereco,
                                            numero_endereco = numero_endereco,
                                            cidade = cidade,
                                            estado = estado,
                                            cep = cep,
                                            data_nascimento = data_nascimento,
                                            sexo = sexo,
                                            profissao = profissao,
                                            data_criacao = data_criacao,
                                            data_modificacao = data_criacao,
                                            id_cliente_fk = id_cliente_fk
            )

            form = PacientesrForm(instance=inclusao_pacientes)
            if form.verify_duplicate():
                inclusao_pacientes.save()

            return redirect('pacientes')

        else:

            return render(request, 'novo_pacientes.html')

@login_required(login_url='login')
def editar_paciente(request):
    if request.user.is_active:
        if request.POST:
            id_cliente_fk = busca_id_cliente(request)

            id_paciente_editado = request.GET['id']
            nome_paciente = request.POST.get('nome_paciente')
            contato_1 = request.POST.get('contato_1')
            contato_2 = request.POST.get('contato_2')
            email = request.POST.get('email')
            cpf = request.POST.get('cpf')
            rg = request.POST.get('rg')
            profissao = request.POST.get('profissao')
            data_nascimento = request.POST.get('data_nascimento')
            endereco = request.POST.get('endereco')
            numero_endereco = request.POST.get('numero_endereco')
            cidade = request.POST.get('cidade')
            estado = request.POST.get('estado')
            cep = request.POST.get('cep')
            sexo = request.POST.get('sexo')

            #Verifica se existe algum paciente desse usuário com os mesmos valores de RG e CPF
            pacientes_existentes = Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).values()
            campo_duplicado = []
            for paciente in pacientes_existentes:
                if (rg == paciente['rg']) and (id_paciente_editado != str(paciente['id'])):
                    campo_duplicado.append('RG')
                elif (cpf == paciente['cpf']) and (id_paciente_editado != str(paciente['id'])):
                    campo_duplicado.append('CPF')

                if len(campo_duplicado) > 0:
                    paciente_list = []

                    paciente_list.append(None)
                    paciente_list.append(nome_paciente)
                    paciente_list.append(email)
                    paciente_list.append(contato_1)
                    paciente_list.append(contato_2)
                    paciente_list.append(cpf)
                    paciente_list.append(rg)
                    paciente_list.append(profissao)
                    paciente_list.append(data_nascimento)
                    paciente_list.append(sexo)
                    paciente_list.append(endereco)
                    paciente_list.append(numero_endereco)
                    paciente_list.append(cidade)
                    paciente_list.append(estado)
                    paciente_list.append(cep)

                    paciente_list = json.dumps(paciente_list)
                    campo_duplicado = json.dumps(campo_duplicado)

                    return render(request, 'editar_pacientes.html', {'paciente': paciente_list,
                                                                     'campo_duplicado': campo_duplicado})


            if contato_1 == "":
                contato_1 = None
            if contato_2 == "":
                contato_2 = None
            if email == "":
                email = None
            if cpf == "":
                cpf = None
            if rg == "":
                rg = None
            if profissao == "":
                profissao = None
            if endereco == "":
                endereco = None
            if numero_endereco == "":
                numero_endereco = None
            if cidade == "":
                cidade = None
            if estado == "":
                estado = None
            if endereco == "":
                endereco = None
            if cep == "":
                cep = None
            if sexo == "":
                sexo = None

            now = datetime.datetime.now()
            data_criacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" +\
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" +\
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

            #Atualiza o registro do paciente em questão
            paciente_editado = Pacientes.objects.get(id=id_paciente_editado)
            paciente_editado.nome = nome_paciente
            paciente_editado.contato_1 = contato_1
            paciente_editado.contato_2 = contato_2
            paciente_editado.email = email
            paciente_editado.cpf = cpf
            paciente_editado.rg = rg
            paciente_editado.endereco = endereco
            paciente_editado.numero_endereco = numero_endereco
            paciente_editado.cidade = cidade
            paciente_editado.estado = estado
            paciente_editado.cep = cep
            paciente_editado.data_nascimento = data_nascimento
            paciente_editado.sexo = sexo
            paciente_editado.profissao = profissao
            paciente_editado.data_modificacao = data_criacao
            paciente_editado.id_cliente_fk = id_cliente_fk

            paciente_editado.save()

            return redirect('pacientes')

        else:
            paciente_list = []

            id_paciente = request.GET['id']
            paciente_editado = Pacientes.objects.get(id=id_paciente)

            paciente_list.append(paciente_editado.id)
            paciente_list.append(paciente_editado.nome)
            paciente_list.append(paciente_editado.email)
            paciente_list.append(paciente_editado.contato_1)
            paciente_list.append(paciente_editado.contato_2)
            paciente_list.append(paciente_editado.cpf)
            paciente_list.append(paciente_editado.rg)
            paciente_list.append(paciente_editado.profissao)
            paciente_list.append(paciente_editado.data_nascimento)
            paciente_list.append(paciente_editado.sexo)
            paciente_list.append(paciente_editado.endereco)
            paciente_list.append(paciente_editado.numero_endereco)
            paciente_list.append(paciente_editado.cidade)
            paciente_list.append(paciente_editado.estado)
            paciente_list.append(paciente_editado.cep)

            paciente_list = json.dumps(paciente_list)

            return render(request, 'editar_pacientes.html', {'paciente': paciente_list,
                                                             'campo_duplicado':json.dumps([])})

@login_required(login_url='login')
def deleta_paciente(request):
    if request.user.is_active:
        id = int(request.GET['id_paciente'].strip('exclui_'))
        paciente = Pacientes.objects.get(id=id)
        paciente.delete()

        # Deleta os atendimentos do paciente
        atendimentos_paciente = Fact_atendimentos_procedimentos.objects.filter(id_paciente=id)
        atendimentos_paciente.delete()

        # Deleta ficha anamnese paciente
        anamnese_paciente = Perfil_saude_pacientes.objects.filter(id_paciente=id)
        anamnese_paciente.delete()

        return redirect('pacientes')
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def deleta_usuario_plataforma(request):
    if request.user.is_active:
        id = int(request.GET['id_usuario'].strip('exclui_'))
        usuario = User.objects.get(id=id)
        usuario.delete()

        #Aciona rotina de exclusão do usuário de todas as bases
        usuario = Governanca_clientes.objects.get(id_auth_user=id)
        id_cliente_fk = usuario.id_cliente_pk
        usuario.delete()

        pacientes = Pacientes.objects.filter(id_cliente_fk=id_cliente_fk)
        pacientes.delete()

        perfil_saude = Perfil_saude_pacientes.objects.filter(id_cliente_fk=id_cliente_fk)
        perfil_saude.delete()

        anamnese_tipos = Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk)
        anamnese_tipos.delete()

        atendimentos = Fact_atendimentos_procedimentos.objects.filter(id_cliente_fk=id_cliente_fk)
        atendimentos.delete()

        procedimentos = Procedimentos_individuais.objects.filter(id_cliente_fk=id_cliente_fk)
        procedimentos.delete()

        return redirect('governanca')

@login_required(login_url='/index/')
def configura_anamnese(request):
    #configura anamnese
    if request.user.is_active:
        id_cliente_fk = busca_id_cliente(request)
        tipos_anamnese = Anamnese_tipos.objects.filter(id_cliente_fk = id_cliente_fk).\
                                            exclude(descricao_questao_anamnese='anamnese_nao_guiada'). \
                                            exclude(descricao_questao_secundaria='anamnese_nao_guiada')

        anamnese_nao_guiada = Anamnese_tipos.objects.filter(id_cliente_fk = id_cliente_fk).\
                                    filter(descricao_questao_anamnese='anamnese_nao_guiada').\
                                    filter(descricao_questao_secundaria='anamnese_nao_guiada')

        dados = {
            'tipos_anamnese' : tipos_anamnese,
            'anamnese_nao_guiada' : anamnese_nao_guiada
        }

        return render(request, 'configura_anamnese.html', dados)

@login_required(login_url='/index/')
def editar_anamnese_paciente(request):
    if request.user.is_active:
        if request.POST:
            try:
                id_paciente = int(request.GET['id'])
                id_cliente_fk = busca_id_cliente(request)
                for resposta in request.POST:
                    resposta_secundaria = False
                    if not resposta.startswith("csrf"):
                        try:
                            if resposta.startswith("anamnese_nao_guiada"):
                                resposta_nao_guiada = request.POST.get(resposta)
                                id_anamnese_nao_guiada = list(Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk). \
                                    filter(descricao_questao_anamnese='anamnese_nao_guiada'). \
                                    filter(descricao_questao_secundaria='anamnese_nao_guiada').values())[0]['id']

                                anamnese_nao_guiada = Perfil_saude_pacientes.objects.filter(id_paciente=id_paciente). \
                                    filter(id_anamnese_tipo=id_anamnese_nao_guiada).values()

                                now = datetime.datetime.now()
                                data = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                                               str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                                               str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

                                if len(anamnese_nao_guiada) > 0:
                                    anamnese_editada = Perfil_saude_pacientes.objects.get(id_paciente=id_paciente,
                                                                                          id_anamnese_tipo=id_anamnese_nao_guiada,
                                                                                          id_cliente_fk=id_cliente_fk)
                                    anamnese_editada.descricao_resposta_anamnese = resposta_nao_guiada
                                    anamnese_editada.data_modificacao = data
                                    anamnese_editada.save(
                                        update_fields=['descricao_resposta_anamnese', 'data_modificacao'])

                                else:
                                    inclusao_anamnese = Perfil_saude_pacientes(id_paciente=id_paciente,
                                                                               id_anamnese_tipo=id_anamnese_nao_guiada,
                                                                               descricao_resposta_anamnese=resposta_nao_guiada,
                                                                               data_criacao=data,
                                                                               data_modificacao=data,
                                                                               id_cliente_fk=id_cliente_fk
                                                                               )

                                    inclusao_anamnese.save()

                            else:
                                #Verifica se a questão é secundária
                                resposta_secundaria = resposta.endswith("sec")

                                if resposta_secundaria:
                                    resposta_questao = request.POST.get(resposta)
                                    resposta = resposta.rstrip('sec')
                                    resposta_secundaria = True
                                else:
                                    resposta_questao = request.POST.get(resposta)

                                #Verifica se existe determinado item de anamnese para o paciente
                                anamnese_paciente = Perfil_saude_pacientes.objects.filter(id_paciente=id_paciente).\
                                                                        filter(id_anamnese_tipo = resposta).values()

                                now = datetime.datetime.now()
                                data = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                                               str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                                               str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

                                if len(anamnese_paciente) == 0:
                                    if not resposta_secundaria:
                                        inclusao_anamnese = Perfil_saude_pacientes(id_paciente = id_paciente,
                                                                                    id_anamnese_tipo = resposta,
                                                                                    descricao_resposta_anamnese=resposta_questao,
                                                                                    data_criacao=data,
                                                                                    data_modificacao=data,
                                                                                    id_cliente_fk=id_cliente_fk
                                                                                    )

                                        inclusao_anamnese.save()

                                    else:
                                        inclusao_anamnese = Perfil_saude_pacientes(id_paciente = id_paciente,
                                                                                    id_anamnese_tipo = resposta,
                                                                                    descricao_resposta_secundaria_anamnese=resposta_questao,
                                                                                    data_criacao=data,
                                                                                    data_modificacao=data,
                                                                                    id_cliente_fk=id_cliente_fk
                                                                                    )
                                        inclusao_anamnese.save()
                                else:
                                    if not resposta_secundaria:
                                        anamnese_editada = Perfil_saude_pacientes.objects.get(id_paciente=id_paciente,
                                                                                              id_anamnese_tipo=resposta,
                                                                                              id_cliente_fk=id_cliente_fk)
                                        #anamnese_editada = anamnese_paciente.filter(id_anamnese_tipo=resposta)
                                        anamnese_editada.descricao_resposta_anamnese = resposta_questao
                                        anamnese_editada.data_modificacao = data
                                        anamnese_editada.save(update_fields=['descricao_resposta_anamnese', 'data_modificacao'])

                                    else:
                                        anamnese_editada = Perfil_saude_pacientes.objects.get(id_paciente=id_paciente,
                                                                                              id_anamnese_tipo=resposta,
                                                                                              id_cliente_fk=id_cliente_fk)
                                        # anamnese_editada = anamnese_paciente.filter(id_anamnese_tipo=resposta)
                                        anamnese_editada.descricao_resposta_secundaria_anamnese = resposta_questao
                                        anamnese_editada.data_modificacao = data
                                        anamnese_editada.save(update_fields=['descricao_resposta_secundaria_anamnese', 'data_modificacao'])

                        except:
                            print('Resposta não salva')

            except:
                pass

            return redirect('anamnese')

        else:
            id_cliente_fk = busca_id_cliente(request)
            # Colhe os dados da anamnses a ser editada
            id_paciente = int(request.GET['id'])

            #Carrega os tipos de anamnese para determinado usuário da plataforma
            tipos_anamnese = Anamnese_tipos.objects.filter(id_cliente_fk = id_cliente_fk).\
                                            exclude(descricao_questao_anamnese='anamnese_nao_guiada'). \
                                            exclude(descricao_questao_secundaria='anamnese_nao_guiada')
            anamnese_nao_guiada = Anamnese_tipos.objects.filter(id_cliente_fk = id_cliente_fk).\
                                    filter(descricao_questao_anamnese='anamnese_nao_guiada').\
                                    filter(descricao_questao_secundaria='anamnese_nao_guiada')

            if len(list(anamnese_nao_guiada.values()))>0:
                id_anamnese_nao_guiada = list(anamnese_nao_guiada.values())[0]['id']
                anamnese_nao_guiada_paciente = list(Perfil_saude_pacientes.objects. \
                                                    filter(id_paciente=id_paciente, id_cliente_fk=id_cliente_fk,
                                                           id_anamnese_tipo=id_anamnese_nao_guiada). \
                                                    values('id_paciente', 'id_anamnese_tipo',
                                                           'descricao_resposta_anamnese',
                                                           'descricao_resposta_secundaria_anamnese'))
                anamnese_paciente = list(Perfil_saude_pacientes.objects.\
                                    filter(id_paciente=id_paciente,id_cliente_fk=id_cliente_fk).\
                                    exclude(id_anamnese_tipo=id_anamnese_nao_guiada).\
                                    values('id_paciente', 'id_anamnese_tipo', 'descricao_resposta_anamnese',
                                           'descricao_resposta_secundaria_anamnese'))
            else:
                anamnese_nao_guiada_paciente = []


                anamnese_paciente = list(Perfil_saude_pacientes.objects.\
                                    filter(id_paciente=id_paciente,id_cliente_fk=id_cliente_fk).\
                                    values('id_paciente', 'id_anamnese_tipo', 'descricao_resposta_anamnese',
                                           'descricao_resposta_secundaria_anamnese'))



            tipos_anamnese_list = list(tipos_anamnese.values())
            anamnese_paciente_list = []
            dict_anamnese_paciente = {}
            for item in anamnese_paciente:
                dict_anamnese_paciente['id_paciente'] = item['id_paciente']
                dict_anamnese_paciente['id_anamnese_tipo'] = item['id_anamnese_tipo']
                for anamnese in tipos_anamnese_list:
                    if int(item['id_anamnese_tipo']) == anamnese['id']:
                        dict_anamnese_paciente['descricao_resposta_anamnese'] =\
                                                                item['descricao_resposta_anamnese']
                        dict_anamnese_paciente['resposta_binaria'] = anamnese['resposta_binaria']
                        dict_anamnese_paciente['descricao_resposta_secundaria_anamnese'] =\
                                                                item['descricao_resposta_secundaria_anamnese']
                        dict_anamnese_paciente['habilita_pergunta_secundaria'] = anamnese['habilita_pergunta_secundaria']
                        dict_anamnese_paciente['resposta_binaria_secundaria'] = anamnese['resposta_binaria_secundaria']
                        dict_anamnese_paciente['status_anamnese'] = anamnese['status_anamnese']
                anamnese_paciente_list.append(dict_anamnese_paciente)
                dict_anamnese_paciente = {}


            anamnese_paciente = json.dumps(anamnese_paciente_list)
            # verifica o status da anamnese não guiada para enviar os dados desse campo
            try:
                if list(anamnese_nao_guiada.values())[0]['nao_guiada']:
                    anamnese_nao_guiada_paciente = anamnese_nao_guiada_paciente
                else:
                    anamnese_nao_guiada_paciente = json.dumps([])
            except:
                anamnese_nao_guiada_paciente = json.dumps([])

            dados = {
                'tipos_anamnese': tipos_anamnese,
                'dados_anamnese': anamnese_paciente,
                'status_anamnese_nao_guiada': anamnese_nao_guiada,
                'anamnese_nao_guiada': json.dumps(anamnese_nao_guiada_paciente)
            }

            return render(request, 'anamnese_paciente.html', dados)

@login_required(login_url='/index/')
def criar_item_anamnese(request):
    if request.user.is_active:
        if request.POST:

            id_cliente_fk = busca_id_cliente(request)

            descricao_questao_anamnese = request.POST.get('descricao_questao_anamnese')
            habilita_descricao = request.POST.get('habilita_descricao')
            habilita_pergunta_sec = request.POST.get('habilita_pergunta_sec')
            descricao_questao_sec_anamnese = request.POST.get('descricao_questao_sec_anamnese')
            habilita_descricao_1 = request.POST.get('habilita_descricao_1')

            if habilita_descricao == 'nao':
                habilita_descricao = True
            else:
                habilita_descricao = False

            if habilita_pergunta_sec == 'nao':
                habilita_pergunta_sec = False
                descricao_questao_sec_anamnese = None
                habilita_descricao_1 = False
            else:
                habilita_pergunta_sec = True
                if habilita_descricao_1 == 'nao':
                    habilita_descricao_1 = True
                else:
                    habilita_descricao_1 = False

            now = datetime.datetime.now()
            data_criacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

            data_modificacao = data_criacao
            status_anamnese = True

            inclusao_tipos_anamnese = Anamnese_tipos(descricao_questao_anamnese = descricao_questao_anamnese,
                                            resposta_binaria = habilita_descricao,
                                            habilita_pergunta_secundaria = habilita_pergunta_sec,
                                            descricao_questao_secundaria = descricao_questao_sec_anamnese,
                                            resposta_binaria_secundaria = habilita_descricao_1,
                                            status_anamnese = status_anamnese,
                                            data_criacao = data_criacao,
                                            data_modificacao = data_modificacao,
                                            id_cliente_fk = id_cliente_fk
            )

            inclusao_tipos_anamnese.save()

            return redirect('configura_anamnese')
        else:
            return render(request, 'cria_nova_anamnese.html')

def habilitar_nao_guiada(request):

    id_cliente_fk = busca_id_cliente(request)
    try:
        nao_guiada = list(Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk).\
                            filter(descricao_questao_anamnese='anamnese_nao_guiada').\
                            filter(descricao_questao_secundaria='anamnese_nao_guiada').values())[0]
    except:
        nao_guiada = []

    if len(nao_guiada) > 0:
        pergunta_nao_guiada = nao_guiada['nao_guiada']
        id_pergunta_nao_guiada = nao_guiada['id']
        nao_guiada = Anamnese_tipos.objects.get(id=id_pergunta_nao_guiada)
        now = datetime.datetime.now()
        data_modificacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

        nao_guiada.data_modificacao = data_modificacao
        if pergunta_nao_guiada:
            nao_guiada.nao_guiada = 0
            nao_guiada.status_anamnese = 0
            nao_guiada.save(update_fields=['nao_guiada', 'data_modificacao', 'status_anamnese'])
        else:
            nao_guiada.nao_guiada = 1
            nao_guiada.status_anamnese = 1
            nao_guiada.save(update_fields=['nao_guiada', 'data_modificacao', 'status_anamnese'])
    else:
        #Cria item da anamnese para pergunta não guiada
        descricao_questao_anamnese = 'anamnese_nao_guiada'
        resposta_binaria = False
        habilita_pergunta_sec = False
        descricao_questao_sec_anamnese = descricao_questao_anamnese
        habilita_descricao_1 = False
        now = datetime.datetime.now()
        data_criacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                       str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                       str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

        data_modificacao = data_criacao
        status_anamnese = True
        nao_guiada = 1

        inclusao_tipos_anamnese = Anamnese_tipos(descricao_questao_anamnese = descricao_questao_anamnese,
                                        resposta_binaria = resposta_binaria,
                                        habilita_pergunta_secundaria = habilita_pergunta_sec,
                                        descricao_questao_secundaria = descricao_questao_sec_anamnese,
                                        resposta_binaria_secundaria = habilita_descricao_1,
                                        status_anamnese = status_anamnese,
                                        nao_guiada=nao_guiada,
                                        data_criacao = data_criacao,
                                        data_modificacao = data_modificacao,
                                        id_cliente_fk = id_cliente_fk
        )
        inclusao_tipos_anamnese.save()

    return redirect('configura_anamnese')


@login_required(login_url='/index/')
def deleta_item_anamnese(request):
    "Função para desativar itens da anamnese"
    if request.user.is_active:

        id_cliente_fk = busca_id_cliente(request)

        id_a_ser_desativado = request.GET['id_anamnese'].split('btn')[0]

        now = datetime.datetime.now()
        data_modificacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                       str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                       str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

        anamnese_desativada = Anamnese_tipos.objects.get(id=id_a_ser_desativado)
        anamnese_desativada.status_anamnese = False
        anamnese_desativada.data_modificacao = data_modificacao
        anamnese_desativada.id_cliente_fk = id_cliente_fk
        anamnese_desativada.save()

        return redirect('configura_anamnese')

@login_required(login_url='/index/')
def ativa_item_anamnese(request):
    "Função para desativar itens da anamnese"
    if request.user.is_active:

        id_cliente_fk = busca_id_cliente(request)

        id_a_ser_desativado = request.GET['id_anamnese'].split('btn')[0]

        now = datetime.datetime.now()
        data_modificacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                       str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                       str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

        anamnese_desativada = Anamnese_tipos.objects.get(id=id_a_ser_desativado)
        anamnese_desativada.status_anamnese = True
        anamnese_desativada.data_modificacao = data_modificacao
        anamnese_desativada.id_cliente_fk = id_cliente_fk
        anamnese_desativada.save()

        return redirect('configura_anamnese')

@login_required(login_url='/index/')
def edita_item_anamnese(request):
    if request.user.is_active:
        id_cliente_fk = busca_id_cliente(request)

        if request.POST:
            id_a_ser_editado = request.GET['id_anamnese'].split('btn')[0]

            descricao_questao_anamnese = request.POST.get('descricao_questao_anamnese')
            habilita_descricao = request.POST.get('habilita_descricao')
            habilita_pergunta_sec = request.POST.get('habilita_pergunta_sec')
            descricao_questao_sec_anamnese = request.POST.get('descricao_questao_sec_anamnese')
            habilita_descricao_1 = request.POST.get('habilita_descricao_1')

            if habilita_descricao == 'nao':
                habilita_descricao = True
            else:
                habilita_descricao = False

            if habilita_pergunta_sec == 'nao':
                habilita_pergunta_sec = False
                descricao_questao_sec_anamnese = None
                habilita_descricao_1 = False
            else:
                habilita_pergunta_sec = True
                if habilita_descricao_1 == 'nao':
                    habilita_descricao_1 = True
                else:
                    habilita_descricao_1 = False

            now = datetime.datetime.now()
            data_modificacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)


            anamnese_desativada = Anamnese_tipos.objects.get(id=id_a_ser_editado)
            anamnese_desativada.descricao_questao_anamnese = descricao_questao_anamnese
            anamnese_desativada.resposta_binaria = habilita_descricao
            anamnese_desativada.descricao_questao_secundaria = descricao_questao_sec_anamnese
            anamnese_desativada.habilita_pergunta_secundaria = habilita_pergunta_sec
            anamnese_desativada.resposta_binaria_secundaria = habilita_descricao_1
            anamnese_desativada.data_modificacao = data_modificacao
            anamnese_desativada.id_cliente_fk = id_cliente_fk
            anamnese_desativada.save()

            return redirect('configura_anamnese')

        else:

            id_a_ser_editado = request.GET['id_anamnese'].split('btn')[0]

            # Verifica se o item da Anamnese já está sendo utilizado
            # Caso esteja, as funções do tipo da pergunta tem suas funções de edição desabilitadas
            usuarios_item_anamnese = list(Perfil_saude_pacientes.objects.filter(id_anamnese_tipo=id_a_ser_editado).\
                values_list('id_cliente_fk'))

            desabilita_config = False
            if len(usuarios_item_anamnese) > 0:
                for value in usuarios_item_anamnese:
                    if id_cliente_fk == value[0]:
                        desabilita_config = True
                        break

            anamnese_editada = Anamnese_tipos.objects.get(id=id_a_ser_editado)
            anamnese_list = []
            anamnese_list.append(anamnese_editada.descricao_questao_anamnese)
            anamnese_list.append(anamnese_editada.resposta_binaria)
            anamnese_list.append(anamnese_editada.habilita_pergunta_secundaria)
            anamnese_list.append(anamnese_editada.descricao_questao_secundaria)
            anamnese_list.append(anamnese_editada.resposta_binaria_secundaria)

            anamnese_editada = json.dumps(anamnese_list)
            desabilita_config = json.dumps(desabilita_config)

            return render(request, 'edita_tipo_anamnese.html', {'anamnese': anamnese_editada,
                                                                'desabilita_config': desabilita_config})


@login_required(login_url='/index/')
def anamnese(request):
    if request.user.is_active:
        id_cliente_fk = busca_id_cliente(request)
        lista_status_anamneses = carrega_dados_anamnese(id_cliente_fk)

        error_atendimento = json.dumps(False)

        return render(request, 'anamnese.html', {'status_anamneses': lista_status_anamneses,
                                                 'error_atendimento': error_atendimento})


def carrega_dados_anamnese(id_cliente_fk):


    pacientes = Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).values('id', 'nome')
    lista_ids_pacientes = []
    for paciente in pacientes:
        lista_ids_pacientes.append(str(paciente['id']))

    if len(lista_ids_pacientes) > 0:
        # Busca anamneses dos pacientes
        query = connection.cursor()
        lista = ["'" + str(i) + "'" for i in lista_ids_pacientes]

        query_str = """
             select
                 id, id_paciente, id_anamnese_tipo
             from
                 web_perfil_saude_pacientes
             where 
                id_cliente_fk = '{}'
                and
                id_paciente in ({})

         """.format(str(id_cliente_fk), ','.join(lista))

        query.execute(query_str)
        anamneses_pacientes = query.fetchall()
        query.close()

        # verifica os pacientes que possuem a anamnese preenchida parcialmente ou totalmente
        dict_status_anamneses = {}
        lista_status_anamneses = []
        for id_paciente in lista_ids_pacientes:
            dict_status_anamneses['id_paciente'] = id_paciente
            nome = pacientes.filter(id=int(id_paciente)).values('nome')[0]
            dict_status_anamneses['nome'] = nome['nome']
            for registro in anamneses_pacientes:
                id_paciente_tabela_anamnese = registro[1]
                if id_paciente_tabela_anamnese == id_paciente:
                    dict_status_anamneses['status_anamnese'] = 'completo'
                    break
                else:
                    dict_status_anamneses['status_anamnese'] = 'incompleto'

            lista_status_anamneses.append(dict_status_anamneses)
            dict_status_anamneses = {}

        lista_status_anamneses = json.dumps(lista_status_anamneses)

    else:
        lista_status_anamneses = []

    return lista_status_anamneses



def verifica_registros_pac_anam_proc(id_cliente_fk,
                                     tabelas_verificadas=['Pacientes',
                                                          'Anamnese_tipos',
                                                          'Procedimentos_individuais']):

    dict_verificacoes = {}
    for tabela in tabelas_verificadas:
        if tabela == 'Pacientes':
            if len(list(Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).values())) > 0:
                dict_verificacoes['Pacientes'] = True
            else:
                dict_verificacoes['Pacientes'] = False

        if tabela == 'Anamnese_tipos':
            if len(list(Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk).\
                                filter(status_anamnese=1).values())) > 0:
                dict_verificacoes['Anamnese_tipos'] = True
            else:
                dict_verificacoes['Anamnese_tipos'] = False

        if tabela == 'Procedimentos_individuais':
            if len(list(Procedimentos_individuais.objects.filter(id_cliente_fk=id_cliente_fk).values())) > 0:
                dict_verificacoes['Procedimentos_individuais'] = True
            else:
                dict_verificacoes['Procedimentos_individuais'] = False

    return dict_verificacoes


@login_required(login_url='login')
def atendimentos(request):
    if request.user.is_active:
        id_cliente_fk = busca_id_cliente(request)

        #Chama função para verificar se o usuário já possui pacientes, anamnese e procedimentos registrados
        dict_verificacoes = verifica_registros_pac_anam_proc(id_cliente_fk)
        if not dict_verificacoes.get('Pacientes'):
            pacientes_list = busca_pacientes(id_cliente_fk)

            error_atendimento = json.dumps(True)

            return render(request, 'pacientes.html', {'pacientes': pacientes_list,
                                                      'error_atendimento': error_atendimento})

        # Verifica se o usuário já criou sua ficha de anamnese
        if not dict_verificacoes.get('Anamnese_tipos'):
            lista_status_anamneses = carrega_dados_anamnese(id_cliente_fk)

            error_atendimento = json.dumps(True)

            return render(request, 'anamnese.html', {'status_anamneses': lista_status_anamneses,
                                                     'error_atendimento': error_atendimento})

        # Verifica se o usuário já criou seus procedimentos
        if not dict_verificacoes.get('Procedimentos_individuais'):
            procedimentos_list = carrega_procedimentos(id_cliente_fk)
            error_atendimento = json.dumps(True)

            return render(request, 'procedimentos.html',
                          {'procedimentos': procedimentos_list,
                           'error_atendimento': error_atendimento})


        atendimentos = list(Fact_atendimentos_procedimentos.objects.filter(id_cliente_fk = id_cliente_fk).values())

        campos_atendimentos = ['id', 'id_paciente',
                               'inicio_atendimento', 'final_atendimento',
                               'pagamento_efetuado']
        dict_atendimentos = {}
        lista_atendimentos = []
        buffer_atendimentos = []
        for i in atendimentos:
            if i['id_atendimento'] not in buffer_atendimentos:
                for j in campos_atendimentos:
                    if j == 'pagamento_efetuado':
                        if i[j] == 0:
                            dict_atendimentos[j] = 'Não'
                        else:
                            dict_atendimentos[j] = 'Sim'
                    elif j == 'id_paciente':
                        paciente = list(Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).filter(id=i[j]).values())[0]
                        dict_atendimentos[j] = i[j]
                        dict_atendimentos['nome_paciente'] = paciente['nome']
                        dict_atendimentos['contato_1'] = paciente['contato_1']
                    else:
                        dict_atendimentos[j] = i[j]
                lista_atendimentos.append(dict_atendimentos)
                buffer_atendimentos.append(i['id_atendimento'])
                dict_atendimentos = {}

        atendimentos = json.dumps(lista_atendimentos)

        return render(request, 'atendimentos.html', {'atendimentos': atendimentos})

@login_required(login_url='login')
def novo_atendimento(request):
    if request.user.is_active:
        # carrega clientes da plataforma
        id_cliente_fk = busca_id_cliente(request)
        pacientes = Pacientes.objects.filter(id_cliente_fk = id_cliente_fk)

        paciente_list = []
        pacientes_list = []

        for paciente in pacientes:
            paciente_list.append(paciente.id)
            paciente_list.append(paciente.nome)
            paciente_list.append(paciente.email)
            paciente_list.append(paciente.contato_1)
            paciente_list.append(paciente.rg)

            pacientes_list.append(paciente_list)
            paciente_list = []

        pacientes_list = json.dumps(pacientes_list)

        return render(request, 'novo_atendimento.html', {'pacientes': pacientes_list})

@login_required(login_url='login')
def editar_atendimento(request):

    # Coleta o ID do atendimento e do paciente através do ID do registro de um dos itens do atendimento
    id_cliente_fk = busca_id_cliente(request)
    if request.POST:
        id_paciente = int(request.POST.get('id_paciente'))
        inicio_atendimento = request.POST.get('inicio_atendimento')
        final_atendimento = request.POST.get('final_atendimento')

        #Utilizada a mesma data de criacao e o id_atendimento
        #Os registros antigos são apagados e os novos são incluídos,
        #pois pode ocorrer inclusão ou deleção de procedimentos nos atendimentos
        id_atendimento = request.POST.get('id_atendimento')
        atendimento = Fact_atendimentos_procedimentos.objects.filter(id_atendimento=id_atendimento)
        data_criacao = list(atendimento.values())[0]['data_criacao']
        atendimento.delete()


        observacoes = request.POST.get('observacoes').strip()
        if observacoes == '':
            observacoes = '-'

        # Atendimento com procedimentos individuais
        if request.POST.get('servico') == 'procedimento':
            # Verificação do pagamento
            pagamento = request.POST.get('pagamento')
            if pagamento == 'sim':
                pagamento = 1
            else:
                pagamento = 0

            # Data de criação/modificação
            now = datetime.datetime.now()
            data_modificacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)


            # Carrega os procedimentos do usuário da plataforma
            procedimentos = Procedimentos_individuais.objects.filter(id_cliente_fk=id_cliente_fk)
            for proc in procedimentos:
                qtde_proc = request.POST.get('quant_proc_' + str(proc.id))
                qtde_proc = int(qtde_proc)
                if qtde_proc > 0:
                    inclusao_atendimento = Fact_atendimentos_procedimentos(
                        id_atendimento=id_atendimento,
                        id_paciente=id_paciente,
                        inicio_atendimento=inicio_atendimento,
                        final_atendimento=final_atendimento,
                        id_procedimento=str(proc.id),
                        qtde_procedimento=qtde_proc,
                        nome_procedimento=proc.nome_procedimento,
                        valor_procedimento=proc.valor_procedimento,
                        pagamento_efetuado=pagamento,
                        observacao_atendimento=observacoes,
                        data_criacao=data_criacao,
                        data_modificacao=data_modificacao,
                        id_cliente_fk=id_cliente_fk
                    )

                    inclusao_atendimento.save()

        return redirect('atendimentos')
    else:
        id = int(request.GET['id'])
        atendimento = \
        list(Fact_atendimentos_procedimentos.objects.filter(id_cliente_fk=id_cliente_fk).filter(id=id).values())[0]

        #Coleta o ID do atendimento
        id_atendimento = atendimento['id_atendimento']

        #Coleta o ID do paciente
        id_paciente = atendimento['id_paciente']
        paciente = list(Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).filter(id=id_paciente).values())[0]
        dados_a_serem_carregados = ['id', 'nome', 'rg', 'cpf', 'email', 'contato_1']
        dict_paciente_json = {}

        dict_procedimentos_json = {}

        for dado in dados_a_serem_carregados:
            dict_paciente_json[dado] = paciente[dado]

        paciente_json = json.dumps(dict_paciente_json)

        # Carga dos procedimentos
        procedimentos = Procedimentos_individuais.objects.filter(id_cliente_fk=id_cliente_fk)
        procedimento_list = []
        procedimentos_list = []
        lista_ids_procedimentos_atuais = []

        for procedimento in procedimentos:
            if procedimento.id not in lista_ids_procedimentos_atuais:
                lista_ids_procedimentos_atuais.append(str(procedimento.id))
            procedimento_list.append(procedimento.id)
            procedimento_list.append(procedimento.nome_procedimento)
            procedimento_list.append(procedimento.descricao_procedimento)
            procedimento_list.append("R$ " + str(procedimento.valor_procedimento).replace(".", ","))

            procedimentos_list.append(procedimento_list)
            procedimento_list = []


        valor_total = 0
        procedimento_list = []
        #Colhe os dados dos procedimentos do atendimento realizado para viabilizar a edição
        procedimentos_atendimento = \
            list(Fact_atendimentos_procedimentos.objects.filter(id_atendimento=id_atendimento).values())
        for proc in procedimentos_atendimento:
            if proc['id_procedimento'] not in lista_ids_procedimentos_atuais:
                # Adicionando na visão do atendimento um procedimento que já foi excluído
                procedimento_list.append(proc['id_procedimento'])
                procedimento_list.append(proc['nome_procedimento'])
                procedimento_list.append("-")
                procedimento_list.append("R$ " + str(proc['valor_procedimento']).replace(".", ","))
                procedimento_list.append(proc['qtde_procedimento'])
                valor_total += float(proc['valor_procedimento']) * proc['qtde_procedimento']

                procedimentos_list.append(procedimento_list)
                procedimento_list = []
            else:
                for i in procedimentos_list:
                    if str(i[0]) == proc['id_procedimento']:
                        i.append(proc['qtde_procedimento'])
                        valor_total += float((i[3]).replace("R$ ", "").replace(",", ".")) * proc['qtde_procedimento']

        #Insere quantidade nula nos procedimentos que não foram inseridos no atendimento
        len_max = 0
        for proc in procedimentos_list:
            if len_max < len(proc):
                len_max = len(proc)

        for proc in procedimentos_list:
            if len(proc) < len_max:
                proc.append(0)

        # Coleta de informações do atendimento
        observacao = atendimento['observacao_atendimento']
        if observacao == "-":
            observacao = ""

        info_atendimento = {
                        'id_atendimento': atendimento['id_atendimento'],
                        'inicio_atendimento': atendimento['inicio_atendimento'],
                        'final_atendimento': atendimento['final_atendimento'],
                        'pagamento_efetuado': atendimento['pagamento_efetuado'],
                        'observacao_atendimento': observacao,
                        'valor_total': valor_total
        }

        procedimentos_list = json.dumps(procedimentos_list)
        info_atendimento = json.dumps(info_atendimento)

        return render(request, 'edita_atendimento.html', {'paciente': paciente_json,
                                                          'procedimentos': procedimentos_list,
                                                          'info_atendimento': info_atendimento})


@login_required(login_url='login')
def deleta_atendimento(request):
    id_cliente_fk = busca_id_cliente(request)
    id = int(request.GET['id_atendimento'].strip('exclui_'))
    atendimento = list(Fact_atendimentos_procedimentos.objects.filter(id_cliente_fk=id_cliente_fk).filter(id=id).values())[0]

    id_atendimento = atendimento['id_atendimento']

    atendimento_excluido = Fact_atendimentos_procedimentos.objects.filter(id_atendimento=id_atendimento)
    atendimento_excluido.delete()

    return redirect('atendimentos')

@login_required(login_url='login')
def procedimento_novo_atendimento(request):
    if request.user.is_active:
        # carrega clientes da plataforma
        id_cliente_fk = busca_id_cliente(request)
        if request.POST:
            id_paciente = int(request.POST.get('id_paciente'))
            inicio_atendimento = request.POST.get('inicio_atendimento')
            final_atendimento = request.POST.get('final_atendimento')
            observacoes = request.POST.get('observacoes').strip()
            if observacoes == '':
                observacoes = '-'

            # Atendimento com procedimentos individuais
            if request.POST.get('servico') == 'procedimento':
                #Verificação do pagamento
                pagamento = request.POST.get('pagamento')
                if pagamento == 'sim':
                    pagamento = 1
                else:
                    pagamento = 0

                #Data de criação/modificação
                now = datetime.datetime.now()
                data_criacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                               str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                               str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

                #Definição do ID do atendimento para que seja possível agrupar vários procedimentos
                #em um único atendimento
                data_atend = inicio_atendimento.split(' ')[0]
                data_atend = data_atend.split('/')[2] + data_atend.split('/')[1] + data_atend.split('/')[0]

                id_atendimento = data_atend + "_" + data_criacao + "_" + str(id_cliente_fk) + "_" + str(id_paciente)

               #Carrega os procedimentos do usuário da plataforma
                procedimentos = Procedimentos_individuais.objects.filter(id_cliente_fk=id_cliente_fk)
                for proc in procedimentos:
                    qtde_proc = request.POST.get('quant_proc_' + str(proc.id))
                    qtde_proc = int(qtde_proc)
                    if qtde_proc > 0:
                        inclusao_atendimento = Fact_atendimentos_procedimentos(
                        id_atendimento=id_atendimento,
                        id_paciente=id_paciente,
                        inicio_atendimento =inicio_atendimento,
                        final_atendimento =final_atendimento,
                        id_procedimento =str(proc.id),
                        qtde_procedimento =qtde_proc,
                        nome_procedimento =proc.nome_procedimento,
                        valor_procedimento =proc.valor_procedimento,
                        pagamento_efetuado =pagamento,
                        observacao_atendimento =observacoes,
                        data_criacao=data_criacao,
                        data_modificacao =data_criacao,
                        id_cliente_fk =id_cliente_fk
                        )

                        inclusao_atendimento.save()

            return redirect('atendimentos')
        else:

            id_paciente = int(request.GET['id'])
            paciente = list(Pacientes.objects.filter(id=id_paciente).values())[0]
            dados_a_serem_carregados = ['id', 'nome', 'rg', 'cpf', 'email', 'contato_1']
            dict_paciente_json = {}

            dict_procedimentos_json = {}

            for dado in dados_a_serem_carregados:
                dict_paciente_json[dado] = paciente[dado]

            paciente_json = json.dumps(dict_paciente_json)

            #Carga dos procedimentos
            procedimentos = Procedimentos_individuais.objects.filter(id_cliente_fk=id_cliente_fk)
            procedimento_list = []
            procedimentos_list = []

            for procedimento in procedimentos:
                procedimento_list.append(procedimento.id)
                procedimento_list.append(procedimento.nome_procedimento)
                procedimento_list.append(procedimento.descricao_procedimento)
                procedimento_list.append("R$ " + str(procedimento.valor_procedimento).replace(".", ","))

                procedimentos_list.append(procedimento_list)
                procedimento_list = []

            procedimentos_list = json.dumps(procedimentos_list)

            return render(request, 'procedimento_novo_atendimento.html', {'paciente':paciente_json,
                                                                          'procedimentos': procedimentos_list})


@login_required(login_url='/index/')
def relatorios(request):
    if request.user.is_active:
        return render(request, 'relatorios.html')

def relatorioporpaciente(request):
    if request.user.is_active:
        # carrega clientes da plataforma
        id_cliente_fk = busca_id_cliente(request)
        pacientes = Pacientes.objects.filter(id_cliente_fk = id_cliente_fk)

        paciente_list = []
        pacientes_list = []

        for paciente in pacientes:
            paciente_list.append(paciente.id)
            paciente_list.append(paciente.nome)
            paciente_list.append(paciente.email)
            paciente_list.append(paciente.contato_1)
            paciente_list.append(paciente.rg)

            pacientes_list.append(paciente_list)
            paciente_list = []

        pacientes_list = json.dumps(pacientes_list)

        return render(request, 'relatorioporpaciente.html', {'pacientes': pacientes_list})

def seleciona_mes_relatorioporpaciente(request):
    if request.user.is_active:
        id_cliente_fk = busca_id_cliente(request)
        paciente_selecionado = int(request.GET['id'])
        #Verifica se realmente existe um ID de paciente relacionado ao usuário da plataforma
        paciente = Pacientes.objects.filter(id_cliente_fk=id_cliente_fk).get(id=paciente_selecionado)

        arquivo = exporta_relatorio(paciente, id_cliente_fk)

        return arquivo

def exporta_relatorio(paciente, id_cliente_fk):
    pdf, page, layout = cria_pdf()
    info_pessoal_paciente_pdf(layout, paciente)

    info_anamnese_paciente_pdf(layout,paciente, id_cliente_fk)
    pdf, page2, layout2 = cria_pdf(append_new_page=True,
             pdf_object=pdf)
    info_atendimentos_paciente_pdf(layout2, paciente, id_cliente_fk)

    #Cria o nome do relatorio
    data = datetime.datetime.now()
    filename = str(id_cliente_fk) + "_" + str(paciente.id) + "_" + str(data.year) + "_" +\
                str(data.month) + "_" + str(data.day) + "_" + str(data.hour) + "_" +\
                str(data.minute) + "_" + str(data.second) + ".pdf"

    # A cada extração de relatórios é recriada uma pasta com o id do usuário da plataforma e inseridos
    # os relatórios nessa pasta
    #todo: toda vez que o usuário logar ou deslogar, realizar a exclusão desse diretório
    # fileDir = os.path.dirname(os.path.realpath('__file__')) + "\\relatorios\\" + str(id_cliente_fk) + "\\"
    #
    # if os.path.exists(fileDir):
    #     shutil.rmtree(fileDir)
    # os.makedirs(fileDir)
    #
    # #Gera o arquivo
    # with open(fileDir + filename, "wb") as out_file_handle:
    #     PDF.dumps(out_file_handle, pdf)
    #
    #
    # return FileResponse(open(fileDir + filename, 'rb'), as_attachment=True, content_type='application/pdf')
    filename = 'relatorio_' + str(id_cliente_fk) + ".pdf"

    with open(filename, "wb") as out_file_handle:
        PDF.dumps(out_file_handle, pdf)


    return FileResponse(open(filename, 'rb'), as_attachment=True, content_type='application/pdf')

def cria_pdf(append_new_page=False,  pdf_object=None):
    if not append_new_page:
        # Create empty Document
        pdf = Document()

        # Create empty Page
        page = Page()

        # Add Page to Document
        pdf.append_page(page)

        # Create PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        return pdf, page, layout

    else:
        # Create empty Page
        page = Page()

        # Add Page to Document
        pdf_object.append_page(page)

        # Create PageLayout
        layout: PageLayout = SingleColumnLayout(page)

        ps: typing.Tuple[Decimal, Decimal] = PageSize.A4_PORTRAIT.value

        # Line
        r: Rectangle = Rectangle(Decimal(50), Decimal(40), Decimal(200), Decimal(1))
        Shape(
            points=LineArtFactory.rectangle(r),
            stroke_color=HexColor("000000"),
            fill_color=HexColor("000000"),
        ).layout(page, r)

        p: Paragraph = Paragraph('Assinatura do responsável', font="Helvetica-Bold", font_size=7)

        # the next line of code uses absolute positioning
        r: Rectangle = Rectangle(Decimal(50),  # x: 0 + page_margin
                                 Decimal(30),  # y: page_height - page_margin - height_of_textbox
                                 Decimal(200),  # width: page_width - 2 * page_margin
                                 Decimal(1))  # height
        p.layout(page, r)

        r: Rectangle = Rectangle(Decimal(350), Decimal(40), Decimal(200), Decimal(1))
        Shape(
            points=LineArtFactory.rectangle(r),
            stroke_color=HexColor("000000"),
            fill_color=HexColor("000000"),
        ).layout(page, r)

        p: Paragraph = Paragraph('Assinatura do paciente', font="Helvetica-Bold", font_size=7)

        # the next line of code uses absolute positioning
        r: Rectangle = Rectangle(Decimal(350),  # x: 0 + page_margin
                                 Decimal(30),  # y: page_height - page_margin - height_of_textbox
                                 Decimal(200),  # width: page_width - 2 * page_margin
                                 Decimal(1))  # height
        p.layout(page, r)

        return pdf_object, page, layout

def info_pessoal_paciente_pdf(layout, paciente):
    # Let's start by adding a heading
    layout.add(Paragraph("Informações do paciente", font="Helvetica-Bold", font_size=13))
    layout.add(Paragraph("________________________________________________________________________",
                         font="Helvetica-Bold", font_size=9))

    # Use a table to lay out the form
    table: FixedColumnWidthTable = FixedColumnWidthTable(number_of_rows=7, number_of_columns=2)
    font_size = 10
    # Nome
    table.add(Paragraph("Nome: " + paciente.nome, font="Helvetica-Bold", font_size=font_size))
    table.add(Paragraph("RG: " + paciente.rg, font="Helvetica-Bold", font_size=font_size))
    if paciente.cpf is None:
        table.add(Paragraph("CPF: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("CPF: " + paciente.cpf, font="Helvetica-Bold", font_size=font_size))
    if paciente.profissao is None:
        table.add(Paragraph("Profissão: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Profissão: " + paciente.profissao, font="Helvetica-Bold", font_size=font_size))
    if paciente.data_nascimento is None:
        table.add(Paragraph("Data de Nascimento: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Data de Nascimento: " + paciente.data_nascimento, font="Helvetica-Bold", font_size=font_size))
    if paciente.sexo == 'masculino':
        table.add(Paragraph("Sexo : " + 'Masculino', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Sexo: " + 'Feminino', font="Helvetica-Bold", font_size=font_size))
    if paciente.email is None:
        table.add(Paragraph("Email: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Email: " + paciente.email, font="Helvetica-Bold", font_size=font_size))
    if paciente.contato_1 is None:
        table.add(Paragraph("Contato 1: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Contato 1: " + paciente.contato_1, font="Helvetica-Bold", font_size=font_size))
    if paciente.contato_2 is None:
        table.add(Paragraph("Contato 2: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Contato 2: " + paciente.contato_2, font="Helvetica-Bold", font_size=font_size))
    if paciente.endereco is None:
        table.add(Paragraph("Endereço: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Endereço: " + paciente.endereco, font="Helvetica-Bold", font_size=font_size))
    if paciente.numero_endereco is None:
        table.add(Paragraph("Número: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Número: " + str(paciente.numero_endereco), font="Helvetica-Bold", font_size=font_size))
    if paciente.cidade is None:
        table.add(Paragraph("Município: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Município: " + paciente.cidade, font="Helvetica-Bold", font_size=font_size))
    if paciente.estado is None:
        table.add(Paragraph("Estado: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("Estado: " + paciente.estado, font="Helvetica-Bold", font_size=font_size))
    if paciente.cep is None:
        table.add(Paragraph("CEP: " + ' ', font="Helvetica-Bold", font_size=font_size))
    else:
        table.add(Paragraph("CEP: " + paciente.cep, font="Helvetica-Bold", font_size=font_size))

    table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
    table.no_borders()

    # Adding Table to PageLayout
    layout.add(table)

def info_anamnese_paciente_pdf(layout, paciente, id_cliente_fk):

    # Let's start by adding a heading
    layout.add(Paragraph("Anamnese", font="Helvetica-Bold", font_size=13))
    layout.add(Paragraph("________________________________________________________________________",
                         font="Helvetica-Bold", font_size=9))
    font_size = 10

    try:
        #Verifica os itens de anamnese ativos para o usuário
        query = connection.cursor()
        query_str = """
                SELECT 
                    id 
                FROM
                    web_anamnese_tipos
                where
                    status_anamnese = 1
                    and
                    id_cliente_fk = {};
         """.format(id_cliente_fk)
        query.execute(query_str)
        ids_anamneses = [i[0] for i in query.fetchall()]
        query.close()


        anamnese_paciente = Perfil_saude_pacientes.objects.filter(id_paciente=paciente.id).\
                                        filter(id_anamnese_tipo__in=ids_anamneses)
        total_itens = len(anamnese_paciente)

        #Verifica se a não guiada está ativa para o usuário para descontar uma linha da tabela
        qtde_nao_guiada = list(Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk).filter(nao_guiada=1).values())

        if len(qtde_nao_guiada) > 0:
            # Configura o total de linhas sendo igual o total de itens da Anamnese
            if total_itens > 0:
                table: FixedColumnWidthTable = FixedColumnWidthTable(number_of_rows=total_itens-1, number_of_columns=2)
            else:
                layout.add(Paragraph("Anamnese não realizada.", font="Helvetica-Bold", font_size=font_size))
                return
        else:
            if total_itens > 0:
                table: FixedColumnWidthTable = FixedColumnWidthTable(number_of_rows=total_itens, number_of_columns=2)
            else:
                layout.add(Paragraph("Anamnese não realizada.", font="Helvetica-Bold", font_size=font_size))
                return

        # Coleta os nomes mais atuais das perguntas da Anamnese através do ID
        for item in anamnese_paciente:
            anamnese = Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk).get(id=item.id_anamnese_tipo)
            descricao_sec_anamnese_escolhida = anamnese.habilita_pergunta_secundaria
            nao_guiada = anamnese.nao_guiada

            if not nao_guiada:
                #Questão primária
                if item.descricao_resposta_anamnese == 'sim':
                    table.add(Paragraph(anamnese.descricao_questao_anamnese + " " + 'Sim', font="Helvetica-Bold", font_size=font_size))
                elif item.descricao_resposta_anamnese == 'nao':
                    table.add(Paragraph(anamnese.descricao_questao_anamnese + " " + 'Não', font="Helvetica-Bold", font_size=font_size))
                else:
                    table.add(Paragraph(anamnese.descricao_questao_anamnese + " " + item.descricao_resposta_anamnese,
                                        font="Helvetica-Bold", font_size=font_size))

                if descricao_sec_anamnese_escolhida == 1:
                    #Questão secundária
                    if item.descricao_resposta_secundaria_anamnese == 'sim':
                        table.add(Paragraph(anamnese.descricao_questao_secundaria + " " + 'Sim', font="Helvetica-Bold", font_size=font_size))
                    elif item.descricao_resposta_secundaria_anamnese == 'nao':
                        table.add(Paragraph(anamnese.descricao_questao_secundaria + " " + 'Não', font="Helvetica-Bold", font_size=font_size))
                    else:
                        table.add(Paragraph(anamnese.descricao_questao_secundaria + " " + item.descricao_resposta_secundaria_anamnese,
                                            font="Helvetica-Bold", font_size=font_size))
                else:
                    table.add(Paragraph(' ', font="Helvetica-Bold", font_size=font_size))

        table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        table.no_borders()

        # Adding Table to PageLayout
        layout.add(table)

        #Inclusão da anamnese não guiada

        anamnese = Anamnese_tipos.objects.filter(id_cliente_fk=id_cliente_fk).filter(nao_guiada=1)
        habilita_observacoes_gerais = True

        if len(list(anamnese.values())) > 0:
            anamnese_paciente = Perfil_saude_pacientes.objects.filter(id_paciente=paciente.id).\
                                    filter(id_anamnese_tipo=list(anamnese.values())[0]['id'])
        else:
            habilita_observacoes_gerais = False

        if len(list(anamnese_paciente.values())) > 0 and habilita_observacoes_gerais:
            table: FixedColumnWidthTable = FixedColumnWidthTable(number_of_rows=2, number_of_columns=1)

            table.add(Paragraph("Observações gerais: ", font="Helvetica-Bold", font_size=font_size))
            nao_guiada_texto = list(anamnese_paciente.values())[0]['descricao_resposta_anamnese']
            nao_guiada_texto = nao_guiada_texto.strip()
            if nao_guiada_texto == '':
                table.add(Paragraph("Não há observações.", font="Helvetica-Bold", font_size=font_size))
                # pass
            else:
                table.add(Paragraph(nao_guiada_texto, font="Helvetica-Bold", font_size=font_size))

        else:
            table: FixedColumnWidthTable = FixedColumnWidthTable(number_of_rows=2, number_of_columns=1)

            table.add(Paragraph("Observações gerais: ", font="Helvetica-Bold", font_size=font_size))
            table.add(Paragraph("-", font="Helvetica-Bold", font_size=font_size))

        table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
        table.no_borders()

        # Adding Table to PageLayout
        layout.add(table)

    except:
        print('Falha de geração da seção de anamnse do PDF')

def info_atendimentos_paciente_pdf(layout, paciente, id_cliente_fk):

    # Let's start by adding a heading
    layout.add(Paragraph("Atendimentos:", font="Helvetica-Bold", font_size=9))

    atendimentos = Fact_atendimentos_procedimentos.objects.filter(id_paciente=paciente.id).\
                                        filter(id_cliente_fk=id_cliente_fk).order_by('-id_atendimento')
    qtde_atendimentos = len(atendimentos)

    # Configura o total de linhas sendo igual o total de itens da Anamnese
    table: FixedColumnWidthTable = FixedColumnWidthTable(number_of_rows=qtde_atendimentos+1, number_of_columns=6,
                                                         column_widths=[3,3,1,2,3,7])
    font_size = 7
    table.add(Paragraph('Início-Término', font="Helvetica-Bold", font_size=font_size))
    table.add(Paragraph('Procedimento', font="Helvetica-Bold", font_size=font_size))
    table.add(Paragraph('Qtde', font="Helvetica-Bold", font_size=font_size))
    table.add(Paragraph('Valor', font="Helvetica-Bold", font_size=font_size))
    table.add(Paragraph('Pag. efetuado', font="Helvetica-Bold", font_size=font_size))
    table.add(Paragraph('Observações', font="Helvetica-Bold", font_size=font_size))

    for i in atendimentos:
        valor = round(int(i.qtde_procedimento) * i.valor_procedimento, 2)
        valor = "R$ " + str(valor).replace('.', ',')

        table.add(Paragraph(i.inicio_atendimento + " - " + i.final_atendimento,
                            font="Helvetica-Bold", font_size=font_size))
        table.add(Paragraph(i.nome_procedimento, font="Helvetica-Bold", font_size=font_size))
        table.add(Paragraph(str(i.qtde_procedimento), font="Helvetica-Bold", font_size=font_size))
        table.add(Paragraph(valor, font="Helvetica-Bold", font_size=font_size))
        if i.pagamento_efetuado == 1:
            table.add(Paragraph('Sim', font="Helvetica-Bold", font_size=font_size))
        else:
            table.add(Paragraph('Não', font="Helvetica-Bold", font_size=font_size))
        if i.observacao_atendimento is None:
            table.add(Paragraph('', font="Helvetica-Bold", font_size=font_size))
        else:
            table.add(Paragraph(i.observacao_atendimento, font="Helvetica-Bold", font_size=font_size))

    table.set_padding_on_all_cells(Decimal(5), Decimal(5), Decimal(5), Decimal(5))
    # table.no_borders()

    # Adding Table to PageLayout
    layout.add(table)

@login_required(login_url='/index/')
def procedimentos(request):
    if request.user.is_active:
        id_cliente_fk = busca_id_cliente(request)
        procedimentos_list = carrega_procedimentos(id_cliente_fk)

        error_atendimento = json.dumps(False)

        return render(request, 'procedimentos.html',
                      {'procedimentos': procedimentos_list,
                       'error_atendimento': error_atendimento})

def carrega_procedimentos(id_cliente_fk):

    procedimentos = Procedimentos_individuais.objects. \
        filter(id_cliente_fk=id_cliente_fk)

    procedimento_list = []
    procedimentos_list = []

    for procedimento in procedimentos:
        procedimento_list.append(procedimento.id)
        procedimento_list.append(procedimento.nome_procedimento)
        procedimento_list.append(procedimento.descricao_procedimento)
        procedimento_list.append("R$ " + str(procedimento.valor_procedimento).replace(".", ","))

        procedimentos_list.append(procedimento_list)
        procedimento_list = []

    procedimentos_list = json.dumps(procedimentos_list)

    return procedimentos_list

@login_required(login_url='login')
def adicionar_procedimento(request):
    if request.user.is_active:
        if request.POST:
            id_cliente_fk = busca_id_cliente(request)

            nome_procedimento = request.POST.get('nome_procedimento')
            descricao_procedimento = request.POST.get('descricao_procedimento')
            valor_procedimento = request.POST.get('valor_procedimento')
            valor_procedimento = float(valor_procedimento.strip('R$ ').replace('.', '').replace(',', '.'))

            now = datetime.datetime.now()
            data_criacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" +\
                           str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" +\
                           str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

            inclusao_procedimento = Procedimentos_individuais(nome_procedimento = nome_procedimento,
                                            descricao_procedimento=descricao_procedimento,
                                            valor_procedimento=valor_procedimento,
                                            data_criacao = data_criacao,
                                            data_modificacao = data_criacao,
                                            id_cliente_fk = id_cliente_fk
            )

            inclusao_procedimento.save()

            return redirect('procedimentos')

        else:
            return render(request, 'novo_procedimento.html')

@login_required(login_url='login')
def editar_procedimento(request):
    id_cliente_fk = busca_id_cliente(request)
    if request.POST:
        id_a_ser_editado = request.GET['id'].split('btn')[0]
        nome_procedimento = request.POST.get('nome_procedimento')
        descricao_procedimento = request.POST.get('descricao_procedimento')
        valor_procedimento = request.POST.get('valor_procedimento')
        valor_procedimento = float(valor_procedimento.strip('R$ ').replace('.','').replace(',', '.'))
        now = datetime.datetime.now()
        data_modificacao = str(now.year).zfill(4) + "_" + str(now.month).zfill(2) + "_" + \
                       str(now.day).zfill(2) + "_" + str(now.hour).zfill(2) + "_" + \
                       str(now.minute).zfill(2) + "_" + str(now.second).zfill(2)

        procedimento_a_ser_editado = Procedimentos_individuais.objects.get(id=id_a_ser_editado)
        procedimento_a_ser_editado.nome_procedimento = nome_procedimento
        procedimento_a_ser_editado.descricao_procedimento = descricao_procedimento
        procedimento_a_ser_editado.valor_procedimento = valor_procedimento
        procedimento_a_ser_editado.data_modificacao = data_modificacao
        procedimento_a_ser_editado.save()

        return redirect('procedimentos')
    else:
        id_a_ser_editado = request.GET['id'].split('btn')[0]
        procedimento_a_ser_editado = Procedimentos_individuais.objects. \
                                        filter(id_cliente_fk=id_cliente_fk).filter(id=id_a_ser_editado).\
                                        values()[0]

        dict_procedimento = {}
        for item in procedimento_a_ser_editado.items():
            if item[0] == 'valor_procedimento':
                dict_procedimento[item[0]] = "R$ " + str(item[1]).replace('.', ',')
            elif item[0] in ['data_criacao', 'data_modificacao', 'id_cliente_fk']:
                pass
            else:
                dict_procedimento[item[0]] = item[1]

        return render(request, 'editar_procedimento.html', {'procedimento': dict_procedimento})


@login_required(login_url='login')
def deleta_procedimento(request):
    if request.user.is_active:
        id = int(request.GET['id_procedimento'].strip('exclui_'))
        procedimento = Procedimentos_individuais.objects.get(id=id)
        procedimento.delete()

    return redirect('procedimentos')

# @login_required(login_url='/index/')
def governanca(request):

    if request.user.is_active and request.user.is_superuser:

        usuarios_list = []
        usuario_list = []
        # Essa lista é originada da Auth users do Django
        usuarios = list(User.objects.all())

        # Essa lista de usuários é a tabela criada sem utilização do Django para linkar
        # todos dados dos pacientes com seus respectivos médicos/esteticistas
        usuarios_plataforma = Governanca_clientes.objects.count()

        # Verifica se a tabela de usuários está vazia e caso esteja, chama a função para carregar
        # todos os usuários da auth users para ela
        if usuarios_plataforma != len(usuarios):
            carrega_usuarios_governanca_clientes()

        # carrega clientes da plataforma
        usuarios = Governanca_clientes.objects.all()

        for usuario in usuarios:
            usuario_list.append(usuario.id_auth_user)
            usuario_list.append(usuario.nome)
            usuario_list.append(usuario.email)
            if (usuario.contato_1 is None) or (usuario.contato_1 == ''):
                contato_1 = '-'
            else:
                contato_1 = usuario.contato_1
            if (usuario.contato_2 is None) or (usuario.contato_2 == ''):
                contato_2 = '-'
            else:
                contato_2 = usuario.contato_2
            usuario_list.append(contato_1)
            usuario_list.append(contato_2)
            if usuario.permissao_acesso == 1:
                permissao_acesso = 'Sim'
            else:
                permissao_acesso = 'Não'

            usuario_list.append(permissao_acesso)
            usuario_list.append(usuario.data_modificacao)
            usuarios_list.append(usuario_list)
            usuario_list = []

        usuarios_list = json.dumps(usuarios_list)

        return render(request, 'governanca.html', {'usuarios': usuarios_list})

    else:
        return render(request, 'inicial.html')

def bancodados(request):
    if request.POST:
        consulta = request.POST.get('consulta')
        query = connection.cursor()
        query_str = str(consulta)
        query.execute(query_str)
        dados = query.fetchall()

        columns = [col[0] for col in query.description]

        query.close()

        columns = json.dumps(columns)
        dados = json.dumps(dados)


        return render(request, 'bancodadosresultado.html', {
                                                            'header': columns,
                                                            'dados': dados
        })

    else:
        return  render(request, 'bancodados.html')

def carrega_usuarios_governanca_clientes():

    # cria uma lista de ids da auth users
    usuarios = list(User.objects.values_list('id', flat=True))
    usuarios = [str(usuario) for usuario in usuarios]

    # cria uma lista de usuarios da governança de clientes
    usuarios_clientes = list(Governanca_clientes.objects.values_list('id_auth_user', flat=True))
    usuarios_a_serem_adicionados = []

    # varre a lista da auth user e verifica quem não estão na lista de governança
    for id in usuarios:
        if id not in usuarios_clientes:
            usuarios_a_serem_adicionados.append(id)

    for id in usuarios_a_serem_adicionados:
        usuario = User.objects.get(id=id)

        #geração de chave aleatória para identificação do usuário da plataforma
        chave_aleatoria = str(usuario.id) + str(rd.randint(0, 1000000)).zfill(7)

        # coleta das datas de criação e modificação
        data_criacao = datetime.datetime.now()
        data_criacao = data_criacao.strftime("%Y/%m/%d %H:%M:%S")
        data_modificacao = data_criacao

        # verifica se o usuario é superuser
        if usuario.is_superuser:
            permissao_acesso = 1
        else:
            permissao_acesso = 0

        # coleta do nome e email
        nome = usuario.username
        email = usuario.email

        # Inclusão do novo dispenser alocando-o para os administradores
        inclusao_clientes = Governanca_clientes(id_auth_user=usuario.id,
                                            id_cliente_pk=chave_aleatoria,
                                            permissao_acesso=permissao_acesso,
                                            nome = nome,
                                            email = email,
                                            data_criacao=data_criacao,
                                            data_modificacao=data_modificacao)


        inclusao_clientes.save()

def deletausuarios(request):
    if request.user.is_superuser:
        id = int(request.GET['id_usuario'].strip('exclui_'))
        user = User.objects.get(id=id)
        user.delete()

        # todo: Criar rotina para pegar a chave da tabela de governança e excluir todos os registros
        # de todas as tabelas
        return redirect('cadastro_usuarios')
    else:
        return redirect('dashboard')

@login_required(login_url='login')
def edita_usuarios(request):
    if request.POST:

        # colhe os parâmetros para salvar no BD
        id_auth_user = str(request.POST.get('id_auth_user'))
        nome_usuario = str(request.POST.get('identificacao_usuario'))
        contato_1 = str(request.POST.get('contato_1'))
        contato_2 = str(request.POST.get('contato_2'))
        permissao_acesso = str(request.POST.get('permissao_acesso'))

        usuario_editado = Governanca_clientes.objects.get(id_auth_user=id_auth_user)
        usuario_editado.nome = nome_usuario
        usuario_editado.contato_1 = contato_1
        usuario_editado.contato_2 = contato_2
        usuario_editado.permissao_acesso = permissao_acesso

        # alteração da data de modificação
        data_modificacao = datetime.datetime.now()
        data_modificacao = data_modificacao.strftime("%Y/%m/%d %H:%M:%S")
        usuario_editado.data_modificacao = data_modificacao

        usuario_editado.save()

    return redirect('governanca')

#Views - Cadastrar dispenser
def busca_info_dispenser(dados_usuarios):
    #Verifica se todos os dispensers estão alocados em id's com usuários válidos
    #caso contrário aloca para algum administrador
    ids_validos = list(dados_usuarios.keys())
    dispensers_desalocados = Ident_dispenser.objects.exclude(id_usuario_id__in = ids_validos)
    for dispenser in dispensers_desalocados:
        dispenser.id_usuario_id = 1
        dispenser.save()

    # Relação de dispensers e usuário
    query = connection.cursor()
    query_str = """
         select
             d.topico_dispenser, a.email, d.localizacao
         from
             web_ident_dispenser d
         inner join
             auth_user a
         on
             a.id = d.id_usuario_id;
     """
    query.execute(query_str)
    dados_dispensers = query.fetchall()
    query.close()
    return dados_dispensers

def busca_usuarios():
    # JSON da relação com todos os usuários
    query = connection.cursor()
    query_str = """
        select 
            a.id, a.email 
        from 
            auth_user a;
    """
    query.execute(query_str)
    dados_usuarios = query.fetchall()
    query.close()
    return dados_usuarios

@login_required(login_url='/index/')
def cadastrardispenser(request):
    if request.user.is_superuser:
        try:
            dados_usuarios = busca_usuarios()
            dados_dispensers = busca_info_dispenser(dict(dados_usuarios))

            dados_dispensers = json.dumps(dados_dispensers)
            dados_usuarios = json.dumps(dados_usuarios)

        except:
            dados_dispensers = 'invalido'
            dados_usuarios = 'invalido'

        return render(request, 'cadastrardispenser.html', {'dados': dados_dispensers,
                                                           'usuarios': dados_usuarios})
    else:
        return render(request, 'dashboard/')

@login_required(login_url='/index/')
def adiciona_dispenser(request):
    #Verifica o último dispenser incluído
    try:
        ultimo_dispenser = Ident_dispenser.objects.order_by('-id')[0].id
    except:
        ultimo_dispenser = 0

    #Montagem da string do topico e client ID
    topico_new_dispenser = 'sdtx' + str(ultimo_dispenser + 1).zfill(9)
    client_new_dispenser = topico_new_dispenser

    if request.user.is_superuser:
        id_admin = auth.get_user(request).id

        #Inclusão do novo dispenser alocando-o para os administradores
        new_dispenser = Ident_dispenser(topico_dispenser = topico_new_dispenser,
                                        client_id_mqtt = client_new_dispenser,
                                        localizacao = 'null',
                                        id_usuario_id = id_admin)

        new_dispenser.save()

    return redirect('cadastrardispenser')

@login_required(login_url='/index/')
def deleta_dispenser(request):
    topico_deletado = request.GET['topico_dispenser'].split('_')[1]

    Ident_dispenser.objects.filter(topico_dispenser=topico_deletado).delete()

    return redirect('cadastrardispenser')



def cadastrousuarios(request):

    usuarios_list = []
    usuario_list = []
    usuarios = list(User.objects.all())
    for usuario in usuarios:
        usuario_list.append(usuario.id)
        usuario_list.append(usuario.username)
        usuario_list.append(usuario.email)
        try:
            usuario.date_joined = usuario.date_joined.strftime("%d/%m/%Y, %H:%M:%S")
            usuario.last_login = usuario.last_login.strftime("%d/%m/%Y, %H:%M:%S")
            usuario_list.append(usuario.date_joined)
            usuario_list.append(usuario.last_login)
        except:
            usuario_list.append('data inválida')
            usuario_list.append('data inválida')
        usuarios_list.append(usuario_list)
        usuario_list = []

    usuarios_list = json.dumps(usuarios_list)

    return render(request, 'cadastrarusuarios.html', {'usuarios': usuarios_list})



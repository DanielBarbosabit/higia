from django.urls import path, re_path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from . import views

urlpatterns = [
    path('', views.index),
    path('cria/receita', views.pacientes, name='pacientes'),
    path('atendimentos', views.atendimentos, name='atendimentos'),
    path('novo_atendimento', views.novo_atendimento, name='novo_atendimento'),
    path('editar_atendimento/', views.editar_atendimento, name='editar_atendimento'),
    path('deleta_atendimento/', views.deleta_atendimento, name='deleta_atendimento'),
    path('procedimento_novo_atendimento/', views.procedimento_novo_atendimento, name='procedimento_novo_atendimento'),
    path('pacientes', views.pacientes, name='pacientes'),
    path('adicionar_paciente', views.adicionar_paciente, name='adicionar_paciente'),
    path('editar_paciente/', views.editar_paciente, name='editar_paciente'),
    path('deleta_paciente/', views.deleta_paciente, name='deleta_paciente'),
    path('relatorios', views.relatorios, name='relatorios'),
    path('relatorioporpaciente', views.relatorioporpaciente, name='relatorioporpaciente'),
    path('seleciona_mes_relatorioporpaciente/', views.seleciona_mes_relatorioporpaciente, name='seleciona_mes_relatorioporpaciente'),
    path('anamnese', views.anamnese, name='anamnese'),
    path('editar_anamnese_paciente/', views.editar_anamnese_paciente, name='editar_anamnese_paciente'),
    path('configura_anamnese', views.configura_anamnese, name='configura_anamnese'),
    path('criar_item_anamnese', views.criar_item_anamnese, name='criar_item_anamnese'),
    path('habilitar_nao_guiada', views.habilitar_nao_guiada, name='habilitar_nao_guiada'),
    path('deleta_item_anamnese/', views.deleta_item_anamnese, name='deleta_item_anamnese'),
    path('edita_item_anamnese/', views.edita_item_anamnese, name='edita_item_anamnese'),
    path('ativa_item_anamnese/', views.ativa_item_anamnese, name='ativa_item_anamnese'),
    path('procedimentos', views.procedimentos, name='procedimentos'),
    path('adicionar_procedimento', views.adicionar_procedimento, name='adicionar_procedimento'),
    path('editar_procedimento/', views.editar_procedimento, name='editar_procedimento'),
    path('deleta_procedimento/', views.deleta_procedimento, name='deleta_procedimento'),
    path('governanca', views.governanca, name='governanca'),
    path('deleta_usuario_plataforma/', views.deleta_usuario_plataforma, name='deleta_usuario_plataforma'),
    path(r'index/', views.index, name='index'),
    path('login', views.login, name='login'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('cria_cadastro', views.cria_cadastro, name='cria_cadastro'),
    path(r'dashboard/', views.dashboard, name='dashboard'),
    path(r'logout/', views.logout, name='logout'),
    path('cadastrardispenser/', views.cadastrardispenser, name='cadastrardispenser'),
    path('cadastrousuarios/', views.cadastrousuarios, name='cadastro_usuarios'),
    path('deleta_usuario/', views.deletausuarios, name='deleta_usuario'),
    path('adddispenser/', views.adiciona_dispenser, name='adddispenser'),
    path('deleta_dispenser/', views.deleta_dispenser, name = 'deletar_dispenser'),
    path('edita_usuarios/', views.edita_usuarios, name='edita_usuarios'),
    path('bancodados/', views.bancodados, name='bancodados')
]

urlpatterns += staticfiles_urlpatterns()
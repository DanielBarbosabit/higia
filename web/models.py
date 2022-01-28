from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory

class Governanca_clientes(models.Model):
    id_auth_user = models.CharField(max_length=100, null=False)
    id_cliente_pk = models.CharField(max_length=100, null=False)
    contato_1 = models.CharField(max_length=20, null=True, default=None)
    contato_2 = models.CharField(max_length=20, null=True, default=None)
    permissao_acesso = models.IntegerField(default=0)
    nome = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=100, null=False)
    data_criacao = models.CharField(max_length=20, null=True)
    data_modificacao = models.CharField(max_length=20, null=True)

class Pacientes(models.Model):

    nome = models.CharField(max_length=100, null=False)
    contato_1 = models.CharField(max_length=20, null=True)
    contato_2 = models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=100, null=True)
    cpf = models.CharField(max_length=20, null=True)
    rg = models.CharField(max_length=20, null=True)
    endereco = models.CharField(max_length=100, null=True)
    numero_endereco = models.IntegerField(null=True)
    cidade = models.CharField(max_length=100, null=True)
    estado = models.CharField(max_length=100, null=True)
    cep = models.CharField(max_length=20, null=True)
    data_nascimento = models.CharField(max_length=20, null=True)
    sexo = models.CharField(max_length=20, null=True)
    profissao = models.CharField(max_length=20, null=True)
    data_criacao = models.CharField(max_length=20, null=True)
    data_modificacao = models.CharField(max_length=20, null=True)
    id_cliente_fk = models.CharField(max_length=100, null=True)

class PacientesrForm(ModelForm):
    class Meta:
        model = Pacientes
        fields = ('cpf', 'rg', 'email', 'id_cliente_fk')

    def verify_duplicate(self):
        objects = self.Meta.model.objects.filter(id_cliente_fk=self.initial['id_cliente_fk'])
        for objeto in objects:
            for key, value in self.initial.items():
                if self.initial != 'id_cliente_fk':
                    print(key)
                    print(value)
                    print(objeto)

            print(objeto)

        return True


class Perfil_saude_pacientes(models.Model):
    id_paciente = models.CharField(max_length=100, null=False)
    id_anamnese_tipo = models.CharField(max_length=100, null=False)
    descricao_resposta_anamnese = models.CharField(max_length=2500, null=True)
    descricao_resposta_secundaria_anamnese = models.CharField(max_length=1000, null=True)
    data_criacao = models.CharField(max_length=20, null=True)
    data_modificacao = models.CharField(max_length=20, null=True)
    id_cliente_fk = models.CharField(max_length=100, null=False)

class Anamnese_tipos(models.Model):
    descricao_questao_anamnese = models.CharField(max_length=105, null=False)
    #caso o campo resposta binária seja falso, então a pessoa poderá inserir uma resposta descritiva
    resposta_binaria = models.BooleanField(null=False)
    habilita_pergunta_secundaria = models.BooleanField(null=False)
    descricao_questao_secundaria = models.CharField(max_length=100, null=True)
    resposta_binaria_secundaria = models.BooleanField(null=False)
    status_anamnese = models.BooleanField(null=False)
    nao_guiada = models.BooleanField(null=False, default=False)
    data_criacao = models.CharField(max_length=20, null=True)
    data_modificacao = models.CharField(max_length=20, null=True)
    id_cliente_fk = models.CharField(max_length=105, null=False)

class Fact_atendimentos_procedimentos(models.Model):
    id_atendimento = models.CharField(max_length=100, null=False)
    id_paciente = models.CharField(max_length=100, null=False)
    inicio_atendimento = models.CharField(max_length=20, null=False)
    final_atendimento = models.CharField(max_length=20, null=False)
    id_procedimento = models.CharField(max_length=100, null=False)
    qtde_procedimento = models.IntegerField(default=0)
    nome_procedimento = models.CharField(max_length=100, null=False)
    valor_procedimento = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    pagamento_efetuado = models.IntegerField(default=0)
    observacao_atendimento = models.CharField(max_length=1000, null=True)
    data_criacao = models.CharField(max_length=20, null=True)
    data_modificacao = models.CharField(max_length=20, null=True)
    id_cliente_fk = models.CharField(max_length=100, null=False)

class Procedimentos_individuais(models.Model):
    nome_procedimento = models.CharField(max_length=100, null=False)
    descricao_procedimento = models.CharField(max_length=200, null=False)
    valor_procedimento = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    data_criacao = models.CharField(max_length=20, null=True)
    data_modificacao = models.CharField(max_length=20, null=True)
    id_cliente_fk = models.CharField(max_length=100, null=False)

# class Dados_pacotes_procedimentos(models.Model):
#     nome_pacote = models.CharField(max_length=100, null=False)
#     descricao_pacote = models.CharField(max_length=200, null=False)
#     valor_pacote = models.IntegerField(default=0)
#     tipo_pacote = models.CharField(max_length=10, null=False)
#     qtde_utilizacoes = models.IntegerField(default=0)
#     data_criacao = models.CharField(max_length=20, null=True)
#     data_modificacao = models.CharField(max_length=20, null=True)
#     id_cliente_fk = models.CharField(max_length=100, null=False)

# class Fact_pacote(models.Model):
#     tipo_pacote = models.CharField(max_length=10, null=False)
#     id_procedimento = models.CharField(max_length=100, null=False)
#     data_inicio_pacote = models.CharField(max_length=20, null=False)
#     data_termino_pacote = models.CharField(max_length=20, null=False)
#     campo_adicional_0 = models.CharField(max_length=20, null=False)
#     id_cliente_fk = models.CharField(max_length=100, null=False)

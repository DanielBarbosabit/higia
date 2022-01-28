$(document).ready(function() {

    $('#nome_paciente').val(paciente[1]);
    $('#email').val(paciente[2]);
    $('#contato_1').val(paciente[3]);
    $('#contato_2').val(paciente[4]);
    $('#cpf').val(paciente[5]);
    $('#rg').val(paciente[6]);
    $('#profissao').val(paciente[7]);
    $('#data_nascimento').val(paciente[8]);
    if(paciente[9] == 'masculino'){
        $("#masculino").prop("checked", true);
    }else{
        $("#feminino").prop("checked", true);
    }
    $('#endereco').val(paciente[10]);
    $('#numero_endereco').val(paciente[11]);
    $('#cidade').val(paciente[12]);
    $('#estado').val(paciente[13]);
    $('#cep').val(paciente[14]);

    setTimeout(function(){
        Object.keys(campo_duplicado).forEach(k =>{
            alert("Já existe um paciente cadastrado com o " + campo_duplicado[k] + " inserido.");
        });
    },1500);
})



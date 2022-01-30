$(document).ready(function() {
    $("#button_4").removeClass("nav_link").addClass("nav_link active");

    var tabela = [];
    carrega_dados(tabela);
    mensagem_atendimentos(error_atendimento);

    $('#table_cadastro_usuario').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese.json"
        },
        "columns": [
            {"data": "Paciente"},
            {"data": "Status"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(anamneses).forEach(k =>{

        dict_linhas['Paciente'] =  anamneses[k]['nome'];
//        dict_linhas['Status'] = usuarios[k]['status_anamnese'];
        if (anamneses[k]['status_anamnese'] == 'completo'){
            dict_linhas['Status'] = '<div><img title="Finalizada" src="/static/img/ok_icon.svg">'+
            '<p hidden>Finalizada</p></div>';

            dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                        '<a id="edita_' + anamneses[k][0] +
                            '" class="btn botao_editar_default" href="/editar_anamnese_paciente/?id='+
                               anamneses[k]['id_paciente'] + '"' + '><div class="editar_letras">Editar</div></a>' +
                     '</div>';
        }else{
            dict_linhas['Status'] = '<div><img title="Não iniciada" src="/static/img/error_icon.svg">'+
            '<p hidden>Não iniciada</p></div>';

            dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                        '<a id="edita_' + anamneses[k][0] +
                            '" class="btn botao_iniciar" href="/editar_anamnese_paciente/?id='+
                               anamneses[k]['id_paciente'] + '"' + '><div class="editar_letras">Iniciar</div></a>' +
                     '</div>';
        }

        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}

function mensagem_atendimentos(error_atendimento){
    if (error_atendimento == true){
        $("#error_atendimento").show();
    }else{
        $("#error_atendimento").hide();
    }
}


function exclui_usuario(id){
    $.ajax({
        url: "/deleta_paciente/",
        data: {'id_paciente': id},
        success: function(){
            location.reload();
        }
    })
}

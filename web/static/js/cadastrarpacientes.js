$(document).ready(function() {
    $("#button_2").removeClass("nav_link").addClass("nav_link active");

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
            {"data": "Email"},
            {"data": "Contato 1"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

});

function mensagem_atendimentos(error_atendimento){
    if (error_atendimento == true){
        $("#error_atendimento").show();
    }else{
        $("#error_atendimento").hide();
    }
}

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(usuarios).forEach(k =>{

        dict_linhas['Paciente'] =  usuarios[k][1];
        dict_linhas['Email'] = usuarios[k][2];
        dict_linhas['Contato 1'] = usuarios[k][3];
        dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                                '<a id="edita_' + usuarios[k][0] +
                                    '" class="btn botao_editar" href="/editar_paciente/?id='+
                                       usuarios[k][0] + '"' + '><div class="editar_letras">Editar</div></a>' +
                                '<a id="exclui_' + usuarios[k][0] +
//                               '" class="btn botao_excluir" onclick="exclui_usuario(id)"><div class="excluir_letras">Excluir</div></a>' +
                               '" class="btn botao_excluir" data-toggle="modal" data-target="#modal_edita_usuarios" onclick="carrega_exclusao(id)"><div class="excluir_letras">Excluir</div></a>' +
                             '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}

function carrega_exclusao(id){
    $("#paciente_excluido").val(id);
}

function exclui_usuario(){
    id_paciente = $("#paciente_excluido").val();

    $.ajax({
        url: "/deleta_paciente/",
        data: {'id_paciente': id_paciente},
        success: function(){
            location.reload();
        }
    })
}

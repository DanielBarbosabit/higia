$(document).ready(function() {
    $("#button_3").removeClass("nav_link").addClass("nav_link active");

    var tabela = [];
    carrega_dados(tabela);

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
            {"data": "RG"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(usuarios).forEach(k =>{

        dict_linhas['Paciente'] =  usuarios[k][1];
        dict_linhas['Email'] = usuarios[k][2];
        dict_linhas['Contato 1'] = usuarios[k][3];
        dict_linhas['RG'] = usuarios[k][4];
        dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                                '<a id="edita_' + usuarios[k][0] +
                                    '" class="btn botao_editar" href="/seleciona_mes_relatorioporpaciente/?id='+
                                       usuarios[k][0] + '"' + '><div class="editar_letras">Selecionar</div></a>' +
                             '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
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

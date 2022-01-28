$(document).ready(function() {
    $("#button_5").removeClass("nav_link").addClass("nav_link active");

    var tabela = [];
    carrega_dados(tabela);

    $('#table_cadastro_procedimento').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese.json"
        },
        "columns": [
            {"data": "Procedimento"},
            {"data": "Descrição"},
            {"data": "Valor"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(procedimentos).forEach(k =>{

        dict_linhas['Procedimento'] =  procedimentos[k][1];
        dict_linhas['Descrição'] = procedimentos[k][2];
        dict_linhas['Valor'] = procedimentos[k][3];
        dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                                '<a id="edita_' + procedimentos[k][0] +
                                    '" class="btn botao_editar" href="/editar_procedimento/?id='+
                                       procedimentos[k][0] + '"' + '><div class="editar_letras">Editar</div></a>' +
                                '<a id="exclui_' + procedimentos[k][0] +
                               '" class="btn botao_excluir" onclick="exclui_procedimento(id)"><div class="excluir_letras">Excluir</div></a>' +
                             '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}


function exclui_procedimento(id){
    $.ajax({
        url: "/deleta_procedimento/",
        data: {'id_procedimento': id},
        success: function(){
            location.reload();
        }
    })
}

$(document).ready(function() {
    $("#button_1").removeClass("nav_link").addClass("nav_link active");

    var tabela = [];

    carrega_dados(tabela);

    $('#table_atendimentos').DataTable({
        paging: true,
        searching: true,
//        ordering: true,
        order: [[0, 'desc']],
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese.json"
        },
        "columns": [
            {"data": "Inicio"},
            {"data": "Termino"},
            {"data": "Paciente"},
            {"data": "Contato"},
            {"data": "Pagamento efetuado"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(atendimentos).forEach(k =>{

        dict_linhas['Inicio'] =  atendimentos[k]['inicio_atendimento'];
        dict_linhas['Termino'] = atendimentos[k]['final_atendimento'];
        dict_linhas['Paciente'] = atendimentos[k]['nome_paciente'];
        dict_linhas['Contato'] = atendimentos[k]['contato_1'];
        dict_linhas['Pagamento efetuado'] = atendimentos[k]['pagamento_efetuado'];
        dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                                '<a id="edita_' + atendimentos[k]['id'] +
                                    '" class="btn botao_editar" href="/editar_atendimento/?id='+
                                       atendimentos[k]['id']  + '"' + '><div class="editar_letras">Editar</div></a>' +
                                '<a id="exclui_' + atendimentos[k]['id']  +
                               '" class="btn botao_excluir" onclick="exclui_atendimento(id)"><div class="excluir_letras">Excluir</div></a>' +
                             '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}


function exclui_atendimento(id){
    $.ajax({
        url: "/deleta_atendimento/",
        data: {'id_atendimento': id},
        success: function(){
            location.reload();
        }
    })
}

$(document).ready(function() {
    var tabela = [];
    carrega_dados(tabela);

    $('#table_cadastro_dispenser').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "columns": [
            {"data": "Dispenser"},
            {"data": "Usuário"},
            {"data": "Localização"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

    select_usuarios();

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(dados).forEach(k =>{

        dict_linhas['Dispenser'] =  dados[k][0];
        dict_linhas['Usuário'] = dados[k][1];
        dict_linhas['Localização'] = dados[k][2];
        dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                            '<button id="edita_' + dados[k][0] +
                            '" class="btn botao_editar" data-toggle="modal" data-target="#modal_edita_dispenser" onclick="editar_dispenser(id)">Editar</button>' +
                               '<a id="exclui_' + dados [k][0] +
                               '" class="btn botao_excluir href="deleta_dispenser/" onclick="exclui_dispenser(id)">Excluir</a>' +
                               '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}

function editar_dispenser(id){
    var dispenser_editado = id.split('_')[1];
    $('#identificao_dispenser').text('Dispenser: ' + dispenser_editado);
    $('#id_disperser').val(dispenser_editado);
    Object.keys(dados).forEach(k =>{
        if (dispenser_editado == dados[k][0]){
            $('#localizacao_dispenser').val(dados[k][2]);
        }
    });
    $('#modal_edita_dispenser').trigger('show');
}

function exclui_dispenser(id){
    $.ajax({
        url: "/deleta_dispenser/",
//        dataType: 'json',
        data: {'topico_dispenser': id},
        success: function(){
            location.reload();
        }
    })
}

function select_usuarios(){
    var dicionario = {};
    var data = usuarios;

    var $select = $('#email_usuario');

    for(i=0; i<data.length; i++){
        $select.append($('<option />', { value: data[i][0], text: data[i][1] }));
    }
}



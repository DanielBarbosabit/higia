$(document).ready(function() {
    var tabela = [];
    carrega_dados(tabela);

    $('#table_cadastro_dispenser').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese.json"
        },
        rowReorder: {
            selector: 'td:nth-child(4)'
        },
        responsive: true,
        "columnDefs": [
            {
                "targets": [ 5 ],
                "visible": false
            }
        ],
        "columns": [
            {"data": "Dispenser"},
            {"data": "Localização"},
            {"data": "Consumo diário (pacotes)"},
            {"data": "Consumo semanal (pacotes)"},
            {"data": "Consumo Mensal (pacotes)"},
            {"data": "Capacidade"},
            {"data": "Configurar/ Excluir"}
        ],
        "data": tabela
    });

    setInterval(function(){
        location.reload();
    }, 30000);
});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(dados).forEach(k =>{

        dict_linhas['Dispenser'] =  dados[k]['dispenser'];
        dict_linhas['Localização'] = dados[k]['localizacao'];
        dict_linhas['Consumo diário (pacotes)'] = dados[k]['diario'];
        dict_linhas['Consumo semanal (pacotes)'] = dados[k]['semanal'];
        dict_linhas['Consumo Mensal (pacotes)'] = dados[k]['mensal'];
        dict_linhas['Capacidade'] = dados[k]['relacao_pacotes'];
        dict_linhas['Configurar/ Excluir']= '<div class="container-sm" align="center">' +
                            '<button id="edita_' + dados[k]['dispenser'] +
                            '" class="btn botao_editar" data-toggle="modal" data-target="#modal_edita_dispenser" onclick="editar_dispenser(id)">Configurar</button>' +
                               '<a id="exclui_' + dados [k]['dispenser'] +
                               '" class="btn botao_excluir href="/historico_excluir/" onclick="exclui_dispenser(id)">Excluir</a>' +
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
        if (dispenser_editado == dados[k]['dispenser']){
            $('#localizacao_dispenser').val(dados[k]['localizacao']);
            $('#relacao_dispenser').val(dados[k]['relacao_pacotes']);
        }
    });
    $('#modal_edita_dispenser').trigger('show');
}

function exclui_dispenser(id){
    $.ajax({
        url: "/historico_excluir/",
//        dataType: 'json',
        data: {'topico_dispenser': id},
        success: function(){
            location.reload();
        }
    })
}



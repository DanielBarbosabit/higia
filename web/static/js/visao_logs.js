$(document).ready(function() {
    var tabela = [];

    $("#qtde_logs").text(qtde_logs);
    carrega_dados(tabela);

    var tabela_logs = $('#table_logs_dispenser').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "order": [[ 0, "desc" ]],
        "columns": [
            {"data": "ID do log"},
            {"data": "Dispenser"},
            {"data": "Data"},
            {"data": "Tensão Baterial"},
            {"data": "Nível de papel"},
        ],
        "data": tabela,
        "destroy": true
    });

});



function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(dados).forEach(k =>{

        dict_linhas['ID do log'] =  dados[k][0];
        dict_linhas['Dispenser'] = dados[k][1];
        dict_linhas['Data'] = dados[k][2];
        dict_linhas['Tensão Baterial']= dados[k][3] / 100;
        dict_linhas['Nível de papel']= dados[k][4] / 10;
        tabela.push(dict_linhas);
        dict_linhas = {};
    });
}

setInterval(function(){
    atualiza_logs();
}, 10000);


function atualiza_logs(){
    $.ajax({
        url: "/atualiza_logs/",
        success: function(){
            location.reload()
        }
    })
}
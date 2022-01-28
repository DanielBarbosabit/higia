//Globais
var tempo_atualizacao = 60000;
var tabela = [];

$(document).ready(function() {
    setTimeout(function () {
//        atualiza_grafico_pizza();
    }, 3000);
});


//function atualiza_grafico_pizza(){
//    $.ajax({
//      dataType: 'json',
//      url: '/busca_dados_atuais/',
////          data: data,
//      success: function(dados){
//        grafico_pizza(dados);
//        tab_dispenser();
//      }
//    });
//    //função para atualizar o chart
//    setInterval(function(){
//        console.log('realizando atualizacao do grafico...')
//        $.ajax({
//          dataType: 'json',
//          url: '/busca_dados_atuais/',
////          data: data,
//          success: function(dados){
//            grafico_pizza(dados);
//            tab_dispenser();
//          }
//        });
//    },tempo_atualizacao);
//}

function grafico_pizza(dados){

    if(dados.dispenser != 0){
        $('#sem_dispenser').hide();

        var logs = dados.dispenser;
        var dicionario_ponto = {};
        var dados_dispenser;
        lista_dados = [];
        var lista_graficos = [];
        var dicts_dispenser = {};

    //    Variaveis do grafico de bateria
        var dicionario_ponto_bateria = {};
        var lista_dados_bateria = [];
        var dicts_dispenser_bateria = {};
        var lista_graficos_baterias = [];

//        Variaveis da tabela
        var dict_linha = {};
        var length_array;
        tabela = [];

        Object.keys(logs).forEach(k =>{
//            console.log(logs[k]);
            dados_dispenser = logs[k].dados;

//            Atualizacao da tabela
            length_array = dados_dispenser.length - 1;
            dict_linha['Dispenser'] = logs[k].topico;
            dict_linha['Localização'] = logs[k].localizacao;
            if (length_array > 0){
                dict_linha['Quantidade de papel'] = dados_dispenser[length_array].papel;
                if (dados_dispenser[length_array].bateria > 4.3){
                    dict_linha['Bateria'] = 'OK';
                }else{
                    dict_linha['Bateria'] = 'Substituir';
                }
            }else{
                dict_linha['Quantidade de papel'] = null;
                dict_linha['Bateria'] = 'Condição indefinida';
            }


            tabela.push(dict_linha);
            dict_linha = {};

            Object.keys(dados_dispenser).forEach(i =>{

    //                Dicionario do gráfico de consumo
                    dicionario_ponto['label'] = dados_dispenser[i].data;
                    dicionario_ponto['y'] = dados_dispenser[i].papel;

    //                Dicionario do grafico de tensão de bateria
                    dicionario_ponto_bateria['label'] = dados_dispenser[i].data;
                    dicionario_ponto_bateria['y'] = dados_dispenser[i].bateria;

    //                Inclusao de pontos do grafico de consumo
                    lista_dados.push(dicionario_ponto);
                    dicionario_ponto = {};

    //                Inclusao de pontos do grafico de tensao
                    lista_dados_bateria.push(dicionario_ponto_bateria);
                    dicionario_ponto_bateria = {};

            })
    //        Inclusao de uma linha para cada dispenser

            dicts_dispenser['type'] = "line";
            dicts_dispenser['visible'] = true;
            dicts_dispenser['showInLegend'] = true;
            dicts_dispenser['yValueFormatString'] = "##.#%" / 100,
            dicts_dispenser['name'] = logs[k].topico;
            dicts_dispenser['dataPoints'] = lista_dados;
            lista_dados = [];

            lista_graficos.push(dicts_dispenser);
            dicts_dispenser = {};

            dicts_dispenser_bateria['type'] = "line";
            dicts_dispenser_bateria['visible'] = true;
            dicts_dispenser_bateria['showInLegend'] = true;
            dicts_dispenser_bateria['yValueFormatString'] = "#.## V",
            dicts_dispenser_bateria['name'] = logs[k].topico;
            dicts_dispenser_bateria['dataPoints'] = lista_dados_bateria;
            lista_dados_bateria = [];

            lista_graficos_baterias.push(dicts_dispenser_bateria);
            dicts_dispenser_bateria = {};
        })

        var chart = new CanvasJS.Chart("chartContainer", {
            theme:"light3",
            animationEnabled: false,
            title:{
                text: "Quantidade de papel (%)"
            },
            axisY :{
                title: "Nível de papel (%)",
                suffix: "%",
                labelAutoFit: false,
                minimum: 0,
                maximum: 100
            },
            toolTip: {
                shared: "true"
            },
            legend:{
                cursor:"pointer",
                itemclick : toggleDataSeries
            },
            data: lista_graficos
        });

        if (dados.admin == true){
            var chart_bateria = new CanvasJS.Chart("grafico_bateria", {
                theme:"light3",
                animationEnabled: false,
                title:{
                    text: "Tensão das baterias"
                },
                axisY :{
                    title: "Tensão (V)",
                    suffix: "V",
                    labelAutoFit: false,
                    minimum: 0,
                    maximum: 7
                },
                toolTip: {
                    shared: "true"
                },
                legend:{
                    cursor:"pointer",
                    itemclick : toggleDataSeries
                },
                data: lista_graficos_baterias
            });
        }

        $('#loader_dash').hide();
        chart.render();

        if (dados.admin == true){
            chart_bateria.render();
        }

        function toggleDataSeries(e) {
            if (typeof(e.dataSeries.visible) === "undefined" || e.dataSeries.visible ){
                e.dataSeries.visible = false;
            } else {
                e.dataSeries.visible = true;
            }
            chart.render();
            chart_bateria.render();
        }
    }else{
        $('#container_tabela').hide();
        $('#loader_dash').hide();
        $('#sem_dispenser').text('Infelizmente, você ainda não possui dispensers :(');
        $('#sem_dispenser').show();
        $('#chartContainer').hide();
        $('#grafico_bateria').hide();
    }
}

function tab_dispenser(){
    $('#tabela_dispenser').show();

    var tabela_logs = $('#tabela_dispenser').DataTable({
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
        "order": [[ 2, "asc" ]],
        "columns": [
            {"data": "Dispenser"},
            {"data": "Localização"},
            {"data": "Quantidade de papel"},
            {"data": "Bateria"}
        ],
        "data": tabela,
        "destroy": true,
        "rowCallback": function( row, data, index ) {
        if ( data['Quantidade de papel'] < 20 ){
            $('td', row).css('background-color', '#FF7777');
        }
        }
    });
}

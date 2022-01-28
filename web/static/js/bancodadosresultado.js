$(document).ready(function() {
    $("#button_6").removeClass("nav_link").addClass("nav_link active");

    var tabela = [];
    carrega_dados(tabela);


});

function carrega_dados(tabela){

    tabela = "<tr>"
    linha = ""
    Object.keys(header).forEach(k =>{
        linha = linha + "<th style='border:1px solid black;'>"+header[k]+"</th>";
    });
    tabela = linha+ "</tr>"
    $("#header_query").append(tabela);

    tabela = ""
    Object.keys(dados).forEach(k =>{
        linha = "<tr>"
        Object.keys(dados[k]).forEach(j =>{
            linha = linha + "<td style='border:1px solid black;'>"+dados[k][j]+"</td>"
        });
        linha = linha + "</tr>"
        tabela = tabela + linha
    });

    $("#tabela_query").append(tabela);
}
$(document).ready(function() {

    $('#id_paciente').val(paciente['id']);
    $('#nome_paciente').val(paciente['nome']).prop("readonly", true);
    $('#email').val(paciente['email']).prop("readonly", true);
    $('#contato_1').val(paciente['contato_1']).prop("readonly", true);
    $('#cpf').val(paciente['cpf']).prop("readonly", true);
    $('#rg').val(paciente['rg']).prop("readonly", true);

    carrega_procedimentos();

})

function carrega_procedimentos(){
   Object.keys(procedimentos).forEach(k =>{

    new_proc =  '<div class="row" style="margin-top:1em;">' +
                    '<div class="col-sm-2" style="width:150px">' +
                        '<div class="input-group">' +
                            '<span class="input-group-prepend">' +
                                '<button type="button" class="btn btn-outline-secondary btn-number" disabled="disabled" data-type="minus" data-field="quant_proc_' + procedimentos[k][0] + '">' +
                                    '<span class="fa fa-minus"></span>' +
                                '</button>' +
                            '</span>' +
                            '<input type="text" name="quant_proc_' + procedimentos[k][0] + '" id="quant_proc_' + procedimentos[k][0] + '" class="form-control input-number" value="0" min="0" max="99">' +
                            '<span class="input-group-append">' +
                                '<button type="button" class="btn btn-outline-secondary btn-number" data-type="plus" data-field="quant_proc_' + procedimentos[k][0] + '">' +
                                    '<span class="fa fa-plus"></span>' +
                                '</button>' +
                            '</span>' +
                        '</div>' +
                    '</div>' +
                '<div class="col-sm-3"><input type="text" id="valor_proc_' + procedimentos[k][0] + '" class="form-control input-number" value="R$ 0,00" disabled="disabled"></div>' +
                '<div class="col-sm-3"><h5>' + procedimentos[k][1] + '</h5></div>' +
           '</div>';
    $('#lista_procedimentos').append(new_proc);

    });

    carrega_funcoes_botoes();
 }

//Funções para configuração dos calendários de data inicial e final
$(function () {
    var dateNow = new Date();
    $('#inicio_atendimento').datetimepicker({
        sideBySide: true,
        locale: 'pt',
        defaultDate: dateNow.setMinutes(0)
    });
});

$(function () {
    var dateNow = new Date();
    dateNow = dateNow.setHours(dateNow.getHours()+1, 0);
    //    dateNow = dateNow.setMinutes(dateNow.getMinutes()+60);
    $('#final_atendimento').datetimepicker({
        sideBySide: true,
        locale: 'pt',
        defaultDate: dateNow
    });
});

function atualiza_valores(botao_quantidade){
    console.log(botao_quantidade);
    id_procedimento = botao_quantidade.replace('quant_proc_', '');

    qtde_procedimento = parseFloat($("#quant_proc_" + id_procedimento).val());

    Object.keys(procedimentos).forEach(k =>{
        if (procedimentos[k][0] == id_procedimento){
            valor_procedimento = parseFloat(procedimentos[k][3].replace('R$ ', '').replace(',', '.'));
        }
    })
    valor_procedimento = qtde_procedimento * valor_procedimento;
    valor_procedimento_str = valor_procedimento.toFixed(2);
    valor_procedimento_str = "R$ " + valor_procedimento_str.replace(".", ",");
    $('#valor_proc_' + id_procedimento).val(valor_procedimento_str);

    calcula_total();
}

function calcula_total(){
    total = 0;
    Object.keys(procedimentos).forEach(k =>{
        parcial = parseFloat($('#valor_proc_' + procedimentos[k][0]).val().replace('R$ ', '').replace(',', '.'));
        total = total + parcial;
    })
    total = total.toFixed(2);
    total = "R$ " + total.replace(".", ",");
    $("#total").val(total);
}


function carrega_funcoes_botoes(){
    //Botões para controle das unidades de procedimentos/pacotes
    $('.btn-number').click(function(e){
        e.preventDefault();

        fieldName = $(this).attr('data-field');
        type      = $(this).attr('data-type');
        var input = $("input[name='"+fieldName+"']");
        var currentVal = parseInt(input.val());
        if (!isNaN(currentVal)) {
            if(type == 'minus') {

                if(currentVal > input.attr('min')) {
                    input.val(currentVal - 1).change();
                }
                if(parseInt(input.val()) == input.attr('min')) {
                    $(this).attr('disabled', true);
                }

            } else if(type == 'plus') {

                if(currentVal < input.attr('max')) {
                    input.val(currentVal + 1).change();
                }
                if(parseInt(input.val()) == input.attr('max')) {
                    $(this).attr('disabled', true);
                }

            }
        } else {
            input.val(0);
        }

        atualiza_valores(fieldName);
    });

    $('.input-number').focusin(function(){
       $(this).data('oldValue', $(this).val());
    });
    $('.input-number').change(function() {

        minValue =  parseInt($(this).attr('min'));
        maxValue =  parseInt($(this).attr('max'));
        valueCurrent = parseInt($(this).val());

        name = $(this).attr('name');
        if(valueCurrent >= minValue) {
            $(".btn-number[data-type='minus'][data-field='"+name+"']").removeAttr('disabled')
        } else {
            alert('Sorry, the minimum value was reached');
            $(this).val($(this).data('oldValue'));
        }
        if(valueCurrent <= maxValue) {
            $(".btn-number[data-type='plus'][data-field='"+name+"']").removeAttr('disabled')
        } else {
            alert('Sorry, the maximum value was reached');
            $(this).val($(this).data('oldValue'));
        }
    });

    $(".input-number").keydown(function (e) {
        // Allow: backspace, delete, tab, escape, enter and .
        if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 190]) !== -1 ||
             // Allow: Ctrl+A
            (e.keyCode == 65 && e.ctrlKey === true) ||
             // Allow: home, end, left, right
            (e.keyCode >= 35 && e.keyCode <= 39)) {
                 // let it happen, don't do anything
                 return;
        }
        // Ensure that it is a number and stop the keypress
        if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
            e.preventDefault();
        }
    });
}

//Seleção do HTML de procedimentos individuais ou pacotes
$("#procedimento").click(function() {
  $("#procedimentos_individuais").css('visibility', 'visible')
});

$("#pacote").click(function() {
  $("#procedimentos_individuais").css('visibility', 'hidden')
});

function coleta_string_data_horario(inicio){
    dia = inicio.split("/")[0]
    mes = inicio.split("/")[1]
    ano = (inicio.split("/")[2]).split(" ")[0]
    hora = ((inicio.split("/")[2]).split(" ")[1]).split(":")[0]
    minuto = ((inicio.split("/")[2]).split(" ")[1]).split(":")[1]

    string = ano + mes + dia + hora + minuto;
    return string
}

//Função para verificar se algum procedimento foi escolhido
function verifica_escolha_procedimento(){
    total = $("#total").val();
    inicio = $("#inicio_atend").val();
    final = $("#final_atend").val();
    inicio_ = inicio.replace(" ", "");
    final_ = final.replace(" ", "");

    if ((inicio_ != "") && (final_ != "")){
        inicio = coleta_string_data_horario(inicio)
        final = coleta_string_data_horario(final)

        if ((inicio > final) || (inicio_ == "") || (final_ == "")) {
            alert("Data de início do atendimento superior à data de término")
        }else if (total == "R$ 0,00"){
            alert("Nenhum procedimento foi escolhido");
        }else{
            $("#form_atendimento").submit();
        }

    }else{
        alert("Data de início ou de término do atendimento inválidas")
    }


}

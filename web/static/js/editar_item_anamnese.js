$("#sim_sec").click(function() {
  $("#linha_questao_secundaria").css('visibility', 'visible')
  $("#linha_resposta_descritiva_secundaria").css('visibility', 'visible')
  $("#descricao_questao_sec_anamnese").prop("required", true);
});

$("#nao_sec").click(function() {
  $("#linha_questao_secundaria").css('visibility', 'hidden')
  $("#linha_resposta_descritiva_secundaria").css('visibility', 'hidden')
  $("#descricao_questao_sec_anamnese").prop("required", false);
});

function carrega_dados(){
    console.log(dados)
    $("#descricao_questao_anamnese").val(dados[0]);

//  verificase a a resposta é binária
    if (dados[1] == true){
        $("#nao").prop("checked", true);
        if(desabilita_config == true){
            $("#sim").prop("disabled", true);
        }
    }else{
        $("#sim").prop("checked", true);
        if(desabilita_config == true){
            $("#nao").prop("disabled", true);
        }
    }

//  Caso já exista alguma anamnese utilizando essa pergunta, ela terá seu tipo bloqueado

//    Verifica se possui pergunta secundária
    if (dados[2] == true){
        $("#sim_sec").prop("checked", true);
        if(desabilita_config == true){
            $("#nao_sec").prop("disabled", true);
        }
        $("#linha_questao_secundaria").css('visibility', 'visible')
        $("#linha_resposta_descritiva_secundaria").css('visibility', 'visible')
        $("#descricao_questao_sec_anamnese").prop("required", true);
        $("#descricao_questao_sec_anamnese").val(dados[3]);
        if (dados[4] == true){
            $("#nao_1").prop("checked", true);
            if(desabilita_config == true){
                $("#sim_1").prop("disabled", true);
            }
        }else{
            $("#sim_1").prop("checked", true);
            if(desabilita_config == true){
                $("#nao_1").prop("disabled", true);
            }
        }
    }else{
        $("#nao_sec").prop("checked", true);
        if(desabilita_config == true){
            $("#sim_sec").prop("disabled", true);
        }
        $("#linha_questao_secundaria").css('visibility', 'hidden')
        $("#linha_resposta_descritiva_secundaria").css('visibility', 'hidden')
        $("#descricao_questao_sec_anamnese").prop("required", false);
    }

}
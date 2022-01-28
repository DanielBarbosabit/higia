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

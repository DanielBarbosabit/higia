$(document).ready(function() {
    $("#button_4").removeClass("nav_link").addClass("nav_link active");

     Object.keys(anamneses).forEach(k =>{
        if (anamneses[k]['status_anamnese'] == true){
            if (anamneses[k]['resposta_binaria'] == true){
                if (anamneses[k]['descricao_resposta_anamnese'] == 'nao'){
                    string_id = "#nao_prim" + anamneses[k]['id_anamnese_tipo']
                    $(string_id).prop("checked", true);
                }else{
                    string_id = "#sim_prim" + anamneses[k]['id_anamnese_tipo']
                    $(string_id).prop("checked", true);
                }

            }else{
                string_id = "#dis_prim" + anamneses[k]['id_anamnese_tipo']
                $(string_id).val(anamneses[k]['descricao_resposta_anamnese']);
            }
            if (anamneses[k]['habilita_pergunta_secundaria']){
                if(anamneses[k]['resposta_binaria_secundaria']){
                    if(anamneses[k]['descricao_resposta_secundaria_anamnese'] == true){
                        string_id = "#nao_sec" + anamneses[k]['id_anamnese_tipo']
                        $(string_id).prop("checked", true);
                    }else{
                        string_id = "#sim_sec" + anamneses[k]['id_anamnese_tipo']
                        $(string_id).prop("checked", true);
                    }
                }else{
                    string_id = "#dis_sec" + anamneses[k]['id_anamnese_tipo']
                    $(string_id).val(anamneses[k]['descricao_resposta_secundaria_anamnese']);
                }
            }
        }
    });

//    #Escreve na caixa de texto da anamnese não guiada
    console.log(anamnese_nao_guiada[0]);
    if(anamnese_nao_guiada.length > 0){
        $("#anamnese_nao_guiada").val(anamnese_nao_guiada[0]['descricao_resposta_anamnese'])
    }

});


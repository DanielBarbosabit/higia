function deleta_item_anamnese(id) {
    $.ajax({
        url: "/deleta_item_anamnese/",
        data: {'id_anamnese': id},
        success: function(){
            location.reload();
        }
    })
}

function ativa_item_anamnese(id) {
    $.ajax({
        url: "/ativa_item_anamnese/",
        data: {'id_anamnese': id},
        success: function(){
            location.reload();
        }
    })
}
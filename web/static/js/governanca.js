$(document).ready(function() {
    $("#button_6").removeClass("nav_link").addClass("nav_link active");

    var tabela = [];
    carrega_dados(tabela);

    $('#table_cadastro_usuario').DataTable({
        paging: true,
        searching: true,
        ordering: true,
        "language": {
            "url": "https://cdn.datatables.net/plug-ins/1.10.21/i18n/Portuguese.json"
        },
        "columns": [
            {"data": "Usuário"},
            {"data": "Email"},
            {"data": "Contato 1"},
            {"data": "Contato 2"},
            {"data": "Permissão"},
            {"data": "Ação"}
        ],
        "data": tabela
    });

});

function carrega_dados(tabela){

    var dict_linhas = {};

    Object.keys(usuarios).forEach(k =>{

        dict_linhas['Usuário'] =  usuarios[k][1];
        dict_linhas['Email'] = usuarios[k][2];
        dict_linhas['Contato 1'] = usuarios[k][3];
        dict_linhas['Contato 2'] = usuarios[k][4];
        dict_linhas['Permissão'] = usuarios[k][5];
        dict_linhas['Ação']= '<div class="container-sm" align="center">' +
                                '<a id="edita_' + usuarios[k][0] +
                                    '" class="btn botao_editar" data-toggle="modal" data-target="#modal_edita_usuarios"'+
                                     ' onclick="editar_usuario(id)">Editar</a>' +
                                '<a id="exclui_' + usuarios[k][0] +
                               '" class="btn botao_excluir" onclick="exclui_usuario(id)">Excluir</a>' +
                             '</div>';
        tabela.push(dict_linhas);

        dict_linhas = {};
    });
}


function exclui_usuario(id){
    $.ajax({
        url: "/deleta_usuario_plataforma/",
        data: {'id_usuario': id},
        success: function(){
            location.reload();
        }
    })
}

function editar_usuario(id){

    var usuario_editado = id.split('_')[1];
//    $('#identificao_usuario').text('Usuário: ' + usuario_editado);
    $('#id_disperser').val(usuario_editado);

    Object.keys(usuarios).forEach(k =>{
        if (usuario_editado == usuarios[k][0]){
            $('#id_auth_user').val(usuarios[k][0]);
            $('#identificacao_usuario').text(usuarios[k][1]);
            $('#contato_1').text(usuarios[k][3]);
            $('#contato_2').text(usuarios[k][4]);
            if (usuarios[k][5] == 'Sim'){
                $('#permissao_acesso').val('1');
            }else{
                $('#permissao_acesso').val('0');
            }
        }
    });
    $('#modal_edita_dispenser').trigger('show');
}



$(document).ready(function(){

  //LOAD LOGIN AND SIGN UP form
  /*$(document).on('click','#modal-user',function(){

    var div_login= $('#login-form')
    var div_signup= $('#signup-form')
    $.ajax({
      url:'/accounts/login/',
      success:function(data){
        div_login.html(data);
      }
    });
    $.ajax({
      url:'/accounts/register/',
      success:function(data){
        div_signup.html(data);
      }
    });
  });

  */
  
  // PRESS BORRAR
  $(document).on('click',".deletebutton",function(){

    var recetaid= $(this).attr("recepy-id");
    $.ajax({
      url: "/delete/"+recetaid,
      method:"GET",
      success: function(data){
        $("#dr-"+recetaid).html(data);
        $("#dr-"+recetaid).slideToggle('slow');

      }
    });
  });

  // PRESS AGREGAR RECETA
    $("#agregar_receta").click(function (){

      if ($("#agregarDiv").is(':hidden')){
        $('#full-container').hide();
        $('footer').hide();

        $('#paginador').hide();
        $("#agregarDiv").slideToggle();
      }else {
        $('#full-container').show();

        $('#paginador').show();
        $('footer').show();
        $("#agregarDiv").slideToggle('slow');

      }
    });




  // PRESS CANCELAR EN EL FORM AGREGAR RECETA
  $(document).on('click','#no_agregar',function(){
    $("#agregarDiv").slideToggle();
    $('footer').show();
    $('#full-container').show();
    $('#paginador').show();
  });

  // SUBMIT EL FORM DE AGREGAR RECETAS
  var form_r= $('#form_r');
  form_r.submit(function(e) {
    e.preventDefault();

    $.ajax({
      type:form_r.attr('method'),
      url:form_r.attr('action'),
      data: form_r.serialize(),
      error: function(data){
        alert('la receta no se guardo CORRECTAMENTE');
        console.log('la receta no se guardo CORRECTAMENTE');
      }
    }).done( function(data){
      var content = $( data ).find( "#recepy-grid" );

      console.log(content);
      var pcont = $(data).find(".pagination");
      $( "#full-container" ).empty().append( content );
      $('#paginador').empty().append(pcont);
      salvattore.recreateColumns(document.querySelector('#grid'));
      $("#agregarDiv").slideToggle();
      $('#full-container').show();
      $('#paginador').show();

      });
    });
});

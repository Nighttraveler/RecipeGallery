$(document).ready(function(){

  function cambiar_pag(event,i) {
        event.preventDefault()
        var pag= $(i).attr('href');
        console.log(pag);
        $.ajax({
            url:pag,
            success:function(data){
              var content = $( data ).find( "#contenedor-recetas" );
              var contentPager = $( data).find('.pagination');

              $( "#full-container" ).fadeTo('fast',0.5);
              $( "#full-container" ).empty().append( content );
              $('#paginador').empty().append( contentPager);
              $( "#full-container" ).fadeTo('fast',1);
            }
        });
  }
  // PRESS BORRAR
  $(document).on('click',".deletebutton",function(){

    var recetaid= $(this).attr("recepy-id");
    console.log(recetaid);

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
//  $(document).ready(function(){

    $("#agregar_receta").click(function (){

      if ($("#agregarDiv").is(':hidden')){
        $('#full-container').hide();
        $('footer').hide();
        console.log("esta a la vista");
        $('#paginador').hide();
        $("#agregarDiv").slideToggle();
      }else {
        $('#full-container').show();
        console.log("esta a la escondido");
        $('#paginador').show();
        $('footer').show();
        $("#agregarDiv").slideToggle('slow');

      }
    });


//  });

  // PRESSS CANCELAR EN EL FORM AGREGAR RECETA
  $(document).on('click','#no_agregar',function(){
    $("#agregarDiv").slideToggle();
    $('#full-container').show();
    $('#paginador').show();
  });



  $(document).on('click','.page-activa',function(event){
    event.preventDefault();
    var pag= $(this).attr('href')+$(this).attr('numpag');

    $.ajax({
        url:pag,
        success:function(data){

          var content = $( data ).find( "#contenedor-recetas" );
          var contentPager = $( data).find('.pagination');
          $( "#full-container" ).fadeTo('fast',0.5);
          $('#paginador').empty().append( contentPager);
          $( "#full-container" ).empty().append( content );
          $( "#full-container" ).fadeTo('fast',1);
        }
    });
  });
  // PAGINA ANTERIOR
  $(document).on('click','#pagina_siguiente',  function(event){
    var i = '#pagina_siguiente';
    cambiar_pag(event,i);
  });
  //PAGINA SIGUIENTE
  $(document).on('click','#pagina_anterior', function(event){
    var i = '#pagina_anterior';
    cambiar_pag(event,i);
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
      var content = $(data).find( "#contenedor-recetas" );
      var contentPager = $(data).find('.pagination');
      $( "#full-container" ).empty().append( content );
      $('#paginador').empty().append( contentPager);
      $("#agregarDiv").slideToggle();
      $('#full-container').show();
      $('#paginador').show();

      });
    });
});

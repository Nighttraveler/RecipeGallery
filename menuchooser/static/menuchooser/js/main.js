$(document).ready(function(){

  $("#agregar_receta").click(function (){

    if ($("#agregarDiv").is(':hidden')){
      $('#full-container').fadeOut("slow");
      console.log("esta a la vista");
      $('#paginador').hide();
      $("#agregarDiv").slideToggle('slow');
    }else {
      $('#full-container').show();
      console.log("esta a la escondido");
      $('#paginador').show();
      $("#agregarDiv").slideToggle('slow');

    }
  });


});

$(document).ready(function(){

    // Add smooth scrolling to all links in navbar + footer link
    $(".slow_scroll").on('click', function(event) {
            // Prevent default anchor click behavior
            event.preventDefault();

            // Store hash
            var hash = this.hash;

            // Using jQuery's animate() method to add smooth page scroll
            // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
            $('html, body').animate({
              scrollTop: $(hash).offset().top
            }, 900, function(){

              // Add hash (#) to URL when done scrolling (default click behavior)
              window.location.hash = hash;
              });
    });



    $(window).scroll(function() {
      $(".slideanim").each(function(){
        var pos = $(this).offset().top;

        var winTop = $(window).scrollTop();
        if (pos < winTop + 600) {
          $(this).addClass("slide");
        }
      });
    });

   //like counting */

      $('.recipe-likes').click(function() {
          $('.glyphicon').toggle();
          var id;
          id = $(this).attr('data-post-id');
          $.get('/like-recipe/', {
              recipe_id: id
          }, function(data) {
              $('.like_count_blog').html(data);
          });
      });



  // PRESS BORRAR
  $(document).on('click',".deletebutton",function(){

    var recetaid= $(this).attr("recepy-id");
    $.ajax({
      url: "/delete/"+recetaid,
      method:"GET",
      success: function(data){
        $("#dr-"+recetaid).html(data);
        $("#dr-"+recetaid).slideDown('slow');

      }
    });
  });


// PRESS AGREGAR RECETA
    $("#agregar_receta").click(function (){

      if ($("#agregarDiv").is(':hidden')){
        $('#full-container').hide();
        $('footer').hide();
        $('.perfil').hide();

        $('#paginador').hide();
        $("#agregarDiv").slideToggle();
      }else {
        $('#full-container').show();
        $('.perfil').show();

        $('#paginador').show();
        $('footer').show();
        $("#agregarDiv").slideToggle('slow');

      }
    });




  // PRESS CANCELAR EN EL FORM AGREGAR RECETA
  $(document).on('click','#no_agregar',function(){
    $("#agregarDiv").slideToggle();
    $('.perfil').show();
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
        alert('error on receta');
        console.log('error on receta');
      }
    }).done( function(data){
      console.log(' receta CORRECTAMENTE');
      var content = $( data ).find( "#recepy-grid" );


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

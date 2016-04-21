$(document).ready(function(){
// Function used for postbanner model to change source and link when post banner
if (window.location.pathname == '/admin/banner/postbanner/add/'){
    $('.field-banner').hide();
    $('.field-source').hide();
    $('.field-link').hide();
}
$('#id_bannerplan').change(function(){
    var selected_option = $( "#id_bannerplan option:selected" ).text();
    if (selected_option.toLowerCase().indexOf("other") >=0){
        $('.field-banner').hide();
        $('.field-link').hide();
        $('.field-source').show();
    }
    else{
        $('.field-source').hide();
        $('.field-banner').show();
        $('.field-link').show();
    }
});
var regex = '[0-9]+$/';
if(new RegExp("[0-9]").test(window.location.pathname)) {
    if($('#id_source').val() == '')
        $('.field-source').hide();
    if($('#id_link').val() == '')
        $('.field-link').hide();
    if($('.field-banner ').find('.file-upload').length ==0)
        $('.field-banner').hide(); 
    if($( "#id_bannertype option:selected" ).text().toLowerCase().indexOf("other") >=0 ) {
        $('.field-height').hide();
        $('.field-width').hide();
    }
}     
// Function used for bannerplan model to show height and widht for own and other banners 
if (window.location.pathname == '/admin/banner/bannerplan/add/'){
    $('.field-height').hide();
    $('.field-width').hide();
}
$('#id_bannertype').change(function(){
    var selected_option = $( "#id_bannertype option:selected" ).text();
    if (selected_option.toLowerCase().indexOf("own") >=0){
        $('.field-height').show();
        $('.field-width').show();
    }
    else{
        $('.field-height').hide();
        $('.field-width').hide();
    }
});
$("#id_banner").change(function(e) {
    var _URL = window.URL || window.webkitURL;
    var file, img;
    if ((file = this.files[0])) {
        img = new Image();
        img.onload = function() {
            height = this.height;
            width = this.width;
            var selected_option = $( "#id_bannerplan option:selected" ).val();
            $.ajax({ 
              type: "POST",
              url: '/get_banner_height_width/',
              data: "selected_option="+selected_option,
              success: function(response) {
                banner_height = JSON.stringify(response.banner_height);
                banner_width = JSON.stringify(response.banner_width);
                if ( height>banner_height || width>banner_width) {
                    $("#id_banner").next('.help-inline').text('Please upload the banner Image with '+ banner_height +' height *'+ banner_width +' width').css({'color':'red'});
                    $("#id_banner").val('');
                }  
                else{
                    $("#id_banner").next('.help-inline').text('');
                }             
              },
            });  
        };
        img.src = _URL.createObjectURL(file);
    }
});
});


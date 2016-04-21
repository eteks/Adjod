
$('.search_btn').click(function() {
    validateSearch();
});

$(function() {
// alert("document ready");
    $("#typeandbrandtxt").autocomplete({
        source : "/autocomplete_brandlist",
        select : function(event, ui) {
            $("#typeandbrand").val(ui.item.value);
        },

        close : function(event, ui) {
            valKey = $("#typeandbrandtxt").val();
            $("#typeandbrand").val(valKey);
            if ($("#typeandbrandtxt").val().length > 15) {
                valKey = jQuery.trim(valKey).substring(0, 15).trim(this) + "...";
            } else {
                valKey = $("#typeandbrandtxt").val();
            }
            $("#typeandbrandtxt").val(valKey);
        }
    });

    $("#q").autocomplete({
        source: "/autocomplete_product_search",
        minLength: 2,
    });
});

function perform_search(){
            var q = $('#form_search_filter').serialize();
            var pageurl = window.location.href;
            var qsort = $("#sorteddata").val();
            q = q +'&sorteddata='+$.trim(qsort);
            if ($('[name=newsearch]').val() == "new")
            {
                    $.get('v2/search/?'+ q, function(data){
                        show_searching(false);
                        $('#search_result').html(data);
                        attach_pagination_events();
                        });
                        $('.product_images1 img').each(function( index ) {
                                    alert("before call");
                                    $(this).center1();
                        });
            }else{
                    $.get('/search/?'+ q, function(data){
                    $('#search_result').html(data);
                    attach_pagination_events();
                });
            }
            $(document).ajaxComplete(function(){
               $('.product_images1 img').each(function () {
                    $(this).center();
                });
            });
}

function attach_pagination_events(){
            $('[data-ajaxlink=true]').click(function(ele){
            $("html, body").animate({ scrollTop: 0 }, "slow");
                        $('[name=page]').val($(ele.currentTarget).attr('data-ajaxpage'));
            perform_search();
            return false;
            });
}
$(document).ready(function() {

            $('.product_images1 img').each(function () {
                $(this).center();
            });
            // $('.brand_folder').hide();
            // $("li.brand_folder > ul").hide();
            attach_pagination_events();

            var url = window.location.href;
            // var pageURL = $(location).attr("href");
            url1=url.split('/')[3];
            url2=url.split('/')[4];

            // Toggle for Categories and SubCategories in Advance Menu
            $('.list_folder').on('click',function(e){
                e.stopImmediatePropagation();
                $(this).find('.hide_list:first').slideToggle();
                $(this).siblings('.list_folder').find('.hide_list').hide();
            });
            $('.categoryselected').on('click',function(e){
                $('[name=subcategoryid]').val('');
                $('#sorteddata').val('');
                $('[name=category]').val($(this).attr('data-target'));
                perform_search();
            });
           $('.brand_name').on('click',function(e){
                e.stopImmediatePropagation();
                $('.list').slideToggle();

                //perform_search();
            });
            $('.get').on('click',function(e){
                var text = $(this).text();
                $('.all').hide();
                $('.list_display').html(text + " <i class='fa fa-angle-right right'></i>");
                $('.list_display').attr('data-target',$(this).attr('data-target'));

            });
             $('.get1').on('click',function(e){
                var text = $(this).text();
                $('.all').hide();
                $('.list_display_subcat').html(text + " <i class='fa fa-angle-right right'></i>");
                $('.list_display_subcat').attr('data-target',$(this).next('.ajax_subid').text());
                $('.list_display_subcat').show();

            });
             $('.list_display').click(function(){
                $('.list_display_subcat').hide();
                    $('input[type="hidden"]#category').val($(this).attr('data-target'));
                     $('input[type="hidden"]#subcategoryid').val('');
                     perform_search();
             });
             $('.categoryselected').click(function(){
                $('.brand_folder').hide();
             });

    //subcategory list choose
    $('.subclick > li .subcategory_choose').click(function () {

        $('.subclick > li .subcategory_choose').each(function( index ) {
            $(this).removeClass('orange_text');
        });

        $(this).addClass('orange_text');

        var subid =  $(this).next('.ajax_subid').text();
        // alert(subid);
        var trim_subid = $.trim(subid);
        var ajax_subid = $('input[type="hidden"]#subcategoryid').val(trim_subid);
        $('input[type="hidden"]#locality').val('');
        $('[name=subcategoryid]').text(trim_subid);
        $('[name=brandtype]').val('');
        $('#sorteddata').val('');
         var trim_subid = $.trim(subid);
         // alert($.trim(subid));
            fill_brands(trim_subid);
        $.trim($.cookie('subcatcookie',JSON.stringify(trim_subid)));
        perform_search();
    });
    //all category
    $('.all_category').click(function(){

        $.get('/search/?q=', function(data){
            $('#search_result').html(data);
            //attach_pagination_events();
        });
    });
    //brand type
    $(document).on("change", 'input.brandtype', function () {
    var checkboxes =  $('input.brandtype');
    // If one item is checked.. Uncheck all and
    // check current item..
    if($(this).is(':checked')){
        checkboxes.attr('checked', false);
        $(this).attr('checked', 'checked');
        //var check = $(this).parent().parent().next('#brandsubcategoryid').val($(this).val());
        // alert("check"+JSON.stringify(check));
        perform_search();
    }
    });
    // $(document).on("change", 'input.brandtype', function () {
    //
    //     if ($(this).prop('checked') == true){
    //         // alert($(this).val());
    //         // alert("true");
    //         var check = $(this).parent().parent().next('#brandsubcategoryid').val($(this).val());
    //         // alert("check"+JSON.stringify(check));
    //         perform_search();
    //     }
    //     else{
    //         // alert("false");
    //         $('#brandsubcategoryid').val('');
    //         perform_search();
    //     }
    // });

	// city based search
	 $(document).on("change", '.locality', function () {
	    // $( ".city" ).change(function () {
		var selected_option = $( ".locality option:selected" ).val();
		$('p#localityselected').html($( ".locality option:selected" ).text());
		var locality = $('input[type="hidden"]#locality').val($(this).val());
        $('input[name="page"]').val('');
        $('[name=brandtype]').val('');
        $('#sorteddata').val('');
        $('input[type="hidden"]#subcategoryid,input[type="hidden"]#category').val('');
		perform_search();
	});


    //sort by dropdown
    $(".prov_custom_sort_value_act").on('change', function(){
        var selected_option = $( ".prov_custom_sort_value_act option:selected" ).text();
        $('#prov_custom_sort_value_act').html(selected_option);
        $('input[type="hidden"]#sorteddata').val($(this).val());
        perform_search();
    });

//price range selection
    $('input.pricerange').on('change', function(){
            $('input.pricerange').not(this).prop('checked', false);  
            if ($(this).prop('checked') == true){
                    var splitprice = [];
                    var splitprice = $(this).val().split("#");
                    // alert(splitprice);
                    $('#price_start').val(splitprice[0]);
                    $('#price_end').val(splitprice[1]);
                    perform_search();
            }

          if ($(this).prop('checked') == false){
                $('[name=price_start]').val('');
                $('[name=price_end]').val('');
                $.cookie("subcatcookie")
                // alert($.cookie("subcatcookie"));
                perform_search();
            }

    });

function show_searching(show) {

    if(show){

        $('.loding_icon').show();
        $('.founded_no').hide();

    }else{

        $('.loding_icon').hide();
        $('.founded_no').show();

    }

}

function validateSearch() {
   left_dyanmic_height();
   // code by Karthikesh on 30/10/2013, for search ajax issue
   var is_search_page = window.location.href.indexOf('/search');
   if(is_search_page > 1)
   {

   		$('[name=q]').val($('#q').val());
		perform_search();
   }
   else
   {

       	if($('#q').val() == ''){

	         $('#q').val('');
    	}
    	$("#f_search").submit();
   }
    //return true;
}


});

function sign_in_center_align() {
    var height = $('.sign_in_div').height();
    var width = $('.sign_in_div').width();
    $('.sign_in_div').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function sign_up_center_align() {
    var height = $('.sign_up_div').height();
    var width = $('.sign_up_div').width();
    $('.sign_up_div').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function category_popup_center_align() {
    var height = $('.choose_category_div,.choose_category_div_mobile').height();
    var width = $('.choose_category_div,.choose_category_div_mobile').width();
    $('.choose_category_div,.choose_category_div_mobile').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function forgot_center_align() {
    var height = $('.forgot_div').height();
    var width = $('.forgot_div').width();
    $('.forgot_div').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function reset_div_center_align() {
    var height = $('.reset_div').height();
    var width = $('.reset_div').width();
    $('.reset_div').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function subscribe_center_align() {
    var height = $('.subscription_popup').height();
    var width = $('.subscription_popup').width();
    $('.subscription_popup').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function urgent_ad_center_align() {
    var height = $('.urgentad_popup').height();
    var width = $('.urgentad_popup').width();
    $('.urgentad_popup').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function premium_ad_center_align() {
    var height = $('.premium_ad_popup').height();
    var width = $('.premium_ad_popup').width();
    $('.premium_ad_popup').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function premium_urgent_ad_center_align() {
    var height = $('.premium_urgent_ad_popup').height();
    var width = $('.premium_urgent_ad_popup').width();
    $('.premium_urgent_ad_popup').css({
        'margin-top': -height / 2 + "px",
        'margin-left': -width / 2 + "px"
    });
}

function checkStrength(password) {
    var strength = 0
    if (password.length < 6) {
        $('#result').removeClass()
        $('#result').addClass('short')
        return 'Too short'
    }
    if (password.length > 7) strength += 1
    if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) strength += 1
    if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) strength += 1
    if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,",%,&,@,#,$,^,*,?,_,~])/)) strength += 1
    if (strength < 2) {
        $('#result').removeClass()
        $('#result').addClass('weak')
        return 'Weak'
    } else if (strength == 2) {
        $('#result').removeClass()
        $('#result').addClass('good')
        return 'Good'
    } else {
        $('#result').removeClass()
        $('#result').addClass('strong')
        return 'Strong'
    }
}

function isValidEmailAddress(emailAddress) {
    var pattern = new RegExp(/^[+a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/i);
    return pattern.test(emailAddress);
};

function updateCountdownTitle() {
    var remaining = 70 - $('.ad_title').val().length;
    $('#ad_title_count').text(remaining);
}

function updateCountdownDesc() {
    var remaining = 500 - $('#your_description').val().length;
    $('#desc_count').text(remaining);
}
var response_cache = {};
var response_cache1 = {};
var response_cache2 = {};
var response_cache3 = {};
var response_cache4 = {};

function find_subcategory(category_id) {
    if (response_cache[category_id]) {
        $(".subcategory_list").html(response_cache[category_id]);
    } else {
        $.getJSON("/subcategory_for_category/", {
            category_id: category_id
        }, function(ret, textStatus) {
            var options = '';
            for (var i in ret) {
                options += '<li><input type="hidden" name="subcategory" value="' + ret[i].id + '">' + ret[i].name + '</li>';
            }
            response_cache[category_id] = options;
            $(".subcategory_list").html(options);
        });
    }
}

function find_brand(sub_category_id) {
    if (response_cache1[sub_category_id]) {
        $(".brand_list").html(response_cache1[sub_category_id]);
    } else {
        $.getJSON("/brand_for_subcategory/", {
            sub_category_id: sub_category_id
        }, function(ret, textStatus) {
            if (ret.length == 0) {
                $(".brand_list").html("no brand for this sub category");
                $('.popup_fade').hide();
                $('.close_btn').hide();
                $('.choose_category_div').hide();
                $('.choose_category_div_mobile').hide();
                document.body.style.overflow = 'auto';
                $('#category_name').val(category_id);
                $('#subcategory_name').val(sub_category_id);
                $('#category').val(category + " » " + sub_category);
                $('.choose_button').text('Change');
            } else {
                var options = '';
                for (var i in ret) {
                    options += '<li><input type="hidden" name="brand" value="' + ret[i].id + '">' + ret[i].name + '</li>';
                }
                response_cache1[sub_category_id] = options;
                $(".brand_list").html(options);
            }
        });
    }
}

function fill_localities(city_id) {
    if (response_cache2[city_id]) {
        $("#id_locality").html(response_cache2[city_id]);
    } else {
        $.getJSON("/localities_for_city/", {
            city_id: city_id
        }, function(ret, textStatus) {
            var options = '';
            $('#select_post_locality').text("Select Locality");
            options += '<option>Select Locality</option>';
            for (var i in ret) {
                options += '<option value="' + ret[i].id + '">' + ret[i].name + '</option>';
            }
            response_cache2[city_id] = options;
            $("#id_locality").html(options);
        });
    }
    response_cache2 = {}
}

function fill_subcategories(category_id) {
    if (response_cache3[category_id]) {
        $("#id_subcategory").html(response_cache3[category_id]);
    } else {
        $.getJSON("/subcategory_for_category/", {
            category_id: category_id
        }, function(ret, textStatus) {
            var options = '';
            options += '<option>Select Subcategory</option>';
            for (var i in ret) {
                options += '<option value="' + ret[i].id + '">' + ret[i].name + '</option>';
            }
            response_cache3[category_id] = options;
            $("#id_subcategory").html(options);
        });
    }
    response_cache3 = {}
}

function fill_brands(sub_category_id) {
    if (response_cache4[sub_category_id]) {
        $("#id_brand").html(response_cache4[sub_category_id]);
    } else {
        $.getJSON("/brand_for_subcategory/", {
            sub_category_id: sub_category_id
        }, function(ret, textStatus) {
            if (ret.length == 0) {
                $('.select_post_brand').hide();
                $('.select_container_brand').css({
                    "opacity": 0.5
                });
                $('.brand_folder').hide();
            } else {
                $('.select_post_brand').show();
                $('.select_container_brand').css({
                    "opacity": 1
                });
                $('.brand_folder').show();
            }
            var options = '';
            if (window.location.href.indexOf("search") >= 0) {
                for (var i in ret) {
                    options += '<li class="list"><input type="checkbox" class="css-checkbox sme brandtype"  name ="brandtype" value ="' + ret[i].id + '"><label for="checkbox1" name="checkbox1_lbl" class="css-label sme depressed">' + ret[i].name + '</label></li>';
                }
                $(".hiddenclass").html(options);
            } else {
                options += '<option>Select Brand</option>';
                for (var i in ret) {
                    options += '<option value="' + ret[i].id + '">' + ret[i].name + '</option>';
                }
                response_cache4[sub_category_id] = options;
                $("#id_brand").html(options);
            }
        });
    }
    response_cache4 = {}
}

function passwordChanged() {
    $('#strength').show();
    var strength = document.getElementById("strength");
    var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\W).*$", "g");
    var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
    var enoughRegex = new RegExp("(?=.{6,}).*", "g");
    var pwd = document.getElementById("pswd1");
    if (false == enoughRegex.test(pwd.value)) {
        strength.innerHTML = "More Character";
    } else if (strongRegex.test(pwd.value)) {
        strength.innerHTML = '<span style="color:green">Strong!</span>';
    } else if (mediumRegex.test(pwd.value)) {
        strength.innerHTML = '<span style="color:orange">Medium!</span>';
    } else {
        strength.innerHTML = '<span style="color:red">Weak!</span>';
    }
}
$(document).ready(function() {
    $.fn.center = function() {
        var height = $(this).height();
        var width = $(this).width();
        $(this).css({
            'margin-top': -height / 2 + "px",
            'margin-left': -width / 2 + "px"
        });
        $(this).css({
            'display': 'block'
        });
        return this;
    }
    sign_in_center_align();
    sign_up_center_align();
    reset_div_center_align();
    subscribe_center_align();
    urgent_ad_center_align();
    premium_ad_center_align();
    premium_urgent_ad_center_align();
    $(".urgent_ad").click(function() {
        urgent_ad_center_align();
        $('.popup_fade').show();
        $('.urgentad_popup ,.popup_close').show();
        document.body.style.overflow = 'hidden';
    });
    $(".premium_ad").click(function() {
        premium_ad_center_align();
        $('.popup_fade').show();
        $('.premium_ad_popup ,.popup_close1').show();
        document.body.style.overflow = 'hidden';
    });
    $(".premium_urgent_ad").click(function() {
        premium_urgent_ad_center_align();
        $('.popup_fade').show();
        $('.premium_urgent_ad_popup ,.popup_close2').show();
        document.body.style.overflow = 'hidden';
    });
    $(".link_tooltip").click(function() {
        subscribe_center_align();
        $('.popup_fade').show();
        $('.subscription_popup ,.close_btn').show();
        document.body.style.overflow = 'hidden';
    });
    var $upperimg = $('.upperimg img');
    $('.thumbs img').click(function() {
        $upperimg.attr('src', this.src);
    });
    $('.product_image img').load(function() {
        $(this).center();
    });
    $('.upperimg img').load(function() {
        $(this).center();
        $('.upperimg img:not(:first)').hide();
    });
    $('.upperimg_mob img').load(function() {
        $(this).center();
    });
    $('.thumbs img').load(function() {
        $(this).center();
    });
    $('.product_images1 img').load(function() {
        $(this).center();
    });
    $(".share_button").click(function() {
        $(".desktop_share").toggle();
    });
    $(".profile_text").hide();
    $(".My_ads").click(function() {
        $(".update_ads").show();
        $(".profile_text").hide();
    });
    $(".My_profile").click(function() {
        $(".profile_text").show();
        $(".update_ads").hide();
    });
    $(".menu_active").click(function() {
        $('.menu_active').removeClass('active');
        $(this).addClass('active');
    });
    $('input[type="checkbox"].check_individual_act').change(function() {
        if ($(this).prop('checked') == true) {
            $(this).parents('ul').find('.inactive_edit_delete_action').hide();
            $(this).parents('ul').find('.active_edit_delete_action').show();
        } else {
            $(this).parents('ul').find('.inactive_edit_delete_action').show();
            $(this).parents('ul').find('.active_edit_delete_action').hide();
        }
    });
    if ($('input[type="checkbox"].check_individual_act').prop('checked') == true) {
        $('.delete_act').prop('disabled', false);
    }
    if ($('input[type="checkbox"].check_individual_act').prop('checked') == false) {
        $('.delete_act').prop('disabled', true);
    }
    $('.delete_act').prop('disabled', true);
    $('.check_all_act').on('click', function() {
        $('.check').prop('checked', true);
        $('.delete_act').prop('disabled', false);
        $('.view_action, .edit_action, .delete_action').hide();
    });
    $('a.edit_action').contents().unwrap();
    $('.view_action,.edit_action,.delete_action').show();
    $('.uncheck_all_act').on('click', function() {
        $('.check').prop('checked', false);
        $('.delete_act').prop('disabled', true);
        $('.view_action,.edit_action,.delete_action').show();
    });

    function getSelectedVals() {
        var tmp = [];
        $("input[name='title_box'].check_individual_act").each(function() {
            if ($(this).attr('checked')) {
                checked = ($(this).val());
                tmp.push(checked);
            }
        });
        var filters = tmp.join(',');
        return filters;
    }
    $('.delete_act, .delete_action').on('click', function() {
        selected = getSelectedVals();
        var myurl = "/delete_ad/"
        $.ajax({
            type: "POST",
            url: myurl,
            data: "selected=" + selected,
            success: function(response) {
                window.location.reload(true);
            },
        });
        return false;
    });
    $(".profile_locality").change(function() {
        var selected_option = $(".profile_locality option:selected").text();
        $('#profile_locality').html(selected_option);
    });
    $(".profile_gender").change(function() {
        var selected_option = $(".profile_gender option:selected").text();
        $('#profile_gender').html(selected_option);
    });
    $('.profile_poster_update').change(function() {
        $(this).siblings('.upload_image_change,.editpost_image_change,.nav_post_image_change').remove();
        $(this).siblings('#clean_img').remove();
        $(this).parents('.simpleFilePreview').siblings('.upload_image_change').remove();
        $(this).parents('.simpleFilePreview').siblings('#clean_img').remove();
    });
    $('.popup_sign_up, .footer_signup').click(function() {
        sign_up_center_align();
        $('.popup_fade').show();
        $('.sign_up_div, .close_btn').show();
        $('.sign_in_div').hide();
        document.body.style.overflow = 'hidden';
    });
    $('.popup_sign_in, .footer_login').click(function() {
        sign_in_center_align();
        $('.popup_fade').show();
        $('.sign_in_div, .close_btn').show();
        $('.sign_up_div').hide();
        document.body.style.overflow = 'hidden';
    });
    $('.na_post_button').click(function() {
        $('.next_path').val('/postad/');
        sign_in_center_align();
        $('.popup_fade').show();
        $('.sign_in_div, .close_btn').show();
        $('.sign_up_div').hide();
        document.body.style.overflow = 'hidden';
    });
    $('.choose_button').click(function() {
        category_popup_center_align();
        $('.popup_fade').show();
        $('.choose_category_div, .choose_category_div_mobile, .close_btn').show();
        document.body.style.overflow = 'hidden';
    });
    $('.cancel_btn').click(function() {
        $('.popup_fade').hide();
        $('.sign_up_div,.sign_in_div,.forgot_div,.reset_div, .close_btn, .popup_close,.popup_close1,.popup_close2,.choose_category_div,.choose_category_div_mobile,.subscription_popup,.urgentad_popup,.premium_ad_popup,.premium_urgent_ad_popup').hide();
        document.body.style.overflow = 'auto';
        $('.labelError,.signup_labelError').hide();
        $('.confirm').prop('checked', false);
    });
    $('.forgot_act').click(function() {
        forgot_center_align();
        $('.popup_fade').show();
        $('.sign_in_div').hide();
        $('.forgot_div, .close_btn').show();
        document.body.style.overflow = 'hidden';
    });
    $('.free_button').click(function() {
        $('.forgot_div').hide();
        $('.sign_up_div, .close_btn').show();
        document.body.style.overflow = 'hidden';
    });
    $('#password').keyup(function() {
        if ($('#password').val() != '') $('#result').html(checkStrength($('#password').val()));
        else
            $('#result').html('');
    });
    $('input[type=text], textarea').focus(function() {
        if (this.value == this.defaultValue) {
            this.value = "";
        }
    }).blur(function() {
        if (!this.value.length) {
            this.value = this.defaultValue;
        }
    });
    $('.banner_rotation').each(function() {
        $(this).find('ul li:first').addClass('banneractive');
    });
    setInterval(function() {
        $('.banner_rotation').each(function() {
            var active = $(this).find('ul li.banneractive');
            var next = active.next();
            if (next.length === 0) {
                next = $(this).find('ul li:first');
            }
            active.removeClass('banneractive');
            next.addClass('banneractive');
        });
    }, 5000);
    var telInput = $("#your_mobile_no"),
        errorMsg = $("#error-msg"),
        validMsg = $("#valid-msg");
    telInput.intlTelInput({
        preferredCountries: ["sg", "gb"],
        utilsScript: "../../static/lib/libphonenumber/build/utils.js"
    });
    var reset = function() {
        telInput.removeClass("error");
        errorMsg.addClass("hide");
        validMsg.addClass("hide");
    };
    $("#post").click(function() {
        reset();
        if ($.trim($("#your_mobile_no").val())) {
            if ($("#your_mobile_no").val().length >= 8) {
                validMsg.removeClass("hide");
                $("#mobile_number_sign_up_home").removeClass("error");
            } else {
                errorMsg.removeClass("hide");
                $("#your_mobile_no").addClass("error");
            }
        }
    });
    telInput.on("keyup change", reset);
    var telInput = $("#mobilenumber"),
        errorMsg = $("#error-msg"),
        validMsg = $("#valid-msg");
    telInput.intlTelInput({
        preferredCountries: ["sg", "gb"],
        utilsScript: "../../static/lib/libphonenumber/build/utils.js"
    });
    var reset = function() {
        telInput.removeClass("error");
        errorMsg.addClass("hide");
        validMsg.addClass("hide");
    };
    $("#alert_button").click(function() {
        reset();
        if ($.trim($("#mobilenumber").val())) {
            if ($("#mobilenumber").intlTelInput("isValidNumber")) {
                validMsg.removeClass("hide");
                $("#mobilenumber").removeClass("error");
            } else {
                $("#mobilenumber").addClass("error");
                errorMsg.removeClass("hide");
            }
        }
    });
    telInput.on("keyup change", reset);
    var telInput = $("#mobile_number_sign_up_home"),
        errorMsg = $("#error-msg"),
        validMsg = $("#valid-msg");
    telInput.intlTelInput({
        preferredCountries: ["sg", "gb"],
        utilsScript: "../../static/lib/libphonenumber/build/utils.js"
    });
    var reset = function() {
        telInput.removeClass("error");
        errorMsg.addClass("hide");
        validMsg.addClass("hide");
    };
    $('#mobile_number_sign_up_home,#your_mobile_no').keypress(function(evt) {
        var theEvent = evt || window.event;
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
        var regex = /^[0-9\b]+$/;
        if (!regex.test(key)) {
            theEvent.returnValue = false;
            if (theEvent.preventDefault) theEvent.preventDefault();
        }
    });
    $("#create").click(function() {
        reset();
        if ($.trim($("#mobile_number_sign_up_home").val())) {
            if ($("#mobile_number_sign_up_home").val().length >= 8) {
                errorMsg.removeClass("hide");
                $("#mobile_number_sign_up_home").removeClass("error");
            } else {
                validMsg.removeClass("hide");
                $("#mobile_number_sign_up_home").addClass("error");
            }
        }
    });
    telInput.on("keyup change", reset);
    $('input[type=file]').simpleFilePreview({
        'buttonContent': '<i class="fa fa-plus-circle fa_small"></i>',
        'shiftLeft': '',
        'shiftRight': '',
        'removeContent': 'Remove'
    });
    $('.ad_type_choice').change(function() {
        var option = $(this).val();
        if (option == "sell") {
            $('.seller_info_div').show();
            $('.buyer_info_div').hide();
        } else {
            $('.buyer_info_div').show();
            $('.seller_info_div').hide();
        }
    });
    $("#alert_button").click(function() {
        if ($('#email').val() == "") $('#email').parent().next('.email_labelError').show();
        else {
            if (!/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test($('#email').val())) {
                $('#email').parent().next('.email_labelError').text("Please enter valid email address");
                $('.email_labelError').show();
            } else {
                $('#email').parent().next('.email_labelError').hide();
            }
        }
        if ($('#select_post_category').text() == "Select Category") $('.select_post_category').parent().next('.labelError').show();
        else
            $('.select_post_category').parent().next('.labelError').hide();
        if ($('#select_post_subcategory').text() == "Select SubCategory") $('.select_post_subcategory').parent().next('.labelError').show();
        else
            $('.select_post_subcategory').parent().next('.labelError').hide();
        if ($('#select_post_locality').text() == "Select Locality") $('.select_post_locality').parent().next('.labelError').show();
        else
            $('.select_post_locality').parent().next('.labelError').hide();
        if ($('.labelError,.email_labelError,.error').is(":visible")) return false;
        else {
            return true;
            $('form[name="alert_button"]').submit();
        }
    });
    sign_up_required = ["email_id", "password", "user_id", "mobile_number_sign_up_home"];
    jQuery('#create').click(function() {
        if ($('.confirm').prop('checked') == true) {
            for (i = 0; i < sign_up_required.length; i++) {
                var input = jQuery('#' + sign_up_required[i]);
                if (input.val() == "") {
                    input.addClass("error_input_field");
                    input.siblings('.error_message').hide();
                    input.siblings('.signup_labelError').show();
                    input.parents('#mobile_number_div').children('.signup_labelError').show();
                } else {
                    input.removeClass("error_input_field");
                    input.siblings('.signup_labelError').hide();
                    input.parents('#mobile_number_div').children('.signup_labelError').hide();
                }
            }
            if ($('#email_id').val() != '') {
                if (!/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test($('#email_id').val())) {
                    $('#email_id').addClass("error_input_field");
                    $('#email_id').siblings('.signup_labelError').hide();
                    $('#email_id').siblings('.error_message').show();
                } else {
                    $('#email_id').removeClass("error_input_field");
                    $('#email_id').siblings('.error_message').hide();
                }
            }
            if ($(":input").hasClass("error_input_field") || $('#mobile_number_sign_up_home').hasClass("error")) {
                return false;
            } else {
                return true;
                $('form[name="sign_in"]').submit();
            }
        } else
            return false;
    });
    required = ["category", "ad_title", "your_price", "your_description", "your_email"];
    jQuery("#post").click(function() {
        return_response = false;
        $.get("/check_authenticate/", function(data, status) {
            if (data == "yes") {
                var regYoutube = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})/i;
                for (i = 0; i < required.length; i++) {
                    var input = jQuery('#' + required[i]);
                    if (input.val() == "") {
                        input.addClass("error_input_field");
                        input.siblings('.labelError').show();
                    } else {
                        input.removeClass("error_input_field");
                        input.siblings('.labelError').hide();
                    }
                }
                if ($('#buy').attr('checked') || $('#sell').attr('checked')) {
                    $('#buy,#sell').removeClass("error_input_field");
                    $('#buy,#sell').siblings('.labelError').hide();
                } else {
                    $('#buy,#sell').addClass("error_input_field");
                    $('#buy,#sell').siblings('.labelError').show();
                }
                if ($('#individual').attr('checked') || $('#dealer').attr('checked')) {
                    $('#individual,#dealer').removeClass("error_input_field");
                    $('#individual,#dealer').siblings('.labelError').hide();
                } else {
                    $('#individual,#dealer').addClass("error_input_field");
                    $('#individual,#dealer').siblings('.labelError').show();
                }
                if (($('#select_post_city').text() == "Select city *") || ($('#select_post_city').text() == "Select City")) {
                    $('.select_container_city').addClass("error_input_field");
                    $('.select_container_city').find('.labelError').show();
                } else {
                    $('.select_container_city').removeClass("error_input_field");
                    $('.select_container_city').find('.labelError').hide();
                }
                if (($('#select_post_locality').text() == "Select locality *") || ($('#select_post_locality').text() == "Select Locality")) {
                    $('.select_container_locality').addClass("error_input_field");
                    $('.select_container_locality').find('.labelError').show();
                } else {
                    $('.select_container_locality').removeClass("error_input_field");
                    $('.select_container_locality').find('.labelError').hide();
                }
                if ($('#your_email').val() != '') {
                    if (!/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test($('#your_email').val())) {
                        $('#your_email').addClass("error_input_field");
                        $('#your_email').siblings('.labelError').text("Please enter valid email address");
                        $('.labelError').show();
                    } else {
                        $('#your_email').removeClass("error_input_field");
                        $('#your_email').siblings('.labelError').hide();
                    }
                }
                if ($('#terms_of_use').attr('checked')) {
                    $('#terms_of_use').removeClass("error_input_field");
                    $('#terms_of_use').next().siblings('.labelError').hide();
                } else {
                    $('#terms_of_use').addClass("error_input_field");
                    $('#terms_of_use').next().siblings('.labelError').show();
                }
                video_url = $('#videos1').val();
                if (regYoutube.test(video_url)) {
                    $('#videos1').removeClass("error_input_field");
                    $('#videos1').siblings('.labelError').hide();
                } else if (video_url != '') {
                    $('#videos1').addClass("error_input_field");
                    $('#videos1').siblings('.labelError').show();
                }
                if ($(":input").hasClass("error_input_field") || $(".select_container_city").hasClass("error_input_field") || $(".select_container_locality").hasClass("error_input_field") || $("#buy,#sell").hasClass("error_input_field") || $("#individual,#dealer,.photo_labelError").hasClass("error_input_field") || $('#your_mobile_no').hasClass("error") || $("#videos1").hasClass("error_input_field")) {
                    return_response = false;
                } else {
                    return_response = true;
                    $('form[name="post_ad"]').submit();
                }
            } else {
                sign_up_center_align();
                $('.popup_fade').show();
                $('.sign_in_div, .close_btn').show();
                $('.sign_up_div').hide();
                document.body.style.overflow = 'hidden';
            }
        });
        return return_response;
    });
    $('input[name=premium_plan]').click(function() {
        var premium_id = this.id;
        if (premium_id == "premium_plan1") $('input[name=amount]').val("9.99");
        else if (premium_id == "premium_plan2") $('input[name=amount]').val("14.99");
        else if (premium_id == "premium_plan3") $('input[name=amount]').val("19.99");
        $('form[name="payment_form"]').submit();
    });
    $(".select_payment").change(function() {
        var selected_option = $(".select_payment option:selected").val();
        $('#payment_method').html(selected_option);
    });
    $(".custom_select_value_act").change(function() {
        var selected_option = $(".custom_select_value_act option:selected").text();
        $('#custom_select_value_act').html(selected_option);
    });
    $(".select_post_city").change(function() {
        var selected_option = $(".select_post_city option:selected").text();
        $('#select_post_city').html(selected_option);
        fill_localities($(this).val());
    });
    $(".select_post_locality").change(function() {
        var selected_option = $(".select_post_locality option:selected").text();
        $('#select_post_locality').html(selected_option);
    });
    $(".select_post_category").change(function() {
        var selected_option = $(".select_post_category option:selected").text();
        $('#select_post_category').html(selected_option);
        fill_subcategories($(this).val());
    });
    $(".select_post_subcategory").change(function() {
        var selected_option = $(".select_post_subcategory option:selected").text();
        $('#select_post_subcategory').html(selected_option);
        fill_brands($(this).val());
    });
    $(".select_post_brand").change(function() {
        var selected_option = $(".select_post_brand option:selected").text();
        $('#select_post_brand').html(selected_option);
    });
    $('.category_list > li').click(function() {
        $(".category_list > li").each(function(index) {
            $(this).removeClass('orange_text');
        });
        $(this).addClass('orange_text');
        category = $(this).text();
        category_id = $('input[type="hidden"]', this).val();
        find_subcategory(category_id);
        $('.brand_list').hide();
    });
    $(".subcategory_list").on("click", ">li", function() {
        $(".subcategory_list > li").each(function(index) {
            $(this).removeClass('orange_text');
        });
        sub_category = $(this).text();
        sub_category_id = $('input[type="hidden"]', this).val();
        $('#brand').html(sub_category);
        find_brand(sub_category_id);
        $('.brand_list').show();
        $('#brand').show();
    });
    $('.brand_list').on("click", ">li", function() {
        $(".brand_list > li").each(function(index) {
            $(this).removeClass('orange_text');
        });
        $(this).addClass('orange_text');
        brand = $(this).text();
        brand_id = $('input[type="hidden"]', this).val();
        $('.popup_fade').hide();
        $('.close_btn').hide();
        $('.choose_category_div').hide();
        document.body.style.overflow = 'auto';
        $('#category_name').val(category_id);
        $('#subcategory_name').val(sub_category_id);
        $('#brand_name').val(brand_id);
        $('#category').val(category + " » " + sub_category + " » " + brand);
        $('.choose_button').text('change');
    });
    $('.signup_tooltip').hide();
    $('.signup_confirm_button').mouseover(function() {
        if ($(".confirm").prop('checked') == false) {
            $('.signup_tooltip').show();
        } else {
            $('.signup_tooltip').hide();
        }
    });
    $('.signup_confirm_button').mouseout(function() {
        $('.signup_tooltip').hide();
    });
    $(".user_dropdown").hide();
    $(".caret_user").click(function(event) {
        event.stopPropagation();
        $('.user_dropdown').toggle();
    });
    $(document).click(function() {
        $('.user_dropdown').hide();
    });
    $('.subscribe_content code').click(function() {
        transaction_type = $('form[name="paypal_account_subscription"]').find("input[name='item_name']").val();
        $('form[name="paypal_account_subscription"]').submit();
    });
    $('input.checkbox_premium').on('change', function() {
        $('input.checkbox_premium').not(this).prop('checked', false);
        if ($(this).is(':checked')) $('.premium_plan').val($(this).val());
        else
            $('.premium_plan').val('');
    });
    $('.your_price').keypress(function(e) {
        var theEvent = e || window.event;
        var key = theEvent.keyCode || theEvent.which;
        key = String.fromCharCode(key);
        if (key.length == 0) return;
        var regex = /^[0-9.\b]+$/;
        if (!regex.test(key)) {
            theEvent.returnValue = false;
            if (theEvent.preventDefault) theEvent.preventDefault();
        }
    });
    $("#password2").keyup(function() {
        var password = $(".pwd_profile").val();
        $("#pswd_label_error1").html(password == $(this).val() ? "Passwords match." : "Passwords do not match!");
        if (password == $(this).val()) {
            $('.delete_btn').removeAttr('disabled');
        } else {
            $('.delete_btn').attr('disabled', 'disabled');
        }
    });
    $('.pwd_profile').focus(function() {
        $('.delete_btn').attr('disabled', 'disabled');
    });
    $('.pwd_profile').blur(function() {
        var value = $(this).val();
        if (value.length <= 0) {
            $('.delete_btn').removeAttr('disabled');
        }
    });
    var showChar = 100;
    var ellipsestext = "...";
    var moretext = "Show more";
    var lesstext = "Show less";
    $('.more').each(function() {
        var content = $(this).html();
        if (content.length > showChar) {
            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);
            var html = c + '<span class="moreellipses">' + ellipsestext + '&nbsp;</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';
            $(this).html(html);
        }
    });
    $(".morelink").click(function() {
        if ($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });
    $("#password_signup").keyup(function(event) {
        if (event.keyCode == 13) {
            $("#signin").click();
        }
    });
    $("#mobile_number_sign_up_home").keyup(function(event) {
        if (event.keyCode == 13) {
            $("#create").click();
        }
    });
    $(".alert-button").click(function() {
        window.location.href = "/?freealert=active";
    });
    $(".scroll_close").click(function() {
        $('html, body').animate({
            scrollTop: '+=1700px'
        }, 800);
    });
    $('.upperimg img').on('hover', function() {
        $('.view_icon').show();
    });
    // $('.edit_after_save').each(function() {
    //     var img = new Image();
    //     img.src = $(this).attr('src');
    //     var canvas = document.createElement("canvas");
    //     var ctx = canvas.getContext("2d");
    //     var MAX_WIDTH = 400;
    //     var MAX_HEIGHT = 300;
    //     var width = img.width;
    //     var height = img.height;
    //     if (width > height) {
    //         if (width > MAX_WIDTH) {
    //             height *= MAX_WIDTH / width;
    //             width = MAX_WIDTH;
    //         }
    //     } else {
    //         if (height > MAX_HEIGHT) {
    //             width *= MAX_HEIGHT / height;
    //             height = MAX_HEIGHT;
    //         }
    //     }
    //     canvas.width = width;
    //     canvas.height = height;
    //     var ctx = canvas.getContext("2d");
    //     ctx.drawImage(img, 0, 0, width, height);
    //     dataUrl = canvas.toDataURL("image/png");
    //     $(this).attr('src', dataUrl);
    // });
});
$(window).load(function() {
    if ($('.simpleFilePreview_multiUI').hasClass('edit_image_available')) {
        image_clone = $('.simpleFilePreview_multi li:last').clone(true);
        class_id = $('.simpleFilePreview_multi li:last').attr('id');
        id_data = Number(class_id.split('_')[1]) + 1;
        image_clone.find('.edit_after_save,.editpost_image_change,.simpleFilePreview_input,.upload_image_remove').remove();
        $('.simpleFilePreview_multi').append("<li id='simpleFilePreview_" + id_data + "' class='simpleFilePreview' data-sfpallowmultiple='1'>\
                                          <a class='simpleFilePreview_input'>\
                                          <span class='simpleFilePreview_inputButtonText'>\
                                          <i class='fa fa-plus-circle fa_small'></i>\
                                          </span></a>" + image_clone.html() + "</li>");
    }
});
$( document ).ready(function() {
  // alert("ready");
  var chat_stat = 0,
  chat_reconnect = 0,
  chat_num_users = 0,
  chat_title_status = 2,
  chat_changed_lang = true,
  user_email,
  user_name,
  user_id,
  user_avatar,
  socket;
  
  var conf_domain,
  conf_server_type,
  conf_server,
  conf_port,
  conf_auto_login,
  conf_debug,
  conf_sound_active,
  conf_bar_default_expand,
  conf_bar_icon_expand,
  conf_bar_icon_collapse,
  conf_theme_default;
  // dialog_status = [];

  var chat_record =new Object();
  var dialog_status=[];
  // var dialog_user_status=[];
  var chat_users=[];

  var xhr_toolbar = $.get( "/toolbar/", function( toolbar ) {
    $( "body" ).append( toolbar );
  });
  
  var previous_chat_record;
  var own_products = [];

  // alert(window.location.pathname);


  $.when( xhr_toolbar ).done(function(r1, r2, r3, r4) {
    // localStorage.clear();
    main_set_conf();
    
    main_set_theme( conf_theme_default );
    
    //Main chat title bar
    main_chat_status( i18n.disconnected, "offline" );
    
    //0 chat users at begining
    main_chat_users_num( 2, 0 );
    
    //Init state of bar, collapse or expand
    if ( conf_bar_default_expand == false ) {
      $( "#main" ).addClass( "toolbar" );
      $( "#main-rpanel" ).addClass( "window" );
      $( "#slide-bar-span" ).toggleClass( conf_bar_icon_collapse );
      $( "#slide-bar" ).attr( "title", i18n.expand );
    } else {
      $( "#main" ).addClass( "toolbar-max" );
      $( "#main-rpanel" ).removeClass( "window" );
      $( "#slide-bar-span" ).toggleClass( conf_bar_icon_expand );
      $( "#slide-bar" ).attr( "title", i18n.collapse );
    }

    //Dialog tools menus
    $(function() { 
      function checkLength( o, n, min, max ) {
        if ( o.val().length > max || o.val().length < min ) {
          o.addClass( "ui-state-error" );
          updateTips( i18n.length_of +" " + n + " "+ i18n.must_be_between + " " +
            min + " " + i18n.and + " " + max + "." );
          return false;
        } else {
          return true;
        }
      }
   
      function checkRegexp( o, regexp, n ) {
        if ( !( regexp.test( o.val() ) ) ) {
          o.addClass( "ui-state-error" );
          updateTips( n );
          return false;
        } else {
          return true;
        }
      }
    });

    //Open new chat
    $( document ).on("click", ".user-button", function() {
      // alert("user button");
      var prefix = "user-button-";
      var iduser = $( this ).attr( "id" ).substring( (prefix.length) );
      var name   = $( this ).find('li').text();
      // alert(user_name);
      // alert(name);
      // if (window.location.pathname == '/search/'){
      //   var product_title = $(this).children().children('.product_title').text();
      //   // alert("product title in user button"+ product_title);
      //   alert(product_title);
      //   var product_id = $(this).children().children('.product_id').text();
      //   alert(product_id);
      // }
      // else{
        var product_title = $(this).children().children('.product_title').text();
        // alert("product title in user button"+ product_title);
        // alert(product_title);
        var product_id = $(this).children().children('.product_id').text();
        // alert(product_id);
        // append_previous_chat_message(user_name,name,product_id);
      // }
      // alert("product title in user button"+ product_id);
      // $(".box-title").text(product_title);
      // alert(product_title);
      // var value = $(this).parent().parent().parent().parent().siblings('.ui-dialog').children('.ui-dialog-content').children('.box').children('.box-header').children('.box-title').text(product_title);
      // alert(value);
      // Del notification if exist
      main_chat_user_alert( iduser, 1, product_id );

      if ( name.length > 15 ) {
        var length = 15;
        var name   = name.substring( 0, length );
        name = name + "...";
      }

      open_chat_box ( iduser, name, product_id, product_title );
      $(".box-title").text(product_title);
      //Set position
      // alert("dialog set position");
      $( "#Dialog" + product_id ).dialog( "option", "position", { my: "right bottom", at: "right top-3", of: this, collision: "flip, none" });
    });

    $( "#users" ).accordion({
      collapsible: false,
      icons: { header: "ui-icon-circle-arrow-e", activeHeader: "ui-icon-circle-arrow-s" },
      heightStyle: "fill"
    });

    //Main hide
    $( "#main-users-resizer" ).hide();

    //Click in user in chat box
    $( document ).on("click", ".user", function() {
      // alert("user");
      product=$(this).parent().parent().siblings('.product_title_for_chat').text();
      // alert("product" +product);
      product_id=$(this).parent().parent().siblings('.product_id').text();
      // alert("productid" +product_id);
      //Do nothing if user is offline
      if ( $( this ).hasClass( "offline" ) )
        return false;

      var prefix = "user-";
      var iduser_product = $( this ).attr( "id" ).substring( (prefix.length) );
      // alert(iduser_product);
      //Append div user in the bar if is not appended
      if ( $( "#users-button-bar" ).parent().find( "#user-button-" + iduser_product ).length == 0 ) {
        // var name = $( this ).text();
        // alert("if");
        var name = $( this ).parent().siblings('.product_users').text();
        // alert(name);
        var stat = $( this ).find( "li" ).attr( "class" );
        // alert(stat);
        $( "#users-button-bar" ).append( "<button id='user-button-" + iduser_product + "' class='user-button btn_user' style='font-size: 65%;'><li class='" + stat + "'>" + name + "</li><span class='product_title' style='display:none;'>" + product + "</span><span class='product_id' style='display:none;'>" + product_id + "</span></button>" );
        // $("#users-button-bar").closest('.product_title').val(product);
        // alert($("#users-button-bar").html());
        $( ".user-button" ).button();
      }

      //Do the same as clicking the user in the bar
      $( "#user-button-" + iduser_product ).trigger( "click" );

      return false;
    });

    //Button close search for clean it
    $( document ).on("click", "#chat-icon-close", function() {
      $( "#chat-search-text" ).val( "" );
      $( "#main-sort-chat" ).find( "li" ).slideDown().parent().show();
      if ( $( "#no-users-found" ).length > 0 )$( "#no-users-found" ).remove();
      return false;
    });

      var user_email=$.cookie('chat_email');
      var user_name=$.cookie('chat_user');
      var user_id=$.cookie('chat_userid');

      if(chat_stat==0)
      {
      if( user_email && user_name){
       
      // previous_chat_record = $.get( "/previous_chat_record/", {'user_name':user_name}, function( data ) {
      //   alert("data"+data);
      // });
        main_chat_init();
        socket_connect();
        socket_handle();
      }
      }
      else{
        main_chat_init();
        socket_connect();
        socket_handle();
      }

    function signin() {
      document.forms["sign_in"].submit();
      }

      sign_in_required =["emailid_signup", "password_signup"];
      jQuery('#signin').click(function(){     
      for (i=0;i<sign_in_required.length;i++) {
      var input = jQuery('#'+sign_in_required[i]);
      if (input.val() == "")  {   
        input.addClass("error_input_field");
        input.siblings('.labelError').show();         
      } else {    
        input.removeClass("error_input_field");
        input.siblings('.labelError').hide();        
      }
    }
    //Validate the e-mail.
    if($('#emailid_signup').val() != '' && $('#emailid_signup').val().indexOf('@') > -1){
    if (!/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/.test($('#emailid_signup').val())) {
      $('#emailid_signup').addClass("error_input_field");
      $('#emailid_signup').siblings('.labelError').text("Please enter valid email address");
      $('#emailid_signup').siblings('.labelError').show();
      //email.val(emailerror);
    }
    else
    {
      $('#emailid_signup').removeClass("error_input_field");
      $('#emailid_signup').siblings('.labelError').hide();
    }
    }
     if ($(":input").hasClass("error_input_field")){
    return false;
    }
    else{
      signin();
      return true;
    }
    });

    //Minus icon in main chat
    $( document ).on("click", "#min-main-chat", function() {
      $( "#main-users-resizer" ).hide();
    });

    //User status msg
    $( document ).on("focusin", "#text-status", function() {
      if ( text_custom_msg.length < 1 )
        $( this ).val("");
      else
        $( this ).val( text_custom_msg );

      return false;
    });
    $( document ).on("focusout", "#text-status", function() {
      if ( text_custom_msg.length < 1 )
        $( this ).val( text_status );
      else
        $( this ).val( text_custom_msg );

      return false;
    });

    //If enter key is pressed on custom message
    // $( document ).on("keydown", "#text-status", function(e) {
    //   if ( (e.which == 13) ) {
    //     if ( $( this ).val().length < 1 ) {
    //       $( this ).val( text_status );
    //       text_custom_msg = "";
    //     } else
    //       text_custom_msg = clean_msg ( $( this ).val() );

    //     if ( text_custom_msg_last != text_custom_msg ) { 
    //       user_status( "user_status_msg", text_custom_msg );
    //     }

    //     text_custom_msg_last = text_custom_msg;
    //     $( this ).blur();
    //     return false;
    //   }
    // });

    //Change text for lang
    function main_chat_set_dialog_lang ( dialogid ) {
      dialogid.parent().find( "#warning-alert" ).text( i18n.alert + " " );//Set text 'alert'
      dialogid.parent().find( "#warning-text" ).text( i18n.user_is + " " + i18n.disconnected.toLowerCase() );//Set text 'user is offline'
      dialogid.parent().find( "#iswriting-text" ).first().text( clean_name( dialogid.data( "name" ) ) + " " + i18n.is_writing );//Set text 'is writing...' 
      dialogid.parent().find( ".minimize-window" ).attr( "title", i18n.minimize );
      dialogid.dialog( { closeText: i18n.close } );
      chat_changed_lang = false;
    }

    // function ret(data, status){
    //   alert(data);
    //   alert(status);
    //   data = data.trim();
    //   if ( $.inArray(data, status) > -1 ){
    //     alert("ret if");
    //     return true;
    //   }
    //   else{
    //     alert("ret else");
    //     return false;
    //   }
    // }

    //Box Dialog for new user
    function main_set_dialog ( id, user, product, status ) {
      // alert("main_set_dialog");
      // alert("dialog status"+$("#Dialog" + product[i]).parents(".ui-dialog").is(":visible"));
      // var referrer =  document.referrer;
      // alert("referrer"+referrer);

      // alert("id"+id);
      // alert("user"+user);
      // alert("product"+ product);
      // alert($.cookie('dialog_status'));
      // status = $.cookie('dialog_status');
      // alert("inside main set"+status);
      product=$.makeArray( product );
      for(var i = 0; i <product.length; i++) {
      // alert("inside loop product_id"+ product[i]);
      $( "#Dialog" + product[i] ).dialog({
        // autoOpen: ret("#Dialog" + product[i], status),
        autoOpen: false,
        closeOnEscape: true,
        resizable: false,
        modal: false,
        minHeight: 200,
        maxHeight: 400,
        height: "auto",
        width: 280,
        appendTo:'#main',

        open: function(event, ui) {
          // alert("open function");
          //Set language in Dialog and init
          // alert("open function");
          if ( chat_changed_lang == true )
            main_chat_set_dialog_lang( $( this ) );

          if ( $( this ).data( "init" ) != 1 ) {

            //Save the top of dialog
            var main = $( this );
            // var name = main.data( "name" );
            var name =  main.attr( "user" );
            // alert(name);

            //Change text for the default lang
            main_chat_set_dialog_lang( main );

            //Extern window button
            //main.parent().find( ".ui-dialog-titlebar" ).append( "<button class='ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only externally-window' role='button' aria-disabled='false' title='Ventana externa'><span class='ui-icon ui-icon-arrowthick-1-nw'></span><span class='ui-button-text'>Ventana externa</span></button>" );
            //Min button
            main.parent().find( ".ui-dialog-titlebar" ).append( "<i class='fa fa-minus ui-button ui-widget ui-state-default ui-corner-all ui-button-icon-only fa fa-times minimize-window' role='button' aria-disabled='false' title='" + i18n.minimize + "'><span class='ui-icon ui-icon-minus'></span></i>" );
            //Status icon
            main.parent().find( ".ui-dialog-title" ).append( "<li id='dialog-status' class='" + main.data( "status" ) + "'>" + name + "</li>" );

            //Set hide 'is writing...'
            main.parent().find( "#iswriting" ).first().addClass( "no-display" );

            //Change flag at init option
            main.data( "init", 1 );

            //Textarea click
            main.parent().find( "textarea" ).click(function() {
              // alert("product_id 2"+JSON.stringify(main.parent().siblings(data("productid"))));
              product_title=$(this).parent().siblings().children('.box-title').text();
              // alert(product_title);
              product_id=$(this).parent().siblings('.box_product_id').text();
              // alert(product_id);
              main_chat_user_alert( id, 1, product_id );
            });

            //Textarea focus fancy in and out
            main.parent().find( "textarea" ).first().focusin(function() {
              main.addClass( "ui-chatbox-input-focus" );
            });
            $( this ).parent().find( "textarea" ).first().focusout(function() {
              main.removeClass( "ui-chatbox-input-focus" );
            });

            //Minimize button
            main.parent().find( ".minimize-window" ).click(function() {
              main.dialog( "close" );
            });

            //Fancy scrollbar
            new_scroll(main.parent().find( ".direct-chat-messages" ));

            //Close button
            // main.parent().find( ".ui-dialog-titlebar-close" ).click(function() {
            //   var iduser = main.attr( "id" ).substring( ( "Dialog".length ) );
            //   alert("#user-button-" + iduser + "_product-" + product_id);
            //   $( "#user-button-" + iduser + "_product-" + product_id ).remove();
            // });
            
            main.parent().find( ".ui-dialog-titlebar-close" ).click(function() {
              // var iduser = main.attr( "id" ).substring( ( "Dialog".length ) );
              productid =  main.attr('productid');
              // alert("#user-button-" + id + "_product-" + productid);
              $( "#user-button-" + id + "_product-" + productid).remove();
            });

            var typingTimeout;
            //Textarea send form when key enter is pressed
            main.find( "textarea" ).first().keyup(function( e ) {
              // product_title=$(this).parent().siblings().children('.box-title').text();
              // alert(product_title);
              // product_id=$(this).parent().siblings('.box_product_id').text();
              // alert(product_id);

              if (typingTimeout !== undefined) clearTimeout(typingTimeout);
              // alert("before call user is writing" +user);
              typingTimeout = setTimeout(function() { call_user_is_writing(user, product_id) }, 400);
              // store_chat_record(user);
              // alert("user" + user);
              //Progressbar of char in textarea
              main.parent().find( "#progressbar-char" ).progressbar( "option", "value", $( this ).val().length );
              if ( $( this ).val().length > 100 ) {
                var remove_excess = $( this ).val().substr(0, 100);
                $( this ).val( remove_excess );
              }

              //Intro event
              if ( (e.which == 13) && !event.shiftKey ) {
                var msg = clean_msg ( $( this ).val() );
                $( this ).val( "" );
                if (msg !== "") {
                  main.parent().find( "#progressbar-char" ).progressbar( "option", "value", 0 );
                  // alert(product[i]);
                  socket.emit('message', { 'user': user, 'msg': msg, 'product_id':product_id, 'product_title': product_title }, function (data) {
                    var recv = JSON.parse(data);
                    // alert("before send message"+JSON.stringify(recv));
                    // alert("before send message"+user);
                    append_msg_me(msg, recv.date, product_title, product_id);
                    // FIXME
                    // Set dialog position
                    main.dialog( "option", "position", { my: "right bottom", at: "right top-3", of: "#user-button-"+id+ "_product-"+product_id, collision: "flip, none" });
                  });
                }
              }
              return false;
            });

            //Init char progress bar
            $( this ).find( "#progressbar-char" ).first().progressbar({ value: 0 });
          }

          //Go to bottom
          new_scroll($( this ).parent().find( ".direct-chat-messages" ));
          // alert("end open");
        },
      
        show: {
          effect: "none"
        },
        hide: {
          effect: "none"
        }
      });
      }
      // alert("end main_set_dialog");
    }

    function call_user_is_writing(user, product_id) {
      // alert("call user");
      // alert("after call user is writing" +user);
      // user_list=user;
      // alert("user_list" +user_list);
      // chat_record['receiver']=user;
      if (socket)
      socket.emit('user_typing', { 'user': user, 'product_id': product_id });
      
    }

    //Socket emit send data
    function user_status ( action, data ) {
      // TODO: user_status_msg
      if (action == 'user_status')
      {
        // alert(data);
        socket.emit('user_status', { 'status': data });
      }
    }

    //Clean text received
    function clean_msg ( text ) {
      //Clean html tags
      var msg_html = text.replace( /(<([^>]+)>)/ig,"" );
      //Clean html tabs and new line
      var msg_done = msg_html.replace(/(\n|\r|\r\n)$/, '');
      return msg_done;
    }

    function minhour(d) {
      var hour = d.getHours();
      var mins = d.getMinutes();
      var ampm = " pm";

      if( hour < 10 ) { hour = "0" + hour; }
      if( hour < 12 ) { ampm = " am"; }
      if( mins < 10 ) { mins = "0" + mins; }

      var r = hour + ":" + mins + ampm;
      return r;
    }

    function get_format_date(date) {
      var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];
      var dayNames = ['Sun','Mon','Tues','Wed','Thur','Fri','Sat'];
      var d = new Date(date);
      var day = d.getDay(); 
      var date = d.getDate();
      var month = d.getMonth();
      var r = dayNames[day] + " " + date + " " + monthNames[month] + " " + minhour(d);
      // alert("r"+r);
      return r
    }

    // Append my messages
    function append_msg_me ( msg, date, product_title, product_id ) {
      // alert(product_title);
      // alert("append_msg_me"+ product_id);
      // alert("date"+date);
      // alert(user);
      var main = $( "#Dialog" + product_id );
      var box = main.parent().find(".box-body");
      var me = box.find('.direct-chat-messages').last();
      var scroll = main.parent().find( ".direct-chat-messages" );
      $('.box-title').text(product_title);
      if (me.children().last().attr('id') == 'me') {
        // alert("me");
        me.children().find('.direct-chat-text').last().append("<div>" + msg + "</div>")
      } else {
        me.append("\
          <div class='direct-chat-msg' id='me'>\
            <div class='direct-chat-info clearfix'>\
              <span class='direct-chat-name pull-left'>" + user_name + "</span>\
              <span class='direct-chat-timestamp pull-right'>" + get_format_date(date) + "</span>\
            </div>\
            <img class='direct-chat-img' src='" + user_avatar + "' alt='message user image' />\
            <div class='direct-chat-text'>\
              <div>" + msg + "</div>\
            </div>\
          </div>");
      };

      // Go to bottom
      new_scroll(scroll);
    }

    function append_msg_he ( msg, name, date, avatar, product_id ) {
      // alert("append_msg_he");
      // alert("date"+date);
      var fullname = '';
      var fname = name.split(' ');
      var main = $( "#Dialog" + product_id );
      var box = main.parent().find(".box-body");
      var he = box.find('.direct-chat-messages').last();
      var scroll = main.parent().find( ".direct-chat-messages" );
      if (fname.length == 2) fullname = fname[0] + " " + fname[1];
      else fullname = fname[0];

      if (he.children().last().attr('id') == 'he') {
        he.children().find('.direct-chat-text').last().append("<div>" + msg + "</div>")
      } else {
        he.append("\
          <div class='direct-chat-msg right' id='he'>\
            <div class='direct-chat-info clearfix'>\
              <span class='direct-chat-name pull-right'>" + fullname + "</span>\
              <span class='direct-chat-timestamp pull-left'>" + get_format_date(date) + "</span>\
            </div>\
            <img class='direct-chat-img' src='" + avatar + "' alt='message user image' />\
            <div class='direct-chat-text'>\
              <div>" + msg + "</div>\
            </div>\
          </div>");
      };

      // Go to bottom
      new_scroll(scroll);
    }

    function new_scroll(s) {
      var sint = s.prop('scrollHeight') + 'px';
      s.slimScroll({
        size: '5px',
        scrollTo : sint,
        height: 'auto',
        start: 'bottom'
      });
    }

    //Function for Open chat box
    function open_chat_box ( iduser, name, product_id, product_title ) {
      // alert("open_chat_box");
      // alert(name);
      // alert(product_id);
      if ( $( "#Dialog" + product_id ).dialog( "isOpen" ) == false ) {
        // dialog_product_status.push(product_id);
        dialog_status.push({"user":iduser.split('_')[0],"name":name,"product":product_id,"title":product_title});
        // alert("dialog_status"+JSON.stringify(dialog_status));
        // $.cookie("dialog_status", JSON.stringify(dialog_status));
        // localStorage.setItem('dialog_status', JSON.stringify(dialog_status));
      
        //Close all dialogs
        $( ".ui-dialog-content" ).dialog( "close" );
        $( "#Dialog" + product_id ).data( "name", name );
        $( "#Dialog" + product_id ).dialog( "open" );
        $(".box-title").text(product_title);
        // alert($.cookie("dialog_status"));
      } else
        $( "#Dialog" + product_id ).dialog( "close" );
    }

    //Debug errors with alert
    if ( conf_debug == true ) {
      window.onerror = function( msg, url, linenumber ) {
        alert( "Error: " + msg + "\nUrl: " + url + "\nLine: " + linenumber );
        return true;
      }
    }

    // $( document ).ready(function() {
    //   //Open chat by default on page ready
    //   if ( conf_auto_login == true )
    //     $( "#chat-title-button" ).trigger( "click" );
    // });

    //Set position on resize of the window
    // $( window ).resize(function() {
    //   set_position();
    // });

    function clean_name( text ) {
      var text_arr = text.split(" ");
      if ( text_arr[0].length > 9 )
        text_arr[0] = text_arr[0].substr(0, 8) + "..";
      
      return text_arr[0]
    }

    function main_chat_status ( text , status ) {
      //TODO:
      //if was discconected, do reconnect
      if ( chat_reconnect == 1 ) {
        socket_reconnect();
      }

      if ( status == "online" )
        $( "#rerun-img" ).attr( "src", "../img/button_online.png" );
      else if ( status == "busy" )
        $( "#rerun-img" ).attr( "src", "../img/busy.png" );
      else if ( status == "offline" )
        $( "#rerun-img" ).attr( "src", "../img/button_offline.png" );

      // $( "#chat-title-button" ).find( "li" ).first().text( i18n.chat + " (" + text + ") " );
      // $( "#chat-title-button" ).find( "li" ).first().removeClass().addClass( status );

    }

    function main_chat_init () {
      //Just in case, close dialogs open
      $( ".ui-dialog-content" ).dialog( "close" );

      //Set accordion property in init
      $( "#users" ).accordion( "refresh" );

      chat_stat = 1;
    }

    function main_chat_set_position ( pos ) {
      //pos = 0, set position
      //pos = 1, increment main chat and set position
      //pos = 2, decrement main chat and set position
      if ( pos > 0 ) {
        //Increment overall height for add the new user
        var height_main_users_resizer = $( "#main-users-resizer" ).height() + 2;
        var height_main_sort_chat = $( "#main-sort-chat" ).height();
        var height_users_window_chat = $( "#users-window-chat" ).height();

        if ( height_main_users_resizer < 600 && height_main_sort_chat > height_users_window_chat ) {

          if ( pos == 1 )
            var newheight = height_main_users_resizer + height_main_sort_chat - height_users_window_chat;
          else if ( pos == 2 )
            var newheight = height_main_users_resizer - height_main_sort_chat - height_users_window_chat;
          else
            alert( "main_chat_set_position() unexpected value '" + pos + "', please report this" );

          if ( newheight < 600 ) {
            $( "#main-users-resizer" ).css( "height", newheight );
            $( "#users" ).accordion( "refresh" );
          }
        }
      }
      $( "#main-users-resizer" ).position({ my: "right bottom", at: "right top", of: "#main", collision: "flip, none" });
    }

    // Delete the user in main chat, but in message box, 
    // you must be able to read the conversation
    function main_chat_user_offline_new ( id, product_id ) {
      // alert("main_chat_user_offline_new");
      // alert(id);
      // alert(product_id);
      product=$.makeArray( product_id );
      for(var i = 0; i <product.length; i++) {
      //Display warning
      // alert(product[i]);
      $( "#Dialog" + product[i] ).parent().find( "#warning" ).first().removeClass( "no-display" );
      //Disable send msg
      $( "#Dialog" + product[i] ).parent().find( "#textarea_msg" ).first().attr( "disabled", "disabled" );

      //if ( has scroll )
      //BUG!!!
      var height = 180 - $( "#Dialog" + product[i] ).parent().find( "#warning" ).height() - 2;
      //Now the height of the box is smaller
      $( "#Dialog" + product[i] ).parent().find( "#box" ).first().css( "max-height", height );

      //Change li status to offline
      main_chat_user_status( id, "offline", product[i] );

      $( "#main-sort-chat" ).find( "#user-"+ id + "_product-" + product[i] ).remove();

      //Decrease total number of current users
      main_chat_users_num( 1, 0 );

      //Add label of no users connected
      // if ( chat_num_users == 0 )
      //   if ( $( "#chat-main-title-label" ).length == 0 )
      //     $( "#main-sort-chat" ).append( "<div id='chat-main-title-label'>" + i18n.no_users + "</div>" );

      //Decrease total chat main heigh for the new user
      main_chat_set_position( 2 );
    }
    }

    function main_chat_user_offline ( id, product_id ) {
      alert("main_chat_user_offline");
      //Display warning
      $( "#Dialog" + product_id ).parent().find( "#warning" ).first().removeClass( "no-display" );
      //Disable send msg
      $( "#Dialog" + product_id ).parent().find( "#textarea_msg" ).first().attr( "disabled", "disabled" );

      //if ( has scroll )
      //BUG!!!
      var height = 180 - $( "#Dialog" + product_id ).parent().find( "#warning" ).height() - 2;
      //Now the height of the box is smaller
      $( "#Dialog" + product_id ).parent().find( "#box" ).first().css( "max-height", height );

      //Change li status to offline
      main_chat_user_status( id, "offline" );
    }

    // function main_chat_user_delete ( id ) {
    //   $( "#main-sort-chat" ).find( "#user-"+id ).remove();
    //   $( "#user-button-" + id ).remove();
    //   $( "#Dialog" + id ).remove();

    //   //Decrease total number of current users
    //   main_chat_users_num( 1, 0 );

    //   //Add label of no users connected
    //   // if ( chat_num_users == 0 )
    //   //   if ( $( "#chat-main-title-label" ).length == 0 )
    //   //     $( "#main-sort-chat" ).append( "<div id='chat-main-title-label'>" + i18n.no_users + "</div>" );

    //   //Decrease total chat main heigh for the new user
    //   main_chat_set_position( 2 );
    // }

    function main_chat_user_status ( id, status, product_id ) {
      $( "#user-" + id + "_product-" + product_id ).find( "li" ).removeClass().addClass( status );
      $( "#user-" + id + "_product-" + product_id ).find( "li" ).removeClass().addClass( status );
      // $( "#user-" + id ).find( "li a" ).removeClass().addClass(status );
      $( "#user-" + id + "_product-" + product_id ).find( "li" ).removeClass().addClass( status );
      $( "#Dialog" + product_id ).parent().find( "#dialog-status" ).removeClass().addClass( status );
      $( "#Dialog" + product_id ).data( "status", status );
    }

    function main_chat_user_new ( id, status, name, product,action ) {
      //Append in the chat!
      // alert("main_chat_user_new");
      // alert("product"+product);
      $( ".product_users" ).each( function( index, element ){
        // if ($(this).text()==name){
          // alert("user name"+ $(this).text());
          // alert("productid"+$(this).parent().next('.product_id').text());
          product_id = $(this).parent().next('.product_id').text();
          if (($(this).text()==name) && ($.inArray($(this).parent().next('.product_id').text(), product) < 0)){
        // $(this).next('.main-sort-chat').append( "<div id='user-" + id + "' class='user'><li class='" + status + "'><a href='#' style='text-decoration:none;' class='btn btn-default contact_button contact-button'> Chat Now </a></li></div>" );
         // $(this).next('.main-sort-chat').append( "<div id='user-" + id + "' class='user'><li class='" + status + "'><span style='display:none;'>"+ name +"</span><a href='#' style='text-decoration:none;' class='btn btn-default contact_button contact-button'>Chat Now</a></li></div>" );
        $(this).next('.main-sort-chat').html( "<div id='user-" + id + "_product-" + product_id + "' class='user'><li class='" + status + "'><a href='#' style='text-decoration:none;' class='btn btn-default contact_button contact-button'> Chat Now </a></li></div>" );
        // $(this).next('.main-sort-chat').append( "<div id='user-" + id + "' class='user'><li class='" + status + "'><a href='#' style='text-decoration:none;' class='btn btn-default contact_button contact-button'>" + name + "</a></li></div>" );
        // $( ".box-title" ).each( function( index, element ){
        // $('.box-title').text($('.product_users').next('.product_title_for_chat').text());
        // });
        // alert(product_id);
        if (action == "usrlist")
          append_previous_chat_message(user_name,name,product_id);
        }
     
      
      // $( "#main-sort-chat" ).append( "<div id='user-" + id + "' class='user user-pad scroll-content-item'><li class='" + status + "'><a href='#' style='text-decoration:none;'>" + name + "</a></li></div>" );

    
      //Set status in dialog
      $( "#Dialog" + product_id ).data( "status", status );

      //Open the chat for styling things
      if ( $( "#main-users-resizer" ).is( ":hidden" ) ) {
        $( "#main-users-resizer" ).show();
        var wasclose = 1;
      }

      //Increase total number of current users
      main_chat_users_num( 0, 0 );

      //Increase total chat main heigh for the new user
      main_chat_set_position( 1 );

      //Close because was closed
      if ( wasclose == 1 )
        $( "#main-users-resizer" ).hide();
       });
    }

    function main_append_dialog ( id, user, product, status ) {
      // alert("main_append_dialog");
      // alert("id1"+ id);
      // alert("user1"+ user);
      // alert("product1"+ product);
      product=$.makeArray( product );
      // alert("product after array" + product);
      // alert("dialog length:" + $( "#Dialog" + id ).length);
      if ( $( "#Dialog" + product ).length == 0 ) {
      //   alert("dialog open");     
      // socket.emit('chat_history', { 'user': user,'product':product }, function (data) {
      //   // append_previous_chat_message();
      // });
      for(var i = 0; i <product.length; i++) {
        // alert("product[i]"+ product[i]);
        // alert("chat_history"+chat_history);
        // alert("chat_history"+JSON.stringify(chat_history));
        $("#main").append("<div id='Dialog" + product[i] + "' title='' user='" + user + "' productid='" + product[i] + "' data-status='" + status + "'>\
            <div class='box box-info direct-chat direct-chat-info ui-widget-content no-content-border'>\
              <div class='box-header with-border'>\
                <h4 class='box-title'></h4>\
                <div class='box-tools pull-right'>\
                  <span data-toggle='tooltip' title='0 New Messages' class='badge bg-blue new-messages'>0</span>\
                  <button class='btn btn-box-tool' data-toggle='tooltip' title='Contacts' data-widget='chat-pane-toggle'><i class='fa fa-comments'></i></button>\
                </div>\
              </div>\
              <div id='warning' class='highlight-padding ui-state-highlight ui-corner-all no-display'>\
                <span class='window ui-icon ui-icon-info'></span>\
                <strong id='warning-alert'></strong><span id='warning-text'></span>\
              </div>\
              <div class='box-body'>\
              <div class='direct-chat-messages'>\
              </div>\
              </div>\
              <div id='iswriting' class='pull-right'>\
                <i class='fa fa-pencil'></i>\
                <small id='iswriting-text'></small>\
              </div>\
              <div id='progressbar-char' class='pull-left'></div>\
              <div class='box_product_id' style='display:none;'>" + product[i] + "</div>\
              <div class='small-box-footer'>\
                <textarea id='textarea_msg' class='form-control textarea-msg' name='message' placeholder='"+ i18n.type_message +"'></textarea>\
              </div>\
            </div>\
          </div>");
      }
    }
      // socket.on('chat_history_data', function (recv) {
      //     // alert("yes");
      //     // var message = JSON.stringify(recv);
      //     // alert("message"+message);
      //     // alert("message"+JSON.stringify(recv.current_user_record));
      //     // alert(user_name);
      //     append_previous_chat_message(recv.current_user_record);
      //   });
  }

 
  // function append_previous_chat_message( message ) {
  //   console.log("append_previous_chat_message===="+JSON.stringify(message));
  //   // alert("append_previous_chat_message");
  //   // alert("message"+message);
  //   // alert("message.current_chat_record"+message.current_chat_record);
  //   // alert("chat_message"+JSON.stringify(message));
  //   // chat_message = JSON.stringify(message);
  //   // alert("chat_message"+chat_message);
  //   // console.log("chat_message"+JSON.stringify(chat_message));
  //   // alert("message"+message['current_user_record']);
  //   // chat_message = JSON.stringify(message);    
  //   // alert("chat_message"+chat_message);
  //   $.each(message, function(i,val){
  //     // alert("loop");
  //   // for(var i = 0; i <product.length; i++) {
        // var main = $( "#Dialog" + val.product );
        // var message = main.find('.direct-chat-messages');
        // var scroll = main.parent().find( ".direct-chat-messages" );
        // // alert(main.attr('user'));
        // // alert(val.sender);
        // // alert(val.receiver);
        // // alert(user_name);
        //     if (val.sender != main.attr('user')){ 
        //           message.append("<div class='direct-chat-msg' id='me'>\
        //                         <div class='direct-chat-info clearfix'>\
        //                           <span class='direct-chat-name pull-left'>" + val.sender + "</span>\
        //                           <span class='direct-chat-timestamp pull-right'>" + get_format_date(val.received_at) + "</span>\
        //                         </div>\
        //                         <img class='direct-chat-img' src='"+ val.sender_image +"' alt='message user image' />\
        //                         <div class='direct-chat-text'>\
        //                           <div>" + val.message + "</div>\
        //                         </div>\
        //                       </div>");              
        //      }
        //      else{        
        //           message.append("<div class='direct-chat-msg right' id='he'>\
        //                         <div class='direct-chat-info clearfix'>\
        //                           <span class='direct-chat-name pull-right'>" + val.sender + "</span>\
        //                           <span class='direct-chat-timestamp pull-left'>" + get_format_date(val.received_at) + "</span>\
        //                         </div>\
        //                         <img class='direct-chat-img' src="+ val.receiver_image +"' alt='message user image' />\
        //                         <div class='direct-chat-text'>\
        //                           <div>" + val.message + "</div>\
        //                         </div>\
        //                       </div>");
        //     }
        //     new_scroll(scroll);
        // });    
  // }

    function append_previous_chat_message( sender, receiver, product ) {
      // var configFile = fs.readFileSync('chat.json');
      // var config = JSON.parse(configFile);
      // alert("append_previous_chat_message");
      record = socket.emit('chat_history', { 'sender': sender,'receiver':receiver,'product':product });
      // console.log("record"+record);
      // console.log("record"+JSON.stringify(record));
      socket.on('chat_history_data', function (data) {
        console.log("data"+JSON.stringify(data));
        $.each(data.current_user_record, function(i,val){
          var main = $( "#Dialog" + val.product );
          var message = main.find('.direct-chat-messages');
          var scroll = main.parent().find( ".direct-chat-messages" );
          if (val.sender == sender){ 
                message.append("<div class='direct-chat-msg' id='me'>\
                              <div class='direct-chat-info clearfix'>\
                                <span class='direct-chat-name pull-left'>" + val.sender + "</span>\
                                <span class='direct-chat-timestamp pull-right'>" + get_format_date(val.received_at) + "</span>\
                              </div>\
                              <img class='direct-chat-img' src='"+ val.sender_image +"' alt='message user image' />\
                              <div class='direct-chat-text'>\
                                <div>" + val.message + "</div>\
                              </div>\
                            </div>");              
           }
           else{        
                message.append("<div class='direct-chat-msg right' id='he'>\
                              <div class='direct-chat-info clearfix'>\
                                <span class='direct-chat-name pull-right'>" + val.sender + "</span>\
                                <span class='direct-chat-timestamp pull-left'>" + get_format_date(val.received_at) + "</span>\
                              </div>\
                              <img class='direct-chat-img' src="+ val.receiver_image +"' alt='message user image' />\
                              <div class='direct-chat-text'>\
                                <div>" + val.message + "</div>\
                              </div>\
                            </div>");
          }
          new_scroll(scroll);
        });
      });
    }
  

    // function main_do_dialog( element, id ) {
    //   $( element ).tipsy( "hide" );

    //   if ( $( id ).dialog( "isOpen" ) == false )
    //     $( id ).dialog( "open" );
    //   else
    //     $( id ).dialog( "close" );

    //   return false;
    // }

    //Set the num of available users
    function main_chat_users_num ( action, set ) {
      //action = 0, increment
      //action = 1, decrement
      //action = 2, set
      var number;

      if ( action == 0 )
        number = chat_num_users + 1;
      else if ( action == 1 )
        number = chat_num_users - 1;
      else if ( action == 2 )
        number = set;
      else
        alert( "main_chat_users_header_num() unexpected value '" + action + "', please report this" );

      chat_num_users = number;
      $( "#users-header-num" ).text( number );
    }

    function main_chat_title( action ) {
      //action == 0, connected
      //action == 1, disconnected
      //action == 2, loading
      var text;
      var label;

      //Reset in changed chat
      if ( chat_changed_lang == true )
        $( "#chat-main-title-ui" ).remove();

      if ( action == 0  ) {
        text  = i18n.connected;
        label = i18n.no_users;
        $( "#progressbar" ).remove();
      }
      else if ( action == 1 ) {
        text  = i18n.disconnected;
        label = i18n.disconnected;
        $( "#progressbar" ).remove();
        $( "#main-sort-chat" ).empty();
      }
      else if ( action == 2 ) {
        text  = i18n.loading;
        label = i18n.loading + " " + i18n.please_wait;
        $( "#main-sort-chat" ).empty();
      }
      else
        alert( "Error, invalid action '" + action + "'" );

      //Fancy progress bar
      if (action == 2) {

        if ( $('#chat-title').find('#chat-main-title-ui').length == 1 )
          $( "#chat-main-title-ui" ).remove();

        if ( $('#chat-title').find('#progressbar').length == 0 ) {
          $( "#chat-title" ).append( "<div id='progressbar'><div id='progressbar-child' class='progress-label'>" + text + "</div></div>" );
          $( "#progressbar" ).progressbar({ value: false });//Loading
        } else
          $( "#progressbar-child" ).text( text );

      } else {
        if ( $('#chat-title').find('#chat-main-title-ui').length == 0 )
          $( "#chat-title" ).append( "<div id='chat-main-title-ui' class='ui-widget'><div id='chat-main-title-id' class='chat-main-title'>" + text + "</div></div>" );
      }

      $( "#chat-main-title-id" ).text( text );
      
      chat_title_status = action;
      main_chat_set_position( 0 );
    }

    //Get all setting in config.js
    function main_set_conf () {
      try {
        if( !conf ) {
          alert( "error, conf not exist" );
          return true;
        }

        conf_domain = conf["domain"];
        conf_server_type = conf["server_type"];
        conf_server = conf["server"];
        conf_port = conf["port"];
        conf_auto_login = conf["auto_login"];

      } catch( error ) {
        alert( error );
        return true;
      }
    }

    //Change theme function
    function main_set_theme( theme ) {
      var theme_css = "../static/"+ "themes/" + theme + "/jquery-ui.min.css";    
      $( "#theme" ).attr( "href" , theme_css );
      return false;
    }

    //Change position on resize window
    // function set_position() {
    //   //Main chat
    //   $( "#main-users-resizer" ).position({ my: "right bottom", at: "right top", of: "#main", collision: "flip, none" });

    //   //Tools dialog
    //   if ( $( "#tools-panel" ).dialog( "isOpen" ) == true )
    //     $( "#tools-panel" ).dialog( "widget" ).position({ my: "left bottom", at: "left top", of: "#main", collision: "flip, none" });

    //   //Options dialog
    //   if ( $( "#options-panel" ).dialog( "isOpen" ) == true )
    //     $( "#options-panel" ).dialog( "widget" ).position({ my: "right bottom", at: "right top", collision: "flip, none", of: "#main"  });

    //   //TODO: change position of all chat dialog opened
    // }

    function main_chat_new_messages (action, main) {
      // action: 0 set to 0 count of messsages no reed
      // action: 1 increment count of messsages no reed
      if (action == 0) {
        var nmsgs = 0;
      } else {
        var msgs = parseInt(main.find( ".new-messages" ).text());
        var nmsgs = msgs + 1;
      }

      var txt = nmsgs + " " + i18n.new_messages;
      main.find( ".new-messages" ).text( nmsgs );
      main.find( ".new-messages" ).prop("title", txt);
    }

    function main_chat_user_alert ( id, action, productid ) {
      //action = 0, add notification if not already have one
      //action = 1, del notification if already have one
      var main = $( "#Dialog" + productid );

      if (action == 0) {
        if ( !main.parent().find( ".ui-dialog-titlebar" ).hasClass( "ui-state-highlight" ) ) {
          main.parent().find( ".ui-dialog-titlebar" ).addClass( "ui-state-highlight", 500 );
          $( "#user-button-" + id + "_product-" + productid ).addClass( "ui-state-error", 500 );  
        }

        //Increment number of new messages not read
        main_chat_new_messages(1, main);

      } else if (action == 1) {
        if ( main.parent().find( ".ui-dialog-titlebar" ).hasClass( "ui-state-highlight" ) ) {
          main.parent().find( ".ui-dialog-titlebar" ).removeClass( "ui-state-highlight", 500 );
          $( "#user-button-" + id + "_product-" + productid ).removeClass( "ui-state-error", 500 );  
        }

        //Set to 0 number of new messages not read
        main_chat_new_messages(0, main);

      } else
        alert( "main_chat_user_alert() unexpected action '" + action + "', please report this" );
    }

    //Disconnect and close
    function main_chat_shutdown() {
      /*chat_stat = 0;
      user_name = '';
      user_email = '';
      user_avatar = '';
      */
      main_chat_disconnect();
    }

    $('.user_logout').click(function(){
      // alert("logout");
      socket.emit('forceDisconnect');
      localStorage.clear();
    });

    //Disconnect
    function main_chat_disconnect() {
      chat_num_users = 0;
      main_chat_users_num( 2, 0 );//0 chat users at begining
      main_chat_title( 1 );
      main_chat_status( i18n.disconnected, "offline" );
      
      //Close all dialogs
      $( ".ui-dialog-content" ).dialog( "close" );

      //Disabled effect
      //$( "#users" ).accordion( "disable" );
      
      //Disconnect session
      if (socket)
        socket_disconnect();
    }

    function socket_connect() {
      socket = io.connect( 'http://'+ conf_server , {
        port: conf_port
        // 'connect timeout': 5000
      });
      // console.log(socket.toSource());
    }

    function socket_handle() {

      socket.on('connect_failed', function ( data ) {
        main_chat_disconnect();
      });

      socket.on('reconnect_failed', function ( data ) {
        main_chat_disconnect();
      });

      socket.on('error', function ( data ) {
        main_chat_disconnect();
      });

      socket.on('custom_error', function ( data ) {
        // alert(data.message);
        main_chat_shutdown();
      });

      socket.on('forceDisconnect', function ( data ) {
        main_chat_disconnect();
      });

      socket.on('connect_timeout', function ( data ) {
        main_chat_disconnect();
      });

      socket.on('reconnecting', function ( data ) {
        //TODO: do something
        // Main chat title, add the loading bar and text
        //main_chat_title( 2 );
      });

      socket.on('connecting', function ( data ) {
        // Main chat title, add the loading bar and text
        main_chat_title( 2 );
      });

      socket.on('connect', function ( data ) {
        console.log('connect');
      });

      socket.on('chat', function (recv) {
        // alert("on chat");
        var message = JSON.parse(recv);
        // alert("on_chat"+JSON.stringify(message));
        // console.log("on_chat"+JSON.stringify(message));
        handle_incoming(message);
      });

      chat_join();
    }

    function chat_join() {
      // alert("chat_join");
      // alert(user_email);
      // alert(user_name);
      $.ajax({
            type: 'POST',
            url:'/get_user_products/',
            data:"user_email="+user_email+"&user_name="+user_name,
            success: function(data){
            // alert(data);
            // var res = eval("("+data+")");
            // jQuery.each(res, function(i,val) {
            // });
            own_products = data;
            // alert("own_products"+data);
            socket.emit('join', { 'uid':user_id,'user': user_email, 'name': user_name, 'data':data }, function (data) { 
                var recv = JSON.parse(data);
                // console.log(recv);
                // console.log(user_email);
                // console.log(user_name);
                // alert(field2);
                chat_record['receiver']=user_name;
                // alert("chat_record['receiver']"+chat_record['receiver']);
                if (recv.login == 'successful') {
                  // user_name = recv.my_settings.name;
                  user_avatar = recv.my_settings.avatar;

                  setTimeout(function () {
                    main_chat_title( 0 );
                    main_chat_status( i18n.connected, 'online' );
                  }, 700);
                }
           });
          }
      });
    }

    function socket_disconnect () {
      socket.disconnect();
      chat_reconnect = 1;
    }

    function socket_reconnect() {
      socket.socket.reconnect();
      chat_join();
      chat_reconnect = 0;
    }


    /***************** incoming events **************************/
    function handle_incoming(recv) {
      // alert("handle_incoming");
      // alert(JSON.stringify(recv));
      // console.log(JSON.stringify(recv));
      var action  = recv.action;
      // alert(action);
      if (action == 'message') {
        // alert("message");
        var date   = recv.date;
        var iduser = recv.data.user.uid;
        var name   = recv.data.user.user;
        var status = recv.data.user.status;
        var avatar = recv.data.user.avatar;
        var msg    = recv.data.msg;

        // alert(name);
        // alert(msg);
        // alert(status);
        product_title=recv.data.product_title;
        // alert("product_title"+ product_title);

        product_id=recv.data.product_id;
        // alert("product_id" + product_id);
        var main   = $( "#Dialog" + product_id );

        //Do nothing if user is offline
        // TODO:
        /*if ( status == 'offline' )
          return false;*/
        // alert("user" +recv.data.user.user);
        // alert("product_id" +product_id);
        // alert("before main append");
        // alert("product_id"+product_id);
     
        // if ($('div').not(main)){
        // 

        if ( $( "#Dialog" + product_id ).length == 0 ) {
        // alert("if");  
        main_append_dialog( recv.data.user.uid, recv.data.user.user, recv.data.product_id,status);
        // append_previous_chat_message( recv.data.user.uid, recv.data.user.user, recv.data.product_id, recv.data.user.chat_message)
        main_set_dialog( recv.data.user.uid, recv.data.user.user, recv.data.product_id,status);
        append_previous_chat_message(recv.data.user.user,user_name,recv.data.product_id);
        
        }
        // alert("after main_set_dialog");

        //Append div user in the bar if is not appended
        if ( $( "#users-button-bar" ).parent().find( "#user-button-" + iduser + "_product-" + product_id ).length == 0 ) {
          // alert("user button bar");
          $( "#users-button-bar" ).append( "<button id='user-button-" + iduser + "_product-" + product_id + "' class='user-button btn_user' style='font-size: 65%;'><li class='" + status + "'>" + name + "</li><span class='product_title' style='display:none;'>" + product_title + "</span><span class='product_id' style='display:none;'>" + product_id + "</span></button>" );
          $( ".user-button" ).button();
          $( "#user-button-" + iduser + "_product-" + product_id ).trigger( "click" );
        }

        // alert("after user button call");
        // Do the same as clicking the user in the bar
        // $( "#user-button-" + iduser + "_product-" + product_id ).trigger( "click" );


        //Check focus state and focus document to do sound and alert
        if( !$(document).is(document.activeElement) || !main.find( "#textarea_msg" ).is(document.activeElement) ) {
          //Do sound effect
          //if sounds has been disabled, dont do it
          if ( conf_sound_active == true )
            $( "#audio-popup" ).trigger( "play" );

          //Add notification if not exist
          main_chat_user_alert( iduser, 0, product_id );
        }
        
        // alert(product_title);
        // alert("before append msg he"); 
        append_msg_he( msg, name, date, avatar, product_id );
        // Set dialog position
        main.dialog( "option", "position", { my: "right bottom", at: "right top-3", of: "#user-button-"+iduser+"_product-"+product_id, collision: "flip, none" });
        chat_record['sender']=name;
        chat_record['message']=msg;
        chat_record['product']=product_id;
        chat_record['sender_image']=user_avatar;
        chat_record['receiver_image']=avatar;
        var d = new Date();
        chat_record['received_at']=d;
  
        // JSONstr=JSON.stringify(chat_record);
        // $.post("/store_chat_record/", {data:JSONstr}, function(data){ console.log("success")});  

        socket.emit('chat_json', { 'chat_record': chat_record }, function (data) {
         alert("data"+data);
        });
      }

      else if ( action == 'newuser' ) {
        //Append the Dialogid
        // sample_f1();
        // alert("newuser" +recv.user.user);
        // alert("newuser");
        status = recv.user.status;
        main_append_dialog( recv.user.uid, recv.user.user, recv.user.product,status);
        // append_previous_chat_message(recv.user.uid, recv.user.user, recv.user.product, recv.user.chat_message);
        main_set_dialog( recv.user.uid, recv.user.user, recv.user.product,status);
        // main_set_dialog( recv.user.uid, recv.user.user);

        //Append the user to chat
        main_chat_user_new( recv.user.uid, recv.user.status, recv.user.user, recv.user.product, "newuser");

        // if ( $( "#Dialog" + own_products ).length == 0 ) {
        //   // alert("if");  
        //   main_append_dialog( recv.user.uid, recv.user.user, own_products);
        //   // append_previous_chat_message( recv.data.user.uid, recv.data.user.user, recv.data.product_id, recv.data.user.chat_message)
        //   main_set_dialog( recv.user.uid, recv.user.user, own_products );
        //   main_chat_user_new( recv.user.uid, recv.user.status, recv.user.user, own_products );
        // }

      }

      else if ( action == 'disconnect' ) {
        //Delete the user to chat
        //main_chat_user_delete( recv.user.uid );
        main_chat_user_offline_new( recv.user.uid, recv.user.product );
      }

      else if ( action == 'offline' ) {
        //Set offline the user in chat
        main_chat_user_offline( recv.user.uid, recv.user.product );
      }

      else if ( action == 'user_typing' ) {
        var userid = recv.data.uid;
        var main = $( "#Dialog" + product_id );

        if ( main.parent().find( "#iswriting" ).first().hasClass( "no-display") ) {
          
          main.parent().find( "#iswriting" ).first().removeClass( "no-display" );

          setTimeout(function () {
            main.parent().find( "#iswriting" ).first().addClass( "no-display" );
          }, 2000);
        }
      }

      else if ( action == 'user_status' ) {
        //TODO: if user goes to offline, set the 'popup disable'
        //TODO: if user comes from offline and is set 'popup disable', enable it
        /*if (recv.user.status == 'offline')
          main_chat_user_offline( recv.user.uid );
        else
        */
        main_chat_user_status( recv.user.uid, recv.user.status );
      }

      // Update my setting from backend
      else if ( action == 'update_settings' ) {
        // alert("update_settings");
        user_name = recv.data.name;
        user_avatar = recv.data.avatar;

        // if ( $( "#Dialog" + product_id ).length == 0 ) {
        // // alert("if");  
        // main_append_dialog( recv.data.user.uid, recv.data.user.user, recv.data.product_id );
        // main_set_dialog( recv.data.user.uid, recv.data.user.user, recv.data.product_id);
        // }
      }

      else if ( action == 'usrlist' ) {
        // console.log(JSON.stringify(recv.user.user));
        // alert("usrlist");
        for (i in recv.user) {
          // sample_f1();
          //Append the Dialogid
          // alert("recv user id: "+recv.user[i].uid);
          // alert("recv user: "+recv.user[i].user);
          // alert("recv product: "+recv.user[i].product);
          status = 'online';
          if (recv.user[i].user!=user_name){
          main_append_dialog( recv.user[i].uid, recv.user[i].user, recv.user[i].product,status);
          // append_previous_chat_message(recv.user[i].uid, recv.user[i].user, recv.user[i].product, recv.user[i].chat_message);
          main_set_dialog( recv.user[i].uid, recv.user[i].user, recv.user[i].product,status);
          // main_set_dialog( recv.user[i].uid, recv.user[i].user);

          //Append the user to chat
          main_chat_user_new( recv.user[i].uid, recv.user[i].status, recv.user[i].user, recv.user[i].product,"usrlist");
          // main_chat_user_new( recv.user[i].uid, recv.user[i].status, recv.user[i].name);
          }
          // else{
          // if ( $( "#Dialog" + own_products ).length == 0 ) {
          // // alert("if");  
          // main_append_dialog( recv.user[i].uid, recv.user[i].user, own_products);
          // // append_previous_chat_message( recv.data.user.uid, recv.data.user.user, recv.data.product_id, recv.data.user.chat_message)
          // main_set_dialog( recv.user[i].uid, recv.user[i].user, own_products);
          // main_chat_user_new( recv.user[i].uid, recv.user[i].status, recv.user[i].user, own_products );
          //  }
          // }
        }
      }

      else {
        console.log('ERROR');
      }   
      }

  }).fail(function() {
    console.log('fail');
  }).always(function() {
    function displayChatOnload() {
      document.getElementById('main').style.display = 'block';
    }

    displayChatOnload();
  });

});

// $(window).load(function() {
//  // executes when complete page is fully loaded, including all frames, objects and images
//  alert("window is loaded");
//  alert($.cookie("dialog_status"));
//  result = jQuery.parseJSON($.cookie("dialog_status"));
//  $.each(result, function(i,val){
//      $("#user-"+i +"_product-" +val).attr('class','user').trigger("click");
//     // $( "#user-button-" + iduser_product ).trigger( "click" );
// });
// });

// $(window).load(function() {
//  // executes when complete page is fully loaded, including all frames, objects and images
//  // alert("window is loaded");
//  // alert(localStorage.getItem('dialog_status'));
//  // result = jQuery.parseJSON(localStorage.getItem('dialog_status'));
//  result = eval(localStorage.getItem('dialog_status'));
//  $.each(result, function(i,val){
//     if (window.location.pathname == '/search/')
//       $("#user-"+val.user +"_product-" +val.product).attr('class','user').trigger("click");
//     else{
//      $( "#users-button-bar" ).append( "<button id='user-button-" + val.user +  "_product-" + val.product +"' class='user-button' style='font-size: 65%;'><li class='online'>" + val.name + "</li><span class='product_title' style='display:none;'>" + val.title + "</span><span class='product_id' style='display:none;'>" + val.product + "</span></button>" );
//      $( "#user-button-" + val.user +  "_product-" + val.product ).trigger( "click" );
//      }
// });
// });



// $(window).load(function() {
//  // executes when complete page is fully loaded, including all frames, objects and images
//  // alert("window is loaded");
//  // alert(localStorage.getItem('dialog_status'));
//  // result = jQuery.parseJSON(localStorage.getItem('dialog_status'));
//  if (localStorage.getItem('dialog_status')!=null){
//    result = eval(localStorage.getItem('dialog_status'));
//    $.each(result, function(i,val){
//     // alert(val.name);
//       // if (window.location.pathname == '/search/')
//       //   // $("#user-"+val.user +"_product-" +val.product).attr('class','user').trigger("click");
//       //   $( "#user-button-" + val.user +  "_product-" + val.product ).trigger( "click" );
//       // else{
//       //   if ( $( "#users-button-bar" ).parent().find( "#user-button-" + val.user +  "_product-" + val.product ).length == 0 ){
//       //     $( "#users-button-bar" ).append( "<button id='user-button-" + val.user +  "_product-" + val.product +"' class='user-button' style='font-size: 65%;'><li class='online'>" + val.name + "</li><span class='product_title' style='display:none;'>" + val.title + "</span><span class='product_id' style='display:none;'>" + val.product + "</span></button>" );
//       //     // $( ".user-button" ).button();
//       //   }
//       //  $( "#user-button-" + val.user +  "_product-" + val.product ).trigger( "click" );
//       //  }
//       if ( $( "#users-button-bar" ).parent().find( "#user-button-" + val.user +  "_product-" + val.product ).length == 0 ){
//           $( "#users-button-bar" ).append( "<button id='user-button-" + val.user +  "_product-" + val.product +"' class='user-button btn_user' style='font-size: 65%;'><li class='online'>" + val.name + "</li><span class='product_title' style='display:none;'>" + val.title + "</span><span class='product_id' style='display:none;'>" + val.product + "</span></button>" );
//           $( ".user-button" ).button();
//         }
//        $( "#user-button-" + val.user +  "_product-" + val.product ).trigger( "click" );
//   });
// }
// });

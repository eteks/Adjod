;
(function($) {
    var edit_remove_photos = "";
    $.fn.simpleFilePreview = function(o) {
        var n = this;
        if (!n || !n.length) {
            return n;
        }
        o = (o) ? o : {};
        o = $.extend({}, $.simpleFilePreview.defaults, o);
        n.each(function() {
            setup($(this), o);
        });
        if (!$.simpleFilePreview.init) {
            $.simpleFilePreview.init = true;
            $('body').on('click', '.simpleFilePreview_input', function(e) {
                $(this).parents('.simpleFilePreview').find('input.simpleFilePreview_formInput').trigger('click');
                e.preventDefault();
                return false;
            }).on('click', '.simpleFilePreview input.simpleFilePreview_formInput', function(e) {
                if ($(this).val().length) {
                    e.preventDefault();
                    $(this).parents('.simpleFilePreview').find('.simpleFilePreview_preview').click();
                    return false;
                }
            }).on('change', '.simpleFilePreview input.simpleFilePreview_formInput', function(e) {
                var file = this.files[0];
                var dataUrl = "";
                var img = document.createElement("img");
                var reader = new FileReader();
                reader.onload = function(e) {
                    img.src = e.target.result;
                    var canvas = document.createElement("canvas");
                    var ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0);
                    var MAX_WIDTH = 400;
                    var MAX_HEIGHT = 300;
                    var width = img.width;
                    var height = img.height;
                    if (width > height) {
                        if (width > MAX_WIDTH) {
                            height *= MAX_WIDTH / width;
                            width = MAX_WIDTH;
                        }
                    } else {
                        if (height > MAX_HEIGHT) {
                            width *= MAX_HEIGHT / height;
                            height = MAX_HEIGHT;
                        }
                    }
                    canvas.width = width;
                    canvas.height = height;
                    var ctx = canvas.getContext("2d");
                    ctx.drawImage(img, 0, 0, width, height);
                    dataUrl = canvas.toDataURL("image/png");
                }
                reader.readAsDataURL(file);
                var s = dataUrl.size;
                var e = getFileExt(this.value);
                if (dataUrl.length < 1000000) {
                    if ((e == null) || ($.inArray(e.toLowerCase(), ['gif', 'png', 'jpg', 'jpeg']) == -1)) {
                        $('.photo_labelError').addClass('error_input_field');
                        $('.photo_labelError').text('Invalid File Format. We allow only gif, png, jpg, jpeg').show();
                        $('.simpleFilePreview:last').append('<img class="simpleFilePreview_preview" style="display:none;">');
                    } else {
                        $('.photo_labelError').removeClass('error_input_field');
                        $('.photo_labelError').hide();
                        var p = $(this).parents('.simpleFilePreview');
                        if ($('.simpleFilePreview').children().not('.editpost_image_change')) {
                            if (p.attr('data-sfpallowmultiple') == 1 && !p.find('.simpleFilePreview_preview').length) {
                                var newId = $.simpleFilePreview.uid++;
                                var newN = p.clone(true).attr('id', "simpleFilePreview_" + newId);
                                newN.find('input.simpleFilePreview_formInput').attr('id', newN.find('input.simpleFilePreview_formInput').attr('id') + '_' + newId).val('');
                                if ($('.simpleFilePreview_multiUI').hasClass('edit_image_notavailable')) {
                                    newN.find('.simpleFilePreview_input').css('display', 'block');
                                }
                                p.after(newN);
                                var nw = p.parents('.simpleFilePreview_multi').width('+=' + newN.outerWidth(true)).width();
                                if (nw > p.parents('.simpleFilePreview_multiClip').width()) {
                                    p.parents('.simpleFilePreview_multiUI').find('.simpleFilePreview_shiftRight').click();
                                }
                            }
                        }
                        if (this.files && this.files[0]) {
                            if ((new RegExp("^image\/(" + $.simpleFilePreview.previewFileTypes + ")$")).test(this.files[0].type.toLowerCase())) {
                                if (window.FileReader) {
                                    if ((new RegExp("^image\/(" + $.simpleFilePreview.previewFileTypes + ")$")).test(this.files[0].type.toLowerCase())) {
                                        var r = new FileReader();
                                        r.onload = function(e) {
                                            addOrChangePreview(p, e.target.result);
                                        };
                                        r.readAsDataURL(this.files[0]);
                                    }
                                }
                            } else {
                                var m = this.files[0].type.toLowerCase().match(/^\s*[^\/]+\/([a-zA-Z0-9\-\.]+)\s*$/);
                                if (m && m[1] && o.icons[m[1]]) {
                                    addOrChangePreview(p, o.iconPath + o.icons[m[1]], getFilename(this.value));
                                } else {
                                    addOrChangePreview(p, o.iconPath + o.defaultIcon, getFilename(this.value));
                                }
                            }
                        } else {
                            var e = getFileExt(this.value);
                            e = (e) ? e.toLowerCase() : null;
                            if (e && !(/fakepath/.test(this.value.toLowerCase())) && (new RegExp("^(" + $.simpleFilePreview.previewFileTypes + ")$")).test(e)) {
                                addOrChangePreview(p, "file://" + this.value);
                            } else {
                                if (o.icons[e]) {
                                    addOrChangePreview(p, o.iconPath + o.icons[e], getFilename(this.value));
                                } else {
                                    addOrChangePreview(p, o.iconPath + o.defaultIcon, getFilename(this.value));
                                }
                            }
                        }
                    }
                } else {
                    $('.photo_labelError').addClass('error_input_field');
                    $('.photo_labelError').text('File size should be less than 1 MB').show();
                    var p = $(this).parents('.simpleFilePreview');
                    $('.simpleFilePreview:last').append('<img class="simpleFilePreview_preview" style="display:none;">');
                    if (p.attr('data-sfpallowmultiple') == 1 && !p.find('.simpleFilePreview_preview').length) {
                        var nw = p.parents('.simpleFilePreview_multi').width('+=' + newN.outerWidth(true)).width();
                        if (nw > p.parents('.simpleFilePreview_multiClip').width()) {
                            p.parents('.simpleFilePreview_multiUI').find('.simpleFilePreview_shiftRight').click();
                        }
                    }
                }
            }).on('mouseover', '.simpleFilePreview_preview, .simpleFilePreview input.simpleFilePreview_formInput', function() {
                var p = $(this).parents('.simpleFilePreview');
                if (p.find('.simpleFilePreview_preview').is(':visible')) {
                    p.find('.simpleFilePreview_remove').show();
                }
            }).on('mouseout', '.simpleFilePreview_preview, .simpleFilePreview input.simpleFilePreview_formInput', function() {
                $(this).parents('.simpleFilePreview').find('.simpleFilePreview_remove').hide();
            }).on('click', '.simpleFilePreview_preview', function() {
                var p = $(this).parents('.simpleFilePreview');
                if (p.attr('data-sfpallowmultiple') == 1 && p.siblings('.simpleFilePreview').length && !p.parents('#upload_photos_div').children().hasClass('error_input_field')) {
                    if (p.hasClass('simpleFilePreview_existing')) {
                        p.parent().append("<input type='hidden' id='" + p.attr('id') + "_remove' name='removeFiles[]' value='" + p.attr('data-sfprid') + "' />");
                    }
                    p.parents('.simpleFilePreview_multi').width('-=' + p.width());
                    if(edit_remove_photos == "")
                        edit_remove_photos += $(this).attr('src');
                    else
                        edit_remove_photos = edit_remove_photos + ","+ $(this).attr('src');         
                    var regex = new RegExp("/media/", 'g');
                    $('.edit_remove_photos').val(edit_remove_photos.replace(regex,""));
                    p.remove();
                } else {
                    if (p.hasClass('simpleFilePreview_existing')) {
                        p.find('input.simpleFilePreview_formInput').show();
                        p.append("<input type='hidden' id='" + p.attr('id') + "_remove' name='removeFiles[]' value='" + p.attr('data-sfprid') + "' />");
                        p.removeClass('simpleFilePreview_existing');
                    }
                    var i = p.find('input.simpleFilePreview_formInput').val('');
                    if (i && i.length && i.val().length) {
                        var attr = i.get(0).attributes;
                        var a = "";
                        for (var j = 0, l = attr.length; j < l; ++j) {
                            if (attr[j].name != 'value' && attr[j].name != 'title') {
                                a += attr[j].name + "='" + i.attr(attr[j].name) + "' ";
                            }
                        }
                        var ni = $("<input " + a + " />");
                        i.before(ni);
                        i.remove();
                    }
                    $(this).remove();
                    p.find('.simpleFilePreview_filename').remove();
                    p.find('.simpleFilePreview_remove').hide().end().find('.simpleFilePreview_input').show();
                }
            }).on('click', '.simpleFilePreview_shiftRight', function() {
                var ul = $(this).parents('.simpleFilePreview_multiUI').find('.simpleFilePreview_multi');
                var r = parseInt(ul.css('left')) + ul.width();
                if (r > ul.parent().width()) {
                    var li = ul.find('li:first');
                }
            }).on('click', '.simpleFilePreview_shiftLeft', function() {
                var ul = $(this).parents('.simpleFilePreview_multiUI').find('.simpleFilePreview_multi');
                var l = parseInt(ul.css('left'));
                if (l < 0) {
                    var w = ul.find('li:first').outerWidth(true);
                }
            });
        }
        return n;
    };
    var setup = function(n, o) {
        var isMulti = n.is('[multiple]');
        n = n.removeAttr('multiple').addClass('simpleFilePreview_formInput');
        if (window.location.href.indexOf("edit_postad_detail") <= -1) {
            var c = $("<" + ((isMulti) ? 'li' : 'div') + " id='simpleFilePreview_" + ($.simpleFilePreview.uid++) + "' class='simpleFilePreview' data-sfpallowmultiple='" + ((isMulti) ? 1 : 0) + "'>" + "<a class='simpleFilePreview_input'><span class='simpleFilePreview_inputButtonText'>" + o.buttonContent + "</span></a>" + "<span class='simpleFilePreview_remove'>" + o.removeContent + "</span>" + "</" + ((isMulti) ? 'li' : 'div') + ">");
            n.before(c);
            c.append(n);
            n.css({
                width: c.width() + 'px',
                height: c.height() + 'px'
            });
            if (isMulti) {
                c.wrap("<div class='simpleFilePreview_multiUI'><div class='simpleFilePreview_multiClip'><ul class='simpleFilePreview_multi'></ul></div></div>");
                c.parents('.simpleFilePreview_multiUI').prepend("<span class='simpleFilePreview_shiftRight simpleFilePreview_shifter'>" + o.shiftRight + "</span>").append("<span class='simpleFilePreview_shiftLeft simpleFilePreview_shifter'>" + o.shiftLeft + "</span>");
            }
            var ex = o.existingFiles;
            if (ex) {
                if (isMulti) {
                    var arr = ($.isArray(ex)) ? 1 : 0;
                    for (var i in ex) {
                        var ni = $.simpleFilePreview.uid++;
                        var nn = c.clone(true).attr('id', "simpleFilePreview_" + ni);
                        nn.addClass('simpleFilePreview_existing').attr('data-sfprid', (arr) ? ex[i] : i).find('input.simpleFilePreview_formInput').remove();
                        c.before(nn);
                        var e = getFileExt(ex[i]);
                        e = (e) ? e.toLowerCase() : null;
                        if (e && (new RegExp("^(" + $.simpleFilePreview.previewFileTypes + ")$")).test(e)) {
                            addOrChangePreview(nn, ex[i]);
                        } else if (o.icons[e]) {
                            addOrChangePreview(nn, o.iconPath + o.icons[e], getFilename(ex[i]));
                        } else {
                            addOrChangePreview(nn, o.iconPath + o.defaultIcon, getFilename(ex[i]));
                        }
                    }
                } else {
                    var f = null;
                    var arr = ($.isArray(ex)) ? 1 : 0;
                    for (var i in ex) {
                        f = {
                            id: (arr) ? ex[i] : i,
                            file: ex[i]
                        };
                    }
                    if (f) {
                        c.attr('data-sfprid', f['id']).addClass('simpleFilePreview_existing').find('input.simpleFilePreview_formInput').hide();
                        var e = getFileExt(f['file']);
                        e = (e) ? e.toLowerCase() : null;
                        if (e && (new RegExp("^(" + $.simpleFilePreview.previewFileTypes + ")$")).test(e)) {
                            addOrChangePreview(c, f['file']);
                        } else if (o.icons[e]) {
                            addOrChangePreview(c, o.iconPath + o.icons[e], getFilename(f['file']));
                        } else {
                            addOrChangePreview(c, o.iconPath + o.defaultIcon, getFilename(f['file']));
                        }
                    }
                }
            }
            if (isMulti) {
                $('.simpleFilePreview_multi').width(c.outerWidth(true) * c.parent().find('.simpleFilePreview').length);
            }
        }
    };
    var addOrChangePreview = function(p, src, fn) {
        fn = (fn) ? ("" + fn) : null;
        p.find('.simpleFilePreview_input').hide();
        var i = p.find('.simpleFilePreview_preview');
        if (i && i.length) {
            i.attr('src', src);
        } else {
            p.append("<img src='" + src + "' class='simpleFilePreview_preview " + ((fn) ? 'simpleFilePreview_hasFilename' : '') + "' alt='" + ((fn) ? fn : 'File Preview') + "' title='Remove " + ((fn) ? fn : 'this file') + "' />");
            p.find('input.simpleFilePreview_formInput').attr('title', "Remove " + ((fn) ? fn : 'this file'));
            $('.simpleFilePreview').css('background-color', '#ffffff !important');
            $('.default_photo,.post_image_change').hide();
        }
        if (fn) {
            var f = p.find('.simpleFilePreview_filename');
            if (f && f.length) {
                f.text(fn);
            } else {
                f = p.append("<span class='simpleFilePreview_filename'>" + fn + "</span>").find('.simpleFilePreview_filename');
            }
        }
    };
    var getFilename = function(p) {
        var m = p.match(/[\/\\]([^\/\\]+)$/);
        if (m && m[1] && m[1].length) {
            return m[1];
        }
        return null;
    };
    var getFileExt = function(p) {
        var m = p.match(/[\.]([^\/\\\.]+)$/);
        if (m && m[1] && m[1].length) {
            return m[1];
        }
        return null;
    };
    $.simpleFilePreview = {
        defaults: {
            'buttonContent': 'Add File',
            'removeContent': 'X',
            'existingFiles': null,
            'shiftLeft': '&lt;&lt;',
            'shiftRight': '&gt;&gt;',
            'iconPath': '',
            'defaultIcon': 'preview_file.png',
            'icons': {
                'png': 'preview_png.png',
                'gif': 'preview_png.png',
                'bmp': 'preview_png.png',
                'svg': 'preview_png.png',
                'jpg': 'preview_png.png',
                'jpeg': 'preview_png.png',
                'pjpg': 'preview_png.png',
                'pjpeg': 'preview_png.png',
                'tif': 'preview_png.png',
                'tiff': 'preview_png.png',
                'mp3': '../static/img/preview_mp3.png',
                'mp4': '../static/img/preview_mp3.png',
                'wav': 'preview_mp3.png',
                'wma': 'preview_mp3.png',
                'pdf': 'preview_pdf.png',
                'txt': 'preview_txt.png',
                'rtf': 'preview_txt.png',
                'text': 'preview_txt.png',
                'plain': 'preview_txt.png',
                'zip': 'preview_zip.png',
                'tgz': 'preview_zip.png',
                'x-rar-compressed': 'preview_zip.png',
                'octet-stream': 'preview_zip.png',
                'odf': 'preview_doc.png',
                'odt': 'preview_doc.png',
                'doc': 'preview_doc.png',
                'msword': 'preview_doc.png',
                'vnd.openxmlformats-officedocument.wordprocessingml.document': 'preview_doc.png',
                'doc': 'preview_doc.png',
                'docx': 'preview_doc.png',
                'ods': 'preview_xls.png',
                'vnd.ms-excel': 'preview_xls.png',
                'xls': 'preview_xls.png',
                'xlx': 'preview_xls.png',
                'msexcel': 'preview_xls.png',
                'x-excel': 'preview_xls.png',
                'x-ms-excel': 'preview_xls.png',
                'vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'preview_xls.png'
            }
        },
        uid: 0,
        init: false,
        previewFileTypes: 'p?jpe?g|png|gif'
    };
})(jQuery);
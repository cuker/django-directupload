function getCookie(c_name) //TODO possibly replace with the jquery cookie plugin
{
    var i,x,y,ARRcookies=document.cookie.split(";");
    for (i=0;i<ARRcookies.length;i++)
    {
      x=ARRcookies[i].substr(0,ARRcookies[i].indexOf("="));
      y=ARRcookies[i].substr(ARRcookies[i].indexOf("=")+1);
      x=x.replace(/^\s+|\s+$/g,"");
      if (x==c_name)
      {
        return unescape(y);
      }
    }
}

function add_csrf(jqXHR, settings) {
    jqXHR.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
}

function make_file_fields_dynamic($, options_url, determine_name_url) {
    function get_form(file) {
        return $('#'+file.id).parents('form:first')
    }
    
    function init_form(form) {
        form = form || get_form(this);
        if (form.data('uploadify_init')) {
            return
        }
        form.data('pending_uploads', {});
        form.data('submit', false);
        form.submit(function() {
            if ($.isEmptyObject(form.data('pending_uploads'))) {
                form.find('.uploadify').replaceWith(function() {
                    var path = $(this).data('path')
                    if (path) {
                        var fname = $(this).attr('id').substr(3) //uploadify is nice enough to nuke this variable /s
                        return '<input type="hidden" name="'+fname+'" id="'+$(this).attr('id')+'" value="'+path+'"/>';
                    }
                });
                return true;
            }
            form.data('submit', true);
            return false;
        });
        form.data('uploadify_init', true);
    }
    
    
    function on_select(file) {
        
        form = get_form(this)
        if (!form.data('uploadify_init')) { //hack around
            init_form(form)
        }
        form.data('pending_uploads')[this.id] = true;
        
        //determine the target path and update post data if our backend requires
        var swfuploadify = window['uploadify_' + this.id];
        var upload_to = $(document).data('uploadify-directories')[this.id];
        if (upload_to.substr(-1) != '/') {
            upload_to += '/';
        }
        
        jQuery.ajax({
            type    : 'POST',
            async   : false,
            dataType: 'json',
            url     : determine_name_url,
            beforeSend : add_csrf,
            data    : {filename: file.name,
                       upload_to: upload_to},
            success : function(data) {
                for (key in data) {
                    swfuploadify.addFileParam(file.id, key, data[key]);
                }
                $('#'+file.id).data('path', data['targetpath'])
            }
        });
    }
    
    function on_upload_success(file, data, response) {
        form = get_form(this)
        delete form.data('pending_uploads')[this.id];
        var path = $('#'+file.id).data('path');
        if (path) {
            $('#'+this.id).data('path', path);
        } else {
            $('#'+this.id).data('path', data);
        }
        if ($.isEmptyObject(form.data('pending_uploads')) && form.data('submit')) {
            form.submit();
        }
    }
    
    function on_upload_error(file,errorCode,errorMsg,errorString, queue) {
        form = get_form(this)
        delete form.data('pending_uploads')[this.id];
    }
    
    function on_upload_cancel() {
        form = get_form(this)
        delete form.data('pending_uploads')[this.id];
    }
    
    $(document).data('uploadify-directories', {})
    $('.uploadifyinput').each(function() {
        $(document).data('uploadify-directories')[$(this).attr('id')] = $(this).attr('data-upload-to');
    });
    
    $.getJSON(options_url, function(data) {
        var options = $.extend({
            'onUploadSuccess': on_upload_success,
            'onSelect': on_select,
            'onUploadError': on_upload_error,
            'onUploadCancel': on_upload_cancel,
            'auto': true,
            'multi': false,
            'removeCompleted': false,
            'uploadLimit': 1
        }, data);
        $('.uploadifyinput').uploadify(options);
    });
}



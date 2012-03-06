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

function make_file_fields_dynamic($, selector, options_url, determine_name_url) {
    function get_form(item) {
        return $(item).parents('form:first')
    }
    
    function init_form(form) {
        if (form.data('uploadify_init')) {
            return
        }
        form.data('pending_uploads', {});
        form.data('submit', false);
        form.submit(function() {
            if ($.isEmptyObject(form.data('pending_uploads'))) {
                form.find(':input').filter(selector).replaceWith(function() {
                    var path = $(this).data('path')
                    if (path) {
                        var fname = $(this).attr('id').substr(3) //uploadify is nice enough to nuke this variable /s
                        return '<input type="hidden" name="'+fname+'" id="'+$(this).attr('id')+'" value="'+path+'"/>';
                    } else {
                        return $(this);
                    }
                });
                return true;
            }
            form.data('submit', true);
            return false;
        });
        form.data('uploadify_init', true);
    }
    
    
    function add(event, data) {
        //console.log(event, data)
        var file = data.files[0];
        var id = $(this).attr('id');
        var options = event.data.fileupload.options;
        form = get_form(this)
        if (!form.data('uploadify_init')) { //hack around
            init_form(form)
        }
        form.data('pending_uploads')[id] = true;
        
        //determine the target path and update post data if our backend requires
        var upload_to = $(event.currentTarget).attr('data-upload-to') || '';
        if (upload_to.substr(-1) != '/') {
            upload_to += '/';
        }
        
        $('#'+id).siblings('.uploadstatus').remove()
        $('#'+id).after('<span class="uploadstatus">Uploading: '+file.name+'</span>')
        
        jQuery.ajax({
            type    : 'POST',
            //async   : false,
            dataType: 'json',
            url     : determine_name_url,
            beforeSend : add_csrf,
            data    : {filename: file.name,
                       upload_to: upload_to},
            success : function(post_data) {
                data.formData = post_data;
                data.fileInput.attr('name', options.fileObjName);
                file.path = post_data['targetpath'];
                data.submit();
            }
        });
    }
    
    function done(event, data) {
        var id = $(this).attr('id')
        var file = data.files[0];
        
        form = get_form(this)
        delete form.data('pending_uploads')[id];
        $('#'+id).data('path', file.path);
        $('#'+id).siblings('.uploadstatus').remove()
        $('#'+id).after('<span class="uploadstatus">File uploaded: '+file.name+'</span>')
        if ($.isEmptyObject(form.data('pending_uploads')) && form.data('submit')) {
            form.submit();
        }
    }
    
    function fail(e, data) {
        var id = $(this).attr('id')
        var file = data.files[0];
        delete form.data('pending_uploads')[id];
        console.log('fail');
        console.log([e, data]);
    }
    
    $(document).data('uploadify-directories', {})
    $(selector).each(function() { //may not be necessary
        $(document).data('uploadify-directories')[$(this).attr('id')] = $(this).attr('data-upload-to');
    });
    
    $.getJSON(options_url, function(data) {
        var options = $.extend({
            //'onUploadSuccess': on_upload_success,
            'add': add,
            'fail': fail,
            'done': done,
            //'onUploadError': on_upload_error,
            //'onUploadCancel': on_upload_cancel,
            'autoUpload': true,
            'multi': false,
            //'removeCompleted': false,
            //'uploadLimit': 1,
            'async': true,
            'type': 'POST'
        }, data);
        $(selector).fileupload(options);
    });
}



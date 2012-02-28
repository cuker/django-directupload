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

function make_file_fields_dynamic($, options_url) {
    $('.uploadifyinput').each(function() {
        var $this = $(this);
        var form = $this.parents('form');
        var upload_to = $this.attr('data-upload-to');
        if (upload_to.substr(-1) != '/') {
            upload_to += '/';
        }
        //TODO if upload_to has already been seen, don't hit the wire
        $.ajax({
            type    : 'POST',
            dataType: 'json',
            url     : options_url,
            data    : {'upload_to': upload_to},
            beforeSend : add_csrf,
            success : function(data) {
                var options = data;
                
                function init_form() {
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
                
                function on_upload_success(file, data, response) {
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
                
                function on_select(file) {
                    if (!form.data('uploadify_init')) { //hack around
                        init_form()
                    }
                    form.data('pending_uploads')[this.id] = true;
                    
                    //determine the target path and update post data if our backend requires
                    var swfuploadify = window['uploadify_' + this.id];
                    if (swfuploadify.settings.determineName) {
                        jQuery.ajax({
                            type    : 'POST',
                            async   : false,
                            dataType: 'json',
                            url     : swfuploadify.settings.determineName,
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
                    } else {
                        //swfuploadify.addFileParam(file.id, 'targetname', file.name);
                    }
                }
                
                function on_upload_error(file,errorCode,errorMsg,errorString, queue) {
                    delete form.data('pending_uploads')[this.id];
                }
                
                function on_upload_cancel() {
                    delete form.data('pending_uploads')[this.id];
                }
                
                options['onUploadSuccess'] = on_upload_success;
                options['onSelect'] = on_select;
                //options['onUploadStart'] = on_upload_start;
                options['onUploadError'] = on_upload_error;
                options['onUploadCancel'] = on_upload_cancel;
                options['onSWFReady'] = init_form; //this may not work
                /* Uploadify Setup */
                options['auto'] = true;
                options['multi'] = false;
                options['removeCompleted'] = false;
                options['uploadLimit'] = 1;
                $this.uploadify(options);
            }
        });
    });
}



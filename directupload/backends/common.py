from django.conf import settings

UPLOADIFY_OPTIONS = ('auto', 'buttonImg', 'buttonText', 'cancelImg', 'checkScript', 'displayData', 'expressInstall', 'fileDataName', 'fileDesc', 'fileExt', 'folder', 'height', 'hideButton', 'method', 'multi', 'queueID', 'queueSizeLimit', 'removeCompleted', 'rollover', 'script','scriptAccess', 'scriptData', 'simUploadLimit', 'sizeLimit', 'uploader', 'width', 'wmode')

UPLOADIFY_METHODS = ('onAllComplete', 'onCancel', 'onCheck', 'onClearQueue', 'onComplete', 'onError', 'onInit', 'onOpen', 'onProgress', 'onQueueFull', 'onSelect', 'onSelectOnce', 'onSWFReady')

BUTTON_TEXT = 'Select File'

# Defaults for required Uploadify options
DEFAULT_CANCELIMG = settings.STATIC_URL + "uploadify/uploadify-cancel.png"
DEFAULT_UPLOADER  = settings.STATIC_URL + "uploadify/uploadify.swf"

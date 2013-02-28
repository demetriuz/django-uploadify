from django import template
from django.template import resolve_variable
from django.utils import simplejson
from django.utils.safestring import mark_safe

from uploadify import settings

register = template.Library()

# -----------------------------------------------------------------------------
#   multi_file_upload
# -----------------------------------------------------------------------------
class MultiFileUpload(template.Node):
    def __init__(self, sender='"uploadify"', unique_id=None, data=None, **kwargs):
        self.sender = sender
        self.unique_id = unique_id
        self.data = data or {}
        self.options = kwargs
       
    def render(self, context):

        if self.unique_id is not None:
            unique_id = "?unique_id=%s" % str(resolve_variable(self.unique_id, context))
        else:
            unique_id = ""

        options = {'fileObjName': mark_safe('"Filedata"')}
        for key, value in self.options.items():
            options[key] = mark_safe(value)


        # js_options = options

        auto = options.get('auto', False)
        
        data = {
            'fileObjName': options['fileObjName'],
            'sender': mark_safe(str(resolve_variable(self.sender, context))),
        }
        for key, value in self.data.items():
            data[key] = resolve_variable(value, context)

        context.update({
            'uploadify_query': unique_id,
            'uploadify_data': data,
            'uploadify_path': settings.UPLOADIFY_PATH,
            'uploadify_version': settings.UPLOADIFY_VERSION,
            'uploadify_options': options,
            'uploadify_filename': options['fileObjName'],
            'uploadify_auto': auto,
        })

        t = template.loader.get_template('uploadify/multi_file_upload.html')
        return t.render(context)


@register.tag
def multi_file_upload(parser, token):
    """
    Displays a Flash-based interface for uploading multiple files.
    For each POST request (after file upload) send GET query with `unique_id`.

    {% multi_file_upload sender='SomeThing' fileObjName='"Filename"' %}

    For all options see http://www.uploadify.com/documentation/

    """
    args = token.split_contents()
    tag_name = args[0]
    args = args[1:]

    options = {}
    for arg in args:
        name, val = arg.split("=")
        if val[0] in ["'", '"']:
            val = val[1:]
        if val[-1] in ["'", '"']:
            val = val[:-1]
        options[name] = val

    return MultiFileUpload(**options)

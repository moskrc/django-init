# -*- coding: utf-8 -*-
from django.conf import settings

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
import os
# import Image
from sorl.thumbnail import get_thumbnail
def thumbnail(image_path):
    im = get_thumbnail(image_path, '200x200', crop='center', quality=99)

    return u'<img src="%s" alt="%s" />' % (im.url, image_path)


class ImageFieldWidget(AdminFileWidget):
    pass
    # template_with_initial = u'<br/>%(initial_text)s: %(initial)s %(clear_template)s<br/> %(input_text)s: %(input)s'
    # template_with_clear = u'<br/><label class="clearable_field" for="%(clear_checkbox_id)s">%(clear_checkbox_label)s: &nbsp; %(clear)s </label> '
    #
    # def render(self, name, value, attrs=None):
    #     output = []
    #     file_name = str(value)
    #     if file_name:
    #         file_path = '%s%s' % (settings.MEDIA_URL, file_name)
    #         try:            # is image
    #             Image.open(os.path.join(settings.MEDIA_ROOT, file_name))
    #             output.append('<a target="_blank" href="%s">%s</a>' % (file_path, thumbnail(file_name),))
    #         except IOError:  # not image
    #             pass
    #     output.append(super(AdminFileWidget, self).render(name, value, attrs))
    #     return mark_safe(u''.join(output))



from crispy_forms.layout import Field
from django import forms
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe

class TreeSelect(forms.Select):
    """
    Represent a tree like select
    """
    def __init__(self, tree, disabled_depth, attrs=None):
        self.tree = tree
        self.disabled_depth = disabled_depth
        super(TreeSelect, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select%s>' % flatatt(final_attrs)]
        options = self.render_options(self.tree, self.disabled_depth, [value])
        if options:
            output.append(options)
        output.append(u'</select>')
        return mark_safe(u'\n'.join(output))

    def render_options(self, tree, disabled_depth, selected_choices):
        def render_option(obj):
            option_value = force_unicode(obj.id)
            option_label = '%s%s' % ('- '*obj.depth, obj.__unicode__())
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            disabled_html = u' disabled="disabled"' if obj.depth <= disabled_depth else u''
            return u'<option value="%s"%s>%s%s</option>' % (escape(option_value), selected_html, disabled_html, conditional_escape(force_unicode(option_label)))

        selected_choices = set([force_unicode(v) for v in selected_choices])
        empty_opt = u'<option value="">%s</option>' % ('-' * 10,)
        output = [empty_opt,]

        for obj in tree:
            output.append(render_option(obj))

        return u'\n'.join(output)



class ModelTreeChoiceField(forms.ModelChoiceField):
    """
    This field represent a tree like select
    """
    def __init__(self, model, disabled_depth=None, query_set=None, *args, **kwargs):
        if not query_set:
            query_set = model.objects.all()
        tree = model.objects.get_tree(query_set)
        widget = TreeSelect(tree=tree, disabled_depth=disabled_depth)
        super(ModelTreeChoiceField, self).__init__(widget=widget, queryset=query_set, *args, **kwargs)


# ---------------

class MultipleTreeSelect(forms.SelectMultiple):
    """
    Represent a tree like select
    """
    def __init__(self, tree, disabled_depth, attrs=None):
        self.tree = tree
        self.disabled_depth = disabled_depth
        super(MultipleTreeSelect, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [u'<select multiple="multiple"%s>' % flatatt(final_attrs)]
        options = self.render_options(self.tree, self.disabled_depth, value)
        if options:
            output.append(options)
        output.append('</select>')
        return mark_safe(u'\n'.join(output))

    def render_options(self, tree, disabled_depth, selected_choices):
        def render_option(obj):
            option_value = force_unicode(obj.id)
            option_label = '%s%s' % ('- '*obj.depth, obj.__unicode__())
            selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
            disabled_html = u' disabled="disabled"' if obj.depth <= disabled_depth else u''
            return u'<option value="%s"%s>%s%s</option>' % (escape(option_value), selected_html, disabled_html, conditional_escape(force_unicode(option_label)))

        selected_choices = set([force_unicode(v) for v in selected_choices])

        output = []

        for obj in tree:
            output.append(render_option(obj))

        return u'\n'.join(output)



class MultipleModelTreeChoiceField(forms.ModelMultipleChoiceField):
    """
    This field represent a tree like select
    """
    def __init__(self, model, disabled_depth=None, query_set=None, *args, **kwargs):
        if not query_set:
            query_set = model.objects.all()
        tree = model.objects.get_tree(query_set)
        widget = MultipleTreeSelect(tree=tree, disabled_depth=disabled_depth,attrs={'style':'height:200px;'})
        super(MultipleModelTreeChoiceField, self).__init__(widget=widget, queryset=query_set, *args, **kwargs)


class ImagePreviewField(Field):
    template = "templates/image_preview_field.html"

# -*- coding: utf-8 -*-
import random
from django import forms
from django.db import models
from django.forms.util import flatatt
from django.utils.encoding import smart_unicode, force_unicode
from django.utils.hashcompat import sha_constructor
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
import os
import sys
# import Image
import random
from django.utils.hashcompat import sha_constructor
import random
from django.utils.hashcompat import sha_constructor

def get_class(class_string):
    """
    Convert a string version of a function name to the callable object.
    """
    try:
        class_string = class_string.encode('ascii')
        mod_name, class_name = get_mod_func(class_string)
        if class_name != '':
            cls = getattr(__import__(mod_name, {}, {}, ['']), class_name)
            return cls
    except (ImportError, AttributeError):
        pass
    raise ImportError('Failed to import %s' % class_string)


def get_mod_func(class_string):
    """
    Converts 'django.views.news.stories.story_detail' to
    ('django.views.news.stories', 'story_detail')

    Taken from django.core.urlresolvers
    """
    try:
        dot = class_string.rindex('.')
    except ValueError:
        return class_string, ''
    return class_string[:dot], class_string[dot + 1:]


def make_uniq_key(noise='owiesdfhlsakdjbfweiursdflajkfhqwexcv'):
    salt = sha_constructor(str(random.random())).hexdigest()[:5]
    activation_key = sha_constructor(salt+noise).hexdigest()
    return activation_key



#############################
### REC BEGIN
#############################

def dfs(node, all_nodes, depth):
    """
    Performs a recursive depth-first search starting at ``node``.  This function
    also annotates an attribute, ``depth``, which is an integer that represents
    how deeply nested this node is away from the original object.
    """
    deep_factor = 2 # how much we are deepen
    node.depth = depth
    to_return = [node,]
    for subnode in all_nodes:
        if subnode.parent and subnode.parent.id == node.id:
            to_return.extend(dfs(subnode, all_nodes, depth+deep_factor))
    return to_return

class ActiveManager(models.Manager):
    """An extended manager to return active objects."""
    def active(self):
        return self.filter(is_active=True)

class RecursiveManager(ActiveManager):
    def get_tree(self, queryset=None):
        if not queryset:
            queryset = self.select_related().iterator()
        queryset = list(queryset)
        to_return = []
        for chain in queryset:
            if not chain.parent:
                to_return.extend(dfs(chain, queryset, 0))
        return to_return


class RecursiveItem(models.Model):
    parent = models.ForeignKey('self',null=True, blank=True,related_name='child',verbose_name=u'Родительский элемент')
    is_active = models.BooleanField(default=True, verbose_name=u'Активна')

    objects = RecursiveManager()
    
    class Meta:
        abstract = True

    def _recurse_for_parents(self, cat_obj):
        p_list = []
        if cat_obj.parent_id:
            p = cat_obj.parent
            p_list.append(p)
            if p != self:
                more = self._recurse_for_parents(p)
                p_list.extend(more)
        if cat_obj == self and p_list:
            p_list.reverse()
        return p_list

    def parents(self):
        """ Category parents """
        return self._recurse_for_parents(self)


    def _flatten(self, L):
        if type(L) != type([]): return [L]
        if L == []: return L
        return self._flatten(L[0]) + self._flatten(L[1:])

    def _recurse_for_children(self, node, only_active=False):
        children = []
        children.append(node)
        for child in node.child.active():
            if child != self:
                if (not only_active):
                    children_list = self._recurse_for_children(child, only_active=only_active)
                    children.append(children_list)
        return children

    def get_active_children(self, include_self=False):
        return self.get_all_children(only_active=True, include_self=include_self)

    def get_all_children(self, only_active=False, include_self=False):
        """
        Gets a list of all of the children categories.
        """
        children_list = self._recurse_for_children(self, only_active=only_active)
        if include_self:
            ix = 0
        else:
            ix = 1
        flat_list = self._flatten(children_list[ix:])
        return flat_list


    def full_path(self):
        if self.parents():
            return ' :: '.join([p.title for p in self.parents()])+' :: '+self.title
        else:
            return self.title

    def level(self):
        return len(self.parents())

#############################
### REC END
#############################



def make_uniq_key(noise='owiesdfhlsakdjbfweiursdflajkfhqwexcv'):
    salt = sha_constructor(str(random.random())).hexdigest()[:5]
    activation_key = sha_constructor(salt+noise).hexdigest()
    return activation_key

def check_censored(word):
    word = smart_unicode(word)
    import re
    patterns = [
         u'\w{0,5}[хx]([хx\s\!@#\$%\^&*+-\|\/]{0,6})[уy]([уy\s\!@#\$%\^&*+-\|\/]{0,6})[ёiлeеюийя]\w{0,7}|\w{0,6}[пp]([пp\s\!@#\$%\^&*+-\|\/]{0,6})[iие]([iие\s\!@#\$%\^&*+-\|\/]{0,6})[3зс]([3зс\s\!@#\$%\^&*+-\|\/]{0,6})[дd]\w{0,10}|[сcs][уy]([уy\!@#\$%\^&*+-\|\/]{0,6})[4чkк]\w{1,3}|\w{0,4}[bб]([bб\s\!@#\$%\^&*+-\|\/]{0,6})[lл]([lл\s\!@#\$%\^&*+-\|\/]{0,6})[yя]\w{0,10}|\w{0,8}[её][bб][лске@eыиаa][наи@йвл]\w{0,8}|\w{0,4}[еe]([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})[uу]([uу\s\!@#\$%\^&*+-\|\/]{0,6})[н4ч]\w{0,4}|\w{0,4}[еeё]([еeё\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})[нn]([нn\s\!@#\$%\^&*+-\|\/]{0,6})[уy]\w{0,4}|\w{0,4}[еe]([еe\s\!@#\$%\^&*+-\|\/]{0,6})[бb]([бb\s\!@#\$%\^&*+-\|\/]{0,6})[оoаa@]([оoаa@\s\!@#\$%\^&*+-\|\/]{0,6})[тnнt]\w{0,4}|\w{0,10}[ё]([ё\!@#\$%\^&*+-\|\/]{0,6})[б]\w{0,6}|\w{0,4}[pп]([pп\s\!@#\$%\^&*+-\|\/]{0,6})[иeеi]([иeеi\s\!@#\$%\^&*+-\|\/]{0,6})[дd]([дd\s\!@#\$%\^&*+-\|\/]{0,6})[oоаa@еeиi]([oоаa@еeиi\s\!@#\$%\^&*+-\|\/]{0,6})[рr]\w{0,12}',
         u'((х|x)(у|y)(й|е|ё|и|я|ли\W|э))',
         u'(п(и|е|ё)(з|с)д)', 
         u'(\Wу?би?л(я\W|яд|ят|юдо?к))', 
         u'(пид(о|а)р|п(е|и)дри)',
         u'(муд(ак|о|и))',
         u'((\W|по|на)(х|x)(е|e)(р|p))',
         u'(з(а|о)луп(а|и))',
         u'((\W|о|д|а|ь|ъ)(е|ё|и)б(а|ы|уч|усь|нут|ись))',
         u'(\W(на|по)х\W)',
         u'(pizd)',
         u'(sosi)',
         u'(су(ка|чк|ки|чь))',
         u'(др(оч|ачи))',
         u'((\W|о|за)трах)',
         u'(к(а|о)зе?ё?л)',
         u'(п(е|ё)р(н|д)(и\W|иc|ы|у))',
         u'(урод)',
         u'(ебан)',
         u'(ебал)',
         u'(еблан)',
         u'(недонос)',
         u'(недоумок)',
         u'(придур)',
         u'(дебил)',
         u'(urod)'     
         ]
    
    for p in patterns:
        if re.findall(p,word,re.IGNORECASE|re.UNICODE):
            return False
    
    return True

# def fit(file_path, max_width, max_height):
#     """Resize file (located on file path) to maximum dimensions proportionally.
#     At least one of max_width and max_height must be not None."""
#     if not (max_width or max_height):
#         # Can't resize
#         return
#     img = Image.open(file_path)
#     w, h = img.size
#     w = int(max_width or w)
#     h = int(max_height or h)
#     img.thumbnail((w, h), Image.ANTIALIAS)
#     img.save(file_path)

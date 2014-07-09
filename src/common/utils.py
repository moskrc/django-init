# -*- coding: utf-8 -*-
import hashlib
import random


def make_uniq_key(noise='owiesdfhlsakdjbfweiursdflajkfhqwexcv'):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    uniq_key = hashlib.sha1(salt + noise).hexdigest()
    return uniq_key


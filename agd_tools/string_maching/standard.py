# -*- coding: utf-8 -*-
"""
Define the class to standardize a string

Created on Thu Oct 29 20:35:59 2015

@author: Alexis
"""

import re

## travaux sur les nombres
#TODO: replace "," by "."
#TODO: remove space between thousands and units

def _remove_last_0(matchobj):
    if isinstance(matchobj, str):
        float_string = matchobj
    else:
        float_string = matchobj.group(0)

    assert isinstance(float(float_string), float) #works if float_string is '0'
    if '.' not in float_string:
        return float_string
    else:
        nb_zeros_to_remove = 0
        for k in float_string[::-1]:
            if k == '0':
                nb_zeros_to_remove += 1
            elif k == '.':
                nb_zeros_to_remove += 1
                break
            else:
                break
        if nb_zeros_to_remove == 0:
            return float_string
        else:
            return float_string[:-nb_zeros_to_remove]


def _zero_apres_la_virgule(chaine):
    return re.sub('\d*\.?\d+', _remove_last_0, chaine)


def _arrondi(chaine, ndigits):

    def __arrondi(matchobj):
        float_string = matchobj.group(0)
        arrondi = round(float(float_string), ndigits)
        if ndigits <= 0:
            arrondi = int(arrondi)
        return str(arrondi)

    return re.sub('\d*\.?\d+', __arrondi, chaine)


class StandardizedFormat(object):
    ''' classe qui définit un standard
        Remarque : l'encoding doit être géré en amont '''

    def __init__(self, dico = {}, lower = False):
        self.dico = dico
        self.lower = lower


    def run(self, string):
        if self.lower:
            string = string.lower()
        return string


if __name__ == '__main__':
    assert _remove_last_0('1.230400') == '1.2304'
    assert _remove_last_0('1.000') == '1'
    _zero_apres_la_virgule('on essaye avec 1.000 et avec 1.230400fin')
    assert _arrondi('123.456', 2) == '123.46'
    assert _arrondi('123.456', 0) == '123'
    assert _arrondi('123.456', -2) == '100'

    standard = StandardizedFormat(lower = True)
    assert standard.run('AbC12é') == 'abc12é'


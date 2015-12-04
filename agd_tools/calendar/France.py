# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 13:58:17 2015

Calendrier utile en France
On pourrait ajouter beaucoup de chose

@author: Flo, Alexis
"""

from agd_tools.calendar.periods import AnnualDay, MultiPeriod

Premier_Janvier = AnnualDay('nouvel_an', 1,1)
Premier_Mai = AnnualDay('premier_mai', 1,5)
Huit_Mai = AnnualDay('huit_mai', 8,5)
Lundi_de_Paques = MultiPeriod('lundi_paques', ['2012-04-09', '2013-04-01', '2014-04-21', '2015-04-06'])
Jeudi_Ascension = MultiPeriod('jeudi_ascension', ['2012-05-17', '2013-05-19', '2014-05-29', '2015-05-14'])
Lundi_Pentecote = MultiPeriod('lundi_pentecote', ['2012-05-28', '2013-05-20', '2014-05-29', '2015-05-25'])
Quatorze_Juillet = AnnualDay('fete_nat', 14,7)
Assomption = AnnualDay('assomption', 15,8)
Tousaint = AnnualDay('toussaint', 1,11)
Onze_Novembre = AnnualDay('onze_novembre', 11,11)
Noel = AnnualDay('noel', 25,12)
Fete_Musique = AnnualDay('fete_musique', 21,6)
Nuit_Blanche = None # TODO:

# --  Données calendaires : 2012, 2013 et 2014 / vacances zone C
vac_toussaint = MultiPeriod('vac_toussaint',
                            [('2011-10-22','2011-11-02'),
                             ('2012-10-27','2012-11-07'),
                             ('2013-10-19','2013-11-04'),
                             ('2014-10-18','2014-11-03')],
                             zone = "zone C")
vac_noel = MultiPeriod('vac_noel',
                       [('2011-12-17','2012-01-02'),
                        ('2012-12-22','2013-01-06'),
                        ('2013-12-21','2014-01-06'),
                        ('2014-12-20','2015-01-05')],
                       zone = "zone C")
vac_hiver = MultiPeriod('vac_hiver',
                        [('2012-02-18','2012-03-04'),
                         ('2013-03-02','2013-03-17'),
                         ('2014-02-15','2014-03-03'),
                         ('2015-02-21','2015-03-09')],
                        zone = "zone C")
vac_printemps = MultiPeriod('vac_printemps',
                            [('2012-04-14','2012-04-29'),
                             ('2013-04-27','2013-05-12'),
                             ('2014-04-12','2014-04-28'),
                             ('2015-04-25','2015-05-11')],
                            zone = "zone C")
vac_ete = MultiPeriod('vac_ete',
                      [('2012-07-05','2012-09-03'),
                       ('2013-07-04','2014-09-03'),
                       ('2014-07-05','2015-09-02'),
                       ('2015-07-03','2015-09-01')
                       ],
                       zone = "zone C")
#!/usr/bin/env python
# -*- coding:utf-8 -*

from pdf2meta import *
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)
logging.getLogger('pdfminer').setLevel(logging.ERROR)

parser = PdfParser()

#Accusé de reception de commande
arc = Document('ARC', 'titre')
arc.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Commandé par : (?P<client_cde>\d+)$')
arc.add_pattern('titre', r'CONFIRMATION DE LA COMMANDE N°(?P<cde_no>\d+) Du  (?P<date_arc>\d{2}/\d{2}/\d{4})')
arc.add_pattern('ref_client', r'Votre réf.: (?P<ref_client>\w*)\s*\|$')
arc.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
parser.add_document(arc)

#Bon de livraison
bl = Document('BL', 'titre')
bl.add_pattern('titre',r'^BORDEREAU DE LIVRAISON N°\s*(?P<no_bl>\d+)\s*du\s*(?P<date_bl>\d{2}/\d{2}/\d{4})$')
bl.add_pattern('destinaire',r'DESTINATAIRE :\s+(?P<destinataire>\d+)')
bl.add_pattern('date_liv',r'^\s*LIVRAISON LE\s*(?P<date_liv>\d{2}/\d{2}/\d{4})$')
parser.add_document(bl)

#Bon de commande d'achat
cde_achat = Document('CDE_ACHAT', 'titre')
cde_achat.add_pattern('titre',r'^BON DE COMMANDE$')
cde_achat.add_pattern('no', r'^\|\sN°\s*(?P<cde_achat_no>\d*)\sdu\s(?P<date_cde>\d{2}/\d{2}/\d{4})\s*\|$')
cde_achat.add_pattern('fournisseur',r'\s+Commandé à\s+:\s+(?P<fournisseur>\d*)')
cde_achat.add_pattern('total_ht', r'\|\s+Total H.T.\s+(?P<total_ht>\d*,\d*)\s*\|')
parser.add_document(cde_achat)

results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\AD20201106155156.pdf')
print(results)
results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\pblive012020072459470.pdf')
print(results)
results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\pecdea012020070252474.pdf')
print(results)

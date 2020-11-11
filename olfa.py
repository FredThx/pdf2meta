#!/usr/bin/env python
# -*- coding:utf-8 -*

from pdf2meta import *
from FUTIL.my_logging import *

my_logging(console_level = DEBUG, logfile_level = INFO, details = True)


parser = PdfParser()

#Accusé de reception de commande
arc = Document('ARC', 'titre')
arc.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Commandé par : (?P<client_cde>\d+)$')
arc.add_pattern('titre', r'CONFIRMATION DE LA COMMANDE N°(?P<cde_no>\d+) Du  (?P<date_arc>\d{2}/\d{2}/\d{4})')
arc.add_pattern('ref_client', r'Votre réf.: (?P<ref_client>\w*)\s*\|$')
arc.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
arc.add_metadata('Title', "ARC Cde n°{cde_no}")
arc.add_metadata('Subject', "Cde client ref:{ref_client}")
arc.add_metadata('Author', "Olfa")
arc.add_metadata('Producer', "Silver CS")
arc.add_metadata('Keywords', "{client_livre};{client_cde};{total_ht}")
parser.add_document(arc)

#proforma
proforma = Document('PROFORMA', 'titre')
proforma.add_pattern('titre',r'^\s*\|\s*PRO FORMA N°\s*(?P<no_proforma>P\d*)\s*Du\s*(?P<date_proforma>\d{2}/\d{2}/\d{4})\s*\|')
proforma.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Commandé par : (?P<client_cde>\d+)$')
proforma.add_pattern('ref_client', r'Votre réf.: (?P<ref_client>\w*)\s*\|$')
proforma.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
proforma.add_metadata('Title', "PROFORMA n°{no_proforma}")
proforma.add_metadata('Subject', "Ref client : {ref_client}")
proforma.add_metadata('Author', "Olfa")
proforma.add_metadata('Producer', "Silver CS")
proforma.add_metadata('Keywords', "{client_livre};{client_cde};{total_ht}")
parser.add_document(proforma)

#Bon de livraison
bl = Document('BL', 'titre')
bl.add_pattern('titre',r'^BORDEREAU DE LIVRAISON N°\s*(?P<no_bl>\d+)\s*du\s*(?P<date_bl>\d{2}/\d{2}/\d{4})$')
bl.add_pattern('destinaire',r'DESTINATAIRE :\s+(?P<client_livre>\d+)')
bl.add_pattern('date_liv',r'^\s*LIVRAISON LE\s*(?P<date_liv>\d{2}/\d{2}/\d{4})$')
bl.add_metadata('Title', "BL n°{no_bl}")
bl.add_metadata('Subject', "Bon de Livraison ref:{ref_client}")
bl.add_metadata('Author', "Olfa")
bl.add_metadata('Producer', "Silver CS")
bl.add_metadata('Keywords', "{client_livre};{date_bl}")
parser.add_document(bl)

#Bon de commande d'achat
cde_achat = Document('CDE_ACHAT', 'titre')
cde_achat.add_pattern('titre',r'^BON DE COMMANDE$')
cde_achat.add_pattern('no', r'^\|\sN°\s*(?P<cde_achat_no>\d*)\sdu\s(?P<date_cde>\d{2}/\d{2}/\d{4})\s*\|$')
cde_achat.add_pattern('fournisseur',r'\s+Commandé à\s+:\s+(?P<fournisseur>\d*)')
cde_achat.add_pattern('total_ht', r'\|\s+Total H.T.\s+(?P<total_ht>\d*,\d*)\s*\|')
cde_achat.add_metadata('Title', "Cde achat n°{cde_achat_no}")
cde_achat.add_metadata('Subject', "Fournisseur : {fournisseur}")
cde_achat.add_metadata('Author', "Olfa")
cde_achat.add_metadata('Producer', "Silver CS")
cde_achat.add_metadata('Keywords', "{fournisseur};{total_ht}")
parser.add_document(cde_achat)

#facture
facture = Document('FACTURE', 'titre')
facture.add_pattern('titre',r'^\s*\|\s*FACTURE N°\s*(?P<no_facture>F\d*)\s*Du\s*(?P<date_facture>\d{2}/\d{2}/\d{4})\s*\|')
facture.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Facturé à:\s+(?P<client_facture>\d+)$')
facture.add_pattern('livraison', r'^\s*Livraison N°:\s*(?P<no_bl>\d+)\s*Du\s*(?P<date_bl>\d{2}/\d{2}/\d{4})\s*Commande N°:\s*(?P<no_cde>\d+)\s*VOTRE REFERENCE: (?P<ref_client>\w*)\s*Du\s*(?P<date_cde>\d{2}/\d{2}/\d{4})')
facture.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
facture.add_metadata('Title', "FACTURE n°{no_facture}")
facture.add_metadata('Subject', "BL n°{no_bl}, Cde ,°{no_cde}")
facture.add_metadata('Author', "Olfa")
facture.add_metadata('Producer', "Silver CS")
facture.add_metadata('Keywords', "{client_livre};{client_facture};{ref_client};{date_bl}")
parser.add_document(facture)

#avoir
avoir = Document('AVOIR', 'titre')
avoir.add_pattern('titre',r'^\s*\|\s*AVOIR\s*N°\s*(?P<no_facture>A\d*)\s*Du\s*(?P<date_facture>\d{2}/\d{2}/\d{4})\s*\|')
avoir.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Facturé à:\s+(?P<client_facture>\d+)$')
avoir.add_pattern('livraison', r'^\s*Livraison N°:\s*(?P<no_bl>\d+)\s*Du\s*(?P<date_bl>\d{2}/\d{2}/\d{4})')
avoir.add_pattern('votre_ref', r'^\s*VOTRE REFERENCE:\s*(?P<ref_client>\w*)')
avoir.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
avoir.add_pattern('commentaires_facture', r'FACTURE\s*(?P<no_facture>F\d*)')
avoir.add_pattern('commentaires_qualité', r'DOSSIER QUALITE\s*(?P<no_dossier_qualite>\d{2}-\d*)')
avoir.add_metadata('Title', "AVOIR n°{no_facture}")
avoir.add_metadata('Subject', "BL n°{no_bl}")
avoir.add_metadata('Author', "Olfa")
avoir.add_metadata('Producer', "Silver CS")
avoir.add_metadata('Keywords', "{client_livre};{client_facture};{ref_client};{no_dossier_qualite};{no_facture}{total_ht}")
avoir.add_metadata('DossierQualite', "{no_dossier_qualite}")
parser.add_document(avoir)


results = parser.parse('q:\\OLFA\\pdf2meta\\out.pdf')
parser.write_metadata()
print(results)
#results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\pblive012020072459470.pdf')
#print(results)
#results = parser.parse('q:\\OLFA\\pdf2meta\\Exemples\\pecdea012020070252474.pdf')
#print(results)

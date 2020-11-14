#!/usr/bin/env python
# -*- coding:utf-8 -*

'''
Un parser de pdf qui permet d'en extraire des métas données

à partir de regex pattern

Usage :

    parser = PdfParser()
    arc = Document("ARC", key = 'titre')
    arc.add_pattern('titre', r'CONFIRMATION DE LA COMMANDE N°(?P<cde_no>\d+) Du  (?P<date_arc>\d{2}/\d{2}/\d{4})')
    arc.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Commandé par : (?P<client_cde>\d+)$')
    arc.add_pattern('ref_client', r'Votre réf.: (?P<ref_client>\w*)\s*\|$')
    arc.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
    parser.add_document(arc)
    results = parser.parse('my_pdf_file.pdf')

    result :
    {'titre': 'ARC', 'client_livre': '744054', 'client_cde': '744054', 'cde_no': '164708', 'date_arc': '06/11/2020', 'ref_client': '003981467', 'total_ht': '156,65'}

'''
from pdfminer.high_level import extract_text
from pdfrw import PdfReader, PdfWriter

import re, logging
logging.getLogger('pdfminer').setLevel(logging.ERROR)

class PdfParser(object):
    '''Un parser de pdf
    '''
    def __init__(self):
        self.documents = []

    def add_document(self, document):
        '''Add a new document
        '''
        self.documents.append(document)

    def parse(self, filename):
        '''Parse a pdf file
        '''
        self.document = None
        self.metadata = None
        self.filename = filename
        logging.debug(f"Lecture du pdf {filename}")
        with open(filename, 'rb') as in_file:
            self.raw_pdf = extract_text(in_file)
        self.lines = self.raw_pdf.split('\n')
        logging.debug(f"Lecture du pdf terminée : {len(self.raw_pdf)} caractères.")
        self.document = self.find_document()
        if self.document:
            logging.info(f"Document trouvé : {self.document}")
            self.metadata = {'titre' : self.document.name}
            for line in self.lines:
                key, dict = self.parse_ligne(line, self.document.get_rx_dict())
                if key:
                    self.metadata.update(dict)
            return self.metadata
        else:
            logging.warning("Document inconnu.")


    def find_document(self):
        '''Renvoie le type de document
        '''
        for document in self.documents:
            for ligne in self.lines:
                key, dict = self.parse_ligne(ligne, document.rx_titre())
                if key:
                    return document

    @staticmethod
    def parse_ligne(line, rx_dict):
        '''Recherche la première occurance de chaque pattern
        renvoie key, groupdict
        '''
        #logging.debug(f"parse line : {line} => {rx_dict}")
        for key, rx in rx_dict.items():
            match = rx.search(line)
            if match:
                return key, match.groupdict()
        return None, None

    def write_metadata(self, filename = None ):
        '''Write metadata to pdf
        '''
        if self.metadata:
            trailer = PdfReader(self.filename)
            for key, fstring in self.document.metadata.items():
                try:
                    value = fstring.format(**self.metadata)
                    cmd = f'trailer.Info.{key} = "{value}"'
                    exec(cmd)
                except KeyError as e:
                    logging.warning(f"Error on metadata : {e} is missing")
            PdfWriter(filename or self.filename, trailer=trailer).write()
        else:
            logging.warning("Non metadata yet found.")

class Document(object):
    '''Un type de document (ex : ARC) généré par Silver CS
    '''
    pdf_infos = ['Author', 'Creationdate', 'Producer','Creator', 'Subject', 'Title', 'Keywords']
    def __init__(self, name, key = 'title'):
        self.name = name
        self.key = key
        self.rx_dict = {}
        self.metadata = {}

    def get_rx_dict(self):
        return self.rx_dict

    def __repr__(self):
        return f"Document({self.name})"

    def add_pattern(self, key, pattern):
        '''Add a regex pattern
        key     :   name of the pattern (spécial key : 'titre')
        '''
        self.rx_dict[key] = re.compile(pattern)

    def rx_titre(self):
        '''Renvoie le rx qui va permettre de tester si on a affaire à ce document
            sous forme {'titre' : rx}
        '''
        return {self.key : self.rx_dict.get(self.key)}

    def add_metadata(self, key, fstring):
        '''Ajoute une metadata au type de document
        key     :   pdf metadata key ( ['Author', 'Creationdate', 'Producer','Creator', 'Subject', 'Title', 'Keywords'])
        fstring :   un string contenant les clefs parsées ex : "Commande client n°{no_cde}"
        '''
        #assert key in self.pdf_infos, f"{key} is not in {self.pdf_infos}!"
        self.metadata[key] = fstring

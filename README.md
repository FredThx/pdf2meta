# pdf2meta
Python script :
Un parser de pdf qui permet d'en extraire des métas données

à partir de regex pattern

Usage :

```python
    parser = PdfParser()
    arc = Document("ARC", key = 'titre')
    arc.add_pattern('titre', r'CONFIRMATION DE LA COMMANDE N°(?P<cde_no>\d+) Du  (?P<date_arc>\d{2}/\d{2}/\d{4})')
    arc.add_pattern('client',r'Livré à:\s+(?P<client_livre>\d+)\s+Commandé par : (?P<client_cde>\d+)$')
    arc.add_pattern('ref_client', r'Votre réf.: (?P<ref_client>\w*)\s*\|$')
    arc.add_pattern('total_ht', r'\|TOTAL H.T.\s*(?P<total_ht>\d*,\d*)\|')
    parser.add_document(arc)
    results = parser.parse('my_pdf_file.pdf')
```
result :
    ```
    {'titre': 'ARC', 'client_livre': '744054', 'client_cde': '744054', 'cde_no': '164708', 'date_arc': '06/11/2020', 'ref_client': '003981467', 'total_ht': '156,65'}
    ```

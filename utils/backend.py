"""
Z39.50 searching.
"""
import logging
import os
import re

from PyZ3950 import zoom

from record import HeldRecord
from pymarc import Record
Record.__bases__ += (HeldRecord,)

def get_env(name):
    val = os.getenv(name)
    if val is None:
        raise Exception("Can't find environment variable {0}.".format(name))
    return val

#Used to determine if publicNote is an actual status
#or a summary holdings statement.
STATUS = re.compile('[A-Z]{2,}')

class Search(object):
    """
    A set of methods for searching a Z39.50 server.
    """
    def __init__(self):
        self.conn = zoom.Connection(
            get_env('HOST'),
            int(get_env('PORT')),
            databaseName=get_env('DB_NAME'),
            #Getting records in "opac" format.
            preferredRecordSyntax='OPAC',
            charset='utf-8',
        )

    def close(self):
        logging.debug('Closing connection.')
        return self.conn.close()

    def _holdings(self, rsp):
        """
        Process the holdings response into usable Json.
        """
        try:
            held = rsp.data.holdingsData
        except AttributeError:
            return []
        out = []
        for meta, item in held:
            try:
                note = item.publicNote
            except AttributeError:
                note = None
            #Skip summary holdings
            if STATUS.search(note) is None:
                continue
            d = {}
            d['callnumber'] = item.callNumber
            d['location'] = item.localLocation
            #Skip online "items"
            #if d['location'] == ('ONLINE SERIAL' or 'ONLINE BOOK'):
            #    continue
            d['availability'] = note
            out.append(d)
        return out

    def _summary_holdings(self, rsp):
        """
        Get the summary holdings for a bib.  e.g.:
        Lib. Has Bd.21- 1994-
        """
        try:
            held = rsp.data.holdingsData
        except AttributeError:
            return []
        out = []
        for _, item in held:
            try:
                pn = item.publicNote
            except AttributeError:
                continue
            #If this note doesn't match STATUS regex
            #then it is a summary holdings statement.
            if STATUS.search(pn) is None:
                out.append(
                    dict(
                        callnumber=item.callNumber,
                        location=item.localLocation,
                        held=pn
                    )
                )
        return out


    def findrecs(self, base, qs, sleep=False, limit=25):
        """
        Query Z39.50 and parse OPAC format into friendlier
        structure.
        """
        qstring = '%s %s' % (base, qs)
        logging.debug("Query: {0}".format(qstring))
        query = zoom.Query('PQF', qstring)
        result_set = self.conn.search(query)
        found = []
        try:
            for result in result_set[:limit]:
                #Get pymarc record from MARC returned.
                bib = Record(data=result.data.bibliographicRecord.encoding[1])
                held = self._holdings(result)
                #Basic metadata about the bib
                out = bib.title_meta()
                #Held items
                out['items'] = held
                out['summary'] = self._summary_holdings(result)
                out['barcodes'] = bib.barcodes()
                found.append(out)
        except zoom.Bib1Err:
            pass
        return found

    def isbn(self, qs, sleep=False):
        base ='@attr 1=7'
        return self.findrecs(base, qs, sleep)

    def issn(self, qs, sleep=False):
        base = '@attr 1=8'
        return self.findrecs(base, qs, sleep)

    def id(self, qs, sleep=False):
        base ='@attr 1=12'
        return self.findrecs(base, qs, sleep)

    def oclc(self, qs, sleep=False):
        base ='@attr 1=1007'
        return self.findrecs(base, qs, sleep)


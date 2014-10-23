"""
Extend pymarcs Record class with methods for local use.
"""

class HeldRecord(object):
    def title_meta(self):
        """
        Return basic metadata.
        """
        out = {}
        out['title'] = self.title()
        out['isbn'] = self.isbn()
        try:
            out['lccn'] = self['010']['a']
        except TypeError:
            out['lccn'] = None
        try:
            if self['003'].data == 'OCoLC':
                out['oclc'] = self['001'].data
        except AttributeError:
            out['oclc'] = None
        out['id'] = self['907']['a'].lstrip('.')[:8]
        out['url'] = 'http://josiah.brown.edu/record=%s' % out['id']
        return out

    def barcodes(self):
        """
        Get the item barcodes associated with the record.

        ToDo - see if there is some system limit on the number of items
        returned by this service.  I recall that being a problem in the
        past.
        """
        items = self.get_fields('945') or []
        out = []
        for item in items:
            bc = item['i']
            if bc is not None:
                bc = bc.replace(' ', '')
            number = item['y'].lstrip('.')
            loc = item['l'].strip()
            #This seems to be the second half of the callnumber only.
            call = item['c']
            d = dict(barcode=bc, item=number, location=loc, callnumber=call)
            out.append(d)
        return out


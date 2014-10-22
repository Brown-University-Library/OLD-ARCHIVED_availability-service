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

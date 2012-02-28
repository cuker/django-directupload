from django.conf import settings
from django.utils.crypto import constant_time_compare, salted_hmac

import base64

def b64_encode(s):
    return base64.urlsafe_b64encode(s).strip('=')

def b64_decode(s):
    pad = '=' * (-len(s) % 4)
    return base64.urlsafe_b64decode(s + pad)

def base64_hmac(salt, value, key):
    return b64_encode(salted_hmac(salt, value, key).digest())

class LegacySigner(object):
    '''
    Limited functionality signer
    '''
    def __init__(self, key=None, sep=':', salt=None):
        self.sep = sep
        self.key = key or settings.SECRET_KEY
        self.salt = salt or ('%s.%s' %
            (self.__class__.__module__, self.__class__.__name__))
    
    def signature(self, value):
        return base64_hmac(self.salt + 'signer', value, self.key)
    
    def sign(self, value):
        return '%s%s%s' % (value, self.sep, self.signature(value))

    def unsign(self, signed_value):
        if not self.sep in signed_value:
            raise ValueError('No "%s" found in value' % self.sep)
        value, sig = signed_value.rsplit(self.sep, 1)
        if constant_time_compare(sig, self.signature(value)):
            return value
        raise ValueError('Signature "%s" does not match' % sig)

try:
    from django.core.signing import Signer
except ImportError:
    Signer = LegacySigner


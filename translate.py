#!/usr/bin/python
 
"""
msmt.py
 
Functions to access the Microsoft Translator API HTTP Interface, using python's urllib/urllib2 libraries
 
"""
 
import urllib, urllib2
import json
 
from datetime import datetime
 
def datestring (display_format="%a, %d %b %Y %H:%M:%S", datetime_object=None):
    """Convert the datetime.date object (defaults to now, in utc) into a string, in the given display format"""
    if datetime_object is None:
        datetime_object = datetime.utcnow()
    return datetime.strftime(datetime_object, display_format)
 
def get_access_token (client_id, client_secret):
    """Make an HTTP POST request to the token service, and return the access_token,
    as described in number 3, here: http://msdn.microsoft.com/en-us/library/hh454949.aspx
    """
 
    data = urllib.urlencode({
            'client_id' : client_id,
            'client_secret' : client_secret,
            'grant_type' : 'client_credentials',
            'scope' : 'http://api.microsofttranslator.com'
            })
 
    try:
 
        request = urllib2.Request('https://datamarket.accesscontrol.windows.net/v2/OAuth2-13')
        request.add_data(data) 
 
        response = urllib2.urlopen(request)
        response_data = json.loads(response.read())
 
        if response_data.has_key('access_token'):
            return response_data['access_token']
 
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print datestring(), 'Could not connect to the server:', e.reason
        elif hasattr(e, 'code'):
            print datestring(), 'Server error: ', e.code
    except TypeError:
        print datestring(), 'Bad data from server'
 
supported_languages = { # as defined here: http://msdn.microsoft.com/en-us/library/hh456380.aspx
    'ar' : ' Arabic',
    'bg' : 'Bulgarian',
    'ca' : 'Catalan',
    'zh-CHS' : 'Chinese (Simplified)',
    'zh-CHT' : 'Chinese (Traditional)',
    'cs' : 'Czech',
    'da' : 'Danish',
    'nl' : 'Dutch',
    'en' : 'English',
    'et' : 'Estonian',
    'fi' : 'Finnish',
    'fr' : 'French',
    'de' : 'German',
    'el' : 'Greek',
    'ht' : 'Haitian Creole',
    'he' : 'Hebrew',
    'hi' : 'Hindi',
    'hu' : 'Hungarian',
    'id' : 'Indonesian',
    'it' : 'Italian',
    'ja' : 'Japanese',
    'ko' : 'Korean',
    'lv' : 'Latvian',
    'lt' : 'Lithuanian',
    'mww' : 'Hmong Daw',
    'no' : 'Norwegian',
    'pl' : 'Polish',
    'pt' : 'Portuguese',
    'ro' : 'Romanian',
    'ru' : 'Russian',
    'sk' : 'Slovak',
    'sl' : 'Slovenian',
    'es' : 'Spanish',
    'sv' : 'Swedish',
    'th' : 'Thai',
    'tr' : 'Turkish',
    'uk' : 'Ukrainian',
    'vi' : 'Vietnamese',
}
 
def print_supported_languages ():
    """Display the list of supported language codes and the descriptions as a single string
    (used when a call to translate requests an unsupported code)"""
 
    codes = []
    for k,v in supported_languages.items():
        codes.append('\t'.join([k, '=', v]))
    return '\n'.join(codes)
 
def to_bytestring (s):
    """Convert the given unicode string to a bytestring, using utf-8 encoding,
    unless it's already a bytestring"""
 
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode('utf-8')
 
def translate (access_token, text, to_lang, from_lang=None):
    """Use the HTTP Interface to translate text, as described here:
    http://msdn.microsoft.com/en-us/library/ff512387.aspx
    and return an xml string if successful
    """
 
    if not access_token:
        print 'Sorry, the access token is invalid'
    else:
        if to_lang not in supported_languages.keys():
            print 'Sorry, the API cannot translate to', to_lang
            print 'Please use one of these instead:'
            print print_supported_languages()
        else:
            data = {'text' : to_bytestring(text), 'to': to_lang}
            if from_lang:
                if from_lang not in supported_languages.keys():
                    print 'Sorry, the API cannot translate from', from_lang
                    print 'Please use one of these instead:'
                    print print_supported_languages()
                    return
                else:
                    data['from'] = from_lang
            try:
                url = 'https://api.datamarket.azure.com/Bing/MicrosoftTranslator/v1/Translate'
                request = urllib2.Request(url + urllib.urlencode(data))
                request.add_header('Authorization', 'Bearer '+access_token)
                response = urllib2.urlopen(request)
                return response.read()
            
            except urllib2.URLError, e:
                if hasattr(e, 'reason'):
                    print datestring(), 'Could not connect to the server:', e.reason
                elif hasattr(e, 'code'):
                    print datestring(), 'Server error: ', e.code

try:
    import simplejson as json
    from simplejson import JSONDecodeError
except ImportError:
    import json
    class JSONDecodeError(Exception): pass
    # Ugly: No alternative because this exception class doesnt seem to be there
    # in the standard python module
import urllib
import urllib2
import warnings
import logging


class ArgumentOutOfRangeException(Exception):
    def __init__(self, message):
        self.message = message.replace('ArgumentOutOfRangeException: ', '')
        super(ArgumentOutOfRangeException, self).__init__(self.message)


class TranslateApiException(Exception):
    def __init__(self, message, *args):
        self.message = message.replace('TranslateApiException: ', '')
        super(TranslateApiException, self).__init__(self.message, *args)


class Translator(object):
    """Implements AJAX API for the Microsoft Translator service

    :param app_id: A string containing the Bing AppID. (Deprecated)
    """

    def __init__(self, client_id, client_secret,
            scope="http://api.microsofttranslator.com",
            grant_type="client_credentials", app_id=None, debug=False):
        """


        :param client_id: The client ID that you specified when you registered
                          your application with Azure DataMarket.
        :param client_secret: The client secret value that you obtained when
                              you registered your application with Azure
                              DataMarket.
        :param scope: Defaults to http://api.microsofttranslator.com
        ;param grant_type: Defaults to "client_credentials"
        :param app_id: Deprecated
        :param debug: If true, the logging level will be set to debug

        .. versionchanged: 0.4
            Bing AppID mechanism is deprecated and is no longer supported.
            See: http://msdn.microsoft.com/en-us/library/hh454950
        """
        if app_id is not None:
            warnings.warn("""app_id is deprected since v0.4.
            See: http://msdn.microsoft.com/en-us/library/hh454950
            """, DeprecationWarning, stacklevel=2)

        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.grant_type = grant_type
        self.access_token = None
        self.debug = debug
        self.logger = logging.getLogger("microsofttranslator")
        if self.debug:
            self.logger.setLevel(level=logging.DEBUG)

    def get_access_token(self):
        """Bing AppID mechanism is deprecated and is no longer supported.
        As mentioned above, you must obtain an access token to use the
        Microsoft Translator API. The access token is more secure, OAuth
        standard compliant, and more flexible. Users who are using Bing AppID
        are strongly recommended to get an access token as soon as possible.

        .. note::
            The value of access token can be used for subsequent calls to the
            Microsoft Translator API. The access token expires after 10
            minutes. It is always better to check elapsed time between time at
            which token issued and current time. If elapsed time exceeds 10
            minute time period renew access token by following obtaining
            access token procedure.

        :return: The access token to be used with subsequent requests
        """
        args = urllib.urlencode({
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': self.scope,
            'grant_type': self.grant_type
        })
        response = json.loads(urllib.urlopen(
            'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13', args
        ).read())

        self.logger.debug(response)

        if "error" in response:
            raise TranslateApiException(
                response.get('error_description', 'No Error Description'),
                response.get('error', 'Unknown Error')
            )
        return response['access_token']

    def call(self, url, params):
        """Calls the given url with the params urlencoded
        """
        if not self.access_token:
            self.access_token = self.get_access_token()

        request = urllib2.Request(
            "%s?%s" % (url, urllib.urlencode(params)),
            headers={'Authorization': 'Bearer %s' % self.access_token}
        )
        response = urllib2.urlopen(request).read()
        rv =  json.loads(response.decode("UTF-8-sig"))

        if isinstance(rv, basestring) and \
                rv.startswith("ArgumentOutOfRangeException"):
            raise ArgumentOutOfRangeException(rv)

        if isinstance(rv, basestring) and \
                rv.startswith("TranslateApiException"):
            raise TranslateApiException(rv)

        return rv

    def translate(self, text, to_lang, from_lang=None,
            content_type='text/plain', category='general'):
        """Translates a text string from one language to another.

        :param text: A string representing the text to translate.
        :param to_lang: A string representing the language code to
            translate the text into.
        :param from_lang: A string representing the language code of the
            translation text. If left None the response will include the
            result of language auto-detection. (Default: None)
        :param content_type: The format of the text being translated.
            The supported formats are "text/plain" and "text/html". Any HTML
            needs to be well-formed.
        :param category: The category of the text to translate. The only
            supported category is "general".
        """
        params = {
            'text': text.encode('utf8'),
            'to': to_lang,
            'contentType': content_type,
            'category': category,
            }
        if from_lang is not None:
            params['from'] = from_lang
        return self.call(
            "http://api.microsofttranslator.com/V2/Ajax.svc/Translate",
            params)

    def translate_array(self, texts, to_lang, from_lang=None, **options):
        """Translates an array of text strings from one language to another.

        :param texts: A list containing texts for translation.
        :param to_lang: A string representing the language code to 
            translate the text into.
        :param from_lang: A string representing the language code of the 
            translation text. If left None the response will include the 
            result of language auto-detection. (Default: None)
        :param options: A TranslateOptions element containing the values below. 
            They are all optional and default to the most common settings.

                Category: A string containing the category (domain) of the 
                    translation. Defaults to "general".
                ContentType: The format of the text being translated. The 
                    supported formats are "text/plain" and "text/html". Any 
                    HTML needs to be well-formed.
                Uri: A string containing the content location of this 
                    translation.
                User: A string used to track the originator of the submission.
                State: User state to help correlate request and response. The 
                    same contents will be returned in the response.
        """
        options = {
            'Category': "general",
            'Contenttype': "text/plain",
            'Uri': '',
            'User': 'default',
            'State': ''
            }.update(options)
        params = {
            'texts': json.dumps(texts),
            'to': to_lang,
            'options': json.dumps(options),
            }
        if from_lang is not None:
            params['from'] = from_lang

        return self.call(
                "http://api.microsofttranslator.com/V2/Ajax.svc/TranslateArray",
                params)

if __name__ =="__main__":
    import oauthlib
    access_token = 'oVyns/fT0RTF7qmvoOxuXvnkxAFJkZcBmyq36hM9eLM'
    to_lang = "cn"
    from_lang = "en"
    text = 'Hello'
    oauthlib.uri_validate
    client = oauthlib.oauth1.Client(access_token, client_secret=access_token)
    uri, headers, body = client.sign('http://example.com/request_token')
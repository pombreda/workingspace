
import urllib
try:
    # ensure a recent request lib is available
    import requests
    assert [int(n) for n in requests.__version__.split('.', 2)][:2] >= [1, 2]
except (ImportError, AssertionError):
    requests = None


def to_bytestring (s):
    """Convert the given unicode string to a bytestring, using utf-8 encoding,
    unless it's already a bytestring"""
    if s:
        if isinstance(s, str):
            return s
        else:
            return s.encode('utf-8')

url = "https://api.datamarket.azure.com/Bing/MicrosoftTranslator/v1/Translate"
client_id = 'souprix'
client_secret = 'oVyns/fT0RTF7qmvoOxuXvnkxAFJkZcBmyq36hM9eLM'

headers = {'User-Agent': 'Mozilla/5.0'}
args = {'Text':to_bytestring("'hello'"), 'From':"'en'", 'To': "'fr'"}
r = requests.Session()
res = r.get(url + '?' + urllib.urlencode(args),
             headers=headers,
             auth=(client_id, client_secret))
text = res.text
from xml.dom import minidom
xmldoc = minidom.parseString(text)

elements = xmldoc.getElementsByTagName("d:Text")
elements[0].value

import xml.etree.ElementTree as ET
root = ET.fromstring(text)
root.findall("./")
res_root = root.find(".//{http://schemas.microsoft.com/ado/2007/08/dataservices}Text")
res_root.text

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 10:35:52 2014

@author: jl237561
"""

import uuid
import time
import libxml2
import quopri
import base64
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))

pdf_path = os.path.join(cur_dir, "helloworld.pdf")
soap_template = os.path.join(cur_dir, "example_soap.xml")

PATIENT_ID = "9d372c19db66411^^^&1.3.6.1.4.1.21367.2005.3.7&ISO"

MIME_BOUNDARY = 'MIMEBoundaryurn_uuid_0FE43E4D025F0BF3DC11582467646812'
URN_UUID_REQUEST = '<0.urn:uuid:0FE43E4D025F0BF3DC11582467646813@apache.org>'
URN_UUID_REQUEST2 = '1.urn:uuid:AFBE87CB65FD88AC4B1220879854390@apache.org'
pdf_encode = base64.b64encode(open(pdf_path, "rb").read())

http_headers_content_type = 'multipart/related; '
http_headers_content_type += 'boundary=%s; ' % MIME_BOUNDARY
http_headers_content_type += 'type="application/xop+xml"; '
http_headers_content_type += 'start="%s"; ' % URN_UUID_REQUEST
http_headers_content_type += 'start-info="application/soap+xml"; '
http_headers_content_type += 'action="urn:ihe:iti:2007:ProvideAndRegisterDocumentSet-b"'

uuid_classification_object = str(uuid.uuid4())
uuid_extrinsic_object = str(uuid.uuid4())
uuid_id_classification = str(uuid.uuid4())
uuid_id_association = str(uuid.uuid4())

now = time.strftime('%Y%m%d%H%M%S')
uuid_external_identifier_value = "1.42." + now + ".61"
uuid_external_identifier_value2 = "1.42." + now + ".62"

#len(uuid_external_identifier_value)
#print len("1.42.20140603060830.62")

soap_args = dict(
    uuid_classification_object=uuid_classification_object,
    uuid_extrinsic_object=uuid_extrinsic_object,
    uuid_id_classification=uuid_id_classification,
    uuid_id_association=uuid_id_association,
    uuid_external_identifier_value=uuid_external_identifier_value,
    uuid_external_identifier_value2=uuid_external_identifier_value2,
    pdf_encode=pdf_encode,
    )


print "soap_args=", repr(soap_args)


def build_mime_message(request, data, is_need_binary_part=False):
    '''
    Build the xml string with MIME attachments and the base64 encoded data string
    '''
    request_part  = '\r\n'
    request_part += '--%s\r\n' % MIME_BOUNDARY
    request_part += 'Content-Type: application/xop+xml; '\
                    'type="application/soap+xml; '\
                    'charset=UTF-8"\r\n'
    # request_part += 'Content-Transfer_Encoding: binary\r\n'
    request_part += 'Content-ID: %s\r\n\r\n' % URN_UUID_REQUEST
    request_part += '%s\r\n' % request
    binary_part  = '\r\n'
    if is_need_binary_part:
        binary_part += '--%s\r\n' % MIME_BOUNDARY
        binary_part += 'Content-Type: text/plain\r\n'
        binary_part += 'Content-Transfer-Encoding: binary\r\n'
        binary_part += 'Content-ID: <%s>\r\n\r\n' % URN_UUID_REQUEST2
        binary_part += '%s\r\n\r\n' % data
    binary_part += '--%s--' % MIME_BOUNDARY
    request_part += binary_part
    return request_part


data2 = open(soap_template, "rb").read()
data2 = data2 % soap_args

# doc = libxml2.parseMemory(data2, len(data2))
# ctxt = doc.xpathNewContext()
# res = ctxt.xpathEval("//urn:ihe:iti:xds-b:2007:Document")

def removeNonAscii(s):
    return "".join(i for i in s if ord(i) < 128)


request = data2
# request = removeNonAscii(data2)
data = build_mime_message(request, data="It is great!")


try:
    # ensure a recent request lib is available
    import requests
    assert([int(n) for n in requests.__version__.split('.', 2)][:2]
           >= [1, 2])
except (ImportError, AssertionError):
    requests = None
    raise ValueError("Cannot import requests")


if __name__ == "__main__":
    # http_headers_content_type="soap+xml; charset=UTF-8"
#    headers = {"Host": "192.168.153.128:9080",
#               "User-Agent": "Axis2",
#               "Content-Type": http_headers_content_type,
#               "Content-Length": len(data)}
    end_point = "http://192.168.153.128:9080/tf6/services/xdsrepositoryb"
    headers = {"Host": "192.168.153.128:9080",
               "User-Agent": "Axis2",
               "Content-Type": http_headers_content_type}
    r = requests.post(end_point, headers=headers, data=data)

#    from pysimplesoap.client import SoapClient
#    from pysimplesoap.simplexml import SimpleXMLElement
#    client = SoapClient(location=end_point,
#                    namespace='http://www.w3.org/2003/05/soap-envelope',
#                    ns="wsa", soap_ns="soapenv")
#    headers = SimpleXMLElement(raw_headers)
#    
#    from suds.client import Client
#    wdsl_end_point = end_point + "?wsdl"
#    client = Client(wdsl_end_point)
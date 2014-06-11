# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 10:35:52 2014

@author: jl237561
"""

MIME_BOUNDARY = 'MIMEBoundaryurn_uuid_0FE43E4D025F0BF3DC11582467646812'
URN_UUID_REQUEST = '<0.urn:uuid:0FE43E4D025F0BF3DC11582467646813@apache.org>'
URN_UUID_REQUEST2 = '1.urn:uuid:AFBE87CB65FD88AC4B1220879854390@apache.org'
http_headers_content_type = 'multipart/related; '
http_headers_content_type += 'boundary=%s; ' % MIME_BOUNDARY
http_headers_content_type += 'type="application/xop+xml"; '
http_headers_content_type += 'start="%s"; ' % URN_UUID_REQUEST
http_headers_content_type += 'start-info="application/soap+xml"; '
# http_headers_content_type += 'action="urn:ihe:iti:2007:RegistryStoredQuery"'


def build_mime_message(request, data):
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
    binary_part += '--%s\r\n' % MIME_BOUNDARY
    binary_part += 'Content-Type: text/plain\r\n'
    binary_part += 'Content-Transfer-Encoding: binary\r\n'
    binary_part += 'Content-ID: <%s>\r\n\r\n' % URN_UUID_REQUEST2
    binary_part += '%s\r\n' % data
    binary_part += '--%s--' % MIME_BOUNDARY

    request_part += binary_part

    return request_part

#data2 = '''
#<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
#    xmlns:wsa="http://www.w3.org/2005/08/addressing">
#    <soapenv:Header>
#        <wsa:To>http://red:9080/tf6/services/xdsregistryb</wsa:To>
#        <wsa:MessageID>urn:uuid:F347E1483350B8D6511198803333967</wsa:MessageID>
#        <wsa:Action>urn:ihe:iti:2007:RegistryStoredQuery</wsa:Action>
#    </soapenv:Header>
#    <soapenv:Body>
#        <query:AdhocQueryRequest xmlns:query="urn:oasis:names:tc:ebxml-regrep:xsd:query:3.0"
#            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#            xmlns:rs="urn:oasis:names:tc:ebxml-regrep:xsd:rs:3.0"
#            xmlns="urn:oasis:names:tc:ebxml-regrep:xsd:rim:3.0">
#            <query:ResponseOption returnComposedObjects="true" returnType="LeafClass"/>
#            <AdhocQuery id="urn:uuid:a7ae438b-4bc2-4642-93e9-be891f7bb155">
#                <Slot name="$uuid">
#                    <ValueList>
#                        <Value>('urn:uuid:133307c9-2a97-41df-b31f-98b7c0982e7e')</Value>
#                    </ValueList>
#                </Slot>
#            </AdhocQuery>
#        </query:AdhocQueryRequest>
#    </soapenv:Body>
#</soapenv:Envelope>
#'''


data2 = '''
<soapenv:Envelope xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
    xmlns:wsa="http://www.w3.org/2005/08/addressing">
    <soapenv:Header xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope">
       <wsa:To soapenv:mustUnderstand="true" xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
             xmlns:wsa="http://www.w3.org/2005/08/addressing">http://192.168.153.128:9080/tf6/services/xdsrepositoryb</wsa:To>
       <wsa:MessageID soapenv:mustUnderstand="true" xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
             xmlns:wsa="http://www.w3.org/2005/08/addressing">urn:uuid:EA153BD5B74B5B0CAD1401996224596</wsa:MessageID>
       <wsa:Action soapenv:mustUnderstand="true" xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope"
             xmlns:wsa="http://www.w3.org/2005/08/addressing">urn:ihe:iti:2007:RetrieveDocumentSet</wsa:Action>
    </soapenv:Header>
    <soapenv:Body>
        <RetrieveDocumentSetRequest xsi:schemaLocation="urn:ihe:iti:xds-b:2007 file:/Users/bill/ihe/Frameworks/ITI-4/XDS.b/schema/IHE/XDS.b_DocumentRepository.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xmlns="urn:ihe:iti:xds-b:2007">
           <DocumentRequest>
              <RepositoryUniqueId>1.3.6.1.4.1.21367.2011.2.3.7</RepositoryUniqueId>
              <DocumentUniqueId>1.42.20140611100915.62</DocumentUniqueId>
           </DocumentRequest>
        </RetrieveDocumentSetRequest>
    </soapenv:Body>
</soapenv:Envelope>
'''


request = data2
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
#    http_headers_content_type="soap+xml; charset=UTF-8"
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
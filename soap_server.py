from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server

class SoapService(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def say_hello(ctx, name):
        return f"Hello {name}"

application = Application(
    [SoapService], 'soap.example',
    in_protocol=Soap11(), out_protocol=Soap11()
)

soap_app = WsgiApplication(application)

if __name__ == "__main__":
    server = make_server('0.0.0.0', 8001, soap_app)
    print("SOAP server running on http://0.0.0.0:8001")
    server.serve_forever()

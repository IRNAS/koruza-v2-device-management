import logging

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from .src.device_management import DeviceManagement

from ..src.constants import DEVICE_MANAGEMENT_PORT

log = logging.getLogger()

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)

    with SimpleXMLRPCServer(("0.0.0.0", DEVICE_MANAGEMENT_PORT),
                            requestHandler=RequestHandler, allow_none=True, logRequests=True) as server:
        server.register_introspection_functions()
        server.register_instance(DeviceManagement())
        log.info(f"Serving XML-RPC on 0.0.0.0 port {DEVICE_MANAGEMENT_PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            log.info("\nKeyboard interrupt received, exiting.")
            # sys.exit(0)
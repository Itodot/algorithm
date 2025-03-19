# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import grpc_gen.sync_pb2 as sync__pb2

GRPC_GENERATED_VERSION = '1.70.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in sync_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class StreamServiceStub(object):
    """定义服务
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.BiStream = channel.stream_stream(
                '/sync.StreamService/BiStream',
                request_serializer=sync__pb2.SyncRequest.SerializeToString,
                response_deserializer=sync__pb2.SyncResponse.FromString,
                _registered_method=True)


class StreamServiceServicer(object):
    """定义服务
    """

    def BiStream(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StreamServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'BiStream': grpc.stream_stream_rpc_method_handler(
                    servicer.BiStream,
                    request_deserializer=sync__pb2.SyncRequest.FromString,
                    response_serializer=sync__pb2.SyncResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'sync.StreamService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('sync.StreamService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class StreamService(object):
    """定义服务
    """

    @staticmethod
    def BiStream(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/sync.StreamService/BiStream',
            sync__pb2.SyncRequest.SerializeToString,
            sync__pb2.SyncResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

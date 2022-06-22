# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from swh.graph.rpc import swhgraph_pb2 as swh_dot_graph_dot_rpc_dot_swhgraph__pb2


class TraversalServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Traverse = channel.unary_stream(
                '/swh.graph.TraversalService/Traverse',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Node.FromString,
                )
        self.FindPathTo = channel.unary_unary(
                '/swh.graph.TraversalService/FindPathTo',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.FindPathToRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Path.FromString,
                )
        self.FindPathBetween = channel.unary_unary(
                '/swh.graph.TraversalService/FindPathBetween',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.FindPathBetweenRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Path.FromString,
                )
        self.CountNodes = channel.unary_unary(
                '/swh.graph.TraversalService/CountNodes',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.CountResponse.FromString,
                )
        self.CountEdges = channel.unary_unary(
                '/swh.graph.TraversalService/CountEdges',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.CountResponse.FromString,
                )
        self.Stats = channel.unary_unary(
                '/swh.graph.TraversalService/Stats',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.StatsRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.StatsResponse.FromString,
                )
        self.GetNode = channel.unary_unary(
                '/swh.graph.TraversalService/GetNode',
                request_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.GetNodeRequest.SerializeToString,
                response_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Node.FromString,
                )


class TraversalServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Traverse(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindPathTo(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindPathBetween(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CountNodes(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CountEdges(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Stats(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetNode(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TraversalServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Traverse': grpc.unary_stream_rpc_method_handler(
                    servicer.Traverse,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Node.SerializeToString,
            ),
            'FindPathTo': grpc.unary_unary_rpc_method_handler(
                    servicer.FindPathTo,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.FindPathToRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Path.SerializeToString,
            ),
            'FindPathBetween': grpc.unary_unary_rpc_method_handler(
                    servicer.FindPathBetween,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.FindPathBetweenRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Path.SerializeToString,
            ),
            'CountNodes': grpc.unary_unary_rpc_method_handler(
                    servicer.CountNodes,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.CountResponse.SerializeToString,
            ),
            'CountEdges': grpc.unary_unary_rpc_method_handler(
                    servicer.CountEdges,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.CountResponse.SerializeToString,
            ),
            'Stats': grpc.unary_unary_rpc_method_handler(
                    servicer.Stats,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.StatsRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.StatsResponse.SerializeToString,
            ),
            'GetNode': grpc.unary_unary_rpc_method_handler(
                    servicer.GetNode,
                    request_deserializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.GetNodeRequest.FromString,
                    response_serializer=swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Node.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'swh.graph.TraversalService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TraversalService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Traverse(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/swh.graph.TraversalService/Traverse',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Node.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FindPathTo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/swh.graph.TraversalService/FindPathTo',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.FindPathToRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Path.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FindPathBetween(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/swh.graph.TraversalService/FindPathBetween',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.FindPathBetweenRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Path.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CountNodes(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/swh.graph.TraversalService/CountNodes',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.CountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def CountEdges(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/swh.graph.TraversalService/CountEdges',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.TraversalRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.CountResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Stats(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/swh.graph.TraversalService/Stats',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.StatsRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.StatsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetNode(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/swh.graph.TraversalService/GetNode',
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.GetNodeRequest.SerializeToString,
            swh_dot_graph_dot_rpc_dot_swhgraph__pb2.Node.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

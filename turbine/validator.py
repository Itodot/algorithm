from shred.shred import Shred

import grpc
from grpc_gen import  sync_pb2_grpc,sync_pb2

channel = grpc.insecure_channel("localhost:50051")
stub = sync_pb2_grpc.StreamServiceStub(channel)

def empty_request_iterator():
    return iter([])
responses = stub.BiStream(empty_request_iterator())
for response in responses:
    print(f"Received from Server: {response.success}:{response.data}")
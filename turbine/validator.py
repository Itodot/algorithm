import base58
import grpc
import json
from nacl.signing import SigningKey
from utils.config_utils import load_config
from shred.shred import Shred
from grpc_gen import sync_pb2_grpc

def create_grpc_stub():
    """
    创建 gRPC 客户端存根。

    返回:
        sync_pb2_grpc.StreamServiceStub: gRPC 客户端存根。
    """
    channel = grpc.insecure_channel("localhost:50051")
    return sync_pb2_grpc.StreamServiceStub(channel)

def get_verify_key():
    """
    从配置文件加载私钥并生成签名密钥对。

    返回:
        nacl.signing.VerifyKey: 验证密钥。
    """
    config = load_config("config.yml")
    private_key = config["private_key"]
    seed = base58.b58decode(private_key)[:32]
    signing_key = SigningKey(seed)
    return signing_key.verify_key

def empty_request_iterator():
    """
    返回一个空的请求迭代器。

    返回:
        iterator: 一个空的迭代器。
    """
    return iter([])

def json_to_shred(d) -> Shred:
    """
    将 JSON 数据转换为 Shred 对象。

    参数:
        d (dict): JSON 数据。

    返回:
        Shred: Shred 对象。
    """
    shred = Shred(d['index'], d['total'], d['payload'])
    shred.signature = d['signature']
    return shred

def process_responses(stub):
    """
    处理来自 gRPC 服务器的响应。

    参数:
        stub (sync_pb2_grpc.StreamServiceStub): gRPC 客户端存根。

    返回:
        bytes: 累积的有效负载数据。
    """
    responses = stub.BiStream(empty_request_iterator())
    payload = b""

    for response in responses:
        res_data = json.loads(response.data, object_hook=json_to_shred)
        verify = res_data.verify_shred(get_verify_key())
        print("验证每个shred的签名:",verify)
        print(f"Received from Server: {response.success}:{res_data}:{verify}")
        payload += base58.b58decode(res_data.payload)
        if res_data.index + 1 == res_data.total:
            break

    return payload

def verify_payload_signature(payload):
    """
    验证累积的有效负载数据的签名。

    参数:
        payload (bytes): 累积的有效负载数据。

    抛出:
        nacl.exceptions.BadSignatureError: 如果签名验证失败。
    """
    dict_data = json.loads(payload.decode('utf-8'))
    signature = dict_data.pop('signature')
    print("接收到的组合完成的数据:", dict_data)
    payload_verify = json.dumps(dict_data).encode()
    signature_bytes = base58.b58decode(signature)
    print("需验证的整体payload:",payload_verify)
    print("需验证的签名:",signature_bytes)
    get_verify_key().verify(payload_verify, signature_bytes)
    print("signature verify success")

def main():
    """
    执行 gRPC 客户端逻辑的主函数。
    """
    stub = create_grpc_stub()
    payload = process_responses(stub)
    verify_payload_signature(payload)

if __name__ == "__main__":
    main()
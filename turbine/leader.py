from shred.shred import Shred
from grpc_gen import sync_pb2_grpc,sync_pb2
import time
import grpc
from concurrent import futures
from nacl.signing import SigningKey
from utils.config_utils import load_config
import base58
import json
#接收到transation数据
transaction = {
    "message_header": {
        "version": 1,
        "account_count": 2,
        "signature_count": 1
    },
    "account_keys": ["Alice", "Bob"],
    "recent_blockhash": "5KQmYg7s8v9wX2y3z4a5b6c7d8e9f0g1h2i3j4k5l6m7n8o9p0q1r2s3t4u5v6w7",
    "instructions": [],
    "program_id": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
}
SHRED_LENGTH=50
def get_signkey():
    # 生成密钥对
    config = load_config("config.yml")
    private_key = config["private_key"]
    seed = base58.b58decode(private_key)[:32]

    signing_key = SigningKey(seed)
    return signing_key
class StreamService(sync_pb2_grpc.StreamServiceServicer):

    def BiStream(self, request_iterator, context):
        while True:
          transaction_data=str(transaction).encode()
          print(transaction_data)
          for i in range(0, len(transaction_data), SHRED_LENGTH):
                 payload=transaction_data[i:i+SHRED_LENGTH]
                 shred = Shred(i//SHRED_LENGTH, len(payload), payload)
                 signKey = get_signkey()
                 shred.sign_shred(signKey)
                 #respone_data=json.dumps(shred)
                 print(shred)
          yield sync_pb2.SyncResponse(success=True,data="recived")  # 服务器持续返回数据
          time.sleep(5) 


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
sync_pb2_grpc.add_StreamServiceServicer_to_server(StreamService(), server)
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()



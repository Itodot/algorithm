# Turbine测试

## 项目简介

该项目实现了一个基于 gRPC 的双向流服务，用于处理交易数据的签名和分片。主要功能包括生成签名密钥、对交易数据进行签名、将交易数据分片以及通过 gRPC 服务进行数据传输。

## 主要功能

### 1. 生成签名密钥

函数 `get_signkey` 用于生成并返回签名密钥。它从配置文件 `config.yml` 中加载私钥，并使用该私钥生成签名密钥。

### 2. 对交易数据进行签名

函数 `sign_transaction` 接收一个交易数据字典，对其进行签名，并返回包含签名的交易数据。

### 3. 将交易数据分片

函数 `create_shreds` 将交易数据分片，并返回分片对象列表。每个分片对象包含分片数据及其签名。

### 4. gRPC 服务

类 `StreamService` 实现了 gRPC 服务的双向流方法 `BiStream`，用于处理客户端请求并返回分片数据。函数 `serve` 创建并启动 gRPC 服务器。

## 代码结构

```python
from shred.shred import Shred
from grpc_gen import sync_pb2_grpc, sync_pb2
import grpc
from concurrent import futures
from nacl.signing import SigningKey
from utils.config_utils import load_config
import base58
import json
from typing import Any

# 接收到的交易数据
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

SHRED_LENGTH = 100  # 每个分片的长度

def get_signkey() -> None:
    """
    生成并返回签名密钥。
    """
    config = load_config("config.yml")  # 加载配置文件
    private_key = config["private_key"]  # 获取私钥
    seed = base58.b58decode(private_key)[:32]  # 解码私钥并取前32字节作为种子

    signing_key = SigningKey(seed)  # 使用种子生成签名密钥
    return signing_key

def sign_transaction(transaction: dict[str, Any]) -> dict[str, Any]:
    """
    对交易数据进行签名并返回签名后的交易数据。
    """
    transaction_signature = get_signkey().sign(json.dumps(transaction).encode()).signature  # 对交易数据进行签名
    transaction.update({"signature": base58.b58encode(transaction_signature).decode()})  # 将签名添加到交易数据中
    return transaction

def create_shreds(transaction_data: str) -> list[Shred]:
    """
    将交易数据分片并返回分片对象列表。
    """
    shreds = []
    for i in range(0, len(transaction_data), SHRED_LENGTH):
        payload = transaction_data[i:i+SHRED_LENGTH]  # 分片数据
        base58_payload = base58.b58encode(payload).decode()  # 对分片数据进行 base58 编码
        shred = Shred(i // SHRED_LENGTH, len(transaction_data) // SHRED_LENGTH + 1, base58_payload)  # 创建分片对象
        signKey = get_signkey()  # 获取签名密钥
        shred.sign_shred(signKey)  # 对分片进行签名
        shreds.append(shred)
    return shreds

class StreamService(sync_pb2_grpc.StreamServiceServicer):
    """
    实现 gRPC 服务的类。
    """

    def BiStream(self, request_iterator, context):
        """
        双向流方法。
        """
        while True:
            signed_transaction = sign_transaction(transaction.copy())  # 对交易数据进行签名
            transaction_data = json.dumps(signed_transaction)  # 将交易数据转换为 JSON 字符串

            shreds = create_shreds(transaction_data)  # 创建分片对象列表
            for shred in shreds:
                response_data = json.dumps(shred.__dict__)  # 将分片对象转换为 JSON 字符串
                yield sync_pb2.SyncResponse(success=True, data=response_data)  # 服务器持续返回数据
            break

def serve():
    """
    创建并启动 gRPC 服务器。
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sync_pb2_grpc.add_StreamServiceServicer_to_server(StreamService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
```

## 运行方法

1. 确保已安装所需的 Python 包：

   ```sh
   pip install grpcio grpcio-tools pynacl base58
   ```

2. 启动 gRPC 服务器：
   ```sh
   python README.md
   ```

## 配置文件

请确保在项目根目录下有一个 `config.yml` 文件，其中包含私钥信息：

```yaml
private_key: "your_private_key_here"
```

## 贡献

欢迎提交问题和贡献代码！

from .shred import Shred
"""
该脚本生成密钥对并对数据进行分片和验证。
模块:
- shred: 包含 Shred 类，用于数据分片和验证。
- nacl.signing: 包含 SigningKey 类，用于生成签名密钥。
- utils.config_utils: 包含 load_config 函数，用于加载配置文件。
- base58: 用于 Base58 编码和解码。
功能:
1. 从配置文件 "config.yml" 中加载私钥。
2. 使用 Base58 解码私钥并生成签名密钥对。
3. 将数据分成多个分片，并使用签名密钥对每个分片进行签名。
4. 验证每个分片的签名。
变量:
- private_key: 从配置文件中加载的私钥。
- seed: 从私钥中提取的种子，用于生成签名密钥。
- signing_key: 使用种子生成的签名密钥。
- verify_key: 从签名密钥生成的验证密钥。
- data: 要分片和签名的数据。
循环:
- 遍历数据的每个分片，创建 Shred 对象并打印分片和验证结果。
"""
from nacl.signing import SigningKey
from utils.config_utils import load_config
import base58
# 生成密钥对
config = load_config("config.yml")
private_key = config["private_key"]
seed = base58.b58decode(private_key)[:32]

signing_key = SigningKey(seed)
verify_key = signing_key.verify_key

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

# 签名数据
transaction_data = str(transaction).encode()  # 将交易数据转换为字节编码

signature = signing_key.sign(transaction_data).signature.__str__()  # 对交易数据进行签名并转换为字符串

transaction.update({"signature": signature})  # 将签名添加到交易数据中

print(transaction)  # 打印包含签名的交易数据

# 分片和验证数据

recived_transaction = b''  # 初始化接收的交易数据

for i in range(0, len(transaction_data), 50):
    shred = Shred(i // 50, 50, transaction_data[i:i+50], signing_key)  # 创建 Shred 对象
    print(shred)  # 领导者节点:发送分片数据
    print(shred.verify_shred(verify_key))  # 验证节点:验证分片签名
    recived_transaction += shred.payload  #  验证节点:组合接收到的分片数据

print(recived_transaction)  # 打印接收的交易数据

recive_signatue = signing_key.sign(recived_transaction).signature.__str__()  # 对接收的交易数据进行签名并转换为字符串

print(recive_signatue)  # 打印接收的交易数据签名

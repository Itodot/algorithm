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

data = b"1234567890123221"

for i in range(0, len(data), 3):
    shred = Shred(i // 3, 3, data[i:i+3], signing_key)
    print(shred)
    print(shred.verify_shred(verify_key))
    
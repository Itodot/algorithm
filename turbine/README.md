# Turbine 分片

## 简介

`Shred` 类表示一个数据分片，并提供签名和验证功能。

## 属性

- `index` (int): 分片的索引。
- `total` (int): 分片的总数。
- `payload` (str): 分片的数据负载。
- `signature` (bytes): 分片的签名。

## 方法

### `__init__(index, total, payload, signing_key)`

初始化 `Shred` 对象，并对其进行签名。

### `sign_shred(signing_key)`

对 `Shred` 头部和数据进行签名。

**参数:**

- `signing_key` (SigningKey): 用于签名的密钥

**返回:**

- `bytes`: 签名后的字节串

### `verify_shred(verify_key)`

验证分片签名。

**参数:**

- `verify_key` (VerifyKey): 用于验证签名的公钥

**返回:**

- `bool`: 如果签名验证成功返回 `True`，否则返回 `False`

### `__str__()`

返回 `Shred` 对象的字符串表示。

## 示例

```python
from nacl.signing import SigningKey, VerifyKey

# 创建签名密钥和验证密钥
signing_key = SigningKey.generate()
verify_key = signing_key.verify_key

# 创建一个 Shred 对象
shred = Shred(index=1, total=10, payload="数据负载", signing_key=signing_key)

# 打印 Shred 对象
print(shred)

# 验证 Shred 签名
is_valid = shred.verify_shred(verify_key)
print(f"签名验证结果: {is_valid}")
```

## 依赖

- `pynacl`: 一个用于加密、签名、密钥交换等操作的 Python 库。

## 安装

使用 `pip` 安装依赖:

```sh
pip install pynacl
```

## 许可证

此项目使用 MIT 许可证。详情请参阅 LICENSE 文件。

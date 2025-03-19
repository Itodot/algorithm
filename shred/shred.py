class Shred:    
    """
    Shred类表示一个数据分片，并提供签名和验证功能。
    属性:
        index (int): 分片的索引。
        total (int): 分片的总数。
        payload (str): 分片的数据负载。
        signature (bytes): 分片的签名。
    方法:
        __init__(index, total, payload, signing_key):
            初始化Shred对象，并对其进行签名。
        sign_shred(signing_key):
            对Shred头部和数据进行签名。
        verify_shred(verify_key):
            验证签名是否有效。
        __str__():
            返回Shred对象的字符串表示。
    """
    def __init__(self, index, total, payload):
        self.index = index
        self.total = total
        self.payload = payload
        self.signature = ""
        
    def sign_shred(self, signing_key):
        """
        对Shred头部和数据进行签名

        参数:
        signing_key (SigningKey): 用于签名的密钥

        返回:
        bytes: 签名后的字节串
        """
        """对Shred头部和数据进行签名"""
        message = f"{self.index}|{self.total}|{self.payload}".encode()
        self.signature=signing_key.sign(message).signature
    
    def verify_shred(self, verify_key):
        """
        验证分片签名

        参数:
        verify_key (VerifyKey): 用于验证签名的公钥

        返回:
        bool: 如果签名验证成功返回 True，否则返回 False
        """
        """验证签名"""
        message = f"{self.index}|{self.total}|{self.payload}".encode()
        try:
            verify_key.verify(message, self.signature)
            return True
        except:
            return False
        
    def __str__(self):
        return f"Shred({self.index}, {self.total}, {self.payload}, {self.signature})"
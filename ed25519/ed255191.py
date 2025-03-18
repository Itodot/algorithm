import hashlib

b = 256  # 位数
q = 2**255 - 19  # 素数 q
l = 2**252 + 27742317777372353535851937790883648493  # 素数 l

# 哈希函数，使用 SHA-512
def H(m):
    """
    计算给定消息的SHA-512哈希值。

    参数:
    m (bytes): 要进行哈希计算的消息。

    返回:
    bytes: 消息的SHA-512哈希值。
    """
    return hashlib.sha512(m).digest()

# 模幂运算，计算 (b^e) % m
def expmod(b, e, m):
    """
    计算 (b^e) % m 的值，使用递归的快速幂算法。

    参数:
    b (int): 底数
    e (int): 指数
    m (int): 模数

    返回:
    int: (b^e) % m 的结果

    示例:
    >>> expmod(2, 10, 1000)
    24

    如果 e == 0，返回 1。
    否则，递归地计算 expmod(b, e // 2, m) 的平方并取模 m。
    如果 e 是奇数，再乘以 b 并取模 m。
    """
    if e == 0:
        return 1
    t = expmod(b, e // 2, m) ** 2 % m  # 使用 `//` 确保 `e` 是整数
    if e & 1:
        t = (t * b) % m
    return t

# 计算 x 的逆元，满足 (x * inv(x)) % q == 1
def inv(x):
    """
    计算给定数值 x 在模 q 下的乘法逆元。

    这是通过使用费马小定理实现的，该定理指出，对于一个素数 q 和一个整数 x，
    x^(q-1) ≡ 1 (mod q)。因此，x^(q-2) ≡ x^(-1) (mod q)。

    参数:
    x (int): 需要计算逆元的整数。

    返回:
    int: x 在模 q 下的乘法逆元。
    """
    return expmod(x, q - 2, q)

d = -121665 * inv(121666)  # 常数 d
I = expmod(2, (q - 1) // 4, q)  # 常数 I

# 根据 y 坐标恢复 x 坐标
def xrecover(y):
    """
    根据给定的 y 值恢复 x 坐标。

    该函数用于从给定的 y 坐标恢复 x 坐标，适用于椭圆曲线密码学中的 Ed25519 算法。

    参数:
    y (int): y 坐标值。

    返回:
    int: 恢复的 x 坐标值。

    注意:
    - 该函数假设存在全局变量 d 和 q，它们分别是 Ed25519 曲线的常数。
    - inv 函数用于计算模逆。
    - expmod 函数用于计算模幂。
    - I 是虚数单位的平方根。
    """
    xx = (y * y - 1) * inv(d * y * y + 1)
    x = expmod(xx, (q + 3) // 8, q)
    if (x * x - xx) % q != 0:
        x = (x * I) % q
    if x % 2 != 0:
        x = q - x
    return x

By = 4 * inv(5)  # 基点 B 的 y 坐标
Bx = xrecover(By)  # 基点 B 的 x 坐标
B = [Bx % q, By % q]  # 基点 B

# 爱德华兹曲线上的点加法
def edwards(P, Q):
    """
    计算爱德华曲线上的点加法。

    参数:
    P (tuple): 第一个点 (x1, y1)。
    Q (tuple): 第二个点 (x2, y2)。

    返回:
    list: 结果点 (x3, y3)，其中 x3 和 y3 都是模 q 的结果。

    公式:

    注意:
    - inv 表示求逆运算。
    - d 是爱德华曲线的常数参数。
    - q 是模数。
    """
    x1, y1 = P
    x2, y2 = Q
    x3 = (x1 * y2 + x2 * y1) * inv(1 + d * x1 * x2 * y1 * y2)
    y3 = (y1 * y2 + x1 * x2) * inv(1 - d * x1 * x2 * y1 * y2)
    return [x3 % q, y3 % q]

# 标量乘法，计算 e * P
def scalarmult(P, e):
    """
    对给定的点 P 进行标量乘法运算，计算 e * P。

    参数:
    P (list): 椭圆曲线上的一个点，表示为 [x, y]。
    e (int): 标量值。

    返回:
    list: 结果点 Q，表示为 [x, y]。

    说明:
    该函数使用二进制方法进行标量乘法运算。初始化结果点 Q 为无穷远点 [0, 1]。
    在循环中，如果 e 的最低位为 1，则将当前点 P 累加到 Q 上。然后将 P 自加（倍点运算），
    并将 e 右移一位（除以 2）。循环结束后返回结果点 Q。
    """
    Q = [0, 1]  # 初始化为无穷远点
    while e > 0:
        if e & 1:
            Q = edwards(Q, P)  # 累加
        P = edwards(P, P)  # 自加（倍点运算）
        e //= 2
    return Q

# 将整数编码为字节
def encodeint(y):
    """
    将整数编码为字节序列。

    参数:
    y (int): 要编码的整数。

    返回:
    bytes: 编码后的字节序列。
    """
    bits = [(y >> i) & 1 for i in range(b)]
    return bytes([sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b//8)])

# 将点编码为字节
def encodepoint(P):
    """
    将给定的点P编码为字节序列。

    参数:
    P (tuple): 一个包含两个整数 (x, y) 的元组，表示点的坐标。

    返回:
    bytes: 编码后的字节序列。

    说明:
    该函数首先将y坐标的每一位提取出来，形成一个位列表，然后将x坐标的最低位添加到该列表的末尾。
    最后，将这些位打包成字节序列并返回。
    """
    x, y = P
    bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
    return bytes([sum([bits[i * 8 + j] << j for j in range(8)]) for i in range(b // 8)])

# 获取哈希值的第 i 位
def bit(h, i):
    """
    返回字节数组 `h` 中第 `i` 位的值（0 或 1）。

    参数:
    h (bytes): 字节数组。
    i (int): 要检查的位的索引。

    返回:
    int: 位的值（0 或 1）。
    """
    return (h[i // 8] >> (i % 8)) & 1  # 修正 `ord()`

# 生成公钥
def publickey(sk):
    """
    生成给定私钥的公钥。

    参数:
    sk (bytes): 私钥，字节序列。

    返回:
    bytes: 公钥，字节序列。

    该函数首先计算私钥的哈希值，然后根据哈希值生成一个标量 a。
    使用标量 a 和基点 B 进行标量乘法运算，得到点 A。
    最后将点 A 编码为字节序列并返回。

    注意:
    - 函数依赖于外部定义的 H、bit、scalarmult、B 和 encodepoint 函数或变量。
    - b 是一个全局变量，表示位数。
    """
    h = H(sk)
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    print(a)
    A = scalarmult(B, a)
    print(A)
    return encodepoint(A)

# 计算消息的哈希值
def Hint(m):
    """
    计算消息 m 的哈希值，并返回哈希值的位的加权和。

    参数:
    m (str): 输入消息。

    返回:
    int: 哈希值的位的加权和。

    该函数首先计算消息 m 的哈希值 h，然后计算 h 的每个位的加权和。
    加权和的计算方式是将每个位乘以 2 的该位索引次方，然后求和。
    """
    h = H(m)
    return sum(2 ** i * bit(h, i) for i in range(2 * b))

# 生成签名
def signature(m, sk, pk):
    """
    生成Ed25519签名。

    参数:
    m (bytes): 要签名的消息。
    sk (bytes): 私钥。
    pk (bytes): 公钥。

    返回:
    bytes: 签名，由 R 和 S 组成。

    过程:
    1. 计算私钥哈希 h。
    2. 从 h 中提取部分位生成私钥 a。
    3. 使用 h 的一部分和消息 m 生成随机数 r。
    4. 计算随机点 R = r * B。
    5. 计算哈希值 c = Hint(encodepoint(R) + pk + m)。
    6. 计算签名 S = (r + c * a) % l。
    7. 返回签名 encodepoint(R) + encodeint(S)。

    注意:
    - r 对于每条不同的消息 m 都是不同的，确保签名的唯一性。
    - S 包含了随机数 r 和私钥 a 的隐藏计算，保证签名的安全性。
    """
    h = H(sk)
    a = 2 ** (b - 2) + sum(2 ** i * bit(h, i) for i in range(3, b - 2))
    #取 h 的部分（h[b // 8 : b // 4]）作为一个随机种子 结合m 生成hash值
    #这样 r 对于每条不同的 m 都是不同的，确保签名的唯一性。
    r = Hint(h[b // 8 : b // 4] + m)
    #随机值生成随机点
    R = scalarmult(B, r)
    #计算 c = Hint(encodepoint(R) + pk + m)，即对 R、公钥 pk 和消息 m 进行哈希。
    #计算 S = (r + c * a) % l，这里：
    #       c * a 相当于用私钥 a 进行了一次隐藏的计算。
    #       r 作为随机数，确保 S 是不可预测的。
    #       mod l 使得 S 处于有限域 l 内，保证安全性。
    S = (r + Hint(encodepoint(R) + pk + m) * a) % l
    print("R:",R)
    print("S:",S)
    return encodepoint(R) + encodeint(S)

# 检查点是否在曲线上
def isoncurve(P):
    """
    检查给定点 P 是否在曲线上。

    参数:
    P (tuple): 包含点的 x 和 y 坐标的元组。

    返回:
    bool: 如果点在曲线上则返回 True，否则返回 False。
    """
    x, y = P
    return (-x * x + y * y - 1 - d * x * x * y * y) % q == 0

# 将字节解码为整数
def decodeint(s):
    """
    解码整数

    该函数将字节串 `s` 解码为一个整数。它通过对每个字节的位进行加权求和来实现这一点。

    参数:
    s (bytes): 要解码的字节串

    返回:
    int: 解码后的整数
    """
    return sum(2**i * bit(s,i) for i in range(0,b))

# 将字节解码为点
def decodepoint(s):
    """
    解码给定的字节串以恢复椭圆曲线上的点。

    参数:
    s (bytes): 要解码的字节串。

    返回:
    list: 椭圆曲线上的点 [x, y]。

    异常:
    Exception: 如果解码的点不在曲线上，则抛出异常。
    """
    y = sum(2**i * bit(s,i) for i in range(0,b-1))
    x = xrecover(y)
    if x & 1 != bit(s,b-1): x = q-x
    P = [x,y]
    if not isoncurve(P): raise Exception("decoding point that is not on curve")
    return P

# 验证签名
def checkvalid(s, m, pk) -> bool:
    """
    验证给定的签名是否有效。
    参数:
    s (bytes): 签名，长度应为 b // 4。
    m (bytes): 消息。
    pk (bytes): 公钥，长度应为 b // 8。
    返回:
    bool: 如果签名有效，返回 True；否则抛出异常。
    异常:
    Exception: 当签名长度或公钥长度不正确时抛出。
    Exception: 当签名验证失败时抛出。
    """
    if len(s) != b // 4:
        raise Exception("Signature length is wrong")
    if len(pk) != b // 8:
        raise Exception("Public-key length is wrong")
    #----------------签名的前半部分和后半部分--------------------------
    R = decodepoint(s[: b // 8])  # s取前32位 (反向计算随机点)
    S = decodeint(s[b // 8 : b // 4]) # s取32到64位
    #-----------------公钥和挑战值-----------------------------------
    A = decodepoint(pk)           # pk为32位 (计算公钥点)
    h = Hint(encodepoint(R) + pk + m) # 计算挑战值
    #-----------------验证签名---------------------------------------
    #计算 c = Hint(encodepoint(R) + pk + m)，即对 R、公钥 pk 和消息 m 进行哈希。
    #计算 S = (r + c * a) % l，这里：
    #       c * a 相当于用私钥 a 进行了一次隐藏的计算。
    #       r 作为随机数，确保 S 是不可预测的。
    #       mod l 使得 S 处于有限域 l 内，保证安全性。
    #       S⋅B=R+c⋅A
    #       S=(r + Hint(encodepoint(R) + pk + m) * a) % l
    #       A=B*a
    #       S*B=B*r+c.B*a=B*(r+c*a)
    #       B*S=B*(r+c*a)
    #       B*r+B*a*c=B*(r+c*a)
    if scalarmult(B, S) != edwards(R, scalarmult(A, h)):
        raise Exception("Signature does not pass verification")
    return True

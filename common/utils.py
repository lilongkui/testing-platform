from passlib.handlers.pbkdf2 import pbkdf2_sha256
import time
from Crypto import Random
from Crypto.Cipher import AES
from binascii import b2a_hex, unhexlify

from config.configure import settings


#################user_token###############
def encryption_token(data):
    """
    加密token
    :param data:{user_id-expires_timestamp}
    :return:
    """
    # 生成长度等于AES块大小的不可重复的密钥向量（随机盐）
    iv = Random.new().read(AES.block_size)
    # 使用key和iv初始化AES对象, 使用MODE_CFB模式
    cipher = AES.new(settings.TOKEN_SECRET_KEY.encode(), AES.MODE_CFB, iv)
    # 加密的明文长度必须为16的倍数，如果长度不为16的倍数，则需要补足为16的倍数
    ciphertext = iv + cipher.encrypt(data.encode())
    # 返回16进制的字符串
    return b2a_hex(ciphertext).decode()


def generate_token(user_id, expires=settings.TOKEN_EXPIRE):
    """
    生成token
    :param user_id: 用户id
    :param expires: 过期时间，单位秒
    :return:
    """
    data = f'{user_id}-{int(time.time()) + expires}'
    return encryption_token(data)


def decrypt_token(user_token):
    """
    解密token
    :param user_token:
    :return:
    """
    # 把16进制的字符串转为字节串
    token = unhexlify(user_token)
    # 解密的话要用key和iv生成新的AES对象，token的前16位为iv密钥向量
    decrypt = AES.new(settings.TOKEN_SECRET_KEY.encode(), AES.MODE_CFB, token[:16])
    # 使用新生成的AES对象，将加密的密文解密，token的16位之后为需要解密的密文
    return decrypt.decrypt(token[16:]).decode()


def verification_token(user_token):
    """
    验证token
    :param user_token:
    :return:
    """
    from common.exception import BusinessException_401
    try:

        original = decrypt_token(user_token)
        user_id, expires = original.split('-')
        if int(time.time()) > int(expires):
            raise BusinessException_401()
        return user_id
    except Exception as e:
        raise BusinessException_401(message=f"请重新登录")


################加解密用户密码###################
def en_password(origin_password: str):
    """
    密码加密
    :param origin_password: 需要加密的密码
    :return: 加密后的密码
    """
    return pbkdf2_sha256.hash(origin_password)


def check_password(origin_password: str, encode_password: str):
    """
    密码校验
    :param origin_password: 用户输入的密码
    :param encode_password: 数据库存储的加密密码
    :return: Boolean
    """
    return pbkdf2_sha256.verify(origin_password, encode_password)


def id_str2int_list(id_str: str, split=","):
    """
    把str转换成数字列表，主要用于根据模型ID批量操作
    :param split:分隔符
    :param id_str: "1,2,3,4"
    :return:
    """
    return [int(item) for item in id_str.split(split)]


if __name__ == '__main__':
    print(generate_token(100))

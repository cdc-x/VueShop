import hashlib
from django.conf import settings


def make_hash(key, salt=settings.SECRET_KEY):
    m = hashlib.md5()
    m.update(salt.encode('utf-8'))  # 对密码加盐
    m.update(key.encode('utf-8'))
    return m.hexdigest()

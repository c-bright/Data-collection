
import redis
from typing import Optional
import json

class RedisClient:
    def __init__(self, host='192.168.211.132', port=6379, db=0, password=None):
        try:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,  # 自动解码字符串
                socket_connect_timeout=5,  # 连接超时
                socket_timeout=5,  # 套接字超时
                health_check_interval=30  # 健康检查间隔
            )
            # 测试连接
            self.client.ping()
            print(f"Redis连接成功: {host}:{port}")
        except redis.ConnectionError as e:
            print(f"Redis连接失败: {host}:{port}, 错误: {e}")
            self.client = None

    def set(self, key: str, value: str, expire: int = None):
        """设置键值对"""
        if self.client:
            return self.client.set(key, value, ex=expire)
        return None

    def get(self, key: str):
        """获取键值"""
        if self.client:
            return self.client.get(key)
        return None

    def set_json(self, key: str, obj: dict, expire: int = None):
        """设置JSON对象"""
        if self.client:
            return self.client.set(key, json.dumps(obj, ensure_ascii=False), ex=expire)
        return None

    def get_json(self, key: str) -> Optional[dict]:
        """获取JSON对象"""
        if self.client:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        return None

    def delete(self, key: str):
        """删除键"""
        if self.client:
            return self.client.delete(key)
        return None

    def exists(self, key: str):
        """检查键是否存在"""
        if self.client:
            return self.client.exists(key)
        return False

    def expire(self, key: str, seconds: int):
        """设置过期时间"""
        if self.client:
            return self.client.expire(key, seconds)
        return None

    def hset(self, name: str, key: str, value: str):
        """设置哈希表字段"""
        if self.client:
            return self.client.hset(name, key, value)
        return None

    def hget(self, name: str, key: str):
        """获取哈希表字段"""
        if self.client:
            return self.client.hget(name, key)
        return None

    def hgetall(self, name: str):
        """获取哈希表所有字段"""
        if self.client:
            return self.client.hgetall(name)
        return {}

    def lpush(self, key: str, *values):
        """左侧插入列表元素"""
        if self.client:
            return self.client.lpush(key, *values)
        return None

    def lrange(self, key: str, start: int, end: int):
        """获取列表范围内的元素"""
        if self.client:
            return self.client.lrange(key, start, end)
        return []
import json

import redis


class RedisManager:

    redis = redis.Redis()

    @classmethod
    def save(cls, user_id, book):
        book_id = str(book.get("id"))
        cls.redis.hset(str(user_id), book_id, json.dumps(book))

    @classmethod
    def all(cls, user_id: str):
        return cls.redis.hgetall(user_id)


if __name__ == '__main__':
    obj = redis.Redis()
    print(obj.keys("*"))
    print(obj.get(b"6"))
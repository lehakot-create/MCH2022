import redis
import json

from new_parser.parser.producersMO_parse import read_from_redis


r = redis.StrictRedis(decode_responses=True)


def test_read_from_redis():
    record = {'url': 'yandex.ru',
                   'processed': 'false'}
    rval = json.dumps(record)
    r.set('9999', rval)
    result = read_from_redis(9999)
    assert result == {'url': 'yandex.ru',
                   'processed': 'false'}

    r.set('99999', 123)
    result = read_from_redis(99999)
    assert result == None


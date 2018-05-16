import sys
import os
sys.path.append('C:/Users/zheng/Desktop/lagou/lagou_server')
os.environ['DJANGO_SETTINGS_MODULE']="lagou_server.settings"

from django.core.cache import cache


def my_cache(func):
    """自定义缓存"""
    func_name = func.__name__

    def inner(*args, **kwargs):
        result = cache.get(func_name, None)
        if result is None:
            print(func_name)
            result = func(*args, **kwargs)
            cache.set(func_name, result)
        return result

    return inner



@my_cache
def test_cache(a):
    print(a)
    return '123%s' % a

if __name__ == '__main__':
    cache.set('test_cache','12345')
    print(test_cache(1))
    import time
    print(test_cache(2))
    time.sleep(12)
    print(test_cache(3))

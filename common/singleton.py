import threading

"""
单例设计模式基类，继承该类的类将会是单例模式
"""
class Singleton:
    __lock=threading.Lock()
    __instance=None
    def __new__(cls, *args, **kwargs):

        if not cls.__instance:
            cls.__lock.acquire()

            if not cls.__instance:
                cls.__instance=super().__new__(cls)
            cls.__lock.release()
        return cls.__instance
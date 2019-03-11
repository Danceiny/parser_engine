#!/usr/bin/env python
# -*- coding:utf-8 -*-

# https://github.com/reyoung/singleton
__author__ = ['reyoung', 'danceiny']

from threading import Lock


class Singleton(object):
    """
    The Singleton class decorator.
    Like:
        from singleton.singleton import Singleton

        @Singleton
        class IntSingleton(object):
            def __init__(self):
                pass
    Use IntSingleton() get the instance
    """

    def __init__(self, cls):
        """
        :param cls: decorator class type
        """
        self.__cls = cls
        self.__instance = None

    def instance(self):
        """
        Get singleton instance
        :return: instance object
        """
        if not self.is_initialized():
            self.initialize()
        return self.__instance

    def initialize(self, *args, **kwargs):
        """
        Initialize singleton object if it has not been initialized
        :param args: class init parameters
        :param kwargs: class init parameters
        """
        if not self.is_initialized():
            self.__instance = self.__cls(*args, **kwargs)

    def is_initialized(self):
        """
        :return: true if instance is initialized
        """
        return self.__instance is not None

    def __call__(self, *args, **kwargs):
        if not self.is_initialized():
            self.initialize(*args, **kwargs)
        return self.__instance

    def __instancecheck__(self, inst):
        """
        Helper for isinstance check
        """
        return isinstance(inst, self.__cls)

    def __getattr__(self, item):
        return getattr(self.__instance, item)


class ThreadSafeSingleton(object):
    def __init__(self, cls):
        self.__cls = cls
        self.__instance = None
        self.__mutex = Lock()

    def is_initialized(self):
        self.__mutex.acquire()
        try:
            return self.__instance is not None
        finally:
            self.__mutex.release()

    def instance(self):
        self.__mutex.acquire()
        try:
            if self.__instance is None:
                self.__instance = self.__cls()
            return self.__instance
        finally:
            self.__mutex.release()

    def __call__(self, *args, **kwargs):
        self.__mutex.acquire()
        try:
            if self.__instance is None:
                self.__instance = self.__cls(*args, **kwargs)
        finally:
            self.__mutex.release()
            return self.__instance

    def __instancecheck__(self, inst):
        """
        Helper for isinstance check
        """
        return isinstance(inst, self.__cls)

    def __getattr__(self, item):
        return getattr(self.__instance, item)

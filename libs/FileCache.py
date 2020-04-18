import os
import hashlib
import pickle


class FileCache:
    def __init__(self, cache_dir: str):
        """
        Init file cache.

        :param str cache_dir:
        """
        self._dir = cache_dir

    @staticmethod
    def __md5(s: str):
        """
        md5

        :param str s: source value
        :return: str
        """
        m = hashlib.md5()
        m.update(s.encode('utf-8'))
        return m.hexdigest()

    def __filename(self, key: str):
        """
        Generate full path to file via key.

        :param str key: key name
        :return: str
        """
        return os.path.join(self._dir, '{}.cache'.format(self.__md5(key)))

    def put(self, key: str, data):
        """
        Cache a key to file.

        :param str key: key name
        :param data: value
        :return: str
        """
        path_to_file = self.__filename(key)

        with open(path_to_file, 'wb') as fp:
            pickle.dump(data, fp)

        return path_to_file

    def get(self, key: str, default=None):
        """
        Read cache from file.

        :param str key: key name
        :param default: default value
        :return:
        """
        path_to_file = self.__filename(key)

        if not os.path.exists(path_to_file):
            return default

        with open(path_to_file, 'rb') as fp:
            data = pickle.load(fp)

        return data

    def pull(self, key: str, default=None):
        """
        Get and forget.

        :param str key: key name
        :param default: default value
        :return:
        """
        data = self.get(key=key, default=default)
        self.forget(key=key)
        return data

    def forget(self, key: str):
        """
        Forget, remove the cache file.

        :param str key: key name
        :return: bool
        """
        path_to_file = self.__filename(key)

        if os.path.exists(path_to_file):
            os.remove(path_to_file)
            return True
        return False

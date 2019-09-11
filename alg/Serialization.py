import struct
import pickle

class Serialization(object):

    def __init__(self):
        pass

    @staticmethod
    def dump(obj):
        _ser = pickle.dumps(obj, 0)
        return (len(_ser), _ser)

    @staticmethod
    def restore(_ser):
        return pickle.loads(_ser)

    pass

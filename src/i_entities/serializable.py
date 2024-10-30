import abc

class Serializable(metaclass=abc.ABCMeta):
    """
    Base class for serialization and deserialization.
    """

    def serialize(self):
        """
        Serialize the object to a dictionary.
        """
        data = {}
        for key, value in self.__dict__.items():
            # If the value is another Serializable object, recursively serialize it
            if isinstance(value, Serializable):
                data[key] = value.serialize()
            else:
                data[key] = value
        return data

    @classmethod
    def deserialize(cls, data):
        """
        Deserialize a dictionary into an instance of the class.
        """
        obj = cls.__new__(cls)  # Create an instance without calling __init__
        for key, value in data.items():
            attr = getattr(cls, key, None)
            # If the attribute is an object, call deserialize recursively
            if isinstance(attr, Serializable):
                setattr(obj, key, attr.deserialize(value))
            else:
                setattr(obj, key, value)
        return obj
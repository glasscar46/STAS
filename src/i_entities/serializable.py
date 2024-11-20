import abc

class Serializable(metaclass=abc.ABCMeta):
    """
    Base class for objects that support serialization and deserialization.

    This class provides methods to convert an object into a dictionary 
    (serialization) and to reconstruct an object from a dictionary (deserialization).
    Any class that inherits from `Serializable` will automatically gain the ability 
    to serialize and deserialize its instances.
    """

    def serialize(self):
        """
        Serializes the object to a dictionary.

        This method recursively converts the object and its attributes into a dictionary 
        representation. If an attribute is another `Serializable` object, it will call 
        the `serialize` method on that object as well.

        Returns:
            dict: A dictionary representation of the object.
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
        Deserializes a dictionary into an instance of the class.

        This method reconstructs an instance of the class from a dictionary 
        representation. If any attribute is a `Serializable` object, it will recursively 
        call the `deserialize` method on that attribute.

        Args:
            data (dict): The dictionary representation of the object.

        Returns:
            Serializable: An instance of the class with attributes populated from the dictionary.
        """
        if data is None:
            return None
        obj = cls.__new__(cls)  # Create an instance without calling __init__
        for key, value in data.items():
            attr = getattr(cls, key, None)
            # If the attribute is an object, call deserialize recursively
            if isinstance(attr, Serializable):
                setattr(obj, key, attr.deserialize(value))
            else:
                setattr(obj, key, value)
        return obj

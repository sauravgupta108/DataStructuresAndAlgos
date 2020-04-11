"""
This module provides functionality to create 1-Dimensional arrays using "ctypes" module.
"""

from ctypes import py_object, c_int32, c_double, c_char_p


class BaseArray(object):
    """
    This class provides the basic functionality (like getitem, setitem, clear array etc.)
    to different kind of arrays. This class cannot be instantiated directly.
    """
    def __new__(cls, *args, **kwargs):
        if cls is BaseArray:
            raise TypeError("Cannot instantiate class 'BaseArray'")
        return super(BaseArray, cls).__new__(cls)

    def __init__(self, array_elems, length):
        self.__array_elems = array_elems
        self.__array_len = length
        self.__iter_cur_index = 0

    def __getitem__(self, index):
        """
        :param index:
        :return: array's element at index
        """
        try:
            if not (0 <= index < self.__array_len):
                raise IndexError("Index out of range")
        except (TypeError, ValueError):
            raise ValueError("Invalid index. It must be a positive integer")
        return self.__array_elems[index]

    def __setitem__(self, index, value):
        """
        Set value of element at index
        :param index:
        :param value:
        :return: Boolean
        """
        try:
            if not (0 <= index < self.__array_len):
                raise IndexError("Index out of range")
        except (TypeError, ValueError):
            raise ValueError("Invalid index. It must be a positive integer")
        self.__array_elems[index] = value

    def __len__(self):
        return self.__array_len

    def __iter__(self):
        return self

    def __next__(self):
        if self.__iter_cur_index < self.__array_len:
            next_val = self.__array_elems[self.__iter_cur_index]
            self.__iter_cur_index += 1
            return next_val
        else:
            self.__iter_cur_index = 0
            raise StopIteration

    def reset(self, default=None):
        """
        Set all elements of array to None.
        :return: None
        """
        for i in range(self.__array_len):
            self.__array_elems[i] = default

    def set_all_to(self, value):
        """
        Set all array elements a common value
        :param value:
        :return: None
        """
        for i in range(self.__array_len):
            self.__array_elems[i] = value


class GenericArray(BaseArray):
    """
    Class to implement generic array
    """
    def __init__(self, size):
        assert type(size) == int and size > 0, "Invalid array size provided"

        self.__gen_array_size = size
        self.__gen_array_type = py_object * self.__gen_array_size
        self.__gen_array = self.__gen_array_type()

        super(GenericArray, self).__init__(self.__gen_array, self.__gen_array_size)
        self.reset()

    def reset(self, default=None):
        default = None
        super(GenericArray, self).reset(default)


class IntArray(BaseArray):
    """
    Class to implement integer array.
    """
    def __init__(self, size):
        assert type(size) == int and size > 0, "Invalid array size provided"

        self.__gen_array_size = size
        self.__gen_array_type = c_int32 * self.__gen_array_size
        self.__gen_array = self.__gen_array_type()

        super(IntArray, self).__init__(self.__gen_array, self.__gen_array_size)
        self.reset(0)

    def __setitem__(self, index, value):
        try:
            super(IntArray, self).__setitem__(index, int(value))
        except ValueError:
            raise ValueError("Value must be an Integer")

    def reset(self, default=None):
        super(IntArray, self).reset(0)

    def set_all_to(self, default_value=0):
        try:
            super(IntArray, self).set_all_to(int(default_value))
        except ValueError:
            raise ValueError("Value must be an Integer")


class FloatArray(BaseArray):
    """
    Class to implement integer array.
    """
    def __init__(self, size):
        assert type(size) == int and size > 0, "Invalid array size provided"

        self.__gen_array_size = size
        self.__gen_array_type = c_double * self.__gen_array_size
        self.__gen_array = self.__gen_array_type()

        super(FloatArray, self).__init__(self.__gen_array, self.__gen_array_size)
        self.reset(0.0)

    def __setitem__(self, index, value):
        try:
            super(FloatArray, self).__setitem__(index, float(value))
        except ValueError:
            raise ValueError("Value must be a Decimal Number")

    def set_all_to(self, default_value=0.0):
        try:
            super(FloatArray, self).set_all_to(float(default_value))
        except ValueError:
            raise ValueError("Value must be a Decimal Number")

    def reset(self, default=0.0):
        super(FloatArray, self).reset(0.0)


class CharArray(BaseArray):
    """
    Class to implement integer array.
    """
    def __init__(self, size):
        assert type(size) == int and size > 0, "Invalid array size provided"

        self.__gen_array_size = size
        self.__gen_array_type = c_char_p * self.__gen_array_size
        self.__gen_array = self.__gen_array_type()

        super(CharArray, self).__init__(self.__gen_array, self.__gen_array_size)
        self.reset()

    def __setitem__(self, index, value):
        if type(value) != str:
            raise TypeError("Value should be single Character")
        else:
            if len(value) != 1:
                raise TypeError("Value should be single Character")
        super(CharArray, self).__setitem__(index, value.encode('utf-8'))

    def __getitem__(self, index):
        value = super(CharArray, self).__getitem__(index)
        return value.decode()

    def __next__(self):
        next_val = super(CharArray, self).__next__()
        return next_val.decode()

    def set_all_to(self, default_value=""):
        if default_value and (type(default_value) != str or len(default_value) != 1):
            raise TypeError("Value should be single Character")
        super(CharArray, self).set_all_to(default_value.encode('utf-8'))

    def reset(self, default=""):
        super(CharArray, self).reset("".encode('utf-8'))

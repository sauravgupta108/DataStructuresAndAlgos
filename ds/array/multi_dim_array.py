"""
This module implements n dimensional arrays of different type.
Concept:
Use generic 1-D array to physically store the elements of the n-D array
by arranging them in order based on size (right to left).
"""

from .array import GenericArray, IntArray, FloatArray, CharArray


class BaseMultiDimensionalArray(object):
    """
    This class implements basic functionality for n-dimensional array. This can not be instantiated.
    """
    def __new__(cls, *args, **kwargs):
        if cls is BaseMultiDimensionalArray:
            raise TypeError("Cannot instantiate class 'BaseArray'")
        return super(BaseMultiDimensionalArray, cls).__new__(cls)

    def __init__(self, size, of_type):
        if not self.__is_valid_size(size):
            raise ValueError("Size should be a tuple with positive values.")
        self.__size = size
        self.__of_type = of_type
        self.__nd_array = self.__initiate_array()

    def __getitem__(self, index):
        """
        :param index:
        :return: array's element at index
        """
        if not self.__is_valid_index(index):
            raise ValueError("Invalid index found")

        pseudo_index = self.__calculate_pseudo_index(index)
        return self.__nd_array[pseudo_index][index[-1]]

    def __setitem__(self, index, value):
        """
        Set value of element at index
        :param index:
        :param value:
        :return: None
        """
        if not self.__is_valid_index(index):
            raise ValueError("Invalid index found")
        pseudo_index = self.__calculate_pseudo_index(index)
        self.__nd_array[pseudo_index][index[-1]] = value

    def __len__(self):
        """
        :return: Total number of elements in array.
        """
        return self.__get_total_number_of_1d_arrays() * self.__size[-1]

    def __iter__(self):
        return self

    def __next__(self):
        # TODO: Iteration logic pending.
        raise StopIteration

    @staticmethod
    def __is_valid_size(size):
        if type(size) != tuple or len(size) == 1:
            return False
        try:
            for i in size:
                if int(i) < 1:
                    return False
        except ValueError:
            return False
        return True

    def __is_valid_index(self, index):
        if type(index) != tuple:
            return False
        if len(self.__size) != len(index):
            return False
        try:
            for i in range(len(self.__size)):
                if not (0 <= int(index[i]) < self.__size[i]):
                    return False
        except ValueError:
            return False
        return True

    def __calculate_pseudo_index(self, index):
        pseudo_index = 0
        total_1d_arrays = self.__get_total_number_of_1d_arrays()
        group_elem = total_1d_arrays
        for i in range(len(self.__size) - 1):
            group_elem = int(group_elem/self.__size[i])
            pseudo_index += (group_elem * index[i])
        return pseudo_index

    def __get_total_number_of_1d_arrays(self):
        result = 1
        # Ignore last element of size as it is the size of each 1-D array.
        for i in self.__size[:-1]:
            result *= i
        return result

    def __initiate_array(self):
        total_number = self.__get_total_number_of_1d_arrays()
        generic_array = GenericArray(total_number)
        for i in range(len(generic_array)):
            if self.__of_type.lower() == "int":
                generic_array[i] = IntArray(self.__size[-1])
            elif self.__of_type.lower() == "float":
                generic_array[i] = FloatArray(self.__size[-1])
            elif self.__of_type.lower() == "char":
                generic_array[i] = CharArray(self.__size[-1])
            else:
                generic_array[i] = GenericArray(self.__size[-1])
        return generic_array

    def size(self):
        """
        :return: Size of array.
        """
        return self.__size

    def reset(self, default=None):
        """
        Set all elements of array to default value (None: Generic, 0: Int, 0.0: Float, "": Char.
        :return: None
        """
        for array in self.__nd_array:
            for i in range(len(array)):
                array[i] = default

    def set_all_to(self, value):
        """
        Set all array elements a common value
        :param value:
        :return: None
        """
        for array in self.__nd_array:
            for i in range(len(array)):
                array[i] = value


class GenericMultiDimensionalArray(BaseMultiDimensionalArray):
    """
    This class implements Generic Multi Dimensional Array.
    """
    def __init__(self, size):
        super(GenericMultiDimensionalArray, self).__init__(size, "gen")

    def reset(self, default=None):
        default = None
        super(GenericMultiDimensionalArray, self).reset(default)


class IntMultiDimensionalArray(BaseMultiDimensionalArray):
    """
    This class implements Integer Multi Dimensional Array.
    """
    def __init__(self, size):
        super(IntMultiDimensionalArray, self).__init__(size, "int")

    def __setitem__(self, index, value):
        try:
            super(IntMultiDimensionalArray, self).__setitem__(index, int(value))
        except ValueError:
            raise ValueError("Value must be an Integer")

    def reset(self, default=None):
        super(IntMultiDimensionalArray, self).reset(0)

    def set_all_to(self, value):
        try:
            super(IntMultiDimensionalArray, self).set_all_to(int(value))
        except ValueError:
            raise ValueError("Value must be an Integer")


class FloatMultiDimensionalArray(BaseMultiDimensionalArray):
    """
    This class implements Integer Multi Dimensional Array.
    """
    def __init__(self, size):
        super(FloatMultiDimensionalArray, self).__init__(size, "float")

    def __setitem__(self, index, value):
        try:
            super(FloatMultiDimensionalArray, self).__setitem__(index, float(value))
        except ValueError:
            raise ValueError("Value must be a Decimal Number")

    def reset(self, default=None):
        super(FloatMultiDimensionalArray, self).reset(0.0)

    def set_all_to(self, value):
        try:
            super(FloatMultiDimensionalArray, self).set_all_to(float(value))
        except ValueError:
            raise ValueError("Value must be a Decimal Number")


class CharMultiDimensionalArray(BaseMultiDimensionalArray):
    def __init__(self, size):
        super(CharMultiDimensionalArray, self).__init__(size, "char")
        self.reset()

    def __getattr__(self, index):
        value = super(CharMultiDimensionalArray, self).__getitem__(index)
        return value.decode()

    def __setitem__(self, index, value):
        if type(value) != str:
            raise TypeError("Value should be single Character")
        else:
            if len(value) != 1:
                raise TypeError("Value should be single Character")
        super(CharMultiDimensionalArray, self).__setitem__(index, value.encode('utf-8'))

    def reset(self, default=None):
        super(CharMultiDimensionalArray, self).reset("".encode('utf-8'))

    def set_all_to(self, value=""):
        if value and (type(value) != str or len(value) != 1):
            raise TypeError("Value should be single Character")
        super(CharMultiDimensionalArray, self).set_all_to(value.encode('utf-8'))

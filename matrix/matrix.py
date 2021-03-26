from typing import Generic,TypeVar,Iterator,Iterable,Callable,Union

T=TypeVar('T')

class Matrix(Generic[T]):
    """Representation of a matrix that support mathematical operations"""
    @classmethod
    def create_matrix(cls,n:int,m:int,function:Callable[[],T]=lambda:.0)->'Matrix[T]':
        """
        Create a matrix using values generated from the given function
        :param n: the rows of the matrix
        :param m: the columns of the matrix
        :param function: a function that returns a value to generate the matrix
        :returns: a new matrix with the given properties
        """
        return Matrix([[function() for _ in range(m)] for _ in range(n)])

    def __init__(self,matrix:Iterable[Iterable[T]]):
        """
        Matrix constructor
        :param matrix: an iterable of iterables to use as a template
        :raises ValueError: if the iterables of matrix have different lengths
        """
        result:tuple[tuple[T,...]]=tuple([tuple([elem for elem in vector]) for vector in matrix])
        for vector in result:
            if len(vector)!=len(result[0]):
                raise ValueError('Matrix arrays have different lengths')
        self._matrix=result

    @property
    def m(self)->int:
        """
        The number of columns
        :returns: the number of columns
        """
        return len(self._matrix[0]) if self.n > 0 else 0

    @property
    def n(self)->int:
        """
        The number of rows
        :return: the number of rows
        """
        return len(self._matrix)

    @property
    def matrix(self)->tuple[tuple[T]]:
        """
        Representation of the matrix as a touple of touples
        :return: the touple of touples
        """
        return self._matrix

    def __getitem__(self, n:int)->'Vector[T]':
        """
        Extract a vector from a matrix row
        :param n: the row number
        :return: the vector
        """
        return Vector(self._matrix[n])

    def __call__(self, m:int)->'Vector[T]':
        """
        Extract a vector from a matrix column
        :param m: the column number
        :return: the vector
        """
        return Vector(map(lambda vector:vector[m], self._matrix))

    def __add__(self, other:'Matrix[T]')->'Matrix[T]':
        """
        Sum two matrix
        :param other: the matrix to sum
        :return: the resulting matrix
        :raises ArithmeticError: if the matrix have different sizes
        """
        if self.n!=other.n or self.m!=other.m:
            raise ArithmeticError('Matrix have different size')
        return Matrix([map(sum,zip(vectors[0],vectors[1])) for vectors in zip(self._matrix, other._matrix)])

    def __neg__(self)->'Matrix[T]':
        """
        A matrix which has all elements negated
        :return: the resulting matrix
        """
        return Matrix([[-num for num in vector] for vector in self._matrix])

    def __sub__(self, other:'Matrix[T]')->'Matrix[T]':
        """
        Subtract two matrix
        :param other: the matrix to subtract
        :return: the resulting matrix
        :raises ArithmeticError: if the matrix have different sizes
        """
        return self+(-other)

    def __invert__(self)->'Matrix[T]':
        """
        Create a matrix with columns and rows inverted
        :return: the resulting matrix
        """
        return Matrix([[self._matrix[i][j] for i in range(self.n)] for j in range(self.m)])

    def __iter__(self)->Iterator['Vector[T]']:
        """
        Iterates over every vector of the matrix
        :return: the iterator of vectors
        """
        return iter(map(Vector, self._matrix))

    def __mul__(self, other)->'Matrix':
        """
        Perform the matrix product between two matrix or multiply every element of the matrix with a constant
        :param other: the matrix or the number to use
        :return: the resulting matrix
        :raises ArithmeticError: if two matrix are used and this matrix hasn't the same number of columns as the other
        matrix
        """
        if isinstance(other,Matrix):
            if self.m!=other.n:
                raise ArithmeticError('Matrix have different size')
            return Matrix([[sum([self._matrix[i][a] * other._matrix[a][j] for a in range(self.m)])
                            for j in range(other.m)] for i in range(self.n)])
        else:
            return Matrix([[elem*other for elem in vector] for vector in self._matrix])

    def __truediv__(self, other)->'Matrix':
        """
        Divide every element of the matrix with a number
        :param other: the number to divide against
        :return: the resulting matrix
        """
        return self*(1/other)

    def __hash__(self)->int:
        """
        Calculate the hash code of the matrix
        :return: the hash code
        """
        return hash(self._matrix)

    def __repr__(self):
        """
        Create a string representation of the matrix
        :return: a string representing the matrix
        """
        result=''
        for i in range(self.n):
            result+='\n|'
            first=True
            for j in range(self.m):
                if not first:
                    result+=' '
                first=False
                result+=str(self._matrix[i][j])
            result+='|'
        return result

    def __eq__(self, other)->bool:
        """
        Check if the given object is equal to this matrix
        :param other: the object to check
        :return: if the two objects are equal
        """
        if not isinstance(other,Matrix) or self.m!=other.m or self.n!=other.n:
            return False
        for i in range(self.n):
            for j in range(self.m):
                if self._matrix[i][j]!=other._matrix[i][j]:
                    return False
        return True


class Vector(Matrix[T],Generic[T]):
    """A single row or column of a matrix"""
    @classmethod
    def create_vector(cls,length:int,function:Callable[[],T]=lambda:.0)->'Vector[T]':
        """
        Create a vector by using a function to generate the values
        :param length: the length of the vector
        :param function: the function to use to generate the values
        :return: the new vector
        """
        return Vector([function() for _ in range(length)])

    def __init__(self,vector:Iterable[T],transposed=False):
        """
        Vector constructor
        :param vector: a list of elements to use to create the matrix or a matrix with a single column or row
        :param transposed: if the matrix should be a column instead of a row
        :raises ValueError: if a matrix is passed and it hasn't a single column or row
        """
        if isinstance(vector,Matrix):
            if vector.n!=1 and vector.m!=1:
                raise ValueError(f"Matrix {vector.n}x{vector.m} isn't a vector")
            super(Vector, self).__init__(vector.matrix)
        else:
            if transposed:
                result=[[elem for elem in vector]]
            else:
                result=[[elem] for elem in vector]
            super(Vector, self).__init__(result)

    @property
    def transposed(self)->bool:
        """
        If the vector is a column instead of a row
        :return: if the vector is a column instead of a row
        """
        return len(self._matrix) == 1

    def __len__(self)->int:
        """
        The length of the vector
        :return: the length of the vector
        """
        return self.m if self.transposed else self.n

    def __add__(self, other:'Vector[T]')->'Vector[T]':
        """
        Sum two vectors together
        :param other: the other vector to sum
        :return: the resulting vector
        :raises ArithmeticError: if the vector have different lengths
        """
        return Vector(super(Vector, self).__add__(other))

    def __sub__(self, other:'Vector[T]')->'Vector[T]':
        """
        Subtract two vectors
        :param other: the other vector to subtract
        :return: the resulting vector
        :raises ArithmeticError: if the vector have different lengths
        """
        return Vector(super(Vector, self).__sub__(other))

    def __getitem__(self, item:int)->T:
        """
        Get an element from the vector
        :param item: the index of the element
        :return: the element
        """
        if self.transposed:
            return self._matrix[0][item]
        else:
            return self._matrix[item][0]

    def __neg__(self)->'Vector[T]':
        """
        Create a vector which has all elements negated
        :return: the resulting vector
        """
        return Vector(super(Vector, self).__neg__())

    def __mul__(self, other)->Union['Vector[T]',T]:
        """
        Multiply this vector with another vector performing a dot product or with a number multiplying every element
        :param other: the vector or the number to use
        :return: the resulting vector
        """
        if isinstance(other,Vector):
            if self.transposed==other.transposed:
                other=~other
            return super(Vector, self).__mul__(other)[0][0]
        else:
            return Vector(super(Vector, self).__mul__(other))

    def __invert__(self)->'Vector[T]':
        """
        Transpose this vector
        :return: the resulting vector
        """
        return Vector(super(Vector, self).__invert__())

    def __iter__(self)->Iterator[T]:
        """
        Iterates over every element of the vector
        :return: the iterator to use
        """
        return iter([self[a] for a in range(len(self))])

class Vector3(Vector[T],Generic[T]):
    """Vector with three elements, useful for 3D physics"""
    def __init__(self,x:T,y:T,z:T):
        """
        3D vector construct
        :param x: the first element of the vector
        :param y: the second element of the vector
        :param z: the third element of the vector
        """
        super(Vector3, self).__init__([x,y,z])

    @property
    def x(self)->T:
        """
        The first element of the vector
        :return: the first element of the vector
        """
        return self[0]

    @property
    def y(self)->T:
        """
        The second element of the vector
        :return: the second element of the vector
        """
        return self[1]

    @property
    def z(self)->T:
        """
        The third element of the vector
        :return: the third element of the vector
        """
        return self[2]

    def __add__(self, other:'Vector3[T]')->'Vector3[T]':
        """
        Sum two 3D vectors together
        :param other: the other 2D vector to use
        :return: the resulting vector
        """
        return Vector3(*super(Vector3, self).__add__(other))

    def __sub__(self, other:'Vector3[T]')->'Vector3[T]':
        """
        Subtract two 3D vectors together
        :param other: the other 3D vector to use
        :return: the resulting vector
        """
        return Vector3(*super(Vector3, self).__sub__(other))

    def __neg__(self)->'Vector3[T]':
        """
        The negative of the vector
        :return: the resulting vector
        """
        return Vector3(*super(Vector3, self).__neg__())

    def __mul__(self, other)->Union['Vector3[T]',T]:
        """
        Multiply two vectors together with a dot product or multiply every element of the vector with a number
        :param other: the 3D vector or the number to use
        :return: the resulting vector
        """
        if isinstance(other,Vector):
            return super(Vector3, self).__mul__(other)
        else:
            return Vector3(*super(Vector3, self).__mul__(other))

    def __repr__(self):
        """
        Create a string representation of this 3D vector
        :return: the string representation of the 3D vector
        """
        return str((self.x,self.y,self.z))

    def __pow__(self, power:'Vector3', modulo=None)->'Vector3':
        """
        Perform the cross product between two 3D vectors
        :param power: the other vector
        :param modulo: unused
        :return: the resulting vector
        """
        return Vector3(self.y*power.z-self.z*power.y,self.z*power.x-self.x*power.z,self.x*power.y-self.y*power.x)

class Vector2(Vector[T],Generic[T]):
    """Vector with two elements, useful for 2D physics"""
    def __init__(self,x:T,y:T):
        """
        2D vector construct
        :param x: the first element of the vector
        :param y: the second element of the vector
        """
        super(Vector2, self).__init__([x,y])

    @property
    def x(self)->T:
        """
        The first element of the vector
        :return: the first element of the vector
        """
        return self[0]

    @property
    def y(self)->T:
        """
        The second element of the vector
        :return: the second element of the vector
        """
        return self[1]

    def __add__(self, other:'Vector2[T]')->'Vector2[T]':
        """
        Sum two 2D vectors together
        :param other: the other 2D vector to use
        :return: the resulting vector
        """
        return Vector2(*super(Vector2, self).__add__(other))

    def __sub__(self, other:'Vector2[T]')->'Vector2[T]':
        """
        Subtract two 2D vectors together
        :param other: the other 2D vector to use
        :return: the resulting vector
        """
        return Vector2(*super(Vector2, self).__sub__(other))

    def __neg__(self)->'Vector2[T]':
        """
        The negative of the vector
        :return: the resulting vector
        """
        return Vector2(*super(Vector2, self).__neg__())

    def __mul__(self, other)->Union['Vector2[T]',T]:
        """
        Multiply two vectors together with a dot product or multiply every element of the vector with a number
        :param other: the 2D vector or the number to use
        :return: the resulting vector
        """
        if isinstance(other,Vector):
            return super(Vector2, self).__mul__(other)
        else:
            return Vector2(*super(Vector2, self).__mul__(other))

    def __repr__(self):
        """
        Create a string representation of this 2D vector
        :return: the string representation of the 2D vector
        """
        return str((self.x,self.y))

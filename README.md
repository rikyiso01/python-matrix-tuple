# python-matrix-tuple
A python matrix implementation with tuple

## Installation

You can install it from [Pypi](https://pypi.org/project/matrix-tuple) or from the [release section](https://github.com/RikyIsola/python-matrix-tuple/releases)

## Usage

Simply import it and start using it

```python3
from matrix_tuple import Matrix

m1 = Matrix([[1, 2], [3, 4], [5, 6]])
m2 = Matrix.create_matrix(3, 2, lambda i, j: 1 + i * 2 + j)
print(m1 + m2)
```

You can read more on the [documentation page](https://rikyisola.github.io/python-matrix-tuple/matrix/matrix.html)

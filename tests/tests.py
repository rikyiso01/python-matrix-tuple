from matrix import Matrix,Vector,Vector3,Vector2
from pytest import raises

class TestMatrix:
    def test_constructor(self):
        Matrix([[0,0,0],[0,0,0],[0,0,0]])
        with raises(ValueError):
            Matrix([[0,0,0],[0,0],[0,0,0]])
        Matrix([])
        Matrix([[],[],[]])

    def test_mn(self):
        assert Matrix([[0,0],[0,0],[0,0]]).sizes==(3,2)
        assert Matrix([]).sizes==(0,0)
        assert Matrix([[],[],[]]).sizes==(3,0)

    def test_get(self):
        assert all(Matrix([[(0,0),(0,1)],[(1,0),(1,1)],[(2,0),(2,1)]])[x][y]==(x,y) for y in range(2) for x in range(3))

    def test_create_matrix(self):
        assert all(Matrix.create_matrix(3,2,lambda i,j:j+i*2)[x][y]==(y+x*2) for y in range(2) for x in range(3))
        assert Matrix.create_matrix(3,0).sizes==(3,0)
        assert Matrix.create_matrix(0,3).sizes==(0,0)

    def test_matrix(self):
        assert all(Matrix.create_matrix(2,3,lambda i,j:j+i*3).matrix[x][y]==(y+x*3) for y in range(3) for x in range(2))

    def test_call(self):
        assert tuple(Matrix.create_matrix(3,1,lambda i,j:i)(0))==(0,1,2)

    def test_equal(self):
        assert Matrix.create_matrix(3,3)==Matrix.create_matrix(3,3)

    def test_add(self):
        assert Matrix.create_matrix(3,3)+Matrix.create_matrix(3,3,lambda i,j:1)==Matrix.create_matrix(3,3,lambda i,j:1)

    def test_neg(self):
        assert -Matrix.create_matrix(3,3,lambda i,j:1)==Matrix.create_matrix(3,3,lambda i,j:-1)

    def test_sub(self):
        assert Matrix.create_matrix(3,3,lambda i,j:1)-Matrix.create_matrix(3,3,lambda i,j:1)==Matrix.create_matrix(3,3)

    def test_invert(self):
        assert ~Matrix.create_matrix(3,2,lambda i,j:j+i*2)==Matrix.create_matrix(2,3,lambda i,j:i+j*2)

    def test_iter(self):
        assert tuple(vector[0] for vector in Matrix([[0],[1],[2]]))==(0,1,2)

# TODO: Finish tests

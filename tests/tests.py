from matrix import Matrix,Vector,Vector3,Vector2
from pytest import raises
from math import pi,sqrt

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

    def test_mul(self):
        assert Matrix([[1,2],[3,4],[5,6]])*Matrix([[-1,-1,-1],[1,1,1]])==Matrix([[1,1,1],[1,1,1],[1,1,1]])
        with raises(ArithmeticError):
            Matrix.create_matrix(3,1)*Matrix.create_matrix(3,1)

    def test_div(self):
        assert Matrix.create_matrix(2,3,lambda i,j:2)/2==Matrix.create_matrix(2,3,lambda i,j:1)

    def test_repr(self):
        assert repr(Matrix.create_matrix(2,2))=='\n|0 0|\n|0 0|'


class TestVector:
    def test_constructor(self):
        Vector([1,2,3])
        Vector([])
        with raises(ValueError):
            Vector(Matrix([[1,2,3],[1,2,3]]))

    def test_length(self):
        assert len(Vector([1,2,3]))==3
        assert len(Vector([]))==0

    def test_transposed(self):
        assert Vector([1,2,3],transposed=True).transposed
        assert not Vector([1,2,3]).transposed
        assert Vector(Matrix([[1,2,3]])).transposed
        assert not Vector(Matrix([[1],[2],[3]])).transposed
        assert Vector([],transposed=True).transposed
        assert not Vector([]).transposed

    def test_get(self):
        assert Vector([1,2,3])[0]==1
        assert Vector([1,2,3],transposed=True)[1]==2

    def test_mul(self):
        assert Vector([1,2,3])*Vector([-1,-1,1])==0
        with raises(ArithmeticError):
            Vector([1,2,3])*Vector([1,2])

    def test_iter(self):
        assert [a for a in Vector([1,2,3])]==[1,2,3]
        assert [a for a in Vector([1,2,3],transposed=True)]==[1,2,3]

    def test_abs(self):
        assert abs(Vector([1,1,1,1]))==2
        assert abs(Vector([1,1,1,1],transposed=True))==2

    def test_unit(self):
        assert Vector([2,0,0]).unit==Vector([1,0,0])
        assert Vector([1,1,1,1]).unit==Vector([.5,.5,.5,.5])
        assert Vector([2,0,0],transposed=True).unit==Vector([1,0,0],transposed=True)
        assert Vector([1,1,1,1],transposed=True).unit==Vector([.5,.5,.5,.5],transposed=True)
        with raises(ArithmeticError):
            print(Vector([0,0,0]).unit)

class TestVector3:
    def test_constructor(self):
        assert tuple(Vector3(1,2,3))==(1,2,3)

    def test_pow(self):
        assert Vector3(1,0,0)**Vector3(0,1,0)==Vector3(0,0,1)

class TestVector2:
    def test_constructor(self):
        assert tuple(Vector2(1,2))==(1,2)

    def test_polar(self):
        assert compare_polar(Vector2(1,0).polar,(1,0))
        assert compare_polar(Vector2(0,2).polar,(2,pi/2))
        assert compare_polar(Vector2(-3,0).polar,(3,pi))
        assert compare_polar(Vector2(0,-4).polar,(4,-pi/2))
        assert compare_polar(Vector2(1,1).polar,(sqrt(2),pi/4))
        with raises(ArithmeticError):
            print(Vector2(0,0).polar)

THRESHOLD=0.00001

def compare_polar(p1:tuple[float,float],p2:tuple[float,float]):
    return p1[0]==p2[0] and p2[1]-THRESHOLD<=p1[1]<=p2[1]+THRESHOLD

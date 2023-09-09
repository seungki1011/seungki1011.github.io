---
layout: post
title:  "Numpy - 1(Introduction)"
author: seungki
categories: [ Numpy ]
image: post_images/numpylogo.png
toc: True
---

---

## Numpy란?

* Numerical Python의 약자
* 과학 계산용 패키지
* N차원 배열 객체, 범용적 데이터 처리 등에 사용 가능한 다차원 컨테이너
* 보로드캐스팅 기능
* 파이썬의 list 자료형과 비슷하지만, 더 빠르고 효율적임
* 반복문 없이 데이터 배열에 대한 처리를 지원
* C, C++, 포트란 등의 언어와 통합 가능

---

## Numpy의 사용법

### Array Dimension

<img src="https://user-images.githubusercontent.com/120040458/218375020-9b3ce42d-4890-465b-8c9f-08d4b48fdfba.png" alt="array_shape1" style="zoom: 50%;" class="center-image"/>

<img src="https://user-images.githubusercontent.com/120040458/218375025-30d3c341-395e-40ec-a86e-390d5ff76b4f.png" alt="numpyarray1" style="zoom:100%;" class="center-image"/>

### Array Shape

#### Array Rank

<img src="https://user-images.githubusercontent.com/120040458/218375599-a55e3abe-f3f6-4521-9630-8063e8919d4e.PNG" alt="array_rank" style="zoom:67%;" class="center-image"/>



#### Vector

<img src="https://user-images.githubusercontent.com/120040458/218376254-3258714f-250b-4fc9-ad63-443ed7c16060.PNG" alt="vector" style="zoom:100%;" class="center-image"/>



#### Matrix

<img src="https://user-images.githubusercontent.com/120040458/218376251-715ad6f0-75cd-425b-a046-a241e612d62c.PNG" alt="matrix" style="zoom:100%;" class="center-image"/>



#### 3rd order tensor

<img src="https://user-images.githubusercontent.com/120040458/218376253-dd0e881c-4b48-46ef-84d1-70e3f747680f.PNG" alt="3rdorder" style="zoom:100%;" class="center-image"/>

---

## 배열 생성

### 리스트로 배열 만들기

* 1차원 배열

```python
a1 = np.array([7,2,9,10])
print(a1)
print(type(a1))
print(a1.shape) # 배열의 모양
print(a1[0],a1[1],a1[2],a1[3]) # 리스트 처럼 인덱스로 접근 가능
a1[0]=8 # 인덱스로 접근해서 수정 가능
print(a1)
```

    [ 7  2  9 10]
    <class 'numpy.ndarray'>
    (4,)
    7 2 9 10
    [ 8  2  9 10]



* 2차원 배열

```python
a2 = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(a2)
print(a2.shape)
print(a2[0,0],a2[1,1],a2[2,2])
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
    (3, 3)
    1 5 9



* 3차원 배열

```python
a3 = np.array([[[1,2,3],[4,5,6],[7,8,9]],
              [[1,2,3],[4,5,6],[7,8,9]],
              [[1,2,3],[4,5,6],[7,8,9]]])
print(a3)
print(a3.shape)
```

    [[[1 2 3]
      [4 5 6]
      [7 8 9]]
    
     [[1 2 3]
      [4 5 6]
      [7 8 9]]
    
     [[1 2 3]
      [4 5 6]
      [7 8 9]]]
    (3, 3, 3)



### 배열 생성 및 초기화

#### zeros()

* 모든 요소를 0으로 초기화

```python
np.zeros(10)
```


    array([0., 0., 0., 0., 0., 0., 0., 0., 0., 0.])



#### ones()

* 모든 요소를 1로 초기화

```python
np.ones(8)
```


    array([1., 1., 1., 1., 1., 1., 1., 1.])

```python
np.ones((3,3)) # shape를 명시해서 2차원 형태로도 만들 수 있음
```


    array([[1., 1., 1.],
           [1., 1., 1.],
           [1., 1., 1.]])



#### full()

* 모든 요소를 지정한 값으로 초기화

```python
np.full((3,3), 1.25)
```


    array([[1.25, 1.25, 1.25],
           [1.25, 1.25, 1.25],
           [1.25, 1.25, 1.25]])



#### eye()

* 단위행렬(identity matrix) 생성

```python
np.eye(4) # 단위 행렬은 정사각행렬임(크기 n만 명시해도 됨)
```


    array([[1., 0., 0., 0.],
           [0., 1., 0., 0.],
           [0., 0., 1., 0.],
           [0., 0., 0., 1.]])



* eye()에서 k의 값을 정의하면 어느 대각선에 1을 넣을건지 정할 수 있음

```python
np.eye(4,k=1,dtype=int)
```

```
array([[0, 1, 0, 0],
       [0, 0, 1, 0],
       [0, 0, 0, 1],
       [0, 0, 0, 0]])
```

```python
np.eye(4,k=-1,dtype=int)
```

```
array([[0, 0, 0, 0],
       [1, 0, 0, 0],
       [0, 1, 0, 0],
       [0, 0, 1, 0]])
```



#### identity()

* 2차원 nxn 정방단위행렬 ndarray 객체 반환

```python
np.identity(3)
```

```
array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]])
```



#### diag()

* 대각 행렬의 값을 추출함

```python
a = np.arange(9).reshape(3,3)
print(a)
np.diag(a)
```

```
[[0 1 2]
 [3 4 5]
 [6 7 8]]
 
array([0, 4, 8])
```

* k로 대각선 정할 수 있음

```python
np.diag(a,k=1)
```

```
array([1, 5])
```



#### tri()

* 삼각행렬 생성

```python
np.tri(3)
```


    array([[1., 0., 0.],
           [1., 1., 0.],
           [1., 1., 1.]])



#### empty()

* 초기화되지 않은 배열 생성

```python
np.empty(8) # 초기화를 하지 않기 때문에 빠름, 대신 기존 메모리에 존재하던 값이 나옴
```


    array([1., 1., 1., 1., 1., 1., 1., 1.])



#### _like()

* 지정된 배열과 shape가 같은 행렬 생성

  

  - np.zeros_like()

    ```python
    test_array1 = [1,2,3,4,5]
    print(test_array1)
    np.zeros_like(test_array1) # test_array1과 shape가 동일한 zeros 생성
    ```

        [1, 2, 3, 4, 5]
        
        array([0, 0, 0, 0, 0])

  

  * np.ones_like()

    ```python
    test_array2 = [[1,2,3,4],[5,6,7,8]]
    print(test_array2)
    np.ones_like(test_array2)
    ```

        [[1, 2, 3, 4], [5, 6, 7, 8]]
        
        array([[1, 1, 1, 1],
               [1, 1, 1, 1]])



### 생성한 값으로 배열 생성

#### arange()

* 정수 범위로 배열 생성

```python
np.arange(0,30,2) # 0부터 30전까지 step은 2로
```


    array([ 0,  2,  4,  6,  8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28])



#### linspace()

* 범위 내에서 균들 간격의 배열 생성

```python
np.linspace(0,10,5) # 0부터 10까지 균등하게 5개의 간격으로 나눔
```


    array([ 0. ,  2.5,  5. ,  7.5, 10. ])

```python
np.linspace(0,1,5) # 0부터 1까지 균등하게 5개의 간격으로 나눔
```


    array([0.  , 0.25, 0.5 , 0.75, 1.  ])



#### logspace()

* 범위 내에서 균등간격으로 로그 스케일로 배열 생성

```python
np.logspace(0.1,1,20)
```


    array([ 1.25892541,  1.40400425,  1.565802  ,  1.74624535,  1.94748304,
            2.1719114 ,  2.42220294,  2.70133812,  3.0126409 ,  3.35981829,
            3.74700446,  4.17881006,  4.66037703,  5.19743987,  5.79639395,
            6.46437163,  7.2093272 ,  8.04013161,  8.9666781 , 10.        ])



### 랜덤값으로 배열 생성

#### random.random()

* 랜덤한 수의 배열 생성

```python
np.random.random((3,3))
```


    array([[0.38789798, 0.42888851, 0.03252684],
           [0.23912518, 0.92076065, 0.70782295],
           [0.54324963, 0.67355909, 0.20873986]])



#### random.randint()

* 일정 구간의 랜덤 정수의 배열 생성

```python
np.random.randint(0,10,(4,4)) # 0부터 10까지의 숫자범위에서 4by4에서 랜덤 정수의 배열
```


    array([[9, 2, 5, 7],
           [0, 7, 3, 1],
           [7, 5, 7, 9],
           [4, 2, 0, 1]])



#### random.normal()

* 정규분포(normal distribution)를 고려한 랜덤한 수의 배열 생성

```python
np.random.normal(0,1,(3,3)) # 평균 0, 표준편차 1, 샘플사이즈 (3,3)
```


    array([[ 0.24864604, -1.46494981, -1.08069346],
           [ 1.94495246, -1.58289044,  0.81391231],
           [ 0.83243239,  1.70062464, -0.86074097]])



#### random.rand()

* 균등분포(uniform distribution)를 고려한 랜덤한 수의 배열 생성

```python
np.random.rand(4,4)
```


    array([[0.0972925 , 0.18570236, 0.17934436, 0.85738151],
           [0.06103397, 0.63004401, 0.45300681, 0.19424704],
           [0.57064646, 0.45949181, 0.29839345, 0.91645405],
           [0.36998513, 0.99162566, 0.72668558, 0.13741028]])



#### random.randn()

* 표준정규분포(standard normal distribution)를 고려한 랜덤한 수의 배열 생성

```python
np.random.randn(3,3)
```


    array([[-0.52672415,  0.56609104,  1.09265444],
           [-0.63231348, -0.26050481, -1.25757581],
           [ 1.75737519, -1.06730305, -0.15958397]])

---

## numpy의 표준 데이터 타입

* bool_ : 바이트로 저장된 boolean, True 또는 False값을 가짐
* int_ : 기본 정수(integer) 타입
* intc : c언어에서 사용되는 int와 동일(int32 or int64)
* intp : 인덱싱에 사용되는 정수(c언어에서의 ssize_t 와 동일)
* int8 : 바이트(Byte) (-128 ~ 127)
* int16 : 정수 (-32768 ~ 32767)
* int32 : 정수 ($ -2^{31} $ ~ $ 2^{31}-1 $)
* int64 : 정수 ($ -2^{63} $ ~ $ 2^{63}-1 $)
* uint : 부호 없는 정수 (0 ~ 255)
* float16 : 반정밀 부동 소수점(half precision float), 부호 비트, 5비트 지수, 10비트 가수
* float32 : 단정밀 부동 소수점(single precision float), 부호 비트, 8비트 지수, 23비트 가수
* float64 : 배정밀 부동 소수점(double precision float), 부호 비트, 11비트 지수, 52비트 가수
* float_ : float64
* complex64  : 복소수(complex number), 두 개의 32비트 부동 소수점으로 표현
* complex128 : 복소수, 두 개의 64비트 부동 소수점으로 표현

> dtype 을 통해서 데이터 타입 명시

```python
np.zeros(15, dtype=int)
```


    array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])




```python
np.ones((3,3), dtype=bool) # 1은 True
```


    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]])




```python
np.full((4,4),1.0,dtype=float)
```


    array([[1., 1., 1., 1.],
           [1., 1., 1., 1.],
           [1., 1., 1., 1.],
           [1., 1., 1., 1.]])



> 데이터 타입을 더 구체적으로 명시하기 위해서 np.datatype 형태로

```python
d1 = np.array([[1,2,3],[4.5,5.5,6.5]], dtype = np.int8)
print(d1)
print(d1.dtype)
```

```
[[1 2 3]
 [4 5 6]]
 
int8
```

## 참고

---

1. [Numpy 한번에 제대로 배우기](https://colab.research.google.com/drive/1qEBbLwNJ0FZA6h1BWHm5wu4mrJhbg3ty?usp=sharing)
2. [이수안 컴퓨터 연구소](https://www.youtube.com/watch?v=mirZPrWwvao)


---
layout: post
title:  "Numpy - 5(Array Operations 3)"
author: seungki
categories: [ Numpy ]
image: post_images/numpylogo.png
toc: True
---

---

Numpy에서 배열의 연산



## 배열 연산

* numpy에서 배열 연산은 벡터화(vectorized) 연산을 사용
* 일반적으로 numpy의 범용 함수(universal functions)를 통해서 구현
* 배열 요소에 대한 반복적인 계산을 효율적으로 수행



### Axis의 의미

* element의 합을 구해주는 sum()을 이용해서 설명하면

#### Matrix

<img src="https://user-images.githubusercontent.com/120040458/218387722-fc1efe60-31fa-4c4a-a379-8ce5ae30c960.PNG" alt="axis_sum1" style="zoom:100%;" class="center-image"/>

```python
test_matrix = np.arange(1,13).reshape(3,4)
test_matrix
```

```
array([[ 1,  2,  3,  4],
       [ 5,  6,  7,  8],
       [ 9, 10, 11, 12]])
```



* axis=1

```python
test_matrix.sum(axis=1) # 같은 row 방향으로 sum
```

```
array([10, 26, 42])
```



* axis=0

```python
test_matrix.sum(axis=0) # 같은 col 방향으로 sum
```

```
array([15, 18, 21, 24])
```



#### 3rd order tensor

<img src="https://user-images.githubusercontent.com/120040458/218387726-7fedd53d-da2e-4842-af8f-02dea5e4b697.PNG" alt="axis_sum2" style="zoom:90%;" class="center-image"/>

```python
test_matrix = np.arange(1,13).reshape(3,4)
third_order_tensor = np.stack([test_matrix,test_matrix,test_matrix],axis=0)
third_order_tensor
```

```
array([[[ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12]],

       [[ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12]],

       [[ 1,  2,  3,  4],
        [ 5,  6,  7,  8],
        [ 9, 10, 11, 12]]])
```



* axis=2

```python
third_order_tensor.sum(axis=2) # 같은 row방향으로 sum
```

```
array([[10, 26, 42],
       [10, 26, 42],
       [10, 26, 42]])
```



* axis=1

```python
third_order_tensor.sum(axis=1) # 같은 col방향으로 sum
```

```
array([[15, 18, 21, 24],
       [15, 18, 21, 24],
       [15, 18, 21, 24]])
```



* axis=0

```python
third_order_tensor.sum(axis=0) # 깊이 방향으로 sum
```

```
array([[ 3,  6,  9, 12],
       [15, 18, 21, 24],
       [27, 30, 33, 36]])
```



### Mean & Std

#### Mean

* 평균 구하기

```python
test_array = np.arange(1,13).reshape(3,4)
test_array
```

```
array([[ 1,  2,  3,  4],
       [ 5,  6,  7,  8],
       [ 9, 10, 11, 12]])
```

```python
test_array.mean()
```

```
6.5
```

```python
test_array.mean(axis=0)
```

```
array([5., 6., 7., 8.])
```



#### Std

* 표준편차 구하기

```python
test_array.std()
```

```
3.452052529534663
```

```python
test_array.std(axis=1)
```

```
array([1.11803399, 1.11803399, 1.11803399])
```

---

## Mathematical Functions

* numpy는 다양한 수학 연산자를 제공함

* absolute(), abs() : 절대값 함수
* square(), sqrt() : 제곱, 제곱근 함수

* cumsum() : 누적합 계산
* diff() : 차분 계산
* prod() : 곱 계산
* dot() : 점곱 계산
* matmul() : 행렬곱 계산
* tensordot() : 텐서곱 계산
* cross() : 벡터곱 계산
* inner() : 내적 계산
* outer() : 외적 계산
* var() : 분산 계산
* min() : 최소값
* max() : 최대값
* argmin() : 최소값 인덱스
* argmax() : 최대값 인덱스
* median() : 중앙값

이 외에도 지수함수, 로그함수, 삼각함수 등 여러가지 함수 제공

---

## Basic Array Operations

```python
test_a = np.array([[1,2,3],[4,5,6]], float)
```

### + operation


```python
test_a + test_a
```


    array([[ 2.,  4.,  6.],
           [ 8., 10., 12.]])

### - operation


```python
test_a - test_a
```


    array([[0., 0., 0.],
           [0., 0., 0.]])

### * operation

* element-wise operation, dot-product와 다름


```python
test_a * test_a # * operation은 element-wise operation, 같은 위치의 값들 끼리 계산
```


    array([[ 1.,  4.,  9.],
           [16., 25., 36.]])



### Dot product

![dot_product](https://user-images.githubusercontent.com/120040458/218392765-f7c96859-b41f-449f-9800-fafea92a03dc.PNG)

* matrix의 기본 연산, dot() 함수 사용

```python
test_a = np.arange(1,7).reshape(2,3)
test_b = np.arange(7,13).reshape(3,2)
test_a.dot(test_b)
```

```
array([[ 58,  64],
       [139, 154]])
```



### Broadcasting

* shape이 다른 배열 간 연산을 지원하는 기능

![broadcasting1](https://user-images.githubusercontent.com/120040458/218393402-25b57733-d870-4d92-a759-4b5d66512b65.PNG)



#### Matrix - Scalar , Vector - Scalar 연산

```python
test_matrix = np.array([[1,2,3],[4,5,6]],float)
scalar = 3
```

* 덧셈


```python
test_matrix + scalar # Matrix-Scalar 덧셈
```


    array([[4., 5., 6.],
           [7., 8., 9.]])

* 뺄셈


```python
test_matrix - scalar # Matrix-Scalar 뺄셈
```


    array([[-2., -1.,  0.],
           [ 1.,  2.,  3.]])

* 곱셈


```python
test_matrix * scalar # Matrix-Scalar 곱셈
```


    array([[ 3.,  6.,  9.],
           [12., 15., 18.]])

* 나눗셈


```python
test_matrix / 5 # Matrix-Scalar 나눗셈
```


    array([[0.2, 0.4, 0.6],
           [0.8, 1. , 1.2]])

* 몫


```python
test_matrix // 0.2 # Matrix-Scalar 몫
```


    array([[ 4.,  9., 14.],
           [19., 24., 29.]])

* 제곱


```python
test_matrix ** 2 # Matrix-Scalar 제곱
```


    array([[ 1.,  4.,  9.],
           [16., 25., 36.]])



#### Vector - Matrix 연산

<img src="https://user-images.githubusercontent.com/120040458/218404024-c183ed6b-e655-4719-8bf0-13a7e3a8a6de.PNG" alt="vector_matrix_broadcast" style="zoom:80%;" class="center-image"/>

<img src="https://user-images.githubusercontent.com/120040458/218404280-2df91c7b-4f19-453f-b133-94a2ca0decd2.PNG" alt="vector_matrix_broadcast2" style="zoom:90%;" class="center-image"/>

```python
test_matrix = np.arange(1,13).reshape(4,3)
test_vector = np.arange(10,40,10)
test_matrix + test_vector
```

```
array([[11, 22, 33],
       [14, 25, 36],
       [17, 28, 39],
       [20, 31, 42]])
```



### Comparison (비교연산)

#### All & Any

* Array의 데이터 전부(and) 또는 일부(or)가 조건에 만족하는지 여부 반환

```python
a = np.arange(10)
a
```


    array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


```python
np.any(a>5), np.any(a<0) # any는 하나라도 조건에 만족하면 True
```


    (True, False)


```python
np.all(a>5), np.all(a<10) # all은 모두가 조건에 만족해야 True
```


    (False, True)



#### Array Comparison Operation

* numpy는 배열의 크기가 동일 할 때 element간 비교의 결과를 Boolean type으로 반환

```python
test_a = np.array([1,3,0], float)
test_b = np.array([5,2,1], float)
test_a > test_b
```


    array([False,  True, False])


```python
test_a == test_b
```


    array([False, False, False])


```python
(test_a > test_b).any() # any는 하나라도 true면 true
```


    True



#### And, Not, Or operation

* logical_and()

```python
a = np.array([1,3,0], float)
np.logical_and(a>0, a<3) # and 조건 condition
```


    array([ True, False, False])



* logical_not()

```python
b = np.array([True,False,True], bool)
np.logical_not(b)
```


    array([False,  True, False])



* logical_or()

```python
c = np.array([False,True,False],bool)
np.logical_or(b,c)
```


    array([ True,  True,  True])



#### np.where()

* where(condition, True, False)

```python
a = np.array([1,3,0], float)
np.where(a>0,3,2) # True면 3 반환, False면 2 반환
```


    array([3, 3, 2])

* 조건을 만족하는 Index 반환

```python
a = np.arange(10)
print(a)
np.where(a>5)
```


    [0 1 2 3 4 5 6 7 8 9]
    (array([6, 7, 8, 9], dtype=int64),)



#### np.isnan()

* NaN일 경우 True 반환

```python
a = np.array([1, np.NaN, np.Inf], float)
np.isnan(a) # not a number, NaN일 경우 True 반환
```


    array([False,  True, False])



#### np.isfinite()

* finite number일 경우 True 반환

```python
np.isfinite(a) # finite number일 경우 True 반환
```


    array([ True, False, False])



#### argmax & argmin

* array내 최대값 또는 최소값의 index 반환

```python
a = np.array([1,2,4,5,8,78,23,3])
np.argmax(a), np.argmin(a)
```

```
(5, 0)
```



* axis 기반의 반환

```python
a = np.array([[1,2,4,7],[9,88,6,45],[9,76,3,4]])
print(a)
```

```
[[ 1  2  4  7]
 [ 9 88  6 45]
 [ 9 76  3  4]]
```

```python
np.argmax(a,axis=1) # 각 row의 최대값의 index 반환
```

```
array([3, 1, 1], dtype=int64)
```

```python
np.argmin(a,axis=0) # 각 col의 최소값의 index 반환
```

```
array([0, 0, 2, 2], dtype=int64)
```

## 참고

---

1. [Numpy 한번에 제대로 배우기](https://colab.research.google.com/drive/1qEBbLwNJ0FZA6h1BWHm5wu4mrJhbg3ty?usp=sharing)
2. [이수안 컴퓨터 연구소](https://www.youtube.com/watch?v=mirZPrWwvao)
3. [부스트 코스 AI numpy - 최성철](https://www.boostcourse.org/onlyboostcampaitech5/lecture/1456479?isDesc=false)
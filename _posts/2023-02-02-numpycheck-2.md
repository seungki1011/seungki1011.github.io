---
layout: post
title:  "Numpy - 2(배열 조회)"
author: seungki
categories: [ Numpy ]
image: post_images/numpylogo.png
toc: True
---
---
## 배열 조회
### 배열 속성 정보
```python
def array_info(array):
    print(array)
    print("ndim:", array.ndim) # 배열의 차원
    print("shape:", array.shape) # 배열의 모양
    print("dtype:", array.dtype) # 배열의 데이터 타입
    print("size:", array.size) # item(element)의 개수
    print("itemsize:", array.itemsize) # 각 item(element)의 byte크기
    print("nbytes:", array.nbytes) # 전체 배열의 byte 크기
    print("strides:", array.strides) # 한 item(element)를 넘어가는데 필요한 byte크기
```

* 1차원 배열

```python
test_array1=np.array([1,3,5,6,7], dtype=int)
array_info(test_array1)
```

    [1 3 5 6 7]
    ndim: 1
    shape: (5,)
    dtype: int32
    size: 5
    itemsize: 4
    nbytes: 20
    strides: (4,)



* 2차원 배열

```python
test_array2=np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]], dtype=int)
array_info(test_array2)
# 2차원 배열에서 strides (다음 차원으로 넘어가는데 필요한 stride, 한 item을 넘어가는데 필요한 stride)
```

    [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 9 10 11 12]]
    ndim: 2
    shape: (3, 4)
    dtype: int32
    size: 12
    itemsize: 4
    nbytes: 48
    strides: (16, 4)



* 3차원 배열

```python
test_array3=np.array([[[1,2,3,4],[5,6,7,8],[9,10,11,12]],
                     [[1,2,3,4],[5,6,7,8],[9,10,11,12]],
                     [[1,2,3,4],[5,6,7,8],[9,10,11,12]],
                     [[1,2,3,4],[5,6,7,8],[9,10,11,12]]], dtype=int)
array_info(test_array3)
```

    [[[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]
    
     [[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]
    
     [[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]
    
     [[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]]
    ndim: 3
    shape: (4, 3, 4)
    dtype: int32
    size: 48
    itemsize: 4
    nbytes: 192
    strides: (48, 16, 4)



### 인덱싱(Indexing)

* 1차원 배열

```python
print(test_array1)
print(test_array1[0])
print(test_array1[2])
print(test_array1[-1]) # 마지막 요소
print(test_array1[-2]) # 마지막에서 두번째 요소
```

    [1 3 5 6 7]
    1
    5
    7
    6



* 2차원 배열

```python
print(test_array2)
print(test_array2[0,0])
print(test_array2[0,2])
print(test_array2[1,1])
print(test_array2[2,-1]) # 2번 row(3번째 row)에서 마지막 요소
```

    [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 9 10 11 12]]
    1
    3
    6
    12



* 3차원 배열

```python
print(test_array3)
print(test_array3[0,0,0])
print(test_array3[1,1,1])
print(test_array3[2,-1,-1]) # 2번 axis의 마지막 row의 마지막 요소
```

    [[[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]
    
     [[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]
    
     [[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]
    
     [[ 1  2  3  4]
      [ 5  6  7  8]
      [ 9 10 11 12]]]
    1
    6
    12



### 슬라이싱(Slicing)

* array[start:stop:step]
* 디폴트값 : start=0, stop=ndim, step=1

* 1차원 배열 슬라이싱

```python
print(test_array1)
print(test_array1[0:2])
print(test_array1[0:])
print(test_array1[:2])
print(test_array1[::2])
print(test_array1[::-1])
print(test_array1[0:5:2])
```

    [1 3 5 6 7]
    [1 3]
    [1 3 5 6 7]
    [1 3]
    [1 5 7]
    [7 6 5 3 1]
    [1 5 7]



* 2차원 배열 슬라이싱

```python
print(test_array2)
print(test_array2[1])
print(test_array2[1, :])
print(test_array2[:2, :2])
print(test_array2[1:, ::-1])
print(test_array2[::-1, ::-1])
```

    [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 9 10 11 12]]
     
    [5 6 7 8]
    
    [5 6 7 8]
    
    [[1 2]
     [5 6]]
     
    [[ 8  7  6  5]
     [12 11 10  9]]
     
    [[12 11 10  9]
     [ 8  7  6  5]
     [ 4  3  2  1]]



### 불리언 인덱싱(Boolean Indexing)

* 배열 각 요소의 선택 여부를 불리언(True, False)로 지정
* True 값인 인덱스의 값만 조회

* 1차원 배열 불리언 인덱싱

```python
print(test_array1)
bi = [True,False,True,True,False]
print(test_array1[bi])
```

    [1 3 5 6 7]
    [1 5 6]



* 2차원 배열 불리언 인덱싱

```python
print(test_array2)
bi = np.random.randint(0,2,(3,4), dtype=bool)
print(bi)
print(test_array2[bi])
```

    [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 9 10 11 12]]
     
    [[ True  True False  True]
     [ True False  True  True]
     [False  True  True False]]
     
    [ 1  2  4  5  7  8 10 11]



### 팬시 인덱싱(Fancy Indexing)

* 1차원 배열 팬시 인덱싱

```python
print(test_array1)
fi = [0,2,3]
print(test_array1[fi])  # 주어진 인덱스에 따라서 출력
fi2 = np.array([[0,1], 
                [2,0]]) # 주어진 인덱스의 배열이 2차원 형태면 뽑는 값도 2차원 형태 
print(test_array1[fi2])
```

    [1 3 5 6 7]
    [1 5 6]
    [[1 3]
     [5 1]]



* 2차원 배열 팬시 인덱싱

```python
print(test_array2)
row=np.array([0,2])
col=np.array([1,2])
print(test_array2[row,col])
print(test_array2[row,:])
print(test_array2[:,col])
print(test_array2[row,1])
print(test_array2[1,col])
print(test_array2[row,:1]) # fancy indexing과 슬라이싱까지
```

    [[ 1  2  3  4]
     [ 5  6  7  8]
     [ 9 10 11 12]]
     
    [ 2 11]
    
    [[ 1  2  3  4]
     [ 9 10 11 12]]
     
    [[ 2  3]
     [ 6  7]
     [10 11]]
     
    [ 2 10]
    
    [6 7]
    
    [[1]
     [9]]



## 참고

---

1. [Numpy 한번에 제대로 배우기](https://colab.research.google.com/drive/1qEBbLwNJ0FZA6h1BWHm5wu4mrJhbg3ty?usp=sharing)
2. [이수안 컴퓨터 연구소](https://www.youtube.com/watch?v=mirZPrWwvao)

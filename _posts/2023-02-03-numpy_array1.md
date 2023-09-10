---
layout: post
title:  "Numpy - 3(Array Operations 1)"
author: seungki
categories: [ Numpy ]
image: post_images/numpylogo.png
toc: True
---
---
## 배열 값 삽입, 수정, 삭제, 복사
> 원본 배열이 변경되지 않는 이유는 속도적인 면에서 이점이 있기 때문

### 배열 값 삽입

#### insert()

* 배열의 특정 위치에 값 삽입
* axis를 지정하지 않으면 1차원 배열로 변환
* 추가(삽입)할 방향을 axis로 지정
* 원본 배열 변경없이 새로운 배열 반환

* 1차원 배열에서의 삽입

```python
a1 = np.array([1,2,3,4,5])
```


```python
print(a1)
b1 = np.insert(a1,0,10) # a1의 0번째 인덱스에 10을 삽입, a1의 값은 변경되지 않음
print(b1)
c1 = np.insert(a1,2,10)
print(c1)
```

    [1 2 3 4 5]
    [10  1  2  3  4  5]
    [ 1  2 10  3  4  5]



* 2차원 배열에서의 삽입

```python
a2 = np.array([[1,2,3],
              [4,5,6],
              [7,8,9]])
```


```python
print(a2)
b2 = np.insert(a2,1,10,axis=0)
print(b2)
c2 = np.insert(a2,1,10,axis=1)
print(c2)
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
     
    [[ 1  2  3]
     [10 10 10]
     [ 4  5  6]
     [ 7  8  9]]
     
    [[ 1 10  2  3]
     [ 4 10  5  6]
     [ 7 10  8  9]]



### 배열 값 수정

* 배열의 인덱싱으로 접근해서 값 수정

* 1차원 배열 값 수정

```python
print(a1)
a1[0] = 11
a1[1] = 22
a1[2] = 33
print(a1)
a1[:2] = 9 # 0~1 까지 9로 수정
print(a1)
i = np.array([1,3,4])
a1[i] = 0 # 1,3,4 인덱스의 값을 0으로 수정
print(a1)
a1[i] += 3 # 1,3,4 인덱스의 값에 +3을 한것으로 수정
print(a1)
```

    [ 9  0 33  0  0] # a1
    [11 22 33  0  0]
    [ 9  9 33  0  0]
    [ 9  0 33  0  0]
    [ 9  3 33  3  3]



* 2차원 배열 값 수정

```python
print(a2)
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]

```python
a2[0,0] = 11
a2[1,1] = 22
a2[2,2] = 33
print(a2)
a2[0] = 1 # 0번 row에 해당하는 것 전부 1로 수정
print(a2)
a2[1:,2] = 9
print(a2)
```

    [[11  1  1]
     [ 4 22  6]
     [ 7  8 33]]
     
    [[ 1  1  1]
     [ 4 22  6]
     [ 7  8 33]]
     
    [[ 1  1  1]
     [ 4 22  9]
     [ 7  8  9]]



### 배열 값 삭제

#### delete()

* 배열의 특정 위치에 값 삭제
* axis를 지정하지 않으면 1차원 배열로 변환
* 삭제할 방향을 axis로 지정
* 원본 배열 변경없이 새로운 배열 변환

* 1차원 배열 값 삭제

```python
print(a1)
b1 = np.delete(a1,1) # a1의 1번째 인덱스를 삭제한 배열을 b1에 할당
print(b1)
print(a1) # 원본 배열은 변경되지 않음
```

    [ 9  3 33  3  3]
    [ 9 33  3  3]
    [ 9  3 33  3  3]

* 2차원 배열 값 삭제

```python
print(a2)
b2 = np.delete(a2,1,axis=0) # 1번 row삭제, axis는 0번
print(b2)
b2 = np.delete(a2,1,axis=1) # 1번 col삭제, axis는 1번, axis를 통해서 삭제하는 방향 정한다!
print(b2)
```

    [[ 1  1  1]
     [ 4 22  9]
     [ 7  8  9]]
    [[1 1 1]
     [7 8 9]]
    [[1 1]
     [4 9]
     [7 9]]



### 배열 복사

#### 배열의 슬라이스와 원본의 관계

* 리스트 자료형과 달리 배열의 슬라이스는 복사본이 아님

* 슬라이싱 되는 결과는 복사본이 아니고 원본을 공유, 메모리를 공유한다고 보면 됨

```python
print(a2)
print(a2[:2,:2])
a2_sub = a2[:2,:2]
print(a2_sub)
a2_sub[:,1] = 0 # 원본 배열도 바뀜
print(a2_sub)
print(a2)
```

    [[ 1  1  1]
     [ 4 22  9]
     [ 7  8  9]]
     
    [[ 1  1]
     [ 4 22]]
     
    [[ 1  1]
     [ 4 22]]
     
    [[1 0]
     [4 0]]
     
    [[1 0 1]
     [4 0 9]
     [7 8 9]]



#### copy()

* 배열이나 하위 배열 내의 값을 명시적으로 복사

```python
print(a2)
a2_sub_copy = a2[:2,:2].copy()
print(a2_sub_copy)
a2_sub_copy[:,1] = 1
print(a2_sub_copy)
print(a2) # 복사본을 통해서 값을 바꿨기 때문에 원본은 바뀌지 않음
```

    [[1 0 1]
     [4 0 9]
     [7 8 9]]
     
    [[1 0]
     [4 0]]
     
    [[1 1]
     [4 1]]
     
    [[1 0 1]
     [4 0 9]
     [7 8 9]]

## 참고

---

1. [Numpy 한번에 제대로 배우기](https://colab.research.google.com/drive/1qEBbLwNJ0FZA6h1BWHm5wu4mrJhbg3ty?usp=sharing)
2. [이수안 컴퓨터 연구소](https://www.youtube.com/watch?v=mirZPrWwvao)

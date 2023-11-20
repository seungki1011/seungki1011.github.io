---
layout: post
title:  "Numpy (4)(Array Operations 2)"
author: seungki
categories: [ Numpy ]
image: post_images/numpylogo.png
toc: True
---
---
## 배열 변환
### 배열 전치(Transpose) 및 축 변경
#### T 메소드

* 2차원 배열 T 메소드

```python
a2 = np.array([[1,2,3],
               [4,5,6],
               [7,8,9]])
```


```python
a3 = np.array([[[1,2,3],
               [4,5,6],
               [7,8,9]],
               [[1,2,3],
               [4,5,6],
               [7,8,9]],
               [[1,2,3],
               [4,5,6],
               [7,8,9]]])
```


```python
print(a2)
print(a2.T) # 배열의 전치(Transpose)
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
     
    [[1 4 7]
     [2 5 8]
     [3 6 9]]



* 3차원 배열 T 메소드

```python
print(a3)
print(a3.T)
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
      
    [[[1 1 1]
      [4 4 4]
      [7 7 7]]
    
     [[2 2 2]
      [5 5 5]
      [8 8 8]]
    
     [[3 3 3]
      [6 6 6]
      [9 9 9]]]



#### swapaxes()

* 배열의 축 교환

```python
a4 = np.array([[[ 0,  1,  2,  3],
                [ 4,  5,  6,  7],
                [ 8,  9, 10, 11]],
                [[12, 13, 14, 15],
                 [16, 17, 18, 19],
                 [20, 21, 22, 23]]])
print(a4)
print(a4.shape) 
# 현재 정의된 축의 길이 axis0=2, axis1=3, axis2=4
# 3행 4열의 배열이 2층 쌓인 3차원 배열
```

    [[[ 0  1  2  3]
      [ 4  5  6  7]
      [ 8  9 10 11]]
    
     [[12 13 14 15]
      [16 17 18 19]
      [20 21 22 23]]]
      
    (2, 3, 4)

```python
a4_swap = a4.swapaxes(0,1) # axis0과 axis1 교환
print(a4_swap) 
print(a4_swap.shape) # 나오는 shape는 (3,2,4)
```

    [[[ 0  1  2  3]
      [12 13 14 15]]
    
     [[ 4  5  6  7]
      [16 17 18 19]]
    
     [[ 8  9 10 11]
      [20 21 22 23]]]
      
    (3, 2, 4)



#### transpose()

```python
print(a4)
print(a4.shape)
# 기존 shape인 (2,3,4)는 axis 0,1,2에 매칭되어 있음
```

    [[[ 0  1  2  3]
      [ 4  5  6  7]
      [ 8  9 10 11]]
    
     [[12 13 14 15]
      [16 17 18 19]
      [20 21 22 23]]]
      
    (2, 3, 4)

```python
a4_transpose = a4.transpose(2,1,0) # 새로입력한 (2,1,0)으로 축 순서 변경
print(a4_transpose) 
print(a4_transpose.shape) # shape은 (4,3,2)로 변경됨
```

    [[[ 0 12]
      [ 4 16]
      [ 8 20]]
    
     [[ 1 13]
      [ 5 17]
      [ 9 21]]
    
     [[ 2 14]
      [ 6 18]
      [10 22]]
    
     [[ 3 15]
      [ 7 19]
      [11 23]]]
      
    (4, 3, 2)



### 배열 재구조화

#### reshape() 

* 배열의 형상을 변경

```python
print(a2)
print(a2.shape)
print(a2.reshape(1,9)) # (3,3)을 (1,9)로
print(a2.reshape(9)) 
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
     
    (3, 3)
    
    [[1 2 3 4 5 6 7 8 9]]
    
    [1 2 3 4 5 6 7 8 9]

```python
a1 = np.array([1,2,3,4,5,6,7,8,9])
print(a1.shape)
print(a1.reshape(3,3))
```

    (9,)
    
    [[1 2 3]
     [4 5 6]
     [7 8 9]]



#### newaxis

* 새로운 축 추가

```python
print(a1)
print(a1[np.newaxis, :5])
print(a1[:5, np.newaxis])
```

    [1 2 3 4 5 6 7 8 9]
    
    [[1 2 3 4 5]]
    
    [[1]
     [2]
     [3]
     [4]
     [5]]



### 배열 크기 변경

#### resize()

* 배열의 크기와 모양 변경 가능, 원본 배열 직접적으로 변경함
* 배열 모양만 변경하는 경우

```python
n2 = np.random.randint(0,10,(2,5))
print(n2)
n2.resize((5,2))
print(n2)
```

    [[6 6 1 7 9]
     [5 2 9 2 0]]
     
    [[6 6]
     [1 7]
     [9 5]
     [2 9]
     [2 0]]



* 배열 크기가 증가하는 경우
* 남은 공간은 0으로 채워짐

```python
n2.resize((5,5)) # 남은 공간은 0으로 채움
print(n2)
```

    [[6 6 1 7 9]
     [5 2 9 2 0]
     [0 0 0 0 0]
     [0 0 0 0 0]
     [0 0 0 0 0]]



* 배열 크기가 감소하는 경우
* 포함되지 않은 영역은 삭제됨

```python
n2.resize((3,3)) # 포함되지 않은 값은 삭제됨
print(n2)
```

    [[6 6 1]
     [7 9 0]
     [0 0 0]]



### 배열 추가

#### append()

* 배열 끝에 값 추가
* axis 지정이 없으면 1차원 배열 형태로 변형되어 결합

```python
a2 = np.arange(1,10).reshape(3,3)
print(a2)
b2 = np.arange(10,19).reshape(3,3)
print(b2)
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
     
    [[10 11 12]
     [13 14 15]
     [16 17 18]]

```python
c2 = np.append(a2,b2) # 2차원 배열끼리 append해도 1차원 배열 형태로 결합됨
print(c2) 
```

    [ 1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18]



* axis = 0
* shape[0]을 제외한 나머지 shape는 같아야 함

```python
c2 = np.append(a2,b2,axis=0) # axis를 통해서 append되는 방향 결정
print(c2)
```

    [[ 1  2  3]
     [ 4  5  6]
     [ 7  8  9]
     [10 11 12]
     [13 14 15]
     [16 17 18]]



* axis = 1
* shape[1]을 제외한 나머지 shape는 같아야 함

```python
c2 = np.append(a2,b2,axis=1)
print(c2)
```

    [[ 1  2  3 10 11 12]
     [ 4  5  6 13 14 15]
     [ 7  8  9 16 17 18]]



### 배열 연결

#### concatenate()

* 튜플이나 배열의 리스트를 인수로 사용해 배열 연결

```python
a1 = np.array([1,3,5])
b1 = np.array([2,4,6])
c1 = np.concatenate([a1,b1])
print(c1)
```

    [1 3 5 2 4 6]

```python
d1 = np.array([7,8,9])
e1 = np.concatenate([a1,b1,d1])
print(e1)
```

    [1 3 5 2 4 6 7 8 9]



* axis 설정 안하는 경우

```python
a2 = np.array([[1,2,3],
               [4,5,6]])
print(np.concatenate([a2,a2])) # axis 설정안하면 아래로 붙음
```

    [[1 2 3]
     [4 5 6]
     [1 2 3]
     [4 5 6]]



* axis=1

```python
print(np.concatenate([a2,a2], axis=1)) # axis=1이면 오른쪽옆으로 붙음
```

    [[1 2 3 1 2 3]
     [4 5 6 4 5 6]]



#### vstack()

* 수직 스택(vertical stack), 1차원으로 연결

```python
print(np.vstack([a2,a2])) # 아래로 붙음(수직)
```

    [[1 2 3]
     [4 5 6]
     [1 2 3]
     [4 5 6]]



#### hstack()

* 수평 스택(horizontal stack), 2차원으로 연결

```python
print(np.hstack([a2,a2])) # 옆으로 붙음(수평)
```

    [[1 2 3 1 2 3]
     [4 5 6 4 5 6]]



#### dstack()

* depth stack, 3차원으로 연결

```python
print(np.dstack([a2,a2])) # depth로 붙음, 3차원으로 바뀜
```

    [[[1 1]
      [2 2]
      [3 3]]
    
     [[4 4]
      [5 5]
      [6 6]]]



#### stack()

* 새로운  차원을 추가해서 연결됨

```python
print(np.stack([a2,a2])) # 새로운 차원을 추가해서 연결이 됨
```

    [[[1 2 3]
      [4 5 6]]
    
     [[1 2 3]
      [4 5 6]]]



### 배열 분할

#### split()

* 배열 분할

```python
a1 = np.arange(0,10)
print(a1)
b1,c1 = np.split(a1,[5]) # 5번째 요소를 기준으로 분할
print(b1,c1)
```

    [0 1 2 3 4 5 6 7 8 9]
    [0 1 2 3 4] [5 6 7 8 9]

```python
b1,c1,d1,e1,f1 = np.split(a1,[2,4,6,8]) # 2,4,6,8 번째 요소 기준으로 분할
print(b1,c1,d1,e1,f1)
```

    [0 1] [2 3] [4 5] [6 7] [8 9]



#### vsplit()

* 수직 분할, 1차원으로 분할

```python
a2 = np.arange(1,10).reshape(3,3)
print(a2)
b2,c2 = np.vsplit(a2,[2]) # 2번째 row를 기준으로 수직으로 분할
print(b2) 
print(c2)
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
     
    [[1 2 3]
     [4 5 6]]
     
    [[7 8 9]]



#### hsplit()

* 수평 분할, 2차원으로 분할

```python
a2 = np.arange(1,10).reshape(3,3)
print(a2)
b2,c2 = np.hsplit(a2,[2]) # 2번째 col을 기준으로 수직으로 분할
print(b2) 
print(c2)
```

    [[1 2 3]
     [4 5 6]
     [7 8 9]]
     
    [[1 2]
     [4 5]
     [7 8]]
     
    [[3]
     [6]
     [9]]



#### dsplit()

* 깊이 분할, 3차원으로 분할

```python
a3 = np.arange(1,28).reshape(3,3,3)
print(a3)
b3,c3 = np.dsplit(a3,[2]) # depth 기준으로 분할
print(b3) 
print(c3)
```

    [[[ 1  2  3]
      [ 4  5  6]
      [ 7  8  9]]
    
     [[10 11 12]
      [13 14 15]
      [16 17 18]]
    
     [[19 20 21]
      [22 23 24]
      [25 26 27]]]
      
    [[[ 1  2]
      [ 4  5]
      [ 7  8]]
    
     [[10 11]
      [13 14]
      [16 17]]
    
     [[19 20]
      [22 23]
      [25 26]]]
      
    [[[ 3]
      [ 6]
      [ 9]]
    
     [[12]
      [15]
      [18]]
    
     [[21]
      [24]
      [27]]]

## 참고

---

1. [Numpy 한번에 제대로 배우기](https://colab.research.google.com/drive/1qEBbLwNJ0FZA6h1BWHm5wu4mrJhbg3ty?usp=sharing)
2. [이수안 컴퓨터 연구소](https://www.youtube.com/watch?v=mirZPrWwvao)
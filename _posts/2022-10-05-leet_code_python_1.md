---
layout: post
title:  "코딩 테스트를 위한 파이썬 (1)"
author: seungki
categories: [ Python ]
tags: [코딩 테스트]
image: post_images/python logo.png
toc: True

---
---
코딩 테스트를 위한 파이썬

---

## List

### List data type

```python
a = [1,2,3,4,5]
print(a)
```

```python
[1,2,3,4,5]
```

```python
b = [0] * 5
print(b)
```

```python
[0,0,0,0,0]
```

### 	indexing

* 음의 정수를 이용해 접근하는 경우 원소를 거꾸로 탐색

```python
c = [1,2,3,4,5,6,7,8,9]
print(c[-1]) # 뒤에서 첫 번째 원소
print(c[-3]) # 뒤에서 세 번째 원소
```

```
9
7
```

### slicing

* 연속적인 위치를 갖는 원소들을 가져올때 사용 가능
* 시작 인덱스 : 끝 인덱스(실제 인덱스 + 1)

```python
d = [1,2,3,4,5,6,7,8,9]
print(d[1:5]) # 2 번째 원소 부 5 번째 원소 까지
```

```python
[2,3,4,5]
```

### List comprehension

#### example 1

* 대괄호안에 조건문과 반복문을 적용하여 리스트를 초기화 할 수 있는 방법

```python
a = [i for i in range(10)]
print(a)
```

```python
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

* 위의 list comprehension을 기존 방식으로 코딩하는 경우

```python
a = []
for i in range(0, 10):
    a.append(i)
print(a)
```

```python
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```

#### example 2

* 조건문까지 포함하는 경우

```python
# 0 ~ 9 까지의 원소에서 2로 나눴을 때 나머지값이 1인 경우(홀수)
a = [i for i in range(10) if i % 2 == 1] 
print(a)
```

```python
[1, 3, 5, 7, 9]
```

```python
# 2~10 까지의 정수들의 제곱 값에 대한 리스트
b = [i*i for i in range(2, 11)]
print(b)
```

```python
[4, 9, 16, 25, 36, 49, 64, 81, 100]
```

### List comprehension을 사용하는 경우

* 2차원 리스트 초기화 할 때 효과적으로 사용 가능

#### example 1

* **NxM** 크기의 2차원 리스트를 한 번에 초기화

```python
# a = [[0]* m for _ in range(n)]
a = [[0]* 5 for _ in range(3)]
print(a)
```

```python
[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
```

#### 잘못 사용하는 경우

```python
# b = [[0] * m] * n
b = [[1] * 5] * 3
print(b)
b[0][0] = 2
print(b)
```

```python
[[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]]
[[2, 1, 1, 1, 1], [2, 1, 1, 1, 1], [2, 1, 1, 1, 1]]
```

* 위의 경우 전체 리스트 안에 포함된 각 리스트가 모두 같은 객체로 인식 됨
* ```b[0][0]``` 을 다시 명시했지만 나머지 리스트들도 변하는 것을 확인
* 문제의 의도에 맞게 사용하자

---

## Methods for list

### .append()

* 시간 복잡도 O(1)
* 리스트에 원소 삽입

### .sort()

* 리스트 정렬
* 오름차순 정렬이 디폴트
* ```.sort(reverse=True)``` 내림차순 정렬
* 시간 복잡도 O(NlogN)

### .reverse()

* 리스트의 원소 순서 전부 뒤집기
* 시간 복잡도 O(N)

### .insert()

* 특정 인덱스 위치에 원소 삽입

```python
#.insert(삽입할 위치 인덱스, 삽입할 값)
a = [1,2,3,4,5]
# 3번 인덱스에 99 삽입
a.insert(3, 99)
print(a)
# 뒤에서 1번 인덱스에 -99 삽입
a.insert(-1,-99)
print(a)
```

```python
[1, 2, 3, 99, 4, 5]
[1, 2, 3, 99, 4, -99, 5]
```

* 시간 복잡도 O(N)

### .count()

* 특정한 값을 가지는 데이터의 개수를 셈
* 시간 복잡도 O(N)

### .remove()

* 특정한 값을 갖는 원소 제거
* 똑같은 값을 가지는 원소가 여러개인 경우 하나만 제거
* **전부 제거하는 경우 set 자료형을 이용해서 제거**
* 시간 복잡도 O(N)



## 참고

---

1. [이것이 취업을 위한 코딩 테스트다](https://www.youtube.com/watch?v=m-9pAwq1o3w&list=PLRx0vPvlEmdAghTr5mXQxGpHjWqSz0dgC&t=2921s)
2. [제대로 파이썬](https://wikidocs.net/22805)
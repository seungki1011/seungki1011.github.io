---
layout: post
title:  "코딩 테스트를 위한 파이썬 - 2"
author: seungki
categories: [ Python ]
tags: [코딩 테스트]
image: post_images/python logo.png
toc: True

---
---
코딩 테스트를 위한 파이썬

---

## Input

### 기본 입출력

* ```input()``` : 한 줄의 문자열을 입력 받음
* ```map()``` : 리스트의 모든 원소에 각각 특정한 함수를 적용할 때 사용

```python
# 공백 기준으로 구분된 데이터 입력
a,b,c = map(int, input().split())

print(a,b,c)
```

```
10 20 30
10 20 30
```

```python
input_data = list(map(int, input().split()))

print(input_data)

for x in input_data:
    print(x, end=' ')
```

```
1 2 3 4 50 60 70 80
[1, 2, 3, 4, 50, 60, 70, 80]
1 2 3 4 50 60 70 80
```

* 정수 입력하는 경우

```python
n = int(input())
```

### 빠른 입력

* sys 라이브러리의 ```sys.stdin.readline()```사용
* 엔터도 줄 바꿈 기호로 입력되기 때문에 ```rstrip()```함께 사용

```python
import sys
fast_input = sys.stdin.readline().rstrip()
```

---

## 자주 사용되는 라이브러리

### 내장 함수

#### sorted()

```python
org_list = [5,4,2,1,1,3,6]
sorted_list = sorted(org_list)
rev_sorted_list = sorted(org_list, reverse=True)

print(org_list)
print(sorted_list)
print(rev_sorted_list)
```

```
[5, 4, 2, 1, 1, 3, 6]
[1, 1, 2, 3, 4, 5, 6]
[6, 5, 4, 3, 2, 1, 1]
```

#### sorted() with key and lambda

```python
array = [('a', 33, 3), ('b', 15, 2), ('c', 20, 1)]

# x[1] 기준 -> 두 번째 인덱스 기준으로 정렬
result_1 = sorted(array, key=lambda x: x[1])
# x[2] 기준 -> 세 번째 인덱스 기준으로 정렬
result_2 = sorted(array, key=lambda x: x[2])

print(array)
print(result_1)
print(result_2)
```

```
[('a', 33, 3), ('b', 15, 2), ('c', 20, 1)]
[('b', 15, 2), ('c', 20, 1), ('a', 33, 3)]
[('c', 20, 1), ('b', 15, 2), ('a', 33, 3)]
```



### Itertools

#### 순열(Permutation)

* 서로 다른 n개에서 서로 다른 r개를 선택하여 일렬로 나열하는 것
* {'a','b','c'}에서 3개 선택 -> 'abc', 'acb', 'bac', 'bca', 'cab', 'cba'

```python
from itertools import permutations

data = ['a', 'b', 'c', 'd']

# 순열 구하기
result = list(permutations(data, 2)) # list로 변환하지 않고 출력시, permutation object의 인스턴스로 나옴
print(result)

for x in permutations(data, 2):
    print(x)
```

```
[('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'a'), ('b', 'c'), ('b', 'd'), ('c', 'a'), ('c', 'b'), ('c', 'd'), ('d', 'a'), ('d', 'b'), ('d', 'c')]
('a', 'b')
('a', 'c')
('a', 'd')
('b', 'a')
('b', 'c')
('b', 'd')
('c', 'a')
('c', 'b')
('c', 'd')
('d', 'a')
('d', 'b')
('d', 'c')
```

#### 조합(Combination)

* 서로 다른 n개에서 순서에 상관 없이 서로 다른 r개를 선택하는 것
* {'a','b','c'}에서 순서를 고려하지 않고 두개 뽑는 경우 -> 'ab', 'ac', 'bc'

```python
from itertools import combinations

data = ['a', 'b', 'c', 'd']

# 조합 구하기
result = list(combinations(data, 2))
print(result)

for x in combinations(data, 2):
    print(x)
```

```
[('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
('a', 'b')
('a', 'c')
('a', 'd')
('b', 'c')
('b', 'd')
('c', 'd')
```

#### 중복 순열

```python
from itertools import product

data = ['a', 'b', 'c', 'd']

# 중복 순열 구하기
result = list(product(data, repeat=2))
print(result)

for x in product(data, repeat=2):
    print(x)
```

```
[('a', 'a'), ('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'a'), ('b', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'a'), ('c', 'b'), ('c', 'c'), ('c', 'd'), ('d', 'a'), ('d', 'b'), ('d', 'c'), ('d', 'd')]
('a', 'a')
('a', 'b')
('a', 'c')
('a', 'd')
('b', 'a')
('b', 'b')
('b', 'c')
('b', 'd')
('c', 'a')
('c', 'b')
('c', 'c')
('c', 'd')
('d', 'a')
('d', 'b')
('d', 'c')
('d', 'd')
```

#### 중복 조합

```python
from itertools import combinations_with_replacement

data = ['a', 'b', 'c', 'd']

# 중복 순열 구하기
result = list(combinations_with_replacement(data, 2))
print(result)

for x in combinations_with_replacement(data, 2):
    print(x)
```

```
[('a', 'a'), ('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'b'), ('b', 'c'), ('b', 'd'), ('c', 'c'), ('c', 'd'), ('d', 'd')]
('a', 'a')
('a', 'b')
('a', 'c')
('a', 'd')
('b', 'b')
('b', 'c')
('b', 'd')
('c', 'c')
('c', 'd')
('d', 'd')
```

### Collections

#### Counter

* 등장 횟수를 세는 기능
* iterable 객체가 주어졌을 때 특정원소가 몇 번씩 등장했는지 알려줌

```python
from collections import Counter

fruits = ['apple', 'orange', 'apple', 'grape', 'apple', 'grape', 'melon']
counter_example = Counter(fruits)

print(counter_example)

# 'apple' 그리고 'grape'가 등장한 횟수
print(counter_example['apple'])
print(counter_example['grape'])

# 사전 자료형으로 반환 후 출력
print(dict(counter_example))
```

```
Counter({'apple': 3, 'grape': 2, 'orange': 1, 'melon': 1})
3
2
{'apple': 3, 'orange': 1, 'grape': 2, 'melon': 1}
```



## 참고

---

1. [python document](https://docs.python.org/ko/3/library/itertools.html)
2. [이것이 취업을 위한 코딩 테스트다](https://www.youtube.com/watch?v=m-9pAwq1o3w&list=PLRx0vPvlEmdAghTr5mXQxGpHjWqSz0dgC&t=2921s)


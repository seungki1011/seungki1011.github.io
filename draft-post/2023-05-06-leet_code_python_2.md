---
# layout: post
# title:  "코딩 테스트를 위한 파이썬 - 2"
# author: seungki
# categories: [ Python ]
# tags: [코딩 테스트]
# image: post_images/python logo.png
# toc: True


---

---

## String

### String Operation

* ```+```을 이용해서 concat
* 양의 정수와 곱하는 경우, 그 값만큼 여러 번 더해짐
* 리스트와 마찬가지로 인덱싱과 슬라이싱 이용 가능
  * 문자열은 특정 인덱스의 값을 변경하는 것을 불가 (immutable)

---

## Tuple

### Tuple datatype

* 튜플은 리스트와 유사하나 한 번 선언된 값을 변경하지 못함 (immutable)
* 튜플은 소괄호```()```를 이용
* 튜플은 리스트에 비해 공간 효율적임
  * [https://builtin.com/software-engineering-perspectives/python-tuples-vs-lists](https://builtin.com/software-engineering-perspectives/python-tuples-vs-lists)
  * [https://nedbatchelder.com/blog/201608/lists_vs_tuples.html](https://nedbatchelder.com/blog/201608/lists_vs_tuples.html)

```python
t = (1,2,3,4,5)
print(t)
print(t[1:3])
```

```
(1, 2, 3, 4, 5)
(2, 3)
```

### 튜플 사용하기 좋은 경우(코테)

* 서로 다른 성질의 데이터를 묶어서 관리하는 경우
  * 최단 경로 알고리즘에서 (비용, 노드 번호) 형태로 관리
* 데이터의 나열을 Hashing의 키 값으로 사용하는 경우
  * 튜플은 immutable 하기 때문에 키 값으로 사용가능

---

## Dictionary

### Dictionary datatype

* key - value 쌍을 데이터로 가지는 자료형
* immutable 자료형을 키로 사용 가능
* 파이썬의 사전 자료형은 Hash Table을 이용
  * 데이터의 조회 및 수정을 O(1)의 시간으로 처리 가능

```python
data = dict()

data['name'] = 'ksk'
data['job'] = 'engineer'
data['location'] = 'seoul'

print(data)

if 'job' in data:
    print('job is found')
```

```
{'name': 'ksk', 'job': 'engineer', 'location': 'seoul'}
job is found
```

### Methods for dictionary type

* 사전 자료형은 key-value를 별도로 뽑아내기 위한 메서드 지원
  * key 데이터만 뽑아서 리스트로 이용 : ```keys()```사용
  * value 데이터만 뽑아서 리스트로 이용 : ```values()```사용

```python
data = dict()

data['name'] = 'ksk'
data['job'] = 'engineer'
data['location'] = 'seoul'

print(data)

key_list = data.keys()
value_list = data.values()

print(f'key 값을 담은 리스트 : {key_list}')
print(f'value 값을 담은 리스트 : {value_list}')
```

```
{'name': 'ksk', 'job': 'engineer', 'location': 'seoul'}
key 값을 담은 리스트 : dict_keys(['name', 'job', 'location'])
value 값을 담은 리스트 : dict_values(['ksk', 'engineer', 'seoul'])
```

---

## Set

### Set datatype

* 집합 자료형은 중복을 허용하지 않음
* 순서가 없음
  * [ordered set에 대해 알아보기](https://www.geeksforgeeks.org/python-ordered-set/)
  * [python set의 구현에 대해 알아보기](https://stackoverflow.com/questions/3949310/how-is-set-implemented)

* 리스트 또는 문자열을 이용해서 초기화 가능함
  * ```set()```함수를 이용해서 초기화
  * ```{}```안의 각 원소를 콤마 기준으로 구분해서 초기화
* 데이터의 조회 및 수정은 O(1)으로 처리 가능

```python
a = set([1,2,3,4,4,4,5,5])
print(a)

b_list = [1,1,2,2,3,4,5,6]
b_set = set(b_list)
print(b_set)

c = {1,1,1,2,2,3,4}
print(c)
```

```
{1, 2, 3, 4, 5}
{1, 2, 3, 4, 5, 6}
{1, 2, 3, 4}
```

### Set operation

* 합집합, 교집합, 차집합

```python
a_set = set(['a','a','b','c','d','e'])
b_set = set(['c','c','d','e','f','g'])

print(f'집합 a : {a_set}')
print(f'집합 b : {b_set}')

# 합지합
print(f'집힙 a와 b의 합집합 : {a_set | b_set}')

# 교잡합
print(f'집힙 a와 b의 교집합 : {a_set & b_set}')

# 차집합
print(f'집힙 a의 b에 대한 차집합 : {a_set - b_set}')
```

```
집합 a : {'a', 'b', 'd', 'c', 'e'}
집합 b : {'f', 'd', 'c', 'e', 'g'}
집힙 a와 b의 합집합 : {'a', 'f', 'b', 'd', 'c', 'e', 'g'}
집힙 a와 b의 교집합 : {'e', 'd', 'c'}
집힙 a의 b에 대한 차집합 : {'a', 'b'}
```

### Methods for set type

```python
data = {1,2,3,4}

# 새 원소 추가
data.add(6)
print(data)

# 원소 여러개 추가
data.update([6,7,8])
print(data)

# 특정 값을 가진 원소 제거
data.remove(1)
print(data)
```

```
{1, 2, 3, 4, 6}
{1, 2, 3, 4, 6, 7, 8}
{2, 3, 4, 6, 7, 8}
```

### 사전과 집합 자료형

* 리스트와 튜플과 달리 순서가 없기 때문에 인덱싱을 통해 값을 접근하는 것은 불가능
* 사전의 경우 key, 집합은 원소를 통해 조회(시간 복잡도 O(1))



## 참고

---

1. [이것이 취업을 위한 코딩 테스트다](https://www.youtube.com/watch?v=m-9pAwq1o3w&list=PLRx0vPvlEmdAghTr5mXQxGpHjWqSz0dgC&t=2921s)
2. [제대로 파이썬](https://wikidocs.net/22805)
3. [https://builtin.com/software-engineering-perspectives/python-tuples-vs-lists](https://builtin.com/software-engineering-perspectives/python-tuples-vs-lists)
4. https://www.geeksforgeeks.org/python-ordered-set/
5. https://stackoverflow.com/questions/3949310/how-is-set-implemented

---
layout: post
title:  "Numpy - 7(Numpy Performance)"
author: seungki
categories: [ Numpy ]
image: post_images/numpylogo.png
toc: True
---
---
## Numpy performance check
### timeit
* Jupyter 환경에서 코드의 퍼포먼스 체크하는 함수

```python
def sclar_vector_product(scalar, vector):
    result = []
    for value in vector:
        result.append(scalar * value)
    return result

iternation_max = 100000000
vector = list(range(iternation_max))
scalar = 2
```

```python
%timeit sclar_vector_product(scalar, vector) # for loop을 이용한 성능
%timeit [scalar * value for value in range(iternation_max)]
# list comprehension을 이용한 성능
%timeit np.arange(iternation_max) * scalar # numpy를 이용한 성능
```



### 속도 비교

> 일반적으로 속도는
>
> for loop < list comprehension < numpy

* 100,000,000번(1억 번)의 loop가 돌 때, 약 4배 이상의 성능 차이
* numpy는 C로 구현되어 있어, 성능을 확보하는 대신 파이썬의 dynamic typing을 포기함
* 대용량 계산에서는 가장 흔히 사용됨
* concatenate 처럼 계산이 아닌 할당에서는 연산 속도의 이점 없음



## 참고

---

1. [부스트 코스 AI numpy - 최성철](https://www.boostcourse.org/onlyboostcampaitech5/lecture/1456479?isDesc=false)


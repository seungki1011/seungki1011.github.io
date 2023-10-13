---
#layout: post
#title:  "Pandas 실습 - 1"
#author: seungki
#categories: [ Data Engineering, Pandas ]
#tags: [Pandas, Data Processing]
#image: post_images/pandaslogo.png
#toc: True


---

---

Pandas 라이브러리를 사용한 실습 및 정리.

---

## 소개

Pandas는 데이터 조작을 위한 두 가지 구조를 지원해준다.

* DataFrame
  * 데이터프레임은 2차원 형태의 데이터 구조
  * Data aligned in tabular fashion (rows and columns) 
  * 리스트, 사전 자료형으로부터 만들 수 있다
* Series
  * 인덱스가 붙은 데이터의 1차원 배열

인덱스는 데이터 값에 접근하기 위해서 사용한다. 데이터 프레임의 열을 Series라고 볼 수 있다.

 
---
layout: post
title:  "Versioning"
author: seungki
categories: [ Software Engineering ]
image: post_images/versioning.png
toc: True

---
---
## Version and Versioning
### 버전(Version)
* 소프트웨어 제품의 특정 릴리스에 대한 고유한 식별자
* 소프트웨어의 출시나 업데이트가 이루어질 때마다 새로운 버전을 부여함

<br>

### 버저닝(Versioning)

* 소프트웨어의 버전 작성은 특정 상태에 대한 유일한 버전 번호를 결정하는 일이라고 보면 된다
* 다양한 버전을 관리하고 식별하기 위해 사용되는 방법

<br>

### 버저닝 방법(Versioning strategy)

1. **CalVer(Calendar Versioning)**

   * 날짜 기반 시스템을 활용한 버저닝
   * 버전 번호는 연도와 월로 구성
   * 날짜 기반으로 출시 시기 예측이 수월
   * ex. Ubuntu 20.04

   

   <img src="../post_images/Versioning/calVersioning.png" alt="calVersioning" style="zoom: 67%;" class="center-image"/>

   <p align="center">출처 - https://blog.datalust.co/switching-to-calendar-versioning/ </p>

<br>

2. **SemVer(Semantic Versioning)**

   * 마침표로 구분된 주 번호, 부 번호, 패치 번호로 구성
   * 이전 버전과 호환되지 않은 변경이 있는 경우 주 번호 증가
   * 이전 버전과 호환되며 새로운 기능이 추가되면 부 번호 증가
   * 이전 버전의 버그 수정이 진행되면 패치 번호가 증가
   * ex. Python 3.11.0

   

<img src="../post_images/Versioning/sem ver.png" alt="sem ver" style="zoom: 67%;" class="center-image"/>

<p align="center">출처 - https://forums.ubports.com/topic/1822/semantic-versioning-for-ut </p>

<br>

3. **HashVer(Hash Versioning)**
   * SHA-1, SHA-256 해시 알고리즘을 사용해 버전에 대한 고유 식별자를 생성
   * 코드가 변결될 때마다 해시가 변경되므로 모든 버전이 고유한 식별자를 가지도록 보장
   * ex. Git command 7e6d3fd



버저닝이라는 것은 결국 코드의 특정 상태를 표현하는 것이 핵심이다. 협업을 할 때에도 특정 상태에 대한 통일된 명칭을 만들어야 커뮤니케이션이 원활하다는 것을 알 것이다.

<br>

## 참고

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://semver.org/](https://semver.org/)
3. [https://calver.org/](https://calver.org/)

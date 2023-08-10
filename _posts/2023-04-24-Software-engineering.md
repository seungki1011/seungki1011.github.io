---
layout: post
title:  "Software Engineering"
author: seungki
categories: [ Software Engineering ]
image: post_images/소프트웨어엔지니어링.jpeg
toc: True

---

---
## 소프트웨어 엔지니어링이란
소프트웨어의 개발, 운용, 유지보수 등의 life cycle 전반을 체계적이고 정량적으로 다루는 개념이다. 한 마디로 소프트웨어의 품질과 유지 보수성을 보장하는 학문이라고 봐도 무방할 것 같다.

---

## Software Development Life Cycle(SDLC)

소프트웨어의 개발 수명 주기는 고품질 소프트웨어를 설계하고 구축하기 위해 필수적인 비용 및 시간 효율적인 프로세스이다.

### 계획(Planning) & 분석(Analysis)

* 비용 분석, 스케쥴링, 리소스 추정 및 할당과 같은 작업
* client, 전문가, 관리자 등 여러 이해 관계자들의 요구 사항을 수집하여 공통 목표를 정의
  * 보통 협의된 요구사항들에 대해서 문서화 해서 수령하고, 이 요구사항에 대한 문서를 SRS(Software Requirement Specification)라고 부릅니다
* 공통 목표를 달성하기 위한 세부 계획을 수립

### 설계(Design architecture)

* 요구 사항을 만족하는 최적의 솔루션 찾기
* 모듈을 통합하거나, 기술을 선택하고, 개발 도구를 찾고 기능이 동작할 수 있는 아키텍쳐를 설계하는 단계
* 데이터의 flow나 동작에 대한 고민

### 구현(Implementation)

* 실제적인 제품의 개발이 시작되는 단계
* 개발 가이드라인을 준수하면서 코드의 개발부터 시작해서 통합해서 빌드하는 단계까지 모두 포함

### 검증(Testing)

* 기능이 동작하는지, 오류가 있는지 테스트하는 단계
* client의 요구 사항을 충족하는지 확인하는 작업이 포함
* 구현 단계와 동시에 진행되는 경우가 많음

### 배포(Deployment)

* 사용자가 사용하는 소프트웨어를 ***프로덕션*** 이라고 하고 개발팀에서 지속적으로 개발하고 테스트하는 소프트웨어의 복사본을 **테스트 환경** 또는 **빌드 환경**
* 패키징, 환경 구성 및 설치 하는 작업도 배포에 포함

### 유지관리(Maintenance)

* 소프트웨어의 변경 사항 관리, 버그 픽스, 성능 및 사용자 환경 모니터링이 들어가는 단계



<img src="../post_images/2023-04-24-Software-engineering/SDLC_BWC.png" alt="SDLC_BWC" style="zoom: 67%;" class="center-image"/>

<p align="center">출처 - https://bigwater.consulting/2019/04/08/software-development-life-cycle-sdlc/ </p>



SDLC는 위 과정을 계속 반복하는 프로세스. SDLC 모델들은 여러가지가 존재하고, 다른 수명 주기 방법론과 intersect 하는 부분도 많기 때문에 관심이 있다면 terminology에 대한 명확한 설명을 더 찾아보는 것도 좋을 것 같다.

---

## 소프트웨어의 설계

### Modularity, Cohesion, Coupling

1. **모듈성(modularity)**

   * 소프트웨어에서 임의의 두 부분이 직접적인 상호관계가 많아지면 모듈성이 떨어짐
   * 시스템의 구성 요소가 분리되고 재결합 될 수 있는 정도

   

2. **응집도(cohesion)**

   * 모듈 내부의 기능적인 응집 정도
   * 하나의 모듈은 하나의 기능을 수행하는 것이 이상적
   * 하나의 클래스에 모든 기능을 구현하는 것이 아닌 목적에 맞게 나누고 교류하는 인터페이스가 중요

   

3. **결합도(coupling)**
   * 모듈과 모듈같의 상호 결합 정도, 모듈 간의 상호의존성을 나타내는 정도



응집도와 결합도에서 보통 응집도는 높을수록 좋고 결합도는 낮을수록 이상적이다. 응집도와 결합도의 다양한 유형에 대해 추가적으로 알아봐도 좋을 것 같다.



<img src="../post_images/2023-04-24-Software-engineering/modularity.png" alt="modularity" style="zoom:67%;" class="center-image"/>

<p align="center">출처 - https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion </p>

---

## Testing

소프트웨어 개발에서의 테스트는 넓게 보면 프로그램이 예상대로 작동하고 문제가 없는지 확인하는 과정이라고 생각하면 좋을 것 같다. 조금 더 자세히 말하자면 사용자가 안정적으로 소프트웨어를 사용할 수 있도록, 기능이 추가될 때 기존 시스템에서의 오류 확인, 아키텍쳐 확인, 서버에 대한 확인, 데이터베이스의 연결에 대한 확인 등 여러가지 단계가 포함된다.



<img src="../post_images/2023-04-24-Software-engineering/test level.png" alt="test level"  class="center-image"/>

<p align="center">출처 : https://www.geeksforgeeks.org/levels-of-software-testing </p>



딥러닝에서의 testing life cycle에 대해서 더 알아봐야겠다.

---

## 문서화(Documentation)

소프트웨어를 위한 Readme, API 문서, 아키텍쳐 문서 등이 여기에 포함.

파이토치의 documentation을 예시로 들자면

* Pytorch에 대한 소개와 설명
* OS별 설치 방법
* 시작 방법
* 추가 학습 자료
* 오픈소스에 기여하는 방법

---

## 소프트웨어 엔지니어링 역량의 필요성

머신러닝 모델을 설계하고 만드는 것은 전체 과정의 극히 일부. 결국 product를 serving하기 위해서는 소프트웨어 엔지니어링은 필수적이다. 전체 시스템을 알기 위해서는 소프트웨어 엔지니어링 관점으로 생각을 확장해야 함.



<img src="../post_images/2023-04-24-Software-engineering/hidden technical deby in machine learning systems.png" alt="hidden technical deby in machine learning systems" style="zoom: 67%;" class="center-image"/>

<p align="center">출처 : Hidden Technical Debt in Machine Learning Systems </p>

<br>

## 참고

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://zzsza.github.io/](https://zzsza.github.io/)
3. [https://aws.amazon.com/ko/what-is/sdlc/](https://aws.amazon.com/ko/what-is/sdlc/)
4. [https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion/](https://www.geeksforgeeks.org/software-engineering-coupling-and-cohesion/)


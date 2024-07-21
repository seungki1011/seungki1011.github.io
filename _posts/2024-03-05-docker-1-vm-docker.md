---
title: (Docker - 1) VM과 도커의 등장
description: 가상화 기술, 도커 소개, 도커 동작 방식
author: seungki1011
date: 2024-03-05 12:30:00 +0900
categories: [8. 컨테이너(Container), Docker]
tags: [docker]
math: true
mermaid: true
---

---

## 1. 가상화(Virtualization)

### 1.1 가상화 소개

가상화(virtualization)는 서버, 스토리지, 네트워크 및 기타 물리적 시스템에 대한 가상 표현을 생성하는데 사용할 수 있는 기술이다. 가상 소프트웨어는 물리적 하드웨어 기능을 모방하여 하나의 물리적 머신에서 여러 가상 시스템을 동시에 실행할 수 있다.

가상화는 간단하게 말하자면 Local이나 Production 서버에서의 환경을 위한 일종의 템플릿이라고 생각할 수 있다. 개발과 운영 서버의 환경 불일치를 해소할 수 있고, 어느 조건에서나 동일한 환경으로 프로그램을 실행 할 수 있게 된다.

<br>

---

### 1.2. VM(Virtual Machine, 가상 머신)

가상 머신(VM)은 실제 컴퓨터의 가상 표현 또는 에뮬레이션이다. 이를 종종 게스트(Guest)라고 하며, 이를 실행하는 실제 시스템을 호스트(Host)라고 한다. 

쉽게 말해서, VM은 호스트 시스템(Host System)이라고 하는 실제 물리적인 컴퓨터 위에 OS를 포함한 가상화 소프트웨어를 두는 방식이라고 이해하면 된다. 설명에서도 알 수 있듯이, OS 위에 OS를 하나 더 실행시킨다는 점에서 굉장히 많은 리소스를 사용하게 된다. (VM의 하드웨어, OS, 애플리케이션 전부 호스트 시스템 위에서 프로세스로 구현되기 때문에 무겁다)

<br>

![http](../post_images/2024-03-05-docker-1-vm-docker/vm1.png)

<p align='center'>Virtual Machine</p>

* 하이퍼바이저(hypervisor)의 위치에 따라 1형 또는 2형 하이퍼바이저로 분류할 수 있다
* **Type1(Bare-metal Hypervisor)**
  * 기본 시스템 하드웨어와 직접 상호작용
  * 호스트 OS 없이 호스트 시스템의 물리적 하드웨어에 직접 설치된다
  * Type2 보다 오버헤드가 적음
  * 사용 상황 : 데이터 센터, 프로덕션 환경과 같은 고정 애플리케이션
  * 예) Hyper-V, KVM, ESXi



* **Type2(Hosted Hypervisor)**
  * 호스트 OS를 통해 호스트 시스템의 컴퓨터 하드웨어와 상호작용한다
  * 애플리케이션으로 실행되는 시스템에 설치한다, 하이퍼바이저는 OS 위에서 소프트웨어로서 동작한다
  * Host OS 위에 소프트웨어적으로 동작하기 때문에 오버헤드가 크다
  * Host OS의 문제가 전체 Guest OS에 영향을 줄 수 있다
  * 사용 상황 : 운영에 중요하지 않은 데스크톱 또는 개발 환경에 활용
  * 예) VirtualBox, Workstation

<br>

---

### 1.3 컨테이너(Container)

컨테이너의 정의를 찾아보면, **"소프트웨어 서비스를 실행하는 데 필요한 특정 버전의 프로그래밍 언어 런타임 및 라이브러리와 같은 종속 항목과 애플리케이션 코드를 함께 포함하는 경량 패키지이다."** 라고 하는 것을 찾을 수 있다.

쉽게 말하자면 어떤 환경에서든 애플리케이션을 실행할 수 있도록 하기 위해서, 모든 요소를 포함하는 상자 안에 가상 환경을 만들었다고 생각하면 편하다. 

이런 패키지와 같은 가상 환경은 일정 수준의 격리성(Isolation)과 이식성(Portability)을 제공하기 때문에 컨테이너에 비유된다.

<br>

![http](../post_images/2024-03-05-docker-1-vm-docker/con1.png)

<p align='center'>Container</p>

* 애플리케이션이 동작하기 위한 모든 컴포넌트가 들어간 패키지를 컨테이너(Container)라고 하고, 이런 컨테이너는 컨테이너 엔진(런타임)만 있으면 어떤 호스트 시스템 위에서든 작동한다
* 컨테이너는 Guest OS와 하이퍼바이저(Hypervisor)가 필요하지 않기 때문에, 기존 VM에 비해 가볍다
* 일정 수준의 격리성, 이식성을 제공하면서 VM 대비 가벼운 특징 때문에 컨테이너를 통한 서비스의 스케일링(Scaling)이나 마이그레이션(Migration)이 VM보다 용이하다
* 가볍고, 컨테이너 단위로 애플리케이션을 관리하기 쉽고, 스케일 인과 아웃이 상대적으로 쉽기 때문에 클라우드 네이티브(Cloud Native)를 실현하는 중심 기술 중 하나이다

<br>

---

## 2. 도커(Docker)

### 2.1 Docker 소개

도커는 컨테이너를 생성, 실행, 관리, 배포하는 과정을 편리하게 만들어주는 오픈소스 플랫폼이다.

도커는 LCX(Linux Container)라는 기술을 기반으로 동작한다. 도커는 기본적으로 리눅스(Linux) 위에 동작하기 위해서 만들어진 것이기 때문에, 타 운영체제에서 동작하기 위해서는 가상화 기술을 사용한다(쉽게 말해서 리눅스 외의 환경에서 도커를 사용하면 오버헤드가 발생할 수 있다).

<br>

> 도커의 내부 동작 원리를 살펴보고 싶으면 다음의 키워드로 검색하는 것을 추천한다.
>
> * Linux Containers
> * namespaces
> * control groups(cgroups)
> * chroot
> * Docker Engine, Containerd
{: .prompt-tip }

<br>

![http](../post_images/2024-03-05-docker-1-vm-docker/docker1.png)

<p align='center'>Docker image and container</p>

도커에서 컨테이너를 생성하는 과정을 간략히 설명하자면 다음과 같다.

<br>

1. **Dockerfile 생성**
   * Dockerfile은 도커 이미지를 빌드하기 위한 명령어를 포함한 텍스트 파일
   * 사용할 베이스 이미지(base image)에 대한 설정, 필요한 애플리케이션 코드 추가, 의존성(dependency) 추가, 런타임시 수행할 명령어 명시 등이 Dockerfile에 포함된다
   * 베이스 이미지의 경우 DockerHub에서 벤더가 공식적으로 지원하는 이미지를 사용하는 경우가 많다

2. **Docker image 빌드**
   * `docker build` 명령어로 Dockerfile에 기반한 이미지를 만든다
   * 사용할 도커 이미지 파일이 이미 존재하면 해당 이미지 파일을 사용하면 됨

3. **Docker container 실행**
   * `docker run` 명령어로 도커 이미지에 기반한 컨테이너를 실행할 수 있다
   * 컨테이너의 런타임 환경과 관련된 설정을 위한 옵션들을 추가할 수 있다

<br>

---

### 2.2 Docker Architecture

도커는 기본적으로 클라이언트-서버 아키텍쳐를 사용한다. 

<br>

![http](../post_images/2024-03-05-docker-1-vm-docker/dockerarch.webp)

<p align="center">https://docs.docker.com/get-started/overview/#docker-architecture</p>

* **Docker Client**
  * 유저가 도커 엔진과 상호작용할 수 있도록 해주는 CLI 도구
  * 유저들은 도커 클라이언트를 통해서 이미지와 컨테이너 관련 작업들을 수행할 수 있다
  * 도커 클라이언트는 Docker API를 통해 도커 데몬(Docker Daemon)과 요청을 주고 받는다



* **Docker Host**
  * 도커 엔진을 실행하면서 컨테이너들을 호스트 해주는 가상 또는 물리적인 머신을 가리킨다
  * 도커 클라이언트와 호스트가 무조건 같은 로컬에 존재하지 않아도 연결할 수 있다



* **Docker Daemon**(`dockerd`)
  * 컨테이너, 이미지, 볼륨, 네트워크와 같은 도커 오브젝트들을 관리해주는 호스트 시스템 위에서 동작하는 백그라운드 서비스이다
  * 도커 클라이언트로 부터 도커 API 요청을 받고 도커 이미지와 컨테이너에 관한 작업을 수행할 수 있다
  * 아래에서 동작하는 컨테이너 런타임(Containerd)과 상호작용을 하면서 컨테이너 관련 작업과 수명주기(life-cycle)를 관리한다
  * 도커 엔진(Docker Engine)과 상호 교환적으로 용어가 사용될 수 있지만, 보통 도커 엔진은 도커 데몬과 컨테이너 런타임 등을 포함한 더 넓은 범위의 컴포넌트들을 포함한다



* **Docker Registry**
  * 도커 이미지들을 저장하고 있는 중앙 레포지토리
  * 명령어를 통해서 사용자들은 도커 이미지를 `push`(업로드), `pull`(다운로드), 등을 할 수 있다
  * Docker Hub가 Docker가 공식적으로 운영하고 있는 레지스트리(registry)이다 

<br>

---

### 2.3 Docker Hub 소개

Docker가 공식적으로 운영하고 있는, 도커 이미지를 공유하고 관리하기 위한 레지스트리.

도커 허브(Docker Hub)에는 maintainer 들이 제공하는 공식 이미지들과, 사용자들이 직접 만든 이미지를 포함한 다양한 이미지들이 등록되어 있다.

도커 허브를 통해서 각종 이미지들을 업로드 및 다운로드를 할 수 있다.

* Docker Hub 사이트 : [https://hub.docker.com/](https://hub.docker.com/)

---

## Reference

1. [Complete Docker Course - DevOps Directive](https://www.youtube.com/watch?v=RqTEHSBrYFw&list=WL&index=49)
2. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
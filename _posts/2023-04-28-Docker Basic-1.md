---
layout: post
title:  "Docker Basics (1)"
author: seungki
categories: [ Docker ]
image: post_images/dockerlogo.png
toc: True

---

---
## Virtualization
### 가상화란 무엇인가
가상화는 서버, 스토리지, 네트워크 및 기타 물리적 시스템에 대한 가상 표현을 생성하는데 사용할 수 있는 기술이다. 가상 소프트웨어는 물리적 하드웨어 기능을 모방하여 하나의 물리적 머신에서 여러 가상 시스템을 동시에 실행할 수 있다.

가상화는 간단하게 말하자면 Local이나 Production 서버에서의 환경을 위한 일종의 템플릿이라고 생각할 수 있다.   개발과 운영 서버의 환경 불일치를 해소할 수 있고, 어느 조건에서나 동일한 환경으로 프로그램을 실행 할 수 있게 된다.

<br>

## Virtual Machine vs Docker

### VM(Virtual Machine)

도커의 등장 전에는 주로 VM(Virtual Machine)을 사용했다. VM은 호스트 머신이라고 하는 실제 물리적인 컴퓨터 위에 OS를 포함한 가상화 소프트웨어를 두는 방식이라고 이해하면 된다. 그러나 이러한 방식은 OS 위에 OS를 하나 더 실행시킨다는 점에서 굉장히 많은 리소스를 사용하게 된다(무겁다). 

<br>

### Container

컨테이너는 어떤 환경에서나 실행하기 위해 필요한 모든 요소를 포함하는 소프트웨어 패키지같은 형태이다. 컨테이너의 정의를 찾아보면, 

> *소프트웨어 서비스를 실행하는 데 필요한 특정 버전의 프로그래밍 언어 런타임 및 라이브러리와 같은 종속 항목과 애플리케이션 코드를 함께 포함하는 경량 패키지이다.*

으로 정의된다. 



<img src="../post_images/Docker Basic/containers-vs-virtual-machines.jpg" alt="containers-vs-virtual-machines" style="zoom:67%;" class="center-image" />

<p align="center"> 출처 - https://www.weave.works/blog/a-practical-guide-to-choosing-between-docker-containers-and-vms</p>



VM의 경우 host OS 위에 다시 guest OS가 존재하는 형태인 반면에, 컨테이너는 OS 하나 위에서 OS에 상관없이 컨테이너를 띄우는 것을 볼 수 있다.

<br>

## Docker

### 도커 소개

도커는 이런 컨테이너에 기반한 개발과 운영을 매우 빠르게 확장 할 수 있는 오픈소스 프로젝트이다.

도커에 대해 간단히 설명하자면, 도커의 이미지를 만들어두면 재부팅 할 경우 도커의 이미지 상태로 다시 실행이 된다고 보면 된다.

<img src="../post_images/Docker Basic/docker image container.webp" alt="docker image container" style="zoom:50%;" class="center-image"/>

<p align="center"> 출처 - https://medium.com/swlh/understand-dockerfile-dd11746ed183</p>



* Docker Image : 컨테이너를 실행할 때 사용할 수 있는 Template (Read only)
* Docker Container : Docker Image를 활용해 실행된 인스턴스 (Write allowed)

<br>

### 도커로 할 수 있는 일

다른 사람이 만든 소프트웨어를 가져와서 바로 사용 할 수 있음

* MySQL을 도커로 실행
* Jupyter Notebook을 도커로 실행

이 때 다른 사람이 만든 소프트웨어를 Docker Image라고 이해하면 되고, OS를 포함한 실행 환경이 저장되어 있다.  Linux, Windows 등 어디서나 동일하게 실행할 수 있다.

<br>

## 도커로 MySQL 실행 해보기

### 도커 실행

1. ```docker```명령어로 도커 동작 확인

   

2. ```docker pull mysql:8```로 mysql 8 버전의 이미지를 다운

   

3. ```docker images```로 다운 받은 이미지 확인

   

4. ```docker run --name mysql-tutorial -e MYSQL_ROOT_PASSWORD=0000 -d -p 3306:3306 mysql:8``` 

   * 다운 받은 MySQL 이미지 기반으로 docker container를 만들고 실행
   
   * ```--name mysql-tutorial``` : 컨테이너의 이름을 ```mysql-tutorial``` 로 정하겠다는 것. 설정 하지 않으면 랜덤으로 생성 됨
   
   
   * ```-e MYSQL_ROOT_PASSWORD=0000``` : 환경변수 설정을 하는 부분. 사용하는 이미지에 따라 설정이 다르지만, 현재 하고 있는 MySQL의 경우 환경변수를 통해 root 계정의 비밀번호를 설정하고 있음.
   
   
   * ```-d``` : 데몬(백그라운드) 모드. 컨테이너를 백그라운드 상태로 실행. 이 설정을 하지 않을 경우, 현재 실행하는 셸 위에서 컨테이너가 실행되고 컨테이너의 로그를 바로 볼 수 있지만, 컨테이너를 나갈 경우 실행이 종료 됨.
   
   
   * ```-p 3306:3306``` : 포트 지정. ``` -p {localhost port}:{container port}``` 형태로, 현재의 경우 로컬 포트 3306으로 접근 시 컨테이너 포트 3306으로 연결되도록 설정. MySQL은 기본적으로 3306 포트로 통신함.
   



5. ```docker ps``` 로 실행한 컨테이너와 정보를 확인 할 수 있음

   


6. ```docker exec -it mysql-tutorial /bin/bash``` MySQL이 실행되고 있는지 확인하기 위해 컨테이너로 진입 할 수 있다. Compute engine에서 SSH와 접속하는 것과 유사하다.

   * ```docker exec -it {container name or ID} /bin/bash```

   

7. ```mysql -u root -p``` MySQL 프로세스로 들어가면 MySQL 쉘 화면이 보인다.

   


8. ```docker stop {container name or ID}``` 실행 중인 컨테이너를 멈출 수 있다.

   

9. ```docker ps -a```로 작동을 멈춘 컨테이너를 확인 할 수 있다. ```docker ps```의 경우 실행중인 컨테이너 목록만 보여줌.

   

10. ```docker rm {container name or ID}``` 으로 멈춘 컨테이너 삭제 가능

    * ```docker rm {container name or ID} -f``` 로 실행중인 컨테이너도 삭제 가능

<br>

### Volume mount

* Docker run 할 때 파일이 자동으로 공유가 되는 것이 아님. 호스트와 컨테이너를 연결(sync) 해주는 것이 volume mount.

* docker container는 특별한 설정이 없으면 컨테이너를 삭제할 때 파일이 사라짐

* Host와 container는 처음부터 파일 공유가 되지 않음

* 파일을 유지하고 싶을 경우 host와 container의 저장소를 공유해야 함

* Volume mount를 진행하면 host와 container의 폴더가 공유됨

* ```-v``` 옵션을 사용하며 port 처럼 사용함. ```-v host_folder:container_folder``` 

* ex. ```docker run -it -p 8888:8888 -v /some/host/folder/for/work : /home/workspace/jupyter/note```

<br>

### DockerHub

필요한 이미지가 있을 경우, 공개된 모든 이미지를 다운받을 수 있다. 



<img src="../post_images/Docker Basic/dockerhub sql.PNG" alt="dockerhub sql" style="zoom:67%;" class="center-image"/>

<br>

### Docker Image 만들기

pytorch example 코드를 실행하는 docker image 생성 해보기

<br>

#### Dockerfile 생성

* ```vi Dockerfile``` 로 만들든 gui로 만들든 Dockerfile을 생성해서 필요한 내용을 작성한다.

```bash
From pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime
```

* ```From {image name}:{tag}``` 형식은 이미지 빌드에 사용할 베이스 이미지를 지정하는 것이다. 보통 공개된 이미지 기반으로 새로운 설정을 추가하는 방법으로 사용.

```bash
copy . /app
```

* ```copy {로컬 디렉토리(파일)} {컨테니어 내 디렉토리(파일)}``` 컨테이너는 자체적인 파일 시스템을 가짐. ```copy```명령어는 dockerfile이 존재하는 경로 기준 로컬 디렉토리를 컨테이너 내부의 디렉토리로 복사한다.

* 해당 코드의 경우 프로젝트 최상위에 존재하는 모든 파일을 컨테이너 내부 /app 디렉토리로 복사한다.

* 파일을 컨테이너에서 사용하고 싶으면 반드시 ```copy```를 써서 복사해야 함.

  

```bash
WORKDIR /app
```

* ```WORKDIR {컨테이너 내 디렉토리}``` dockerfile의 RUN , CMD, ENTRYPOINT 등의 명령어를 실행할 컨테이너 경로를 지정한다. 아래 라인에 등장하는 RUN, CMD는 컨테이너 내부의 /app에서 실행한다.



```bash
ENV PYTHONPATH=/app
ENV PYTHONBUFFERED=1
```

* ```ENV {환경변수 이름=값}``` 컨테이너 내의 환경변수를 지정한다. 파이썬 애플리케이션의 경우 보통 위의 두 값을 지정한다.

  

```bash
RUN pip install pip==23.0.1 && \
	pip install poetry==1.2.1 && \
	poetry export -o requirements.txt && \
	pip install -r requirements.txt
```

* ```RUN```은 컨테이너 내에서 리눅스 명령어를 실행한다. 한번에 실행할 명령어가 여러 대인 경우 && \로 이어준다. 이전 라인에서 ```COPY``` 와 ```WORKDIR```이 실행 되었기 때문에 requirements.txt가 존재하고, 이를 ```pip install -r``` 명령어로 실행할 수 있다.



```bash
CMD ["python", "main.py"]
```

* ```CMD ["실행할 명령어", "인자", ..]``` docker run으로 이미지를 기반으로 컨테이너를 만들 때, 실행할 명령어의 이미지는 실행되는 즉시 python main.py를 실행한다. ```CMD```는 띄어쓰기를 사용하지 않는다.

<br>

### Docker Image Build

```bash
docker build -t {빌드할 이미지 이름:태그 이름} {Dockerfile이 위치한 경로}
```

```bash
docker build -t 02-docker:latest .
```

* 이미지 생성
* 아래 이미지에서 . 는 현태 폴더에 Dockerfile이 있음을 의미
* -t {빌드할 이미지 이름:태그 이름} 옵션으로 이미지 이름과 태그 지정
* 태그 미지정시 "latest"로 채워짐

<br>

* 빌드를 마치면 ```docker images```명령어로 방금 빌드한 이미지를 확인 할 수 있다.

```bash
docker images | grep 02-docker
```

<br>

### Docker Image 실행

```bash
docker run {image name:tag}
```

* 빌드한 이미지를 실행 할 수 있음
* 태그가 latest인 경우 생략 가능

```bash
docker run 02-docker:latest
```

<br>

### Dockerfile 기타

* ```EXPOSE``` : 컨테이너 외부에 노출할 포트 지정

* ```ENTRYPOINT``` : 이미지를 컨테이너로 뛰울 때 항상 실행하는 커맨드

<br>

### Docker Image Push

* 우리가 만든 이미지를 업로드 할 수 있다. 이를 위해 대표적인 registry인 Dockerhub에 도커 이미지를 push 할 수 있다. (github과 비슷함)

* ```docker login``` 명령어로 내 dockerhub 계정을 cli에 연동 할 수 있음.

* ```docker tag {기존 이미지:태그} {새 이미지 이름:태그}``` dockerhub에 올릴 이미지 이름은 내 계정ID/이미지 이름 형태여야 함.

* ```docker push {이미지이름:태그}``` dockerhub에 이미지를 psuh 한다. Dockerhub에서 push된 이미지 확인 가능.

* 내가 push한 이미지는 pull로 언제든지 다시 받을 수 있음.

<br>

## 참고

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://github.com/zzsza](https://github.com/zzsza)
3. [https://aws.amazon.com/ko/what-is/virtualization/](https://aws.amazon.com/ko/what-is/virtualization/)
4. [https://cloud.google.com/learn/what-are-containers?hl=ko](https://cloud.google.com/learn/what-are-containers?hl=ko)


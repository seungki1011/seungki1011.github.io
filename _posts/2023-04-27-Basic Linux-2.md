---
layout: post
title:  "Linux Basics (2)"
author: seungki
categories: [ Linux ]
image: post_images/linuxlogo.png
toc: True


---
---
## 표준 스트림(standard stream)
표준 스트림은 프로그래밍 언어의 인터페이스를 비롯한 유닉스 계열 운영체제에서 컴퓨터 프로그램과 단말기 사이에 미리 연결된 입출력 통로를 가르킨다. 유닉스에서 통작하는 프로그램은 실행 시 3개의 스트림이 자동으로 열린다. 입력을 위한 스트림(Standard Input, STDIN, 0), 출력을 위한 스트림(Standard Output, STDOUT, 1), 마지막으로 오류 메시지의 출력을 위한 스트림(Standard Error , STDERR, 2)가 존재한다. 

보통 입출력은 물리적으로 연결된 콘솔을 통해 일어나는데, 표준 스트림을 이것을 추상화한 것이라고 보면 된다.



<img src="../post_images/Basic Linux2/Stdstreams.png" alt="Stdstreams" style="zoom: 50%;" class="center-image"/>

<p align="center">출처 : https://en.wikipedia.org/wiki/Standard_streams</p>


​    

* Standard Input, STDIN, 0 : 입력(비밀번호, 커맨드 등)
* Standard Output, STDOUT, 1 : 출력(터미널에 나오는 값)
* Standard Error , STDERR, 2 : 디버깅 정보나 에러 출력

---

## 환경 변수(Enviroment Variable)

### 환경 변수 소개

* OS level에서 선언하는 변수
* 해당 운영체제 환경에서 실행되는 프로세스가 모두 참조 가능
* 사용하는 경우
  * 자주 사용하는 경로를 저장
  * 기존 변수를 이용한 새로운 변수 저장
  * 프로세스가 실행중 참조할 값을 미리 환경변수에 할당하고 프로세스 실행
  * 여러 프로세스가 참조해야하는 값을 환경변수에 할당

### 임시 선언

* ```export ENV_VAR_NAME=value```
* 시스템 재부팅 또는 로그아웃 시 환경변수 값이 사라짐
* 설정한 환경변수는 ```$ENV_VAR_NAME```으로 불러올수 있음

### 기존 변수 활용

* ```export ENV_VAR_NAME=$ENV_VAR_NAME:{다른내용}```
* ```$ENV_VAR_NAME```으로 기존 환경변수 사용함

### 유저레벨 선언

* 특정 유저에게 영구적으로 적용하고 싶은 경우
* ```~/.bash_profile``` 파일 수정 (홈디렉토리에 존재)
  * user가 처음 로그인할 때 수행됨
* bash shell로 접속했을 때만 동작
  * sh 또는 zsh로 접속시 동작하지 않음

### 영구히 선언

* 모든 유저에게 영구히 적용
* ```/etc/profile``` 파일 수정
* ```sudo```권한 필요

### $PATH

* 운영체제가 명령어의 실행파일을 찾는 경로
* ```which```가 활용
* 추가하기 위해서는 ```export PATH=$PATH:{경로}```
* 프로그램을 설치해서 명령어를 사용할 수 있다는 것은, 해당 프로그램에 대한 PATH를 추가했거나 기존의 PATH에 설치했기 때문

---

## Redirection and Pipe

### Redirection

* 프로그램의 출력을 다른 파일이나 스트림으로 전달하는 것.
  * ``` < ```

* 스트림의 흐름을 바꿔주는 것이라고 이해하면 편하다.

### Pipe

* 프로그램의 출력을 다른 프로그램의 입력으로 사용하고 싶을 때 사용한다. 예를 들어 A라는 명령어의 output을 B의 input으로 사용하고 싶을 경우 처럼, 다양한 커맨드를 조합하는 방식으로 사용 할 수 있다.

* ```ls | grep "vi"``` : 현재 폴더에 있는 파일 명 중 "vi" 가 들어간 단어를 찾기 

---

## 서버에서 자주 사용하는 쉘 커맨드

### ps

* Process Status의 약자. 현재 실행되고 있는 프로세스를 출력한다. 

* ```-e``` : 모든 프로세스

* ```-f``` : full format으로 자세히 보여줌

<img src="../post_images/Basic Linux2/ps.PNG" alt="ps" style="zoom:100%;" class="center-image"/>

### curl

* Client URL의 약자. CL 기반의 data transfer 커맨드이다. Request를 테스트 할 수 있는 명령어이다. 웹 서버를 작성한 후 요청이 제대로 실행되는지 확인할 수 있다.

* ``` curl -X localhost:5000/ {data}``` 

* ```curl``` 외에도 ```httpie``` 또는 ```Postman``` 등이 있다.

### df

* Disk Free의 약자. 현재 사용 중인 디스크의 용량을 확일 할 수 있다.

* ```-h``` : 읽기 쉬운 형태로 출력

### scp

* Secure Copy의 약자. SSH를 이용해 네트워크로 연결된 호스트 간 파일을 주고 받는 명령어이다.

* ```-r``` : 재귀적으로 복사

* ```-P``` : SSH 포트 지정

* ```-i``` : SSH 설정을 활용해 실행

#### **remote to local**

* ```scp user@ip:remote_directory local_path```

#### **remote to remote**

* ```scp user@ip:remote_directory user2@ip2:target_remote_directory```

### nohup

* 터미널 종료 후에도 계속 작업이 유지하도록 실행한다(백그라운드 실행)

* ```nohup python3 app.py &```

* ```nohup```으로 실행될 파일은 permission이 755여야 함.
  * ```chmod 755 {실행파일}```

#### **nohup으로 실행된 파일 종료**

* ``` ps ef | grep app.py ``` : ```app.py```의 pid(Process ID) 찾고 ```kill -9 {pid}```로 프로세스를 kill 하면 된다.

* Log는 nohup.out에 저장 된다. 

### chmod

* Change Mod의 약자. 파일의 권한을 변경하는 경우 사용한다. 유닉스에서 파일이나 디엑토리의 시스템 모드를 변경한다. 

* ```ls -al```로 확인

<img src="../post_images/Basic Linux2/chmod.PNG" alt="chmod" style="zoom:100%;" class="center-image"/>

#### Permission

* ```r``` : Read, 4
* ```w``` : write, 2
* ```x``` : execute, 1
* ```-``` : Denied

## 참고

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://www.youtube.com/watch?v=EL6AQl-e3AQ](https://www.youtube.com/watch?v=EL6AQl-e3AQ)
3. [위키피디아-표준 스트림](https://ko.wikipedia.org/wiki/%ED%91%9C%EC%A4%80_%EC%8A%A4%ED%8A%B8%EB%A6%BC)
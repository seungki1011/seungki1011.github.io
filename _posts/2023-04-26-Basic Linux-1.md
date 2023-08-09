---
layout: post
title:  "Linux Basic - 1"
author: seungki
categories: [ Linux ]
image: post_images/linuxlogo.png
toc: True

---

<br>

## 리눅스 개요

### What is Linux?

리눅스는 오픈소스 운영체제(OS, Operating System)이다. 리눅스 세계 최대의 오픈소스 프로젝트이며, 누구든지 자유롭게 운영체제 프로그램의 소스를 변경하여 재배포 시킬 수 있는 프리웨어다.

<br>

### 리눅스를 배워야하는 이유

CLI를 통한 개발은 필수적이다. Shell script의 작성부터 서버 개발까지, 리눅스는 어떻게 보면 개발자를 위한 필수 교양이기 때문에 학습하는 것을 강력하게 권장한다.

<br>

### 다양한 리눅스 배포판

<img src="../post_images/2023-04-26-Basic Linux-1/linux_dist.PNG" alt="linux_dist" style="zoom:67%;" />

<p align="center">출처 : https://en.wikipedia.org/wiki/List_of_Linux_distributions</p>



* Debian
* Ubuntu
* Redhat
* Centos

이 외에도 정말 다양한 리눅스 배포판이 존재한다. 목적에 맞게 골라서 사용하면 된다.

<br>

## Introduction to Shell

### 쉘의 종류

쉘은 커널(kernel)과 사용자간의 다리역할을 해서, 사용자로부터 명령을 받아서 해석하고 프로그램을 실행해준다.(여기서 커널은 운영체제의 메모리에 항상 올라가 있는 부분으로, 하드웨어와 소프트웨어 사이의 인터페이스를 제공해주는 역할을 해준다고 보면 된다) 조금 더 간단하게 말하면, 사용자가 문자를 입력해 컴퓨터에 명령할 수 있도록 하는 프로그램이다.

* sh : 최초의 쉘
* bash : 리눅스 표준 쉘
* zsh : Mac OS 기본 쉘

이것 외에도 다양한 쉘이 존재한다.

<br>

### 쉘을 사용하는 상황

- 서버에 접속해서 사용하는 경우
- crontab 등 리눅스의 내장 기능을 활용하는 경우
- Docker를 사용하는 경우
- 서버를 관리할 경우
- Test code의 실행이나 배포 파이프라인(github action)의 실행

이것 외에도 정말 많은 이유로 쉘을 사용하는 상황이 온다.

```bash
kimseungki@DESKTOP-1P30XXX:~
```

* username : 사용자 이름 (kimseungki)
* hostname : 컴퓨터 네트워크에 접속된 장치에 할당된 이름. IP 대신 기억하기 쉬운 이름으로 저장하는 경우가 많음 (DESKTOP-1P30XXX)

<br>

## Shell Command

### 기본적인 shell 명령어

#### man

* 쉘 커맨드의 매뉴얼 문서를 보고 싶은 경우 사용. 

```man python```

* 종료는 ```q``` 입력.

<br>

#### mkdir

* Make Directory의 약자. 폴더를 생성한다. 

```mkdir linux-test``` (linux-test라는 폴더를 현재의 경로에 생성)

<br>

#### ls

* List Segments의 약자. 현재 접근한 폴더의 구성요소 확인.

**옵션**

```-a``` : .으로 시작하는 파일, 폴더를 포함해 전체 파일 출력

```-l```  : 퍼미션, 소유자, 만든 날짜, 용량까지 출력

```-h```  : 용량을 사람이 읽기 쉽도록 표현

```ls -a``` 또는 ```ls -alh``` 처럼 사용

<br>

#### pwd

* Print Working Directory의 약자. 현재 폴더의 경로를 절대 경로로 보여줌.

```pwd```

<br>

#### cd

* Change Directory의 약자. 명시한 폴더의 경로로 이동한다.

```cd linux-test```

<br>

#### echo

* 파이썬의 print 처럼 터미널에 텍스트를 출력해준다.

```echo "hi"``` : 터미널에 hi 출력

```echo `쉘커맨드` ``` 입력시 쉘 커맨드의 결과를 출력

* ex. ```echo `pwd` ```

<br>

#### cp

* Copy의 약자. 파일 또는 폴더를 복사한다.

```cp vi-test.sh vi-test2.sh```

**옵션**

```-r``` : 디렉토리를 복사할 때 디렉토리 안에 파일이 있으면 재귀적으로 모두 복사

```-f``` : 복사할 때 강제로 실행

<br>

#### vi

* vim 편집기로 파일을 생성한다. INSERT 모드에서만 수정 할 수 있음.

```vi vi-test.sh``` 를 사용하면 vim 편집기로 vi-test.sh라는 파일을 생성함. ```i```를 눌러서 INSERT 모드로 변경해서 수정을 할 수 있음.

* 나가기 위해서는 ESC + ```wq``` 또는 ESC + ! 후에 wq 입력으로 저장하고 나갈 수 있다. 그냥 ```q```의 경우 저장하지 않고 나간다.

<img src="../post_images/2023-04-26-Basic Linux-1/vim insert mode-2.PNG" alt="vim insert mode-2" style="zoom:150%;" class="center-image"/>

<p align="center">vim editor mode</p>



##### vi 편집기 mode

1. Command mode

   * vi 실행시 기본 모드
   * 방향키를 통해 커서 이동 가능
   * ``dd`` : 현재 위치한 한 줄 삭제
   * ```i``` : INSERT 모드로 변경
   * ```x``` : 커서가 위치한 곳의 글자 1개 삭제
   * ```p``` : 현재 커서가 있는 줄 바로 아래에 붙여넣기
   * ```k``` : 커서 위로 / ```j``` : 커서 아래로 / ```l``` : 커서 오른쪽으로 / ```h``` : 커서 왼쪽으로

   

2. Last Line mode
   * ESC 누른 후 콜론(:)을 누르면 나오는 모드
   * ```w``` : 현재 파일명으로 저장
   * ```q``` : vi 종료(저장되지 않음)
   * ```q!``` : vi 강제 종료
   * ```wq``` : 저장 후 종료
   * ```set nu``` : 라인 번호 출력

<br>

#### bash

* bash로 쉘 스크립트 실행

```bash vi-test.sh``` 로 ```vi-test.sh``` 라는 쉘 스크립트 파일을 실행

<img src="../post_images/2023-04-26-Basic Linux-1/shell script bash.PNG" alt="shell script bash" style="zoom: 150%;" class="center-image" />

<p align="center">vi-test.sh</p>

<br>

#### sudo

* 관리자 권한으로 실행하고 싶은 경우 앞에 ```sudo```를 붙임. 한 마디로 최고 권한을 가진 슈퍼 유저로 프로그램을 실행하겠다는 뜻이다. ```sudo```의 사용에는 신중을 가하고 사용하는 것을 권장한다.

<br>

#### mv

* Move의 약자. 파일 또는 폴더를 이동하기 위해 사용한다. 이름을 바꾸기 위해 사용 할 수 도 있다.

```mv vi-test.sh vi-test3.sh``` 를 사용하면 ```vi-test.sh```가 ```vi-test3.sh```로 이름이 변경된다.

<img src="../post_images/2023-04-26-Basic Linux-1/mv command.PNG" alt="mv command" style="zoom: 150%;" class="center-image"/>

```mv {원본파일} {이동위치}``` 로 파일을 이동 시킬 수 있다.

<br>

#### cat

* Concatenate의 약자. 특정 파일 내용을 출력하기 위해 사용한다. 여러 파일을 인자로 주면 합쳐서(concat) 출력 해준다. Concat을 한 상태에서 파일에 저장(overwrite)또는 추가(append) 할 수 있다.

```cat vi-test3.sh```

* concat 해서 출력

```cat vi-test2.sh vi-test3.sh```

* 파일에 overwrite

```cat vi-test2.sh vi-test3.sh > new_test.sh```

* 파일에 append

```cat vi-test2.sh vi-test3.sh >> new_test.sh```

<br>

#### history

* 최근데 입력한 쉘 커맨드의 역사를 출력. History 결과에서 느낌표를 붙이고 숫자 입력시 그 커맨드를 다시 활용 할 수 있음.



#### find

* 파일 및 디렉토리를 검색할 때 사용 할 수 있다.

```find . -name "File"``` : 현재 폴더에서 File이란 이름을 가지는 파일 및 디렉토리 검색

```find . -type file -name "*.txt"``` : 현재 경로에서 하위 디렉토리까지 .txt라는 확장자를 가진 모든 파일 검색

<br>

#### alias

* 기본 명령어를 별칭으로 설정 할 수 있음.

```alias ll2='ls -l'``` : ```ll2``` 입력시 ```ls -l```이 동작 됨

```alias gp='git push'``` : ```gp``` 입력시 ```git push```가 동작 됨

<br>

#### tree

* 폴더의 하위 구조를 계층적으로 표현해줌. 프로젝트의 구조를 설명 할 때 유용하다.

```tree -L {level}``` 의 형태로 사용

```tree -L 1 ``` : 1 level 까지 보여주기

<br>

#### head, tail

* 파일의 앞 또는 뒤 n행을 출력함. 

```head -n 1 vi-test3.sh``` : ```vi-test3.sh```의 앞 1 행 출력

```cat``` 로 파일 전체를 보기에 너무 긴 경우 활용 할 수 있음.

<br>

#### sort

* 행 단위로 정렬 해줌.

```-r``` :  정렬을 내림차순으로 정렬(기본:오름차순)

```-n``` :  numeric sort

```cat fruits.txt | sort ``` : ```fruits.txt```를 ```cat```로 출력할때 오름차순 정렬을 해서 출력한다.

<br>

#### uniq

* 중복된 행이 연속으로 있는 경우 중복 제거한다. ```sort```와 함께 사용하면 효과적이다.

```-c``` : 중복된 행의 개수 출력

```cat fruits.txt | sort | uniq``` 

<br>

#### grep

* 파일에 주어진 패턴 목록과 매칭되는 라인을 검색 해줌. ```grep```은 뒤에서 나올 ```pipe```와 같이 사용하곤 한다.

```grep {option} {filename}```

**옵션**

```-i``` : 대소문자 구분 없이 찾기

```-w``` : 정확히 그 단어만 찾기

```-v``` : 특정 패턴 제외한 결과 출력

```-E``` : 정규 표현식 사용

<img src="../post_images/2023-04-26-Basic Linux-1/grep1.PNG" alt="grep1" style="zoom: 150%;" class="center-image"/>

<br>

#### cut

파일에서 특정 필드를 추출한다.

```-f``` : 잘라낼 필드 지정

```-d ``` : 필드를 구분하는 구분자



<br>

**참고**

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://www.youtube.com/watch?v=EL6AQl-e3AQ](https://www.youtube.com/watch?v=EL6AQl-e3AQ)
3. [FabioLolix/LinuxTimeline: Linux Distributions Timeline](https://github.com/FabioLolix/LinuxTimeline)

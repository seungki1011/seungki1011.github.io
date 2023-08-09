---
layout: post
title:  "Version Control"
author: seungki
categories: [ Software Engineering ]
image: post_images/versioncontrol.jpeg
toc: True

---

<br>

## Python Versioning

### Python is Semantic Versioning

1. **파이썬 3.11.x 버전은 아래 마이너 버전(3.10.x, 3.9.x ..)에 호환**

   * 3.8.x에서 생성한 코드가 있다면 그대로 3.11.x에 실행해도 문제가 없음
   * 하지만 패키지가 3.11.x를 지원하지 않는 문제가 있을 수도 있음

   

2. **파이썬 3.x 버전은 아래 메이저 버전 2.x에 호환 안됨**

   * 2.x의 코드는 3.x의 버전에서 실행 되지 않음

<br>

### 프로젝트의 파이썬 버전 표시

파이썬 버전은 보통 프로젝트의 github readme에 작성

1. python **3.8** **이상**에서 실행 가능

   * python>=3.8, python 3.8+, python 3.8^

   

2. python **3.8** **만** 실행 가능

   * python == 3.8

   

3. python **3.10 이상**, **3.11 미만**에서 실행 가능

   * python=">=3.10, <3.11"

<br>

### 파이썬 설치 방법

파이썬의 설치 방법에는 여러 종류가 있고, 각각의 장단점이 있다.



1. **파이썬 공식 홈페이지에서 파일을 다운받아 설치**
   * 홈페이지의 바이너리 파일을 다운받아서 설치한다. 이렇게 설치는 케이스가 제일 적다.

2. **Conda를 이용하여 설치**

   * 만약 python 3.11을 설치한다면 ```conda install python=3.11.0``` 으로 설치한다. Python의 버전 관리를 conda에 맡김.

   * 장점 : conda 사용 중이라면, 별다른 도구 없이 바로 설치 가능

   * 단점 : conda가 무겁기 때문에 production 환경에선 잘 사용되지 않음


   * 사용하는 경우 : conda 중심의 셋팅이 이미 되어 있는 경우


3. **Docker로 파이썬 3.11.0 이미지 설치**

   * ```docker pull python:3.11.0```으로 파이썬 버전 관리를 컨테이너 이미지로 진행한다. 파이썬을 사용하고 싶으면 ```docker run -it python python```으로 Docker 컨테이너 실행과 접속을 한다.

   * 장점 : 로컬환경에 바이너리를 설치하지 않기 때문에 파이썬 설치 및 삭제가 쉬움

   * 단점 : 파이썬을 이용하기 위해서는 컨데이너에 매번 접속해야 함


   * 사용하는 경우 : 로컬 환경과 파이썬 환경을 완전히 격리하고 싶은 경우


4. **패키지 매니저로 설치**

   * 패키지 관리자(brew, apt, winget)로 파이썬 설치

     * **Mac OS의 경우**
       * ```brew install python@3.11```

     * **Linux의 경우(Ubuntu)**
       * ```apt install python3.11```

     * **Window의 경우**
       * ```winget install Python3.11```

   * 장점 : 설치가 간단

   * 단점 : 패치 버전까지 포함하는 파이썬 특정 버전을 설치할 수 없음


   * 사용하는 경우 : CLI로 빠르고 간단하게 설치하고 싶은 경우


5. **pyenv로 설치하기**

   * pyenv는 파이썬의 여러 버전을 cli로 쉽게 설치할 수 있는 도구. ```pyenv install 3.11.0```을 사용해서 설치. 

   * 장점 : 파이썬의 여러 버전을 설치하고 다룰 수 있음

   * 단점 : pyenv를 먼저 설치해야 함


   * 사용하는 경우 : 여러 버전의 파이썬을 바꿔줘야 하는 경우


파이썬 설치 시 여러 방법을 사용하면 충돌이 날 가능성이 존재한다. 파이썬 설치 전 지금 사용하는 python이 어디서 설치된 것인지 확인하는 과정이 필요함. ```which python{version}``` 으로 확인 가능.

<br>

### Pyenv

#### MacOS, Linux

Mac

```shell
brew install pyenv
```

Linux

```bash
sudo apt-get install -y make build-essential libsqlite3-dev wget curl llvm libncurses5-dev libssl-dev zlib1g-dev libbz2-dev libreadline-dev libncursesw5-dev xz-utils tk-dev
```

```bash
curl https://pyenv.run | bash
```



Mac이나 linux는 본인이 사용하는 shell 설정 파일(~/.bashrt, ~/.zshrc) 끝에 환경 변수들을 추가해야 함

```bash
export PATH="~/.pyenv/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

shell을 확인하는 방법

```bash
echo $SHELL
```

환경 변수 추가 후 source "shell 설정 파일"로 shell 설정 업데이트

```bash
source ~/.bashrc
```

<br>

#### Windows

Powershell에서 다음 명령어 입력

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "install-pyenv-win.ps1"; ./install-pyenv-win.ps1
```

Powershell 재실행, 필요한 경우 환경 변수 추가

```pyenv shell 3.11.0``` 으로 현재 shell에 파이썬 버전 활성화

```pyenv global 3.11.0```으로 shell의 기본 파이썬 버전 설정

<br>

## 파이썬 프로젝트의 버전 관리

### 가상환경

하나의 로컬 환경에서 두개 이상의 프로젝트를 진행하면, 각각 사용하는 파이썬이나 패키지의 버전이 달라서 문제가 발생 할 수 있음. 이런 문제를 해결 하고자 가상 환경을 생성해 프로젝트 별로 각자의 환경을 갖게 함.

<br>

### 가상환경을 만드는 방법

venv, conda, pyenv-virtualenv, pipenv 등 다양한 방법이 있음. 그 중 venv가 파이썬 가상 환경 구축에 많이 사용 됨.

<br>

#### venv

```python
python -m venv "가상 환경 폴더를 만들 경로"
```

* 보통 프로젝트 최상위 경로에서 .venv로 만드는 것이 관습
* venv는 파이썬 내장 모듈
* 가상 환경 접속 : ```source {가상환경폴더}/bin/activate```
* 접속하면 shell 왼쪽에 .venv 같은 가상환경 접속이 표시됨

<br>

##### windows venv activation

``` 
path\to\venv\Scripts\activate.bat
```

또는 

```
path\to\venv\Scripts\Activate.ps1
```

<br>

### 패키지 매니저

패키지 매니저는 패키지를 설치하고 버전을 관리해준다. 파이썬의 패키지 매니저에는 pip, poetry, conda 등이 존재한다. (conda는 anaconda 자체의 패키지 매니저로 보는 것이 맞다)

<br>

#### pip

pip는 항상 최신 버전의 pip를 사용하는 것이 좋음

<br>

**패키지 설치**

```pip install {package name}[==version]```

ex. ```pip install pandas==2.0.0```

**패키지 목록 확인**

```pip list```

```pip list --not-required --format=freeze``` (의존성 패키지 제외)

**설치한 패키지 목록을 저장**

```freeze > requirements.txt```

**저장한 패키지 목록을 다른 환경에서 설치**

```pip install -r requirements.txt```

<br>

##### pip의 단점

1. 개발 환경과 배포 환경의 패키지가 분리되지 않음

   * black이라는 파이썬 코드 formatter 패키지가 있는데, black은 개발 환경에서만 사용될 뿐, 실제 배포 환경에서는 사용하지 않음
   * pip를 사용할 경우 requirements.txt에 black이 포함되고 실제 배포할 때 설치되어 용량을 더 사용하게 됨

   

2. pip list로 패키지간 의존성을 알 수 없음

   * pip install로 설치한 패키지는 black 하나 뿐인데 pip list에는 이 외의 패키지들도 등장한다. 이 패키지들은 black이 의존하는 패키지들인데, 이런 의존성에 대한 정보가 없음

   

3. pip uninstall 시 의존성이 있던 패키지들은 삭제되지 않음

   * black을 삭제해도 black과 함께 설치된 패키지들은 삭제되지 않음



요약하자면 pip로는 정교한 패키지 관리가 불가능하기 때문에 협업을 하는 경우 곤란한 상황이 올 수도 있다.

<br>

#### Poetry

pip의 문제를 해결하기 위해 poetry라는 대체재가 등장했다.

Poetry 설치는 [공식문서](https://python-poetry.org/docs/) 참조

<br>

##### poetry 사용

* 프로젝트의 경로에서 ```poetry init``` 으로 파이썬 프로젝트 초기화. 기본적인 설정을 하고나면 프로젝트 경로에 ```pyproject.toml``` 이라는 파일이 생성된다. ```pyproject.toml```는 파이썬 프로젝트에 대한 메타 정보를 담고 있는 파일임.

* 패키지의 설치는 ```poetry add``` 명령어로 설치한다. ```-D``` 옵션을 붙일 경우 개발 환경에서만 사용할 패키지를 설치 할 수 있음. 

ex. ```add black -D```

* ```pyproject.toml``` 에서 dev 환경과 build 환경을 나눠서 관리 할 수 있기 때문에 정교한 패키지 관리가 가능함.

<br>

## 참고

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://peps.python.org/pep-0440/](https://peps.python.org/pep-0440/)


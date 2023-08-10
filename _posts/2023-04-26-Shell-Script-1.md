---
layout: post
title:  "Shell Script Basic - 1"
author: seungki
categories: [ Linux ]
image: post_images/linuxlogo.png
toc: True


---

---
## Shell Script
* 쉘 스크립트는 쉘에서 사용 할 수 있는 명어들의 조합을 모아서 만든 파일이라고 보면 편하다. 기본적으로 쉘을 이용해서 명령어들을 순차적으로 읽으면서 실행시켜준다. 

* .sh 파일을 생성해서 그 안에 쉘 커맨드를 추가 할 수 있다. If, while, case 문이 존재하며 작성후 ```bash {name.sh}``` 로 실행이 가능하다.

---

## 쉘 스크립트의 사용

* ```#!/bin/bash``` : 이 스크립트를 Bash 쉘로 해석 하겠다는 선언문 같은 것

* ```$(date +%s) ``` : date를 %s (unix timestamp)로 변형

* ```START=$(date +%s)``` : START라는 변수에 저장

---

* 쉘 스크립트를 통해 편리하게 자동화를 구축할 수 있다. 많이 연습해두자.

* 쉘 스크립트를 통해 구현 할 수 있는 기능 예시 : [https://www.geeksforgeeks.org/introduction-linux-shell-shell-scripting/](https://www.geeksforgeeks.org/introduction-linux-shell-shell-scripting/ )

* 위 링크에서 쉘 스크립팅에 대한 더 자세한 내용을 볼 수 있다.

<br>

## 참고

---

1. Naver Connection Boostcamp AI Tech 5th - Product Serving(변성윤)
2. [https://www.youtube.com/watch?v=cXnVygkAg4I](https://www.youtube.com/watch?v=cXnVygkAg4I)
3. [https://www.geeksforgeeks.org/introduction-linux-shell-shell-scripting/](https://www.geeksforgeeks.org/introduction-linux-shell-shell-scripting/)
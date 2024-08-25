개발 블로그 by [seungki1011](https://github.com/seungki1011)

## 수정 사항
* 프로젝트 탭 추가
  * [projects.html](): 기존 categories를 이용한 프로젝트 페이지. 메인 카테고리가 "Project"인 모든 포스트를 서브 카테고리 별로 분류한다.
  * [projects2.html](): 메인 카테고리가 "Project"인 모든 포스트를 카드를 사용해서 서브 카테고리로 분류한다. 해당 서브 카테고리를 누르면, 서브 카테고리의 포스트 목록으로 이동한다. 
  * [projects3.html](): projects2.html과 같지만, 해당 서브 카테고리 또는 카드를 누르면 바로 포스트로 이동한다.

## 적용 방법 
* [_tabs/projects.md]()의 layout에 사용하고 싶은 레이아웃을 명시한다

## front matter(메타데이터)
예시
```html
---
title: 테스트 프로젝트 1
description: 프로젝트 UI 테스트를 위한 프로젝트
author: 김아무개
date: 2020-05-05 10:30:00 +0900
categories: [Project, Test-Project] <!--메인 카테고리 Projects는 필수!-->
tags: [project, ai, machine learning]
pin: true
math: true
mermaid: true
project_overview: "이 프로젝트는 ABC라는 주제로 개발되었습니다." <!--프로젝트 소개-->
project_start_date: "2023/05/01" <!--시작 날짜-->
project_end_date: "2023/08/05" <!--종료 날짜-->
project_topic: "AI, 머신 러닝" <!--주제-->
project_tech_stack: "Python, TensorFlow, Keras, Airflow" <!--기술 스택-->
project_team_size: 5 <!--인원-->
project_github: "https://github.com/seungki1011/seungki1011.github.io" <!--깃헙-->
project_organization: "(Optional)" <!--주관 단체(미입력시 표시안됨)-->
---
```

<br>

This blog uses [Chirpy Jekyll Theme](https://github.com/cotes2020/jekyll-theme-chirpy)
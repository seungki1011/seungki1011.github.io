---
title: OCR Data-Centric 대회
description: 모델을 고정한 상태로 데이터만을 활용하여 OCR model의 성능을 최대한 끌어 올리는 프로젝트
author: seungki1011
date: 2023-06-03 10:30:00 +0900
categories: [Project, OCR Data-Centric 대회]
tags: [project, cv, ai, data-centric, labeling]
pin: false
math: true
mermaid: true
project_overview: "모델을 고정한 상태로 데이터만을 활용하여 OCR model의 성능을 최대한 끌어 올리는 프로젝트입니다.(Naver Boostcamp AITech 5기에서 주관한 경진대회입니다.)"
project_start_date: "2023/05/22"
project_end_date: "2023/06/01"
project_topic: "컴퓨터 비전, AI, Data-Centric, 데이터 전처리, 라벨링"
project_tech_stack: "Python, PyTorch, East Text Detector, CVAT"
project_team_size: 5
project_github: "https://github.com/boostcampaitech5/level2_cv_datacentric-cv-03"
project_organization: "Naver Boostcamp AITech 5기"
---

---

> **주관 단체**
>
> `Naver Boostcamp AITech 5기 CV 트랙`내에서 진행된 AI 모델 경진대회입니다.
{: .prompt-info }

---

---

## 1. 개요

> **참고**
>
> * **프로젝트 깃헙(레포지토리 내용은 동일합니다)**
>   * [개인 레포지토리](https://github.com/seungki1011/AI-Tech5-Data-Centric-Competetion)
>   * [팀 레포지토리](https://github.com/boostcampaitech5/level2_cv_datacentric-cv-03)
> * [팀 리포트](https://github.com/seungki1011/AI-Tech5-Data-Centric-Competetion/blob/master/etc/wrap_up_report.pdf)
> * [최종 발표 자료](https://github.com/seungki1011/AI-Tech5-Data-Centric-Competetion/blob/master/etc/presentation.pdf)
{: .prompt-info }

<br>

![ocr](../post_images/Untitled/ocr.png)_OCR_

**OCR(Optimal Character Recognition) 기술은 사람이 직접 쓰거나 이미지 속에 있는 문자를 얻은 다음 이를 컴퓨터가 인식할 수 있도록 하는 기술**입니다. 스마트폰으로 카드를 결제하거나, 카메라로 카드를 인식할 경우 자동으로 카드 번호가 입력되거나 주차장에 들어가면 차량 번호가 자동으로 인식되는 등 일상생활에 이미 보편적으로 사용되고 있습니다. 

이번 대회는 OCR의 대표적인 모델 중 하나인 EAST(Efficient and Accurate Scene Text Detector) 모델을 활용하여 진료비 계산서 영수증안에 있는 글자를 인식하는 대회입니다.

이번 대회는 Data-Centric 대회로 다음과 같은 제약사항이 있습니다.

- 대회에서 주어지는 EAST 모델만을 사용해야 하며 모델과 관련된 코드를 바꿔서는 안됩니다.
- 이미지넷 기학습 가중치 외에는 사용이 불가합니다.

즉 이번 대회는 모델을 고정한 상태로 데이터만을 활용하여 OCR 모델의 성능을 최대한 끌어 올리는 프로젝트입니다.

최종 평가는 `F1-score`로 진행되었습니다.

<br>

---




























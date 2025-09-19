---
title: "You Only Look Once: Unified, Real-Time Object Detection"
tags:
  - CV
  - 논문리딩스터디
  - YBIGTA
draft: "true"
---
- 제목: You Only Look Once: Unified, Real-Time Object Detection
- 저자: Joseph Redmon, Santosh Divvala, Ross Girshick, Ali Farhadi
- 게재된 학회: CVPR 2016 (Conference on Computer Vision and Pattern Recognition)
- 발표 연도: 2016
- 논문 링크: https://arxiv.org/pdf/1506.02640
---
참고한 글들:
- https://bkshin.tistory.com/entry/%EB%85%BC%EB%AC%B8-%EB%A6%AC%EB%B7%B0-YOLOYou-Only-Look-Once
# Summary
YOLO는 컴퓨터 비전의 과제중 하나인 객체 탐지를 수행하는 모델이다.

**YOLO 이전의 객체 탐지:** 
이전 모델들은 슬라이딩 윈도우 방식으로 이미지 전체를 돌아다니면서 분류하거나(DPM), 분류 CNN모델을 활용하여 객체가 있을만한 후보영역을 몇천개 생성한후, 그 후보 영역 각각에 CNN을 수행하는 방식으로(R-CNN)으로 만들어져 있었다.

이전 모델의 방식들은 복잡한 파이프라인으로 이루어져서 속도 저하가 일어났고, 각각의 영역에 CNN을 적용하기 때문에 전체 이미지에 대한 컨텍스트도 부족했다.

**YOLO의 핵심 방법론:** 
YOLO는 객체 탐지를 하나의 회귀문제로 바라보았다. 후보영역 추출과 분류 없이, 이미지를 한번만 보고 객체의 위치와 종류를 예측하도록 설계했다.

YOLO는 하나의 회귀 문제로 바라본 모델 덕에 복잡한 파이프라인이 없을 수 있었고, 그로인해 속도가 훨씬 빠르게 되었다. 또한, 항상 이미지 전체를 보기 때문에 전체 이미지의 컨텍스트가 들어가 배경을 객체로 잘못 탐지하는 배경 오류도 줄어들 수 있게 되었다.

# Unified Detection
![[Screenshot from 2025-09-20 01-31-27.png]]

어떻게 YOLO는 하나의 뉴럴네트워크로 객체탐지를 해낼 수 있었을까?

YOLO는 일단 이미지를 $S \times S$ 그리드로 나눈다. 만일 어떤 객체의 중점이 특정 cell 안에 들어가 있다면, 그 cell은 **객체를 탐지할 책임**이 있다.

각각 셀은 $B$ 개의 bounding boxes와, 박스에 대한 confidence scores를 예측해야한다.
confidence 의 정의는 다음과 같다. ([[IoU]])
$$
Pr(Object) ∗ IOU_{pred}^{truth}
$$


# Architecture


# Experiments

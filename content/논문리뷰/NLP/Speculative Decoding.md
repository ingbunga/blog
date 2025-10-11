---
tags:
  - NLP
  - 1일1독스터디
  - YBIGTA
title: Fast Inference from Transformers via Speculative Decoding
draft: "true"
---
- **논문 제목:** Fast Inference from Transformers via Speculative Decoding (추측 디코딩을 통한 트랜스포머의 빠른 추론)
- **저자:** Yaniv Leviathan, Matan Kalman, Yossi Matias (Google Research)
- **게재된 학회:** Proceedings of the 40th International Conference on Machine Learning (ICML)
- **발표 연도:** 2023년
- **논문 링크:** https://arxiv.org/pdf/2211.17192
---
> *생성형 ai로 생성된 리뷰입니다*

Autoregressive Transformer 아키텍처에 기반한 거대 언어 모델(LLM)의 성공은 자연어 처리 분야에 패러다임 전환을 가져왔습니다. 그러나 이러한 모델의 막대한 파라미터 수는 추론(Inference) 과정, 특히 순차적 토큰 생성이 필수적인 자기회귀 디코딩에서 심각한 지연 시간(Latency) 문제를 야기합니다. 이로 인해 모델의 성능과 실제 서비스 응용성 사이에 괴리가 발생하는 것이 현실입니다.

ICML 2023에 발표된 Yaniv Leviathan 등의 논문, **"Fast Inference from Transformers via Speculative Decoding"**은 이 고질적인 문제에 대한 매우 정교하고 원칙적인 해결책을 제시합니다. 본고는 해당 논문이 제안하는 추측 디코딩의 방법론적 핵심을 분해하고, 그 이론적 기반과 실증적 성과를 심도 있게 분석하여 이 연구가 갖는 학술적 의의를 고찰하고자 합니다.

#### **1. 문제 정의: Autoregressive Decoding의 본질적 한계**

표준적인 Autoregressive 디코딩 과정은 이전 스텝까지 생성된 시퀀스 $x_{<t}$를 조건으로, 다음 토큰 $x_t$의 확률 분포 $P(x_t | x_{<t})$를 계산하는 과정을 반복합니다. 즉, $K$개의 토큰을 생성하기 위해서는 거대한 모델의 전체 Forward Pass가 $K$번 순차적으로 수행되어야 합니다. 이는 GPU와 같은 병렬 연산 장치의 리소스를 온전히 활용하지 못하게 만들며, 특히 메모리 대역폭(Memory Bandwidth)이 주된 병목으로 작용하는 환경에서 비효율을 극대화합니다.

기존의 가속화 연구들은 주로 지식 증류(Knowledge Distillation)나 모델 양자화(Quantization)와 같이, 모델의 출력 분포를 근사(approximating)하거나 변경하는 '손실(Lossy)' 접근법에 의존해왔습니다. 이는 원본 모델의 성능을 필연적으로 저하시키는 한계를 내포합니다.

Speculative Decoding은 이러한 트레이드오프를 거부하고, **"원본 모델의 출력 분포를 수학적으로 완벽하게 보존하면서(lossless)"** 어떻게 지연 시간을 단축할 것인가라는 질문에 집중합니다.

#### **2. 방법론의 핵심: Speculative Sampling과 Parallel Verification**

이 논문의 핵심은 두 가지 모델, 즉 우리가 최종 출력을 얻고자 하는 크고 정확한 **타겟 모델($M_p$)**과, 작고 빠른 **근사 모델($M_q$)**의 협업에 기반합니다.

전체 프로세스는 다음과 같이 구성됩니다.

1.  **초안 생성 (Drafting):** 현재까지의 prefix가 주어졌을 때, 작고 빠른 $M_q$를 자기회귀적으로 $\gamma$번 실행하여, 후보 토큰 시퀀스(draft) $x_1, ..., x_\gamma$를 생성합니다.
2.  **병렬 검증 (Parallel Verification):** 거대한 $M_p$ 모델의 단일 Forward Pass를 통해, $M_q$가 생성한 prefix+draft 시퀀스들에 대한 다음 토큰 확률 분포를 **한 번에** 계산합니다. 즉, $P(x|prefix), P(x|prefix, x_1), ..., P(x|prefix, x_1, ..., x_\gamma)$를 병렬적으로 얻어냅니다. 이는 기존 방식의 $\gamma+1$번의 순차적 호출을 단 한 번의 호출로 대체하는, 속도 향상의 핵심적인 부분입니다.
3.  **수용/기각 결정 (Acceptance/Rejection):** $i=1$부터 $\gamma$까지, $M_q$가 예측한 토큰 $x_i$를 수용할지 여부를 아래의 **Speculative Sampling** 규칙에 따라 결정합니다.
    *   $p_i$와 $q_i$를 각각 $M_p$와 $M_q$가 예측한 $x_i$의 확률이라고 할 때,
    *   만약 $p_i \geq q_i$이면, $x_i$를 수용합니다.
    *   만약 $p_i < q_i$이면, 확률 $\frac{p_i}{q_i}$로 $x_i$를 수용하고, 확률 $1-\frac{p_i}{q_i}$로 기각합니다.
4.  **수정 및 샘플링 (Correction & Sampling):**
    *   만약 $i=n$에서 처음으로 토큰이 기각되면, $x_1, ..., x_{n-1}$까지의 초안은 최종 시퀀스에 추가됩니다. 이후, $M_p$가 $n-1$번째 토큰까지를 기반으로 예측한 확률 분포 $p_n(x)$와 $M_q$의 분포 $q_n(x)$의 차이를 보정한 새로운 분포 $p'(x) = \text{norm}(\max(0, p_n(x) - q_n(x)))$로부터 새로운 토큰 $x'_n$을 샘플링합니다.
    *   만약 모든 초안($\gamma$개)이 수용되면, $x_1, ..., x_\gamma$를 모두 채택하고, 마지막으로 $M_p$가 $\gamma$개의 토큰을 모두 고려하여 예측한 분포 $p_{\gamma+1}(x)$에서 다음 토큰을 샘플링합니다.

이 정교한 샘플링 절차를 통해, 최종적으로 생성되는 시퀀스의 확률 분포는 $M_p$를 단독으로 사용했을 때와 정확히 일치함이 수학적으로 보장됩니다. (Appendix A.1. 참조)

#### **3. 이론적 분석: 성능 향상과 비용의 정량화**

논문은 이 방법론의 효율성을 정량적으로 분석하기 위한 이론적 토대를 제공합니다.

*   **수용률 (Acceptance Rate, $\alpha$):** $M_q$의 제안이 $M_p$에 의해 수용될 확률의 기댓값으로, $M_q$가 $M_p$를 얼마나 잘 근사하는지를 나타내는 핵심 지표입니다. 이는 $\alpha = E[\sum_x \min(p(x), q(x))]$로 정의됩니다.
*   **예상 토큰 생성 수:** 한 번의 $M_p$ 호출 당 생성되는 토큰 수의 기댓값은 $\frac{1-\alpha^{\gamma+1}}{1-\alpha}$ 입니다. $\alpha$가 1에 가까울수록, 그리고 $\gamma$가 클수록 이 값은 커집니다.
*   **실행 시간 향상 (Walltime Improvement):** $M_q$ 실행 비용($c$, $M_p$ 대비 상대적 시간)을 고려한 실제 시간 향상률은 $\frac{1-\alpha^{\gamma+1}}{(1-\alpha)(c\gamma+1)}$로 모델링됩니다. 이는 $\alpha$는 높게, $c$는 낮게 유지하는 것이 최적임을 시사합니다. 실험적으로 $M_q$가 $M_p$보다 약 2-order of magnitude 작은 경우에 $c$와 $\alpha$ 사이의 균형이 가장 좋았다고 보고합니다.
*   **산술 연산량과의 트레이드오프:** Speculative Decoding은 지연 시간을 줄이는 대신, 기각된 토큰에 대한 계산이 낭비되므로 총 산술 연산량(FLOPs)은 증가합니다. 이는 'free lunch'가 아니라, 유휴(idle) 상태의 병렬 컴퓨팅 자원을 활용하여 지연 시간 병목을 해결하는 전략임을 명확히 합니다.

#### **4. 실증적 검증: 이론의 현실화**

저자들은 T5-XXL (11B)을 $M_p$로, T5-Small (77M), T5-Base 등을 $M_q$로 사용하여 WMT 영-독 번역 및 CNN/DM 요약 태스크에서 실험을 수행했습니다.

*   **주요 결과:** 표준 T5X 구현 대비, argmax 샘플링(temp=0)에서 최대 **3.4x**, 일반 샘플링(temp=1)에서 최대 **2.6x**의 실제 실행 시간(wall-time) 가속을 달성했습니다.
*   **흥미로운 발견:** 심지어 n-gram과 같은 매우 단순한 'negligible-cost' 모델을 $M_q$로 사용했을 때도, $\alpha$값이 0.2 수준으로 측정되어 1.25x의 의미 있는 속도 향상을 보였습니다. 이는 Speculative Decoding의 범용성과 강력함을 보여주는 대목입니다.

#### **5. 결론 및 학술적 의의**

"Fast Inference from Transformers via Speculative Decoding"은 LLM 추론 가속화 분야에 다음과 같은 중요한 기여를 했습니다.

1.  **무손실 가속의 실현:** 성능 저하를 감수하던 기존 패러다임에서 벗어나, 출력 분포의 완전한 보존을 수학적으로 증명하며 가속을 달성한 최초의 실용적 방법론 중 하나입니다.
2.  **모델 무관성 및 실용성 (Model-Agnostic & Practical):** 특정 아키텍처에 종속되지 않으며, 사전 학습된(off-the-shelf) 모델들을 재학습 없이 즉시 활용할 수 있어 산업적 적용 가능성이 매우 높습니다.
3.  **새로운 연구 방향 제시:** 이 연구는 추론 과정에서의 효율성을 최적화하기 위한 새로운 관점을 제시했습니다. 향후 빔 서치(beam search)로의 확장, 계층적(hierarchical) 추측 디코딩, $M_q$ 모델의 최적화 등 다양한 후속 연구의 기틀을 마련한 foundational work라고 평가할 수 있습니다.

결론적으로, 이 논문은 LLM의 느린 추론 속도라는 근본적인 한계를 이론적 우아함과 실용적 효율성을 겸비한 방식으로 돌파하며, 고성능 언어 모델의 대중적 확산에 있어 중요한 기술적 진보를 이룩했다고 할 수 있습니다.

#### 6. 개인적 소감

![[Screenshot 2025-10-11 at 4.32.04 AM.png]]

간단하게 논문에 대한 아이디어를 들었을때, "작은 모델에서 가져오는데 큰 모델보다 성능이 안좋지 않을까?" 하고 생각했는데, 수학적으로 같은 분포에서 나온다는걸 증명해서 대단했다.

여러개를 마구마구 깊게 만들고 그중에 좋은곳 까지만 가져간다는게 재밌다. 살짝 그리디하게 트리서치 하고 백트래킹 하는 느낌.

작은모델을 두개 돌려서 더 나은 결과를 뽑는다던가, 중간에 중간 모델을 넣어서 큰 모델과의 간격을 줄이거나 하면 어떨까?

Hugging Face Transformers, NVIDIA TensorRT-LLM 같은 라이브러리들에서 기본으로 지원해준다고 한다. 이제 Speculative Decoding은 추론 속도를 높이는 표준적인 방법이 된듯?
---
tags:
  - 정보이론
---
두 분포가 얼마나 비슷한지 나타내는 KL 다이버전스는 다음과 같다.
$$
D(p||q) = \mathbb{E}_{p(X)}\left[\log \frac{p(X)}{q(X)}\right] = \sum_xp(x)(\log p(x) - \log q(x)) = -\sum_x p(x)\log \frac{1}{p(x)} -\sum_xp(x)\log q(x)
$$
여기서
$$
\text{CrossEntropy: } H(p, q) = -\sum_x p(x)\log q(x)
$$
$$
\text{H(p)} = \sum_x p(x)\log \frac{1}{p(x)}
$$
그러므로
$$
D(p||q) = H(p, q) - H(p)
$$
인데, KL다이버전스는 0과 가까울수록 두개의 분포가 비슷하다. 우리가 원하고자 하는건 모델이 내는 분포와 정답 분포를 비슷하게 하고자 하는것이므로 이를 이용해보자.

만일 우리가 p를 정답 레이블로 한다면, 우리는 모델이 낸 가중치에 대해서만 역전파 하면 되므로 $H(p,q)$를 최소화 하는것과 동일하다.
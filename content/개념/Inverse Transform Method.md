어떻게 $Unif(0, 1)$ 값을 생성하는 함수를 가지고 있을때, 특정 분포를 따르는 함수를 만들게 할 수 있을까?

# 정리
$U \sim Unif(0, 1)$을 따를때, $X \sim F^{-1}(U)$ 라고 하면, $X \sim F$ 이다.
# 증명
nondecreasing $h : X \rightarrow Y$ 에 대해 역함수를 일반화 하면 infimum을 사용해서 다음과 같이 정의할 수 있다.
$$
F^{-1}(y) = inf \{x \in X : F(x) \ge y\}
,\space y \in Y
$$
그러면 연속분포와 이산분포 모두에서 다음과 같이 증명할 수 있다.
$$
Pr\{X\le x\} = Pr\{F^{-1}(U) \le x\} = Pr\{U \le F(x)\} = F(x)
$$
# 코드
```r
hist(qnorm(runif(10000)))
```
![[Pasted image 20250918031638.png]]
# Quartz v4

> “[One] who works with the door open gets all kinds of interruptions, but [they] also occasionally gets clues as to what the world is and what might be important.” — Richard Hamming

Quartz is a set of tools that helps you publish your [digital garden](https://jzhao.xyz/posts/networked-thought) and notes as a website for free.
Quartz v4 features a from-the-ground rewrite focusing on end-user extensibility and ease-of-use.

🔗 Read the documentation and get started: https://quartz.jzhao.xyz/

[Join the Discord Community](https://discord.gg/cRFFHYye7t)

## Sponsors

<p align="center">
  <a href="https://github.com/sponsors/jackyzha0">
    <img src="https://cdn.jsdelivr.net/gh/jackyzha0/jackyzha0/sponsorkit/sponsors.svg" />
  </a>
</p>

네 가지 성질을 만족함을 보이면 된다.

## $||v|| \ge 0$
정의에 따라 자명하다.

## $||v|| = 0$ 라면 $v = 0$
$||v|| = 0$ 일 때 $v \neq 0$ 인 v가 존재한다고 가정하자.(귀류법) Innter product의 성질에 따라 $\langle v, v\rangle > 0$이다. 그런데 $\langle v, v\rangle = ||v||$이므로 모순이다. 따라서 $||v|| = 0$ 라면 $v = 0$.

## $||ax||=|a| \space||x||$
$$
||ax||=\sqrt{\langle ax,ax \rangle}=\sqrt{|a|^2\langle x, x\rangle} = |a|\sqrt{\langle x, x\rangle}=|a| \space ||x||
$$

## $||x + y||\le||x||+||y||$
$$\sqrt{\langle x + y,x+y\rangle}\le\sqrt{\langle x,x\rangle}+\sqrt{\langle y,y \rangle}$$
정의에 따라 위와 동치이다.
$$\langle x + y,x+y\rangle\le{\langle x,x\rangle}+{\langle y,y \rangle}+2\sqrt{\langle y,y \rangle\langle x,x \rangle}$$
양 변이 음수가 아니므로 양 변을 제곱한 것과 동치이다.
$$\langle x,x\rangle+\langle y,y\rangle+\langle x,y\rangle+\langle y,x\rangle\le{\langle x,x\rangle}+{\langle y,y \rangle}+2\sqrt{\langle y,y \rangle\langle x,x \rangle}$$
선형성을 이용해 풀 수 있다.
$$2\text{Re}\langle x,y\rangle= \langle x,y\rangle+\langle y,x\rangle\le2\sqrt{\langle y,y \rangle\langle x,x \rangle}$$
그런데
$$
\text{Re}\langle x,y\rangle \le|\langle x,y\rangle|
$$
이고, Cauchy-schwarz Inequality에 따르면
$$
|\langle x,y\rangle| \le \sqrt{\langle y,y \rangle\langle x,x \rangle}
$$
이므로,
$$2\text{Re}\langle x,y\rangle\le2\sqrt{\langle y,y \rangle\langle x,x \rangle}$$
만족한다.
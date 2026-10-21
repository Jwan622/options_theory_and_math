# Black-Scholes-Merton (BSM) Primer

## Learning Goal

Get the math in Part I of Euan Sinclair's *Volatility Trading* (2nd ed., Wiley, 2013) to feel earned rather than magic. Chapter 1 there is **Option Pricing** (the BSM model). Chapter 2 is **Volatility Measurement**, which covers close-to-close, Parkinson, Garman-Klass and similar estimators. Sinclair writes for practitioners and moves fast. This primer fills in the steps he skips.

You need: derivatives (including partial derivatives), Taylor series, the normal distribution, and expected value. Everything else is built here.

How to read it:

```text
Part 0  Vocabulary              what an option is; the Greek letters
Part 1  Toolbox                 e^x, log returns, normal & lognormal, sqrt(time), Taylor
Part 2  Randomness in time      random walk -> Brownian motion -> GBM
Part 3  Ito's lemma             the one new calculus rule
Part 4  Replication             why the stock's expected return drops out (binomial)
Part 5  The BSM equation        delta hedging -> a PDE
Part 6  The BSM formula         solving it with an expectation, every step
Part 7  Worked numbers          price a real call and put
Part 8  The Greeks              where each one comes from
Part 9  Hedged P&L              C - Delta*S line by line; realized vs implied vol
Part 10 Measuring volatility    preview of Sinclair Ch. 2
Part 11 Where BSM breaks        why the rest of the book exists
```

Each step depends on the ones before it. If something feels unmotivated, go back one part.

---

# Part 0: Vocabulary

**Underlying**: the asset the option is written on. Here it's a stock with price $S$.

**Call option**: the right, but not the obligation, to **buy** the underlying at a fixed price.

**Put option**: the right, but not the obligation, to **sell** the underlying at a fixed price.

**Strike** $K$: that fixed price.

**Expiry** $T$: the date the right ends, measured in years from today. $T = 0.5$ means six months.

**European option**: can only be exercised *at* expiry. BSM prices European options. American options can be exercised any time, and that is a separate problem.

**Payoff**: what the option is worth at the instant of expiry, when $S_T$ is the stock price then.

- Call: if $S_T > K$, you exercise, buy at $K$, and hold something worth $S_T$. You gain $S_T - K$. If $S_T \le K$, you walk away with $0$. So

$$\text{call payoff} = \max(S_T - K,\ 0)$$

- Put: by the same reasoning,

$$\text{put payoff} = \max(K - S_T,\ 0)$$

**Premium**: what you pay *today* for the option. **The whole question of option pricing is: what should the premium be?**

**Volatility** $\sigma$: how much the stock's returns wiggle. Defined precisely in Part 1.

## 0.1 The Greek letters you'll see

Option math borrows Greek letters. Here they are, with how to say them and what each one means in this primer:

| Symbol | Name | Meaning here |
|---|---|---|
| $\Delta$ | capital delta | **delta**: how much the option's value changes per \$1 move in the stock. Also the number of shares you short to hedge. |
| $\Gamma$ | capital gamma (looks like an upside-down L) | **gamma**: how much delta changes per \$1 move in the stock. It measures the option's curvature. |
| $\Theta$ | capital theta | **theta**: how much the option's value changes as time passes, holding the stock fixed. |
| $\mathcal V$ or $\nu$ | vega (not really a Greek letter; $\nu$ is "nu") | **vega**: how much the option's value changes per change in volatility. |
| $\rho$ | rho | **rho**: sensitivity to the interest rate. |
| $\sigma$ | sigma | volatility. |
| $\mu$ | mu | the stock's real-world expected return. |
| $\Pi$ | capital pi | value of a **portfolio** (here, not 3.14159). |
| $\tau$ | tau | time remaining until expiry, $T - t$. |

**Warning: $\Delta$ does double duty.** In math generally, $\Delta$ means "change in", so $\Delta S$ means "the change in $S$" and $\Delta t$ means "a small step of time". In options, $\Delta$ alone means the Greek delta. Books, Sinclair's included, use both meanings, sometimes in the same line. A quick test: if $\Delta$ sits directly in front of a variable with no space or multiplication meant ($\Delta t$, $\Delta S$ written as a change), it means "change in". If it multiplies something ($\Delta \cdot S$, "$\Delta$ shares"), it's the hedge ratio. In this primer, $\Delta t$ always means a time step, and a price change is written out as $S_{t+1} - S_t$ or $\delta S$ to avoid the clash.

---

# Part 1: The Toolbox

## 1.1 Continuous compounding and discounting

**The problem.** A dollar today and a dollar in one year are not the same. To compare them we need an interest rate.

Bank pays 5% a year. Compound $n$ times a year and \$1 grows to

$$\left(1 + \frac{0.05}{n}\right)^n$$

| $n$ | value after 1 year |
|---|---|
| 1 (yearly) | 1.050000 |
| 12 (monthly) | 1.051162 |
| 365 (daily) | 1.051267 |
| $\infty$ | 1.051271 |

As $n \to \infty$, this converges to $e^{0.05}$. That is a standard calculus limit:

$$\lim_{n\to\infty}\left(1 + \frac{r}{n}\right)^n = e^r$$

So with **continuous compounding** at rate $r$, \$1 grows to $e^{rT}$ after $T$ years.

Run it backwards. If you will receive $X$ dollars at time $T$, what is that worth today? You need an amount $P$ such that $P \cdot e^{rT} = X$. Divide both sides by $e^{rT}$:

$$P = X e^{-rT}$$

This is **discounting**. The factor $e^{-rT}$ appears in every option formula, and it always means: "convert money at time $T$ into money today."

## 1.2 Simple returns vs log returns

Stock goes from $S_0 = 100$ to $S_1 = 110$.

- **Simple return**: $\dfrac{S_1 - S_0}{S_0} = \dfrac{110-100}{100} = 0.10$
- **Log return**: $\ln\!\left(\dfrac{S_1}{S_0}\right) = \ln(1.10) = 0.0953$

Why bother with logs? **Log returns add across time. Simple returns don't.**

Suppose the stock goes $100 \to 110 \to 99$.

Simple returns: $+10\%$, then $\frac{99-110}{110} = -10\%$. Adding them gives $0\%$, but the stock is down 1%. Adding is **wrong**.

Log returns:

$$\ln\frac{110}{100} + \ln\frac{99}{110}$$

Use the rule $\ln a + \ln b = \ln(ab)$:

$$= \ln\left(\frac{110}{100}\cdot\frac{99}{110}\right)$$

The 110s cancel:

$$= \ln\frac{99}{100} = -0.01005$$

which is exactly the log return from start to finish. Adding is **right**.

In general, for prices $S_0, S_1, \dots, S_n$:

$$\ln\frac{S_n}{S_0} = \ln\left(\frac{S_1}{S_0}\cdot\frac{S_2}{S_1}\cdots\frac{S_n}{S_{n-1}}\right) = \sum_{i=1}^{n} \ln\frac{S_i}{S_{i-1}}$$

This matters because statistics is good at **sums** of random things: the Central Limit Theorem is about sums. When daily log returns are sums, we can use all of it.

For small moves the two are close. Taylor-expand $\ln(1+x) = x - \frac{x^2}{2} + \dots$, so a 1% simple return is about a 0.995% log return. Sinclair, like almost all vol traders, works in log returns.

## 1.3 The normal distribution and $N(x)$

$Z \sim \mathcal{N}(0,1)$ means $Z$ is **standard normal**: mean 0, variance 1. Its density is

$$n(z) = \frac{1}{\sqrt{2\pi}}\, e^{-z^2/2}$$

We write $n(z)$ for the density (height of the bell curve), and

$$N(x) = P(Z \le x) = \int_{-\infty}^{x} n(z)\,dz$$

for the **cumulative distribution function (CDF)**: the area under the bell to the left of $x$.

Facts used later:

1. **Symmetry.** The bell is symmetric about 0, so the area right of $-x$ equals the area left of $x$:

$$P(Z > -x) = N(x)$$

2. **Scaling.** If $X = \mu + s Z$, then $X \sim \mathcal{N}(\mu, s^2)$: mean $\mu$, standard deviation $s$. Any normal is a shifted, stretched standard normal.

3. Some values: $N(0) = 0.5$, $N(0.15) = 0.5596$, $N(0.35) = 0.6368$, $N(1.645) = 0.95$.

## 1.4 The lognormal distribution and the "$+\tfrac{1}{2}\sigma^2$" term

If $X$ is normal, then $Y = e^X$ is **lognormal**: its log is normal. Stock prices in BSM are lognormal because

$$S_T = S_0 \cdot e^{(\text{log return})}$$

and the total log return is a sum of many small pieces, so it is (approximately) normal.

Lognormal prices are never negative ($e^{\text{anything}} > 0$), and they are skewed right: big up moves are possible, down moves are capped at $-100\%$.

**Key result.** If $X = a + bZ$ with $Z \sim \mathcal{N}(0,1)$, then

$$E\left[e^{a + bZ}\right] = e^{a + b^2/2}$$

Note that this is **not** $e^{a}$, even though $E[a + bZ] = a$. The convexity of $e^x$ adds a bonus of $b^2/2$. This shows up in BSM again and again, so let's derive it fully.

**Derivation.**

Step 1. Write the expectation as an integral against the normal density:

$$E\left[e^{a+bZ}\right] = \int_{-\infty}^{\infty} e^{a+bz}\cdot\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz$$

Step 2. $e^a$ doesn't depend on $z$, so pull it out. Combine the other two exponentials, since $e^{p}e^{q} = e^{p+q}$:

$$= e^{a}\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{z^2}{2} + bz}\,dz$$

Step 3. **Complete the square** in the exponent. We want to write $-\frac{z^2}{2} + bz$ as $-\frac{(z - \text{something})^2}{2} + \text{constant}$. Expand a guess:

$$-\frac{(z-b)^2}{2} = -\frac{z^2 - 2bz + b^2}{2} = -\frac{z^2}{2} + bz - \frac{b^2}{2}$$

That has the $-\frac{z^2}{2} + bz$ we want, plus an unwanted $-\frac{b^2}{2}$. Add $\frac{b^2}{2}$ back:

$$-\frac{z^2}{2} + bz = -\frac{(z-b)^2}{2} + \frac{b^2}{2}$$

Step 4. Substitute, and pull the constant $e^{b^2/2}$ out of the integral:

$$= e^{a}\,e^{b^2/2}\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{(z-b)^2}{2}}\,dz$$

Step 5. The integrand is the density of a normal with mean $b$ and variance 1. Any density integrates to 1. So the integral is 1:

$$E\left[e^{a+bZ}\right] = e^{a + b^2/2} \qquad \blacksquare$$

Remember this trick (complete the square, recognize a shifted density). Part 6 uses it twice.

## 1.5 Volatility and the square root of time

**Volatility** $\sigma$ is the standard deviation of log returns, quoted per year. "The stock has 20% vol" means: the one-year log return has standard deviation 0.20.

**Why vol scales with $\sqrt{T}$.** Let daily log returns $r_1, \dots, r_n$ be independent with the same variance $\sigma_d^2$. The $n$-day log return is their sum (Section 1.2). For **independent** variables, variances add, because the covariance terms are zero (see `../math/variance_covariance.md`):

$$\operatorname{Var}\left(\sum_{i=1}^n r_i\right) = \sum_{i=1}^n \operatorname{Var}(r_i) = n\,\sigma_d^2$$

Take the square root to get standard deviation:

$$\operatorname{SD}\left(\sum_{i=1}^n r_i\right) = \sqrt{n}\,\sigma_d$$

**Variance grows linearly in time. Volatility grows with the square root of time.**

With about 252 trading days a year:

$$\sigma_{\text{annual}} = \sigma_{\text{daily}}\sqrt{252}, \qquad \sigma_{\text{daily}} = \frac{\sigma_{\text{annual}}}{\sqrt{252}}$$

Since $\sqrt{252} \approx 15.87 \approx 16$, traders use the **rule of 16**: a 16% vol stock moves about 1% a day (one standard deviation). A 32% vol stock moves about 2% a day.

In general, over $T$ years the log return has standard deviation $\sigma\sqrt{T}$ and variance $\sigma^2 T$. **$\sigma\sqrt{T}$ will appear in every BSM formula.** It is "how much the stock can move between now and expiry."

## 1.6 Taylor expansions

**The problem.** An option's value $C(S)$ is a complicated function of the stock price. A trader wants a quick answer to: "if the stock moves a little, from $S$ to $S + h$, how much does the option change?" Recomputing the full formula hides the structure. A **Taylor expansion** answers it using only facts known *at the current price*: the value, the slope, and the curvature.

### The idea: approximate a curve with simpler shapes

Zoom in on any smooth curve near a point $x$. Each extra piece of information gives a better local copy:

```text
order 0:  a flat line      "the value doesn't change"         uses f(x)
order 1:  a tangent line   "it changes at the current slope"  uses f(x), f'(x)
order 2:  a parabola       "and the slope itself bends"       uses f(x), f'(x), f''(x)
```

**First order (the tangent line).** Slope means "rise per unit of run." Moving a distance $h$ at slope $f'(x)$ rises about $f'(x)\cdot h$:

$$f(x+h) \approx f(x) + f'(x)\,h$$

This misses curvature. If the curve bends upward, the tangent line undershoots.

**Second order (add curvature).** Add a term in $h^2$:

$$f(x+h) \approx f(x) + f'(x)\,h + \tfrac12 f''(x)\,h^2$$

**Where the $\tfrac12$ comes from.** Look for the parabola $p(h) = a + bh + ch^2$ that matches $f$'s value, slope and curvature at $h = 0$:

1. Match the value. $p(0) = a$, so $a = f(x)$.
2. Match the slope. Differentiate: $p'(h) = b + 2ch$, so $p'(0) = b$, so $b = f'(x)$.
3. Match the curvature. Differentiate again: $p''(h) = 2c$. Set $2c = f''(x)$, so $c = \tfrac12 f''(x)$.

The $\tfrac12$ is there because differentiating $h^2$ twice gives $2$, and we have to divide that 2 back out.

**The general pattern** continues with higher derivatives. The $n$th term is $\frac{f^{(n)}(x)}{n!}h^n$, where $n! = 1\cdot2\cdots n$ (the $\tfrac12$ above is $\tfrac{1}{2!}$):

$$f(x+h) = f(x) + f'(x)h + \frac{f''(x)}{2!}h^2 + \frac{f'''(x)}{3!}h^3 + \dots$$

"**Second-order Taylor expansion**" means: stop after the $h^2$ term. When $h$ is small, $h^3$ is much smaller than $h^2$ (if $h = 0.01$, then $h^2 = 0.0001$ and $h^3 = 0.000001$), so the dropped terms barely matter.

### Worked example: $\sqrt{104}$ without a calculator

$f(x) = \sqrt x$, known point $x = 100$, step $h = 4$.

Derivatives (power rule, $\sqrt x = x^{1/2}$):

$$f(x) = x^{1/2}, \qquad f'(x) = \tfrac12 x^{-1/2}, \qquad f''(x) = -\tfrac14 x^{-3/2}$$

At $x = 100$: $\sqrt{100} = 10$ and $100^{3/2} = 1000$, so

$$f(100) = 10, \qquad f'(100) = \tfrac{1}{2\cdot10} = 0.05, \qquad f''(100) = -\tfrac{1}{4\cdot1000} = -0.00025$$

| Order | Computation | Estimate |
|---|---|---|
| 0 | $10$ | 10.000 |
| 1 | $10 + 0.05\times4$ | 10.200 |
| 2 | $10.2 + \tfrac12(-0.00025)(4^2) = 10.2 - 0.002$ | 10.198 |
| exact | $\sqrt{104}$ | 10.19804 |

Each order gets closer. The second-order term is negative because $\sqrt x$ bends downward ($f'' < 0$).

### The same thing for an option: delta and gamma

Apply it to the call price as a function of the stock price, holding time fixed. The first derivative of $C$ with respect to $S$ is delta, and the second is gamma (Section 0.1):

$$C(S + h) \approx C(S) + \Delta\,h + \tfrac12\Gamma\,h^2$$

**That's all delta and gamma are: the first two Taylor coefficients of the option price.**

Numbers from the worked example in Part 7: $C = 10.4506$, $\Delta = 0.6368$, $\Gamma = 0.01876$ at $S = 100$.

| Stock moves to | 1st order: $C + \Delta h$ | 2nd order: add $\tfrac12\Gamma h^2$ | Exact BSM |
|---|---|---|---|
| 102 ($h = +2$) | $10.4506 + 1.2737 = 11.7243$ | $+\,0.0375 = 11.7618$ | 11.7611 |
| 98 ($h = -2$) | $10.4506 - 1.2737 = 9.1769$ | $+\,0.0375 = 9.2144$ | 9.2151 |

Look at the gamma term: **$+0.0375$ in both cases.** $h^2$ is positive whether the stock goes up or down. If you hedge away the $\Delta h$ part (Part 5 and Part 9), the gamma term is what's left, and a long option makes it on a move in *either* direction. That is the whole reason traders care about gamma.

### Two variables: price and time

An option depends on $S$ and $t$. The two-variable second-order expansion, for a stock move $h$ and a time step $k$, is

$$C(S+h,\ t+k) \approx C + \frac{\partial C}{\partial S}h + \frac{\partial C}{\partial t}k + \tfrac12\frac{\partial^2C}{\partial S^2}h^2 + \frac{\partial^2C}{\partial S\,\partial t}hk + \tfrac12\frac{\partial^2 C}{\partial t^2}k^2$$

In Greek letters, with the last two terms dropped:

$$C(S+h,\ t+k) \approx C + \Delta\,h + \Theta\,k + \tfrac12\Gamma\,h^2$$

**Why drop $hk$ and $k^2$ but keep $h^2$?** Size. Over one trading day, $k = 1/252 \approx 0.004$ years. A typical stock move is about $\sigma S\sqrt{k}$, so $h^2 \approx \sigma^2S^2k$, which is the **same size as $k$**. But $hk$ is about $k^{3/2}$ and $k^2$ is smaller still, so both shrink to nothing next to the terms we keep. Part 2.2 makes this precise as $(dW)^2 = dt$. Part 3 (Itô's lemma) is exactly this expansion.

---

# Part 2: Randomness Through Time

## 2.1 From a coin-flip walk to Brownian motion

**The problem.** We need a model where the stock price wiggles continuously, randomly, every instant.

Start discrete. Divide $[0, t]$ into $n$ small steps, each of length $\Delta t = t/n$. At each step, move by a random amount $\Delta W_i \sim \mathcal{N}(0, \Delta t)$, independently. Let $W_t$ be the sum:

$$W_t = \sum_{i=1}^{n}\Delta W_i$$

By Section 1.5's reasoning (variances add), $\operatorname{Var}(W_t) = n\cdot\Delta t = t$. Let $n \to \infty$ so the steps become infinitely fine. The limit is **Brownian motion** (also called a **Wiener process**) $W_t$, with these properties:

1. $W_0 = 0$.
2. $W_t \sim \mathcal{N}(0, t)$. Equivalently, $W_t = \sqrt{t}\,Z$.
3. Increments over non-overlapping intervals are independent. Past wiggles say nothing about future ones.
4. Paths are continuous but jagged everywhere: they have no slope anywhere.

We write $dW$ for the increment over an infinitesimal time $dt$. It has mean 0 and variance $dt$, so its size is roughly $\sqrt{dt}$.

**Why $\sqrt{dt}$ matters.** When $dt$ is tiny, $\sqrt{dt}$ is much **bigger** than $dt$. If $dt = 0.0001$, then $\sqrt{dt} = 0.01$, 100 times bigger. Over short horizons, randomness dominates drift. That is why a stock's daily moves look like pure noise even if it has a 10% expected annual return.

## 2.2 The surprising rule $(dW)^2 = dt$

In ordinary calculus, $(dx)^2$ is negligible next to $dx$. With Brownian motion, $(dW)^2$ is the same size as $dt$ and is **not** negligible. More strongly: it is not even random in the limit. Here's why.

Sum up the squared increments over $[0,t]$:

$$Q = \sum_{i=1}^{n}(\Delta W_i)^2$$

**Mean of $Q$.** Each $\Delta W_i$ has mean 0 and variance $\Delta t$. Since $\operatorname{Var}(X) = E[X^2] - (E[X])^2$, we get $E[X^2] = \operatorname{Var}(X) + (E[X])^2$. So:

$$E[(\Delta W_i)^2] = \Delta t + 0^2 = \Delta t$$

Sum $n$ of these:

$$E[Q] = n\,\Delta t = t$$

**Variance of $Q$.** Write $\Delta W_i = \sqrt{\Delta t}\,Z_i$ with $Z_i$ standard normal. Then $(\Delta W_i)^2 = \Delta t\,Z_i^2$. A known fact about the standard normal is $E[Z^4] = 3$. So:

$$\operatorname{Var}(Z_i^2) = E[Z_i^4] - (E[Z_i^2])^2 = 3 - 1 = 2$$

$$\operatorname{Var}\big((\Delta W_i)^2\big) = (\Delta t)^2\cdot 2$$

The $(\Delta W_i)^2$ are independent, so variances add:

$$\operatorname{Var}(Q) = n\cdot 2(\Delta t)^2 = 2\,(n\,\Delta t)\,\Delta t = 2t\,\Delta t$$

As $\Delta t \to 0$, $\operatorname{Var}(Q)\to 0$. A random variable with variance 0 is a constant: its mean, $t$.

So the sum of squared Brownian increments over $[0,t]$ is exactly $t$. In infinitesimal shorthand:

$$\boxed{(dW)^2 = dt}$$

Also, for the products we'll meet:

| product | size | in the limit |
|---|---|---|
| $(dt)^2$ | $dt^2$ | $0$ (much smaller than $dt$) |
| $dt\cdot dW$ | $dt^{3/2}$ | $0$ (much smaller than $dt$) |
| $(dW)^2$ | $dt$ | $dt$ (**survives**) |

This little table is the whole engine of stochastic calculus.

## 2.3 Geometric Brownian motion (GBM): the BSM stock model

BSM assumes the stock follows

$$dS = \mu S\,dt + \sigma S\,dW$$

Read it term by term:

- $dS$: change in stock price over the next instant.
- $\mu S\,dt$: **drift**. The stock's expected return is $\mu$ per year, so over $dt$ it expects to gain $\mu\,dt$ *as a fraction of its price*, which is $\mu S\,dt$ in dollars.
- $\sigma S\,dW$: **noise**. Random shock $dW$, scaled by volatility $\sigma$, and by $S$ so that the shock is a *percentage* of price.

Divide both sides by $S$ to see it in return terms:

$$\frac{dS}{S} = \mu\,dt + \sigma\,dW$$

"Instantaneous return = expected return × time + vol × random shock." It's called *geometric* because the randomness is proportional (multiplicative), not additive. A \$10 stock and a \$1000 stock both move about $\sigma$ percent, not the same number of dollars.

---

# Part 3: Itô's Lemma

## 3.1 The problem

An option's value $V$ depends on the stock price $S$ and time $t$: $V = V(S, t)$. We know how $S$ moves (GBM). How does $V$ move?

In ordinary calculus you'd use a Taylor expansion and keep first-order terms. With randomness, one second-order term survives because $(dW)^2 = dt$. **Itô's lemma** is Taylor's theorem with that correction.

## 3.2 Derivation

Taylor-expand $V(S + dS,\ t + dt)$ around $(S, t)$ up to second order (Section 1.6, with $h = dS$ and $k = dt$):

$$dV = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial S}dS + \frac{1}{2}\frac{\partial^2 V}{\partial S^2}(dS)^2 + \frac{\partial^2 V}{\partial S\,\partial t}dS\,dt + \frac{1}{2}\frac{\partial^2 V}{\partial t^2}(dt)^2 + \dots$$

Now find the size of each piece using the table in 2.2.

**Compute $(dS)^2$.** Substitute $dS = \mu S\,dt + \sigma S\,dW$ and expand $(a+b)^2 = a^2 + 2ab + b^2$:

$$(dS)^2 = \mu^2S^2(dt)^2 + 2\mu\sigma S^2\,dt\,dW + \sigma^2S^2(dW)^2$$

Apply the table: $(dt)^2 \to 0$, $dt\,dW \to 0$, $(dW)^2 \to dt$:

$$(dS)^2 = \sigma^2 S^2\,dt$$

**The other terms.** $dS\,dt$ contains $dt^2$ and $dt\,dW$, both $\to 0$. $(dt)^2 \to 0$. Higher terms are smaller still.

Keep what survives:

$$\boxed{dV = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial S}dS + \frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}dt}$$

That is **Itô's lemma** for a function of a GBM. Compared with ordinary calculus, the only new thing is the last term. It says: **curvature in $V$ plus randomness in $S$ produces a predictable drift in $V$.** That term will become the "gamma" profit in Part 9.

Why does curvature turn noise into drift? Take $V = S^2$. If $S$ jumps $+1$ or $-1$ with equal chance from $S=10$, $V$ goes to 121 or 81, averaging 101, not 100. The up and down moves cancel in $S$ but not in $V$, because $V$ curves. Same reason as the $+b^2/2$ in Section 1.4.

## 3.3 Application: solving GBM, and "volatility drag"

Apply Itô to $f(S) = \ln S$. Its derivatives:

$$\frac{\partial f}{\partial t} = 0, \qquad \frac{\partial f}{\partial S} = \frac{1}{S}, \qquad \frac{\partial^2 f}{\partial S^2} = -\frac{1}{S^2}$$

Plug into Itô:

$$d(\ln S) = 0 + \frac{1}{S}dS + \frac{1}{2}\sigma^2S^2\left(-\frac{1}{S^2}\right)dt$$

Simplify the last term ($S^2/S^2 = 1$):

$$d(\ln S) = \frac{dS}{S} - \frac{1}{2}\sigma^2\,dt$$

Substitute $\frac{dS}{S} = \mu\,dt + \sigma\,dW$:

$$d(\ln S) = \mu\,dt + \sigma\,dW - \frac{1}{2}\sigma^2\,dt = \left(\mu - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW$$

The right side has constant coefficients, so we can just add it up from 0 to $T$. The $dt$'s sum to $T$; the $dW$'s sum to $W_T$:

$$\ln S_T - \ln S_0 = \left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma W_T$$

Use $W_T = \sqrt{T}Z$, then exponentiate both sides:

$$\boxed{S_T = S_0\exp\!\left[\left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma\sqrt{T}\,Z\right]}$$

So the log return over $[0,T]$ is normal with mean $(\mu - \frac{1}{2}\sigma^2)T$ and standard deviation $\sigma\sqrt{T}$. The price is lognormal.

**Sanity check with Section 1.4.** $E[S_T] = S_0\,E[e^{a+bZ}]$ with $a = (\mu-\frac12\sigma^2)T$, $b = \sigma\sqrt T$. Then $a + b^2/2 = \mu T - \frac12\sigma^2T + \frac12\sigma^2T = \mu T$. So $E[S_T] = S_0e^{\mu T}$. The average price grows at $\mu$, as intended.

**Volatility drag.** The *typical* (median) log return grows at only $\mu - \frac12\sigma^2$. Concretely: $+10\%$ then $-10\%$ gives $1.1 \times 0.9 = 0.99$, a loss, though the average simple return was zero. Volatility costs compounded growth. Sinclair returns to this when he discusses leveraged ETFs (Ch. 13 in the 2nd edition).

---

# Part 4: Replication, or Why Your Forecast Doesn't Matter

## 4.1 The naive idea and why it fails

Naive idea: option price = expected payoff, discounted. But expected under **whose** probabilities? You think the stock goes up; I think it goes down. Our expected payoffs differ. And how much extra return do we demand for risk? That's subjective too.

Black, Scholes and Merton's insight: **if you can build the option's payoff out of stock and cash, the option must cost what the ingredients cost.** No probabilities, no opinions. Let's see it in a toy world first.

## 4.2 One-period binomial example

Today $S_0 = 100$. In one period it goes to **120** or **90**. Interest rate is 0 to keep the arithmetic clean. A call with $K=100$ pays:

- up: $\max(120-100, 0) = 20$
- down: $\max(90-100, 0) = 0$

**Replicate it.** Buy $\Delta$ shares and borrow/lend $B$ dollars of cash. We need the portfolio to pay what the call pays in **both** states:

$$\text{up:}\quad 120\Delta + B = 20$$
$$\text{down:}\quad 90\Delta + B = 0$$

Subtract the second equation from the first. $B$ cancels:

$$120\Delta - 90\Delta = 20 - 0$$
$$30\Delta = 20$$
$$\Delta = \tfrac{2}{3}$$

Plug $\Delta = 2/3$ into the down equation:

$$90 \cdot \tfrac{2}{3} + B = 0 \;\Rightarrow\; 60 + B = 0 \;\Rightarrow\; B = -60$$

($B = -60$ means *borrow* \$60.)

**Cost today** of this portfolio:

$$\tfrac{2}{3}\cdot 100 + (-60) = 66.67 - 60 = 6.67$$

So the call must cost **\$6.67**. If it traded at \$8, you'd sell the call, buy the replicating portfolio for \$6.67, pocket \$1.33, and owe nothing in either state. That is **arbitrage**, a riskless profit, and markets don't allow it for long.

**Note what never appeared: the probability that the stock goes up.** Whether it's 10% or 90%, the price is \$6.67. That is the mind-bending core of option pricing.

## 4.3 The risk-neutral probability

There is a probability $q$ that makes the stock's expected return equal the risk-free rate (here 0):

$$100 = q\cdot 120 + (1-q)\cdot 90$$

Expand: $100 = 120q + 90 - 90q = 90 + 30q$. Subtract 90: $10 = 30q$. So $q = 1/3$.

Now price the call as a plain expectation under $q$:

$$q\cdot 20 + (1-q)\cdot 0 = \tfrac13\cdot 20 = 6.67$$

Same answer. That's not a coincidence. **Pricing by replication is mathematically identical to taking expectations in a fictional world where every asset grows at the risk-free rate**, then discounting at the risk-free rate. That fictional world is the **risk-neutral measure**, written $\mathbb{Q}$. Nobody believes $q$ is the real probability. It is a calculating device.

Also note $\Delta = 2/3$. In the continuous BSM world this becomes the option's **delta**: the shares you hold to hedge.

---

# Part 5: The Black-Scholes-Merton PDE

Now do Part 4 in continuous time.

**Setup.** Stock follows GBM: $dS = \mu S\,dt + \sigma S\,dW$. Option value is $V(S,t)$. Risk-free rate is $r$.

**Step 1. Form a hedged portfolio.** Own one option and **short** $\Delta$ shares:

$$\Pi = V - \Delta S$$

**Step 2. How does it change over $dt$?** Hold $\Delta$ fixed over the instant:

$$d\Pi = dV - \Delta\,dS$$

**Step 3. Substitute Itô's lemma** (Section 3.2) for $dV$:

$$d\Pi = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial S}dS + \frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}dt - \Delta\,dS$$

**Step 4. Group the $dS$ terms:**

$$d\Pi = \left(\frac{\partial V}{\partial t} + \frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}\right)dt + \left(\frac{\partial V}{\partial S} - \Delta\right)dS$$

**Step 5. Kill the randomness.** All the randomness lives in $dS$. Choose

$$\Delta = \frac{\partial V}{\partial S}$$

and the $dS$ term disappears:

$$d\Pi = \left(\frac{\partial V}{\partial t} + \frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}\right)dt$$

No $dW$ is left. **The portfolio is riskless over this instant.**

**Step 6. No arbitrage.** A riskless portfolio must earn the risk-free rate. Otherwise you'd borrow at $r$ to buy it (if it earns more) or short it and lend at $r$ (if it earns less). So:

$$d\Pi = r\,\Pi\,dt = r\left(V - \frac{\partial V}{\partial S}S\right)dt$$

**Step 7. Set the two expressions for $d\Pi$ equal** and cancel $dt$:

$$\frac{\partial V}{\partial t} + \frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2} = rV - rS\frac{\partial V}{\partial S}$$

**Step 8. Move everything to one side:**

$$\boxed{\frac{\partial V}{\partial t} + \frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2} + rS\frac{\partial V}{\partial S} - rV = 0}$$

This is the **Black-Scholes-Merton PDE**. It holds for any derivative on $S$: calls, puts, anything. The payoff at expiry (the boundary condition, e.g. $V(S,T) = \max(S-K,0)$) picks out which one.

**$\mu$ is gone.** It disappeared in Step 5 along with $dS$. The stock's expected return doesn't affect the option price. Exactly like the binomial example.

**Read it in Greek** (defined fully in Part 8). Writing $\Theta = \partial V/\partial t$, $\Delta = \partial V/\partial S$, $\Gamma = \partial^2V/\partial S^2$:

$$\Theta + \tfrac12\sigma^2S^2\,\Gamma + rS\Delta - rV = 0$$

Ignore the interest-rate terms (set $r=0$) and it says:

$$\Theta = -\tfrac12\sigma^2S^2\,\Gamma$$

**Time decay is the price of convexity.** If you own gamma (curvature that profits from moves), you pay for it with theta (losing value as time passes), at an exchange rate set by $\sigma^2$. This one line is the most important idea in Sinclair's book.

---

# Part 6: The BSM Formula

## 6.1 Strategy

Solving the PDE directly is hard. Part 4 showed an easier route that gives the same answer: **price = discounted expected payoff in the risk-neutral world.**

$$V_0 = e^{-rT}\,E^{\mathbb{Q}}\big[\text{payoff}(S_T)\big]$$

In the risk-neutral world the stock drifts at $r$ instead of $\mu$. So from Section 3.3, with $\mu$ replaced by $r$:

$$S_T = S_0\exp\!\left[\left(r - \tfrac12\sigma^2\right)T + \sigma\sqrt T\,Z\right], \qquad Z\sim\mathcal N(0,1)$$

(That this expectation solves the PDE is a theorem called the **Feynman-Kac formula**. We take it as given. The binomial example is the intuition for why it's true.)

## 6.2 Split the call payoff into two pieces

Use an **indicator** $\mathbf 1_{\{S_T > K\}}$, which equals 1 if $S_T > K$ and 0 otherwise. Then

$$\max(S_T - K, 0) = (S_T - K)\,\mathbf 1_{\{S_T > K\}} = S_T\mathbf 1_{\{S_T > K\}} - K\,\mathbf 1_{\{S_T > K\}}$$

Take expectations. Expectation is linear, and $E[\mathbf 1_A] = P(A)$:

$$E^{\mathbb Q}[\max(S_T-K,0)] = \underbrace{E^{\mathbb Q}\!\left[S_T\,\mathbf 1_{\{S_T>K\}}\right]}_{\text{Piece A}} - K\,\underbrace{P^{\mathbb Q}(S_T > K)}_{\text{Piece B}}$$

## 6.3 Piece B: the probability of finishing in the money

When is $S_T > K$? Substitute the formula for $S_T$:

$$S_0\exp\!\left[\left(r-\tfrac12\sigma^2\right)T + \sigma\sqrt T Z\right] > K$$

Divide by $S_0$ (positive, so the inequality keeps its direction):

$$\exp\!\left[\left(r-\tfrac12\sigma^2\right)T + \sigma\sqrt T Z\right] > \frac{K}{S_0}$$

Take $\ln$ of both sides ($\ln$ is increasing, so the direction holds):

$$\left(r-\tfrac12\sigma^2\right)T + \sigma\sqrt T Z > \ln\frac{K}{S_0}$$

Subtract the drift term:

$$\sigma\sqrt T Z > \ln\frac{K}{S_0} - \left(r-\tfrac12\sigma^2\right)T$$

Divide by $\sigma\sqrt T$ (positive):

$$Z > \frac{\ln\frac{K}{S_0} - \left(r-\tfrac12\sigma^2\right)T}{\sigma\sqrt T}$$

Use $\ln\frac{K}{S_0} = -\ln\frac{S_0}{K}$ and pull out a minus sign:

$$Z > -\,\frac{\ln\frac{S_0}{K} + \left(r-\tfrac12\sigma^2\right)T}{\sigma\sqrt T}$$

**Define**

$$\boxed{d_2 = \frac{\ln\frac{S_0}{K} + \left(r-\tfrac12\sigma^2\right)T}{\sigma\sqrt T}}$$

so the condition is just $Z > -d_2$. By symmetry (Section 1.3):

$$P^{\mathbb Q}(S_T > K) = P(Z > -d_2) = N(d_2)$$

**Meaning:** $N(d_2)$ is the risk-neutral probability that the call finishes in the money. $d_2$ is "how many standard deviations the strike is below where the stock is expected to land (in log terms)."

## 6.4 Piece A: expected stock value, counting only the in-the-money outcomes

Write it as an integral over $z$, using only $z > -d_2$:

$$E^{\mathbb Q}\!\left[S_T\,\mathbf 1_{\{S_T>K\}}\right] = \int_{-d_2}^{\infty} S_0\exp\!\left[\left(r-\tfrac12\sigma^2\right)T + \sigma\sqrt T z\right]\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz$$

Pull out $S_0$ and $e^{rT}$ (constants), and combine the remaining exponents:

$$= S_0e^{rT}\int_{-d_2}^{\infty}\frac{1}{\sqrt{2\pi}}\exp\!\left[-\frac{z^2}{2} + \sigma\sqrt T z - \frac{\sigma^2T}{2}\right]dz$$

**Complete the square** (same trick as Section 1.4, with $b = \sigma\sqrt T$):

$$-\frac{(z-\sigma\sqrt T)^2}{2} = -\frac{z^2 - 2\sigma\sqrt T z + \sigma^2T}{2} = -\frac{z^2}{2} + \sigma\sqrt T z - \frac{\sigma^2T}{2}$$

That is *exactly* our exponent. So:

$$= S_0e^{rT}\int_{-d_2}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-\frac{(z-\sigma\sqrt T)^2}{2}}\,dz$$

**Substitute** $u = z - \sigma\sqrt T$, so $du = dz$. The lower limit $z = -d_2$ becomes $u = -d_2 - \sigma\sqrt T$. The upper limit stays $\infty$:

$$= S_0e^{rT}\int_{-d_2-\sigma\sqrt T}^{\infty}\frac{1}{\sqrt{2\pi}}e^{-u^2/2}\,du$$

**Define**

$$\boxed{d_1 = d_2 + \sigma\sqrt T = \frac{\ln\frac{S_0}{K} + \left(r+\tfrac12\sigma^2\right)T}{\sigma\sqrt T}}$$

(Check: adding $\sigma\sqrt T = \frac{\sigma^2T}{\sigma\sqrt T}$ to $d_2$ turns $-\frac12\sigma^2T$ in the numerator into $+\frac12\sigma^2T$.)

The integral is now $P(U > -d_1)$ for standard normal $U$, which is $N(d_1)$:

$$E^{\mathbb Q}\!\left[S_T\,\mathbf 1_{\{S_T>K\}}\right] = S_0e^{rT}N(d_1)$$

## 6.5 Assemble

$$C_0 = e^{-rT}\Big[\text{Piece A} - K\cdot\text{Piece B}\Big] = e^{-rT}\Big[S_0e^{rT}N(d_1) - K\,N(d_2)\Big]$$

Distribute $e^{-rT}$. The first term's $e^{-rT}e^{rT} = 1$:

$$\boxed{C_0 = S_0\,N(d_1) - K e^{-rT}N(d_2)}$$

That's the **Black-Scholes-Merton call price**.

**Read it as a replicating portfolio:**

```text
C  =   S0 * N(d1)          -    K e^{-rT} * N(d2)
       ----------               -----------------
       hold N(d1) shares        borrow PV(K) * N(d2) dollars
       (this is delta)          (prob-weighted cost of paying K)
```

Same shape as the binomial: $\Delta = 2/3$ shares and borrowed \$60.

**Why $N(d_1) \neq N(d_2)$:** $N(d_2)$ is the risk-neutral probability of exercise. $N(d_1)$ is bigger, because when you exercise you receive the stock, and the in-the-money outcomes are the ones where the stock is *high*. Piece A weights those outcomes by $S_T$, which tilts the probability up. (Formally, $N(d_1)$ is the exercise probability under a measure that uses the stock as the unit of account.)

## 6.6 The put, via put-call parity

**Claim.** For European options with the same $K$ and $T$:

$$C - P = S_0 - Ke^{-rT}$$

**Proof.** At expiry, check both cases:

- $S_T > K$: call pays $S_T - K$, put pays $0$. Difference: $S_T - K$.
- $S_T \le K$: call pays $0$, put pays $K - S_T$. Difference: $0 - (K - S_T) = S_T - K$.

Either way, long call + short put pays exactly $S_T - K$ at expiry. Another way to get $S_T - K$ at $T$: own one share today (cost $S_0$) and borrow $Ke^{-rT}$ today, which grows to $K$ owed at $T$. Identical payoffs mean identical prices, or there's an arbitrage. $\blacksquare$

**Solve for $P$:**

$$P = C - S_0 + Ke^{-rT}$$

Substitute the call formula:

$$P = S_0N(d_1) - Ke^{-rT}N(d_2) - S_0 + Ke^{-rT}$$

Group: $S_0(N(d_1) - 1) + Ke^{-rT}(1 - N(d_2))$. Use symmetry $1 - N(x) = N(-x)$:

$$\boxed{P_0 = Ke^{-rT}N(-d_2) - S_0N(-d_1)}$$

---

# Part 7: Worked Numbers

$S_0 = 100$, $K = 100$ (at the money), $r = 5\%$, $\sigma = 20\%$, $T = 1$ year.

**$\sigma\sqrt T$:** $0.20 \times \sqrt1 = 0.20$.

**$d_1$:**

$$d_1 = \frac{\ln(100/100) + (0.05 + \frac12(0.20)^2)(1)}{0.20} = \frac{0 + (0.05 + 0.02)}{0.20} = \frac{0.07}{0.20} = 0.35$$

**$d_2$:**

$$d_2 = d_1 - \sigma\sqrt T = 0.35 - 0.20 = 0.15$$

**Normal CDFs** (table or `scipy.stats.norm.cdf`):

$$N(0.35) = 0.6368, \qquad N(0.15) = 0.5596$$

**Discount factor:** $e^{-0.05} = 0.95123$, so $Ke^{-rT} = 95.123$.

**Call:**

$$C = 100(0.6368) - 95.123(0.5596) = 63.68 - 53.23 = \mathbf{10.45}$$

**Put** (parity):

$$P = C - S_0 + Ke^{-rT} = 10.45 - 100 + 95.123 = \mathbf{5.57}$$

Interpretation: the risk-neutral chance of exercise is about 56%. The hedge is about 0.64 shares per call.

**Quick approximation traders use.** For an at-the-money option with small $r$, $C \approx 0.4\,S\,\sigma\sqrt T$. The $0.4$ is $1/\sqrt{2\pi} \approx 0.399$. Here: $0.4 \times 100 \times 0.2 = 8$. With $r=0$ the exact price is 7.97. Option price is roughly **linear in vol** and in $\sqrt{\text{time}}$.

---

# Part 8: The Greeks

**The problem.** A trader needs to know how the option's value changes when inputs change. Each sensitivity is a partial derivative, and each gets a Greek letter.

| Greek | Definition | Plain English |
|---|---|---|
| Delta $\Delta$ | $\partial V/\partial S$ | \$ change per \$1 stock move; shares to hedge |
| Gamma $\Gamma$ | $\partial^2 V/\partial S^2$ | how fast delta changes; curvature |
| Vega $\mathcal V$ | $\partial V/\partial\sigma$ | \$ change per 1.00 change in vol |
| Theta $\Theta$ | $\partial V/\partial t$ | \$ change per year passing (usually negative) |
| Rho $\rho$ | $\partial V/\partial r$ | \$ change per 1.00 change in rates |

Write $\tau = T - t$ for time remaining and $n(x)$ for the normal density.

## 8.1 A key identity first

We need this to simplify all the Greeks:

$$S\,n(d_1) = Ke^{-r\tau}\,n(d_2)$$

**Proof.** Take the ratio of densities. Since $n(x) = \frac{1}{\sqrt{2\pi}}e^{-x^2/2}$, the $\frac1{\sqrt{2\pi}}$ cancels:

$$\frac{n(d_1)}{n(d_2)} = \exp\!\left(-\frac{d_1^2 - d_2^2}{2}\right)$$

Difference of squares: $d_1^2 - d_2^2 = (d_1 - d_2)(d_1 + d_2)$.

- $d_1 - d_2 = \sigma\sqrt\tau$ (by definition).
- $d_1 + d_2$: the numerators add, and $+\frac12\sigma^2\tau$ cancels $-\frac12\sigma^2\tau$:

$$d_1 + d_2 = \frac{2\ln\frac SK + 2r\tau}{\sigma\sqrt\tau}$$

Multiply. The $\sigma\sqrt\tau$ cancels:

$$d_1^2 - d_2^2 = \sigma\sqrt\tau\cdot\frac{2\ln\frac SK + 2r\tau}{\sigma\sqrt\tau} = 2\ln\frac SK + 2r\tau$$

So:

$$\frac{n(d_1)}{n(d_2)} = \exp\!\left(-\ln\frac SK - r\tau\right) = \frac KS\,e^{-r\tau}$$

Multiply both sides by $S\,n(d_2)$ to get $S\,n(d_1) = Ke^{-r\tau}n(d_2)$. $\blacksquare$

## 8.2 Delta

Differentiate $C = S\,N(d_1) - Ke^{-r\tau}N(d_2)$ with respect to $S$. Use the product rule on the first term, and the chain rule ($\frac{d}{dS}N(d) = n(d)\frac{\partial d}{\partial S}$) on both:

$$\frac{\partial C}{\partial S} = N(d_1) + S\,n(d_1)\frac{\partial d_1}{\partial S} - Ke^{-r\tau}n(d_2)\frac{\partial d_2}{\partial S}$$

Both $d_1$ and $d_2$ depend on $S$ only through $\ln S$, and $\frac{d}{dS}\ln S = \frac1S$, so

$$\frac{\partial d_1}{\partial S} = \frac{\partial d_2}{\partial S} = \frac{1}{S\sigma\sqrt\tau}$$

Factor that out of the last two terms:

$$\frac{\partial C}{\partial S} = N(d_1) + \frac{1}{S\sigma\sqrt\tau}\Big[S\,n(d_1) - Ke^{-r\tau}n(d_2)\Big]$$

By the identity in 8.1 the bracket is **zero**. So:

$$\boxed{\Delta_{\text{call}} = N(d_1)}, \qquad \Delta_{\text{put}} = N(d_1) - 1$$

(Put delta: differentiate parity $C - P = S - Ke^{-r\tau}$ in $S$ to get $\Delta_C - \Delta_P = 1$.)

Call delta runs from 0 (far out of the money) to 1 (deep in the money). At the money it's a bit above 0.5.

## 8.3 Gamma

Differentiate delta again, using the chain rule:

$$\Gamma = \frac{\partial}{\partial S}N(d_1) = n(d_1)\frac{\partial d_1}{\partial S} = \boxed{\frac{n(d_1)}{S\sigma\sqrt\tau}}$$

Same for calls and puts (parity's $S$ term has zero second derivative). Gamma is largest at the money and **grows as expiry approaches** (because of $\sqrt\tau$ in the denominator). Short-dated ATM options are the most convex.

## 8.4 Vega

Differentiate the call with respect to $\sigma$:

$$\frac{\partial C}{\partial\sigma} = S\,n(d_1)\frac{\partial d_1}{\partial\sigma} - Ke^{-r\tau}n(d_2)\frac{\partial d_2}{\partial\sigma}$$

By 8.1, $Ke^{-r\tau}n(d_2) = S\,n(d_1)$, so factor that out:

$$= S\,n(d_1)\left[\frac{\partial d_1}{\partial\sigma} - \frac{\partial d_2}{\partial\sigma}\right] = S\,n(d_1)\frac{\partial(d_1 - d_2)}{\partial\sigma}$$

Since $d_1 - d_2 = \sigma\sqrt\tau$, its derivative in $\sigma$ is $\sqrt\tau$:

$$\boxed{\mathcal V = S\,n(d_1)\sqrt\tau}$$

Same for puts. Vega is largest at the money and **grows** with time to expiry, the opposite of gamma. Long-dated options are vol bets. Short-dated options are gamma (realized-move) bets.

## 8.5 Theta

Differentiate with respect to $\tau$ (time remaining). Theta is with respect to calendar time $t$, and $\tau = T - t$, so $\Theta = -\partial C/\partial\tau$.

$$\frac{\partial C}{\partial\tau} = S\,n(d_1)\frac{\partial d_1}{\partial\tau} - \left[-rKe^{-r\tau}N(d_2) + Ke^{-r\tau}n(d_2)\frac{\partial d_2}{\partial\tau}\right]$$

(The middle term comes from $\frac{\partial}{\partial\tau}e^{-r\tau} = -re^{-r\tau}$.) Use 8.1 again to combine the $n(\cdot)$ terms:

$$= S\,n(d_1)\frac{\partial(d_1-d_2)}{\partial\tau} + rKe^{-r\tau}N(d_2)$$

$\frac{\partial}{\partial\tau}(\sigma\sqrt\tau) = \frac{\sigma}{2\sqrt\tau}$. So:

$$\boxed{\Theta_{\text{call}} = -\frac{S\,n(d_1)\,\sigma}{2\sqrt\tau} - rKe^{-r\tau}N(d_2)}$$

The first term is the "pay for gamma" part. Check: $\frac12\sigma^2S^2\Gamma = \frac12\sigma^2S^2\frac{n(d_1)}{S\sigma\sqrt\tau} = \frac{S\,n(d_1)\sigma}{2\sqrt\tau}$. That matches Part 5's $\Theta = -\frac12\sigma^2S^2\Gamma$. The second term is interest on the borrowed cash.

## 8.6 Numbers, and a check that the PDE holds

Same example: $S=100, K=100, r=0.05, \sigma=0.2, \tau=1$, $d_1 = 0.35$.

$$n(0.35) = \frac{1}{\sqrt{2\pi}}e^{-0.35^2/2} = 0.39894\times e^{-0.06125} = 0.39894\times0.94059 = 0.37524$$

| Greek | Computation | Value |
|---|---|---|
| $\Delta$ | $N(0.35)$ | 0.6368 |
| $\Gamma$ | $0.37524 / (100\times0.2\times1)$ | 0.01876 |
| $\mathcal V$ | $100\times0.37524\times1$ | 37.52 per 1.00 vol, so **0.375 per vol point** |
| $\Theta$ | $-\frac{100\times0.37524\times0.2}{2} - 0.05\times95.123\times0.5596$ | $-3.752 - 2.662 = -6.414$/yr, about **−0.018/calendar day** |

**Plug into the PDE** $\Theta + \frac12\sigma^2S^2\Gamma + rS\Delta - rV$:

$$-6.414 + \tfrac12(0.04)(10{,}000)(0.01876) + 0.05(100)(0.6368) - 0.05(10.45)$$
$$= -6.414 + 3.752 + 3.184 - 0.5225 = -0.0005 \approx 0 \;\checkmark$$

(The tiny residual is rounding.) The formula really does solve the equation.

---

# Part 9: Hedged P&L: Realized vs Implied Volatility

This is where theory turns into a trade, and it's the lens for Sinclair's entire book.

## 9.1 Two different volatilities

- **Implied volatility** $\sigma_i$: the $\sigma$ you plug into BSM to match the option's **market price**. Price comes first; vol is backed out. It is the market's quote, a price in vol units.
- **Realized volatility** $\sigma_r$: the standard deviation of the stock's actual log returns over the option's life. You only know it afterwards.

If you buy an option and delta-hedge, do you make money? Derive it.

## 9.2 The delta-hedged position: $C - \Delta S$

Sinclair's opening chapter works with a portfolio written as

$$\Pi_t = C(S_t) - \Delta\,S_t$$

Symbol by symbol:

- $S_t$: the stock price at time $t$.
- $C(S_t)$: the value of **one call option** when the stock is at $S_t$. You **own** it.
- $\Delta$: the option's delta, which is also **the number of shares you are short**.
- $\Pi_t$: the value of the whole position.

**Yes, that's a minus sign, and it's there because you are short.** Being short a share means you sold a share you borrowed, and you owe it back. If the share price rises \$1, what you owe rises \$1, so you lose \$1. A short position is worth *minus* the share price. Short $\Delta$ shares is worth $-\Delta S_t$.

**Why short, and why exactly $\Delta$ shares?** A call gains value when the stock rises; that's what $\Delta > 0$ says. To cancel that, you need something that *loses* the same amount when the stock rises. Short stock does. From Section 1.6, the option changes by about $\Delta$ per \$1, and $\Delta$ short shares change by exactly $-\Delta$ per \$1, so the two cancel to first order.

With the Part 7 numbers ($\Delta = 0.6368$):

| Stock moves | Option changes by about | Short 0.6368 shares change by | Net (first order) |
|---|---|---|---|
| $+\$1$ | $+0.6368$ | $-0.6368$ | $0$ |
| $-\$1$ | $-0.6368$ | $+0.6368$ | $0$ |

What's left after this cancellation is the gamma term, and that is what the trade is really about.

## 9.3 The cash side: where the interest terms come from

Positions involve cash, and cash earns or costs interest at rate $r$.

- **Buying the option costs $C$.** Say you borrow that money. Over a time step $\Delta t$ you owe interest of $r\,C\,\Delta t$. That's a **cost**: $-rC\,\Delta t$.
- **Short-selling $\Delta$ shares brings in cash $\Delta S_t$.** You sold shares, so you received money. Deposit it and earn $r\,\Delta S_t\,\Delta t$. That's a **gain**: $+r\Delta S_t\,\Delta t$.

Add them:

$$\text{financing} = -rC\,\Delta t + r\Delta S_t\,\Delta t = -r\left(C - \Delta S_t\right)\Delta t$$

That's the $-r(C - \Delta S_t)$ term in Sinclair's expression. Writing it as one bracket hides the two pieces. **The $+r\Delta S_t$ inside it is the interest you earn on the short-sale cash, and $-rC$ is the interest you pay to fund the option.**

With the Part 7 numbers, $C - \Delta S = 10.45 - 63.68 = -53.23$. That's negative: you took in \$63.68 from the short sale but spent only \$10.45 on the option. You are **net lending** \$53.23 and collecting interest on it. For one trading day ($\Delta t = 1/252$, $r = 5\%$):

$$-r(C - \Delta S)\Delta t = -0.05\times(-53.23)\times\tfrac{1}{252} = +\$0.0106$$

Books sometimes write the term without the $\Delta t$. That just means they measure time in units of one period, so $\Delta t = 1$ and $r$ is the per-period rate. (Real-world details this ignores: the fee for borrowing shares to short, and dividends you owe on shorted shares.)

## 9.4 One period of P&L, term by term

Move from time $t$ to $t+1$, one step of length $\Delta t$. The stock goes from $S_t$ to $S_{t+1}$. Keep $\Delta$ fixed during the step. The change in the position's value is

$$\text{P\&L} = \underbrace{C(S_{t+1}) - C(S_t)}_{\text{(1) option}} \;\underbrace{-\;\Delta\,(S_{t+1} - S_t)}_{\text{(2) short stock}} \;\underbrace{-\;r\,(C - \Delta S_t)\,\Delta t}_{\text{(3) financing}}$$

(Strictly, the option's value also depends on time, so term (1) is $C(S_{t+1}, t+\Delta t) - C(S_t, t)$. Sinclair writes $C(S_{t+1})$ as shorthand.)

1. **Option.** New value minus old value. You own it, so its change is your gain.
2. **Short stock.** The stock moved $S_{t+1} - S_t$. Each share you're short loses that amount, and you're short $\Delta$ shares. Hence $-\Delta(S_{t+1} - S_t)$: the **same minus sign** as in $\Pi = C - \Delta S$, for the same reason.
3. **Financing.** From 9.3.

**Numbers.** Part 7's option, one trading day, the stock moves from 100 to 102. Full BSM revaluation gives $C(102,\ \text{1 day later}) = 11.7352$.

| Term | Computation | Value |
|---|---|---|
| (1) option | $11.7352 - 10.4506$ | $+1.2846$ |
| (2) short stock | $-0.6368 \times (102 - 100)$ | $-1.2737$ |
| (3) financing | from 9.3 | $+0.0106$ |
| **Total** | | **$+0.0215$** |

The option and the stock almost cancel. What's left is small, and it's what this section is about.

## 9.5 Taylor-expand the option term

Use the two-variable second-order Taylor expansion from Section 1.6, with $h = S_{t+1} - S_t$ (write it $\delta S$) and $k = \Delta t$:

$$C(S_{t+1}) - C(S_t) \approx \Delta\,\delta S + \Theta\,\Delta t + \tfrac12\Gamma\,(\delta S)^2$$

Substitute into the P&L from 9.4:

$$\text{P\&L} \approx \Delta\,\delta S + \Theta\,\Delta t + \tfrac12\Gamma(\delta S)^2 - \Delta\,\delta S - r(C - \Delta S_t)\Delta t$$

**The $\Delta\,\delta S$ terms cancel.** That is the hedge doing its job:

$$\text{P\&L} \approx \tfrac12\Gamma(\delta S)^2 + \Big[\Theta - r(C - \Delta S_t)\Big]\Delta t$$

Two things are left: a **gamma** gain from the size of the move, and a **time** term, theta plus financing.

## 9.6 Use the BSM equation to simplify the time term

The option was priced with implied vol $\sigma_i$, so it satisfies the BSM PDE (Part 5) with $\sigma = \sigma_i$:

$$\Theta + \tfrac12\sigma_i^2S^2\Gamma + rS\Delta - rC = 0$$

Move $\tfrac12\sigma_i^2S^2\Gamma$ to the right side:

$$\Theta + rS\Delta - rC = -\tfrac12\sigma_i^2S^2\Gamma$$

The left side is $\Theta - r(C - \Delta S)$, the exact bracket from 9.5. So:

$$\Theta - r(C - \Delta S_t) = -\tfrac12\sigma_i^2S^2\Gamma$$

**The interest terms vanish into theta.** Theta already includes the option's financing drift, so combined with the cash interest, all that's left is "pay for gamma at the implied rate." Substitute:

$$\text{P\&L} \approx \tfrac12\Gamma(\delta S)^2 - \tfrac12\Gamma\sigma_i^2S^2\,\Delta t$$

Factor out $\tfrac12\Gamma S^2$. The first term becomes $\tfrac12\Gamma S^2\left(\frac{\delta S}{S}\right)^2$:

$$\boxed{\text{P\&L} \approx \tfrac12\,\Gamma S^2\left[\left(\frac{\delta S}{S}\right)^2 - \sigma_i^2\,\Delta t\right]}$$

Read the bracket:

- $\left(\frac{\delta S}{S}\right)^2$ is **this period's squared return**: what actually happened.
- $\sigma_i^2\Delta t$ is **the squared return the option price assumed** for one period.

If the move was bigger than implied, you make money. If smaller, you lose. Up or down doesn't matter, because the move is squared.

**Check with the 100 → 102 day:** $\tfrac12(0.01876)(2^2) - \tfrac12(0.01876)(0.04)(10{,}000)\tfrac{1}{252} = 0.0375 - 0.0149 = 0.0226$. The exact revaluation gave $0.0215$. The gap is the higher-order terms the expansion drops. A move to 98 gives the same $+0.0226$ approximation (exact: $+0.0239$). A small move to 100.5 gives $\tfrac12(0.01876)(0.25) - 0.0149 = -0.0126$ (exact: $-0.0127$). A move smaller than the breakeven loses money.

## 9.7 Add up many periods

Over many periods, the average squared return is realized variance per period: $\left(\frac{\delta S}{S}\right)^2$ averages to $\sigma_r^2\,\Delta t$. Replace it, and shrink $\Delta t$ to $dt$:

$$\boxed{d(\text{P\&L}) = \tfrac12\,\Gamma S^2\left(\sigma_r^2 - \sigma_i^2\right)dt}$$

**Read it:** a delta-hedged long option makes money when realized variance beats implied variance, and loses when it doesn't. You are **long realized vol, short implied vol**. The amount scales with **dollar gamma** $\frac12\Gamma S^2$, which is largest near the money. That is why path matters: the same realized vol earns more if the big moves happen while the stock is near the strike.

## 9.8 Daily breakeven, with numbers

Each day, theta costs you (with $r=0$, for the gamma part)

$$\tfrac12\Gamma S^2\sigma_i^2\,\Delta t = \tfrac12\Gamma\,(S\sigma_i\sqrt{\Delta t})^2$$

and the day's move earns $\tfrac12\Gamma(\delta S)^2$. So you break even when

$$|\delta S| = S\,\sigma_i\sqrt{\Delta t}$$

With $S = 100$, $\sigma_i = 20\%$, $\Delta t = 1/252$: breakeven move is $100\times0.2/15.87 = \$1.26$. That's the rule of 16 again.

With $\Gamma = 0.01876$:

- Daily gamma rent: $\frac12(0.01876)(1.26)^2 \approx \$0.0149$.
- If the stock moves \$2: you earn $\frac12(0.01876)(4) = \$0.0375$. Net about $+\$0.023$.
- If it moves \$0.50: you earn $\frac12(0.01876)(0.25) = \$0.0023$. Net about $-\$0.0126$.

Being long options is renting volatility. Each day you pay rent (theta) and collect on the moves (gamma). Sinclair's chapters on hedging and on the distribution of hedged P&L (Ch. 6-7) are about how noisy that collection is in practice.

---

# Part 10: Preview of Sinclair Chapter 2: Measuring Realized Volatility

To compare $\sigma_r$ with $\sigma_i$, you have to estimate $\sigma_r$ from data.

**Close-to-close estimator.** With closing prices $S_0,\dots,S_n$:

1. Log returns: $x_i = \ln(S_i/S_{i-1})$ for $i = 1..n$.
2. Mean: $\bar x = \frac1n\sum x_i$.
3. Sample variance with $n-1$ (see `../math/variance_covariance.md` for why): $s^2 = \frac{1}{n-1}\sum (x_i - \bar x)^2$.
4. Annualize. Variance scales with time (Section 1.5), so multiply variance by 252, then take the square root:

$$\hat\sigma = \sqrt{252\cdot\frac{1}{n-1}\sum_{i=1}^n (x_i - \bar x)^2}$$

Practitioners often drop $\bar x$ (set it to 0), since daily mean returns are tiny next to daily noise. Recall drift scales with $dt$ and noise with $\sqrt{dt}$.

**Range-based estimators.** Close-to-close throws away what happened during the day. A stock that ranged from 95 to 105 and closed unchanged had a volatile day that close-to-close calls zero. **Parkinson's estimator** uses each day's high $H_i$ and low $L_i$:

$$\hat\sigma^2_{\text{P}} = \frac{1}{4\ln 2}\cdot\frac1n\sum_{i=1}^n\left(\ln\frac{H_i}{L_i}\right)^2 \quad(\times 252 \text{ to annualize})$$

The odd constant $4\ln 2$ comes from the known distribution of the range of Brownian motion. It's the factor that makes the estimator unbiased under GBM. Using the range makes the estimate several times more statistically efficient (less noisy for the same number of days). Garman-Klass, Rogers-Satchell and Yang-Zhang add opens and closes, and handle drift and overnight gaps. The tradeoff Sinclair stresses is **efficiency vs bias**: richer estimators are less noisy but more sensitive to how reality violates GBM (discrete trading, jumps, opening gaps).

---

# Part 11: Assumptions, and Where BSM Breaks

BSM rests on assumptions. Each failure is a chapter of real-world vol trading.

| Assumption | Reality | Consequence |
|---|---|---|
| Constant volatility | Vol clusters, mean-reverts, jumps | Implied vol differs by strike and expiry (smile/skew, term structure) |
| Log returns normal (GBM) | Fat tails, crashes | Deep OTM puts priced richer than BSM says |
| Continuous hedging | You hedge discretely | Hedged P&L is noisy, not the clean formula in 9.2 |
| No transaction costs | Spreads and fees | Hedging too often bleeds money; too rarely adds noise |
| Constant known $r$, no dividends | Neither holds exactly | Small corrections (dividends enter as a $-q$ in the drift) |

So why does everyone use BSM? Because traders use it as a **quoting convention and a hedging map**, not as truth. Implied vol is just a unit for option prices, the way yield is a unit for bond prices. The interesting question, and Sinclair's subject, is: **is the implied vol I'm paying too high or too low relative to the realized vol I'll actually get?** That is Part 9's formula, played out under real-world messiness.

---

# Recap

1. **Log returns add** across time, so they're approximately normal, and prices are lognormal. Variance grows like $T$, vol like $\sqrt T$.
2. **Brownian motion** moves $\sqrt{dt}$ per step, so $(dW)^2 = dt$. That makes a second-order term survive: **Itô's lemma**, where curvature turns noise into drift.
3. **Delta hedging** removes all randomness from (option − Δ·stock) for an instant. No arbitrage then forces the **BSM PDE**, and the stock's expected return $\mu$ drops out.
4. Equivalently, price = **discounted expectation in a risk-neutral world** (drift $r$). Splitting the payoff and completing the square gives $C = SN(d_1) - Ke^{-rT}N(d_2)$.
5. The PDE says **theta pays for gamma** at rate $\sigma^2$. A delta-hedged option earns $\frac12\Gamma S^2(\sigma_r^2 - \sigma_i^2)\,dt$: it's a bet on **realized vs implied** variance.

---

# Check Your Understanding

**1. Why doesn't the stock's expected return $\mu$ appear in the BSM formula?**
The option can be replicated by continuously delta hedging, which removes the $dS$ (and therefore $\mu$) term. Anything replicable must cost what its replication costs, regardless of anyone's forecast.

**2. In ordinary calculus $(dx)^2$ is negligible. Why isn't $(dW)^2$?**
Brownian increments have size about $\sqrt{dt}$, so their squares are size $dt$, the same order as the terms we keep. Summed over an interval they total exactly the elapsed time, not zero.

**3. You're long a delta-hedged ATM option bought at 25% implied vol. The stock realizes 18%. What happens, and when is the damage worst?**
You lose, because $\sigma_r^2 < \sigma_i^2$, so theta rent beats gamma gains. The loss is worst when dollar gamma is high: the stock sitting near the strike close to expiry.

**4. Gamma rises as expiry approaches, but vega falls. What does that imply about which options to use for which view?**
Short-dated options are mainly bets on realized moves (gamma/theta). Long-dated options are mainly bets on implied vol changing (vega).

---

# Vocabulary

```text
Arbitrage:            A riskless profit with no net investment; pricing assumes none exist.
Brownian motion:      Continuous random walk with independent N(0, t) increments; W_t.
Delta hedging:        Holding -Delta shares per option to cancel first-order stock risk.
d1, d2:               Standardized distances (in sigma*sqrt(T) units) between log stock and log strike;
                      d1 - d2 = sigma*sqrt(T).
GBM:                  dS = mu S dt + sigma S dW; percentage moves are normal, prices lognormal.
Implied volatility:   The sigma that makes BSM match the market price.
Ito's lemma:          Chain rule for random processes; keeps the 1/2 sigma^2 S^2 V_SS term.
Lognormal:            Distribution of e^X when X is normal; positive and right-skewed.
N(x), n(x):           Standard normal CDF and density.
Realized volatility:  Annualized standard deviation of actual log returns.
Replication:          Building a payoff from stock and cash so its price is forced.
Risk-neutral measure: Fictional probabilities under which every asset drifts at r; used for pricing.
```

---

# Sources and Further Reading

- Euan Sinclair, *Volatility Trading*, 2nd ed., Wiley, 2013 (ISBN 9781118347133). Part I chapters: Option Pricing; Volatility Measurement. Chapter list confirmed from a [library catalog record](https://opac.iub.edu.bd/bib/21860) and [publisher listing](https://www.ebook.de/de/product/19812667/.html). Chapter numbers above follow that record.
- Original papers (standard references, not quoted here): F. Black and M. Scholes, "The Pricing of Options and Corporate Liabilities," *Journal of Political Economy*, 1973; R. C. Merton, "Theory of Rational Option Pricing," *Bell Journal of Economics and Management Science*, 1973.
- For more derivations at this level: John Hull, *Options, Futures, and Other Derivatives* (binomial trees, Itô, BSM chapters). For the rigorous measure-theory version: Steven Shreve, *Stochastic Calculus for Finance I & II*.
- M. Parkinson, "The Extreme Value Method for Estimating the Variance of the Rate of Return," *Journal of Business*, 1980 (the range estimator in Part 10).

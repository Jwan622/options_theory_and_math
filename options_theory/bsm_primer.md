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

**Warning: $\Delta$ does double duty.** In math generally, $\Delta$ means "change in", so $\Delta S$ means the change in the stock price $S$, and $\Delta t$ means "a small step of time". In options, $\Delta$ alone means the Greek delta. Books, Sinclair's included, use both meanings, sometimes in the same line. A quick test: if $\Delta$ sits directly in front of a variable with no space or multiplication meant ($\Delta t$, $\Delta S$ written as a change), it means "change in". If it multiplies something ($\Delta \cdot S$, or short $\Delta$ shares), it's the hedge ratio. In this primer, $\Delta t$ always means a time step, and a price change is written out as $S_{t+1} - S_t$ or $\delta S$ to avoid the clash.

---

# Part 1: The Toolbox

## 1.1 Continuous compounding and discounting

**The problem.** A dollar today and a dollar in one year are not worth the same. Today's dollar can sit in a bank and earn interest, so by next year it is more than a dollar. To compare money at different times we need a rule for how money grows. Every option formula has one built in.

### Step 1: compounding a few times a year

The bank pays 5% a year. "Compounding $n$ times a year" means: split the year into $n$ equal periods, pay $\frac{5\%}{n}$ interest at the end of each period, and let the next period's interest be earned on the new, bigger balance.

**Yearly** ($n = 1$). One period, pay 5% once:

$$1 \times (1 + 0.05) = 1.05$$

**Monthly** ($n = 12$). Each month pays $\frac{0.05}{12} = 0.0041667$ (about 0.417%). Watch the balance:

| After month | Calculation | Balance |
|---|---|---|
| 1 | $1 \times 1.0041667$ | 1.0041667 |
| 2 | $1.0041667 \times 1.0041667$ | 1.0083507 |
| 3 | $1.0083507 \times 1.0041667$ | 1.0125522 |
| ... | keep multiplying by 1.0041667 | ... |
| 12 | $1.0041667^{12}$ | 1.0511619 |

Each month you multiply by the same factor $\left(1 + \frac{0.05}{12}\right)$, and twelve multiplications is a power of 12. So the general rule, for $n$ periods a year, is that \$1 grows to

$$\left(1 + \frac{0.05}{n}\right)^n$$

Plugging in different $n$:

| $n$ | Calculation | Value after 1 year |
|---|---|---|
| 1 (yearly) | $1.05^1$ | 1.050000 |
| 2 (half-yearly) | $1.025^2$ | 1.050625 |
| 12 (monthly) | $1.0041667^{12}$ | 1.051162 |
| 365 (daily) | $1.000137^{365}$ | 1.051267 |
| 1,000,000 | $1.00000005^{1{,}000{,}000}$ | 1.051271 |

**What this shows.** Compounding more often helps, because interest starts earning interest sooner. But the gains shrink fast: going from daily to a million times a year adds almost nothing. The values approach a ceiling, 1.051271.

### Step 2: the ceiling is $e^{r}$

The number $e = 2.71828\ldots$ is defined by this limit:

$$e = \lim_{m\to\infty}\left(1 + \frac{1}{m}\right)^m$$

Our expression has $\frac{r}{n}$ instead of $\frac{1}{m}$. Turn one into the other:

1. Define $m = \frac{n}{r}$. Then $\frac{r}{n} = \frac{1}{m}$, and $n = m\,r$.
2. Substitute both into $\left(1 + \frac{r}{n}\right)^n$:

$$\left(1 + \frac{r}{n}\right)^n = \left(1 + \frac{1}{m}\right)^{m r}$$

3. Use the exponent rule $a^{bc} = (a^b)^c$:

$$= \left[\left(1 + \frac{1}{m}\right)^{m}\right]^{r}$$

4. As $n \to \infty$, $m \to \infty$ too, so the bracket becomes $e$:

$$\lim_{n\to\infty}\left(1 + \frac{r}{n}\right)^n = e^{r}$$

Check with $r = 0.05$: $e^{0.05} = 1.051271$, exactly the ceiling in the table.

### Step 3: many years

Over $T$ years you compound the one-year growth $T$ times: $e^r \times e^r \times \cdots = (e^r)^T = e^{rT}$.

**With continuous compounding at rate $r$, \$1 grows to $e^{rT}$ after $T$ years.**

**Example.** \$100 at 5% for 3 years:

1. $rT = 0.05 \times 3 = 0.15$
2. $e^{0.15} = 1.161834$
3. $100 \times 1.161834 = \$116.18$

### Step 4: run it backwards (discounting)

Now flip the question. Someone promises you \$100 in 2 years. What is that promise worth **today**?

Call today's value $P$. If you put $P$ in the bank today, it grows to $P\,e^{rT}$. It's a fair trade if that equals the \$100 you'll get:

$$P\,e^{rT} = 100$$

Divide both sides by $e^{rT}$:

$$P = \frac{100}{e^{rT}} = 100\,e^{-rT}$$

(Dividing by $e^{rT}$ is the same as multiplying by $e^{-rT}$, because $e^{-x} = \frac{1}{e^{x}}$.)

Plug in $r = 0.05$, $T = 2$:

1. $rT = 0.05 \times 2 = 0.10$
2. $e^{-0.10} = 0.904837$
3. $P = 100 \times 0.904837 = \$90.48$

Check by going forward: $90.48 \times e^{0.10} = 90.48 \times 1.105171 = 100.00$. ✓

In general, an amount $X$ received at time $T$ is worth today

$$P = X\,e^{-rT}$$

This is **discounting**. $e^{-rT}$ is the **discount factor**.

### What this means for options

In the BSM call formula (Part 6) you'll see $K e^{-rT}$. When you exercise a call you pay the strike $K$, but you pay it at expiry, not today. $K e^{-rT}$ is what that future payment is worth today. In Part 7's example ($K = 100$, $r = 5\%$, $T = 1$):

$$K e^{-rT} = 100 \times e^{-0.05} = 100 \times 0.951229 = 95.12$$

**High level:** whenever you see $e^{-rT}$, read it as "this amount is paid at time $T$, so shrink it to today's money." Whenever you see $e^{rT}$, read it as "grow today's money forward to time $T$."

## 1.2 Simple returns vs log returns

**The problem.** We need to measure how much a stock moved in a way that (a) adds up correctly across days and (b) behaves well in statistics. The everyday percentage return fails (a). The log return passes both.

### First: what is $\ln$?

$\ln(x)$, the **natural log**, answers: "what power do I raise $e$ to, to get $x$?"

- $\ln(1) = 0$, because $e^0 = 1$.
- $\ln(e) = 1$, because $e^1 = e$.
- $\ln(1.10) = 0.0953$, because $e^{0.0953} = 1.10$.

$\ln$ and $e^{(\cdot)}$ undo each other: $e^{\ln x} = x$ and $\ln(e^{y}) = y$.

**The one log rule we need:** $\ln(a \cdot b) = \ln a + \ln b$.

Why it's true: write $a = e^{p}$ and $b = e^{q}$, so $p = \ln a$ and $q = \ln b$. Then $a\cdot b = e^{p}\,e^{q} = e^{p+q}$, using the exponent rule $e^p e^q = e^{p+q}$. Taking $\ln$ of both sides, $\ln(ab) = p + q = \ln a + \ln b$. Logs turn multiplication into addition. That is the entire reason for using them.

A matching rule for division: $\ln\frac{a}{b} = \ln a - \ln b$.

### Two ways to measure one move

Stock goes from $S_0 = 100$ to $S_1 = 110$.

**Simple return** ("percentage change"):

$$\frac{S_1 - S_0}{S_0} = \frac{110 - 100}{100} = \frac{10}{100} = 0.10 = 10\%$$

**Log return**: the log of the price ratio.

$$\ln\frac{S_1}{S_0} = \ln\frac{110}{100} = \ln(1.10) = 0.0953 = 9.53\%$$

Both describe the same move. They're different units, like Celsius and Fahrenheit. To get back from a log return $x$ to the price, exponentiate:

$$S_1 = S_0\,e^{x} = 100 \times e^{0.0953} = 100 \times 1.10 = 110$$

### Why log returns win: they add

The stock goes $100 \to 110 \to 99$. Overall it fell from 100 to 99, which is a 1% loss.

**Simple returns.**

- Day 1: $\frac{110 - 100}{100} = +0.10$
- Day 2: $\frac{99 - 110}{110} = \frac{-11}{110} = -0.10$
- Add them: $0.10 + (-0.10) = 0$

Adding says "no change," but the stock lost 1%. **Adding simple returns is wrong.** To combine them correctly you have to multiply growth factors: $(1 + 0.10)(1 - 0.10) = 1.10 \times 0.90 = 0.99$, so a 1% loss. Multiplying is awkward in statistics.

**Log returns.**

- Day 1: $\ln\frac{110}{100} = \ln(1.10) = +0.09531$
- Day 2: $\ln\frac{99}{110} = \ln(0.90) = -0.10536$
- Add them: $0.09531 + (-0.10536) = -0.01005$

The overall log return, start to finish:

$$\ln\frac{99}{100} = \ln(0.99) = -0.01005$$

**They match.** Adding log returns is right. Here's why, step by step:

$$\ln\frac{110}{100} + \ln\frac{99}{110}$$

Use $\ln a + \ln b = \ln(ab)$:

$$= \ln\left(\frac{110}{100}\cdot\frac{99}{110}\right)$$

The 110 on top cancels the 110 on the bottom:

$$= \ln\frac{99}{100}$$

The same cancellation works for any number of days. With prices $S_0, S_1, \dots, S_n$, every middle price cancels:

$$\frac{S_1}{S_0}\cdot\frac{S_2}{S_1}\cdot\frac{S_3}{S_2}\cdots\frac{S_n}{S_{n-1}} = \frac{S_n}{S_0}$$

Take $\ln$ of both sides and split the left side with the log rule:

$$\ln\frac{S_n}{S_0} = \ln\frac{S_1}{S_0} + \ln\frac{S_2}{S_1} + \cdots + \ln\frac{S_n}{S_{n-1}} = \sum_{i=1}^{n}\ln\frac{S_i}{S_{i-1}}$$

The $\sum$ ("sigma") just means "add up these terms for $i = 1, 2, \dots, n$."

**In words: the total log return equals the sum of the daily log returns.**

Another nice property: log returns are symmetric. A $+0.10$ log return followed by $-0.10$ returns exactly to the start, since $e^{0.10}\,e^{-0.10} = e^{0} = 1$. With simple returns, $+10\%$ then $-10\%$ leaves you down 1%.

### When are they close?

| Simple return | Log return $\ln(1 + \text{simple})$ | Gap |
|---|---|---|
| +1% | +0.995% | tiny |
| +10% | +9.53% | small |
| −10% | −10.54% | small |
| +50% | +40.55% | big |
| −50% | −69.31% | big |

For small moves they're nearly equal. The reason is a Taylor expansion (Section 1.6): $\ln(1 + x) = x - \frac{x^2}{2} + \dots$ For $x = 0.01$: $0.01 - \frac{0.0001}{2} = 0.01 - 0.00005 = 0.00995$. Daily stock moves are usually a percent or two, so in practice the two are close. Over long horizons or big moves they differ a lot.

### Why this matters

Statistics is very good at **sums** of random things. The Central Limit Theorem says a sum of many small independent random pieces is approximately normal. A year's log return is a sum of about 252 daily log returns, so it should be roughly normal. That's the starting assumption of BSM. Sinclair, like almost all volatility traders, works in log returns for this reason.

## 1.3 The normal distribution and $N(x)$

**The problem.** BSM needs answers like "what's the chance the stock ends above the strike?" To answer those we need a model of how random outcomes are spread out. The normal distribution (the bell curve) is that model, and $N(x)$ is the tool that turns it into probabilities.

### Distributions, densities and areas

A **random variable** is a number whose value is uncertain, like tomorrow's return. Its **distribution** says which values are likely.

For a continuous variable, we draw a curve called the **density**. Read it like this:

- Where the curve is high, values are likely. Where it's low, they're rare.
- **Probabilities are areas under the curve.** The chance of landing between $a$ and $b$ is the area under the curve from $a$ to $b$.
- The total area under the whole curve is 1, because something has to happen.

### The standard normal and its density $n(z)$

$Z \sim \mathcal{N}(0,1)$ reads: $Z$ is normally distributed with mean 0 and variance 1. This is the **standard normal**. Its density is

$$n(z) = \frac{1}{\sqrt{2\pi}}\, e^{-z^2/2}$$

What each piece does:

- $e^{-z^2/2}$ creates the bell shape. At $z = 0$ it's $e^0 = 1$, the peak. As $z$ moves away from 0 in either direction, $z^2$ grows, so $e^{-z^2/2}$ shrinks toward 0. Because $z$ is squared, $z$ and $-z$ give the same height, so the curve is symmetric.
- $\frac{1}{\sqrt{2\pi}} = 0.39894$ is a scaling constant. It makes the total area exactly 1.

Plug in a few values:

| $z$ | $z^2/2$ | $e^{-z^2/2}$ | $n(z) = 0.39894 \times e^{-z^2/2}$ |
|---|---|---|---|
| 0 | 0 | 1.00000 | 0.39894 |
| 1 (or −1) | 0.5 | 0.60653 | 0.24197 |
| 2 (or −2) | 2 | 0.13534 | 0.05399 |

**What this shows.** A value near 0 is most likely. At one standard deviation away, the curve is at 61% of its peak height. At two standard deviations it's down to 14%. Far-out values are rare.

```text
 n(z)
 0.40 |        ***
      |      *     *
 0.24 |    *         *
      |   *           *
 0.05 | *               *
      +--+----+----+----+--+-->  z
        -2   -1    0    1   2
```

### The CDF $N(x)$: area to the left

$$N(x) = P(Z \le x) = \int_{-\infty}^{x} n(z)\,dz$$

In words: $N(x)$ is the probability that $Z$ comes out at or below $x$. Geometrically, it's the area under the bell from the far left up to $x$. This is the **cumulative distribution function (CDF)**.

$N(x)$ has no simple formula (the integral can't be done by hand), so you look it up. In Python it's `scipy.stats.norm.cdf(x)`. In Excel it's `NORM.S.DIST(x, TRUE)`.

Values to know, with what each one means:

| $x$ | $N(x)$ | Meaning |
|---|---|---|
| 0 | 0.5000 | Half the area is left of the center. |
| 0.15 | 0.5596 | Used in Part 7. |
| 0.35 | 0.6368 | Used in Part 7. |
| 1 | 0.8413 | 84% chance $Z$ is below +1. |
| 1.645 | 0.9500 | 95% chance $Z$ is below 1.645. |
| 2 | 0.9772 | 98% chance $Z$ is below +2. |

**Worked example: chance of landing within one standard deviation.** What's $P(-1 < Z < 1)$?

1. Area left of 1 is $N(1) = 0.8413$.
2. Area left of −1 is $N(-1) = 0.1587$.
3. The area *between* them is the difference: $0.8413 - 0.1587 = 0.6827$.

So about 68% of outcomes land within one standard deviation of the mean. Repeat with 2: $N(2) - N(-2) = 0.9772 - 0.0228 = 0.9545$, about 95%. That's the familiar 68-95 rule.

### Fact 1: symmetry

The bell is a mirror image around 0. So the area to the left of $-x$ equals the area to the right of $+x$. Two useful consequences:

**(a)** $N(-x) = 1 - N(x)$.

Why: the area right of $x$ is $1 - N(x)$ (total area 1 minus the left part). By the mirror, that equals the area left of $-x$, which is $N(-x)$.

Example: $N(-0.35) = 1 - N(0.35) = 1 - 0.6368 = 0.3632$.

**(b)** $P(Z > -x) = N(x)$.

Why: the area right of $-x$ is the mirror image of the area left of $+x$.

Example with $x = 0.15$, done the long way:

1. $P(Z > -0.15) = 1 - P(Z \le -0.15) = 1 - N(-0.15)$
2. $N(-0.15) = 0.4404$
3. $1 - 0.4404 = 0.5596$
4. And $N(0.15) = 0.5596$. ✓

Part 6 uses (b) to get the $N(d_2)$ term in the BSM formula.

### Fact 2: every normal is a stretched, shifted standard normal

If $X = \mu + sZ$ with $Z$ standard normal, then $X$ is normal with mean $\mu$ and standard deviation $s$. Check with the rules $E[a + bZ] = a + b\,E[Z]$ and $\operatorname{Var}(a + bZ) = b^2\operatorname{Var}(Z)$:

- Mean: $E[X] = \mu + s \cdot E[Z] = \mu + s \cdot 0 = \mu$
- Variance: $\operatorname{Var}(X) = s^2 \cdot \operatorname{Var}(Z) = s^2 \cdot 1 = s^2$, so the standard deviation is $s$

Going the other way, any normal $X$ can be converted to a standard normal by **standardizing**: $Z = \frac{X - \mu}{s}$. That counts "how many standard deviations $X$ is from its mean." This is what lets one table of $N(x)$ handle every normal distribution.

**Worked example.** A stock's one-year log return $X$ is normal with mean $\mu = 0.05$ and standard deviation $s = 0.20$. What's the chance the log return is worse than $-0.15$?

1. Write $X$ in terms of $Z$: $X = 0.05 + 0.20\,Z$.
2. Set up the event: $0.05 + 0.20\,Z < -0.15$.
3. Subtract 0.05 from both sides: $0.20\,Z < -0.20$.
4. Divide both sides by 0.20 (positive, so the inequality keeps its direction): $Z < -1$.
5. Look it up: $P(Z < -1) = N(-1) = 0.1587$.

About a 16% chance. Steps 2–4 are exactly what Part 6 does to find when the stock finishes above the strike. There, the number you end up comparing $Z$ against is called $d_2$.

**High level:** the normal distribution says how outcomes spread around their average. $N(x)$ converts "how many standard deviations away" into "how likely." Almost every probability in BSM is computed by standardizing to $Z$ and then reading off $N$.

## 1.4 The lognormal distribution and the $+\tfrac{1}{2}\sigma^2$ term

**The problem.** Section 1.2 said log returns are roughly normal. But options pay off based on the **price**, not the log return. So we need to know what the price distribution looks like, and what the price is worth on average. The answer has a surprise in it: the average price is *higher* than you'd naively expect, by a factor involving $\tfrac12\sigma^2$. That factor shows up all over BSM.

### From normal log returns to lognormal prices

Undo the log (Section 1.2): if the log return over the period is $X$, the price at the end is

$$S_T = S_0\,e^{X}$$

If $X$ is normal, then $e^X$ is called **lognormal**: "its log is normal."

**Worked example.** $S_0 = 100$. The one-year log return $X$ is normal with mean 0.05 and standard deviation 0.20, so $X = 0.05 + 0.20\,Z$ (Section 1.3, Fact 2). Plug in some values of $Z$:

| $Z$ | $X = 0.05 + 0.20Z$ | $S_T = 100\,e^{X}$ |
|---|---|---|
| −2 | $0.05 - 0.40 = -0.35$ | $100 \times 0.7047 = 70.47$ |
| −1 | $0.05 - 0.20 = -0.15$ | $100 \times 0.8607 = 86.07$ |
| 0 | $0.05$ | $100 \times 1.0513 = 105.13$ |
| +1 | $0.05 + 0.20 = 0.25$ | $100 \times 1.2840 = 128.40$ |
| +2 | $0.05 + 0.40 = 0.45$ | $100 \times 1.5683 = 156.83$ |

Look at the gaps. In log-return terms every step is the same size, 0.20. In price terms they're not:

- From $Z = 0$ down to $Z = -1$: $105.13 - 86.07 = 19.06$
- From $Z = 0$ up to $Z = +1$: $128.40 - 105.13 = 23.27$

Equal steps in log returns become **bigger steps going up than going down** in price. That gives two properties:

1. **Prices are never negative.** $e^{\text{anything}} > 0$, so even $Z = -10$ gives a tiny positive price. A stock can lose at most 100%.
2. **Prices are skewed right.** The upside stretches out further than the downside.

### The average price is above the middle price

The middle outcome ($Z = 0$) is the **median**: half the outcomes are below it. Here the median price is $105.13$.

But the **mean** (average) price is higher, because the stretched-out upside pulls the average up. The formula below will give the mean as $107.25$. Before deriving it, here's the effect with just two outcomes.

**Two-outcome example.** Let $Z$ be $+1$ or $-1$ with equal chance. (That has mean 0 and variance 1, like a standard normal.) Take $b = 0.2$ and compute $E[e^{bZ}]$:

1. If $Z = +1$: $e^{0.2} = 1.2214$
2. If $Z = -1$: $e^{-0.2} = 0.8187$
3. Average: $\frac{1.2214 + 0.8187}{2} = \frac{2.0401}{2} = 1.0201$

The average of $bZ$ is 0, and $e^0 = 1$. But the average of $e^{bZ}$ is 1.0201, about **2% higher**. The up outcome gains 0.2214 while the down outcome loses only 0.1813. That's because $e^x$ curves upward (it's **convex**), so it rewards ups more than it punishes downs. Notice $\tfrac12 b^2 = \tfrac12(0.04) = 0.02$, about the size of the bonus. The key result below says that's no coincidence.

### Key result: $E[e^{a+bZ}] = e^{a + b^2/2}$

If $Z \sim \mathcal{N}(0,1)$ and $a, b$ are constants, then

$$E\left[e^{a + bZ}\right] = e^{a + b^2/2}$$

Compare: the average of the exponent is $E[a + bZ] = a$. If you naively plugged in the average you'd get $e^a$. The true answer is bigger by a factor of $e^{b^2/2}$: that's the convexity bonus.

**Check with the two-outcome example:** $a = 0$, $b = 0.2$ gives $e^{0.02} = 1.0202$. The two-point version gave 1.0201. Very close, even though a real normal has many outcomes, not two.

### Derivation, step by step

**Step 1. Write the expectation as an integral.** For a discrete variable, the expected value of $g(Z)$ is $\sum g(z)\,P(Z = z)$: each outcome times its probability, added up. For a continuous variable, the sum becomes an integral and the probability becomes the density $n(z)\,dz$:

$$E[g(Z)] = \int_{-\infty}^{\infty} g(z)\,n(z)\,dz$$

Here $g(z) = e^{a+bz}$ and $n(z) = \frac{1}{\sqrt{2\pi}}e^{-z^2/2}$:

$$E\left[e^{a+bZ}\right] = \int_{-\infty}^{\infty} e^{a+bz}\cdot\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz$$

**Step 2. Tidy up.** Split $e^{a+bz} = e^{a}\,e^{bz}$. $e^a$ doesn't depend on $z$, so it comes outside the integral. Then combine $e^{bz}$ and $e^{-z^2/2}$ by adding exponents ($e^{p}e^{q} = e^{p+q}$):

$$= e^{a}\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{z^2}{2} + bz}\,dz$$

**Step 3. Complete the square in the exponent.** The exponent $-\frac{z^2}{2} + bz$ is almost the exponent of a normal density, just off-center. We want to rewrite it as $-\frac{(z - \text{something})^2}{2}$ plus a constant. Try "something" $= b$ and expand:

$$-\frac{(z-b)^2}{2} = -\frac{z^2 - 2bz + b^2}{2} = -\frac{z^2}{2} + bz - \frac{b^2}{2}$$

That matches our exponent except for an extra $-\frac{b^2}{2}$. Add $\frac{b^2}{2}$ to both sides to cancel it:

$$-\frac{(z-b)^2}{2} + \frac{b^2}{2} = -\frac{z^2}{2} + bz$$

Check with numbers, $b = 0.2$ and $z = 1$. Left side: $-\frac{(0.8)^2}{2} + \frac{0.04}{2} = -0.32 + 0.02 = -0.30$. Right side: $-\frac{1}{2} + 0.2 = -0.30$. ✓

**Step 4. Substitute and pull out the constant.** Replace the exponent, then split $e^{(\ldots) + b^2/2} = e^{(\ldots)}\,e^{b^2/2}$ and move the constant $e^{b^2/2}$ outside:

$$= e^{a}\,e^{b^2/2}\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{(z-b)^2}{2}}\,dz$$

**Step 5. The leftover integral equals 1.** Substitute $u = z - b$. Then $du = dz$, and when $z$ runs from $-\infty$ to $\infty$, so does $u$:

$$\int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{(z-b)^2}{2}}\,dz = \int_{-\infty}^{\infty}\frac{1}{\sqrt{2\pi}}\,e^{-\frac{u^2}{2}}\,du = 1$$

That's the total area under the standard normal bell, which is 1. (In words: it's the same bell, just slid over by $b$, and sliding doesn't change the area.)

**Result:**

$$E\left[e^{a+bZ}\right] = e^{a}\,e^{b^2/2} \cdot 1 = e^{a + b^2/2} \qquad \blacksquare$$

### Back to the stock example

$S_T = 100\,e^{0.05 + 0.20Z}$, so $a = 0.05$ and $b = 0.20$:

1. $\tfrac12 b^2 = \tfrac12 (0.20)^2 = \tfrac12(0.04) = 0.02$
2. $a + \tfrac12 b^2 = 0.05 + 0.02 = 0.07$
3. $E[S_T] = 100\,e^{0.07} = 100 \times 1.0725 = 107.25$

Mean $107.25$ versus median $105.13$. The difference is the convexity bonus.

**High level:** when a quantity is $e^{(\text{something random})}$, its average is bigger than $e^{(\text{average of the something})}$, by the factor $e^{\frac12 \text{variance}}$. Remember the trick (complete the square, recognize a shifted bell, which has area 1). Part 6 uses it twice to derive the BSM formula.

## 1.5 Volatility and the square root of time

**The problem.** Volatility gets quoted per year ("20% vol"), but you trade over a day, a week, or the 3 months until an option expires. How do you convert? The answer is **not** proportional to time. It's proportional to the *square root* of time, and that $\sqrt{T}$ appears in every BSM formula.

**Definition.** **Volatility** $\sigma$ is the standard deviation of log returns, quoted per year. "20% vol" means the one-year log return has standard deviation 0.20.

### Why variances add

Take two days with log returns $r_1$ and $r_2$. The two-day log return is $r_1 + r_2$ (Section 1.2). The variance of a sum is (see `../math/variance_covariance.md`):

$$\operatorname{Var}(r_1 + r_2) = \operatorname{Var}(r_1) + \operatorname{Var}(r_2) + 2\operatorname{Cov}(r_1, r_2)$$

If the days are **independent** (today's move tells you nothing about tomorrow's), the covariance is 0:

$$\operatorname{Var}(r_1 + r_2) = \operatorname{Var}(r_1) + \operatorname{Var}(r_2)$$

The same works for $n$ days. If each day has variance $\sigma_d^2$:

$$\operatorname{Var}(r_1 + \cdots + r_n) = \underbrace{\sigma_d^2 + \cdots + \sigma_d^2}_{n \text{ times}} = n\,\sigma_d^2$$

Standard deviation is the square root of variance. Use $\sqrt{n\,\sigma_d^2} = \sqrt{n}\,\sqrt{\sigma_d^2} = \sqrt{n}\,\sigma_d$:

$$\operatorname{SD}(r_1 + \cdots + r_n) = \sqrt{n}\,\sigma_d$$

**Variance grows in proportion to time. Volatility grows with the square root of time.**

### Worked example: daily vol of 1%

Each day has standard deviation $\sigma_d = 0.01$, so variance $\sigma_d^2 = 0.0001$.

| Horizon | Variance $= n \times 0.0001$ | Std dev $= \sqrt{\text{variance}}$ | Naive guess $n \times 1\%$ |
|---|---|---|---|
| 1 day | 0.0001 | 0.01 = 1% | 1% |
| 4 days | 0.0004 | 0.02 = 2% | 4% |
| 25 days | 0.0025 | 0.05 = 5% | 25% |
| 252 days (1 year) | 0.0252 | 0.1587 = 15.87% | 252% |

Four days of 1% vol is 2%, not 4%. **Why less than the naive guess?** Over several days, some up days and some down days partly cancel. Variance captures that cancelling correctly; adding standard deviations doesn't.

### Converting between daily and annual

There are about 252 trading days in a year, so $n = 252$ and

$$\sigma_{\text{annual}} = \sigma_{\text{daily}}\sqrt{252}, \qquad \sigma_{\text{daily}} = \frac{\sigma_{\text{annual}}}{\sqrt{252}}$$

$\sqrt{252} = 15.87$, roughly 16. Traders call this the **rule of 16**:

- 16% annual vol → $16\% / 16 = 1\%$ typical daily move
- 32% annual vol → $32\% / 16 = 2\%$ typical daily move
- 20% annual vol → $20\% / 15.87 = 1.26\%$ typical daily move

("Typical" here means one standard deviation. About 68% of days are smaller than that, per Section 1.3.)

### Any horizon $T$

Over $T$ years, the log return has variance $\sigma^2 T$ and standard deviation $\sigma\sqrt{T}$. Examples with $\sigma = 20\%$:

| Horizon | $T$ (years) | $\sqrt{T}$ | $\sigma\sqrt{T}$ |
|---|---|---|---|
| 1 day | $1/252$ | 0.0630 | 1.26% |
| 1 month (21 trading days) | $21/252$ | 0.2887 | 5.77% |
| 3 months | 0.25 | 0.5 | 10% |
| 1 year | 1 | 1 | 20% |
| 4 years | 4 | 2 | 40% |

**High level:** $\sigma\sqrt{T}$ is "how far the stock can typically move between now and expiry." Every BSM formula contains it. Doubling the time to expiry doesn't double the possible move; it multiplies it by $\sqrt2 = 1.41$.

## 1.6 Taylor expansions

**The problem.** An option's value $C(S)$ is a complicated function of the stock price. A trader wants a quick answer to: "if the stock moves a little, from $S$ to $S + h$, how much does the option change?" Recomputing the full formula hides the structure. A **Taylor expansion** answers it using only facts known *at the current price*: the value, the slope, and the curvature.

### The idea: approximate a curve with simpler shapes

Zoom in on any smooth curve near a point $x$. Each extra piece of information gives a better local copy:

```text
order 0:  a flat line      "the value doesn't change"         uses f(x)
order 1:  a tangent line   "it changes at the current slope"  uses f(x), f'(x)
order 2:  a parabola       "and the slope itself bends"       uses f(x), f'(x), f''(x)
```

**First order (the tangent line).** Slope means rise per unit of run. Moving a distance $h$ at slope $f'(x)$ rises about $f'(x)\cdot h$:

$$f(x+h) \approx f(x) + f'(x)\,h$$

This misses curvature. If the curve bends upward, the tangent line undershoots.

**Second order (add curvature).** Add a term in $h^2$:

$$f(x+h) \approx f(x) + f'(x)\,h + \tfrac12 f''(x)\,h^2$$

**Where the $\tfrac12$ comes from.** Look for the parabola $p(h) = a + bh + ch^2$ that matches $f$'s value, slope and curvature at $h = 0$:

1. Match the value. $p(0) = a + b\cdot0 + c\cdot0 = a$, so $a = f(x)$.
2. Match the slope. Differentiate: $p'(h) = b + 2ch$. At $h=0$, $p'(0) = b$, so $b = f'(x)$.
3. Match the curvature. Differentiate again: $p''(h) = 2c$. Set $2c = f''(x)$, so $c = \tfrac12 f''(x)$.

The $\tfrac12$ is there because differentiating $h^2$ twice gives $2$, and we have to divide that 2 back out.

**Check on a function we can expand by hand: $f(x) = x^2$.** Algebra gives $(x+h)^2 = x^2 + 2xh + h^2$ exactly. Taylor: $f(x) = x^2$, $f'(x) = 2x$, $f''(x) = 2$, so

$$f(x+h) \approx x^2 + 2x\cdot h + \tfrac12\cdot 2\cdot h^2 = x^2 + 2xh + h^2$$

Identical. For a parabola the second-order expansion is exact, and the $\tfrac12$ is exactly what's needed to make it so.

**The general pattern** continues with higher derivatives. The $n$th term is $\frac{f^{(n)}(x)}{n!}h^n$, where $n! = 1\cdot2\cdots n$ (the $\tfrac12$ above is $\tfrac{1}{2!}$):

$$f(x+h) = f(x) + f'(x)h + \frac{f''(x)}{2!}h^2 + \frac{f'''(x)}{3!}h^3 + \dots$$

**Second-order Taylor expansion** means: stop after the $h^2$ term. When $h$ is small, $h^3$ is much smaller than $h^2$ (if $h = 0.01$, then $h^2 = 0.0001$ and $h^3 = 0.000001$), so the dropped terms barely matter.

### Worked example: $\sqrt{104}$ without a calculator

$f(x) = \sqrt x$, known point $x = 100$, step $h = 4$.

Derivatives, using the power rule $\frac{d}{dx}x^p = p\,x^{p-1}$ with $\sqrt x = x^{1/2}$:

$$f(x) = x^{1/2}, \qquad f'(x) = \tfrac12 x^{-1/2}, \qquad f''(x) = \tfrac12\cdot\left(-\tfrac12\right) x^{-3/2} = -\tfrac14 x^{-3/2}$$

At $x = 100$: $100^{1/2} = 10$ and $100^{3/2} = 10^3 = 1000$, so

$$f(100) = 10, \qquad f'(100) = \tfrac{1}{2\cdot10} = 0.05, \qquad f''(100) = -\tfrac{1}{4\cdot1000} = -0.00025$$

| Order | Computation | Estimate |
|---|---|---|
| 0 | $10$ | 10.000 |
| 1 | $10 + 0.05\times4 = 10 + 0.2$ | 10.200 |
| 2 | $10.2 + \tfrac12(-0.00025)(16) = 10.2 - 0.002$ | 10.198 |
| exact | $\sqrt{104}$ | 10.19804 |

Each order gets closer. The second-order term is negative because $\sqrt x$ bends downward ($f'' < 0$).

### The same thing for an option: delta and gamma

Apply it to the call price as a function of the stock price, holding time fixed. The first derivative of $C$ with respect to $S$ is delta, and the second is gamma (Section 0.1):

$$C(S + h) \approx C(S) + \Delta\,h + \tfrac12\Gamma\,h^2$$

**That's all delta and gamma are: the first two Taylor coefficients of the option price.**

Numbers from the worked example in Part 7: $C = 10.4506$, $\Delta = 0.6368$, $\Gamma = 0.01876$ at $S = 100$.

| Stock moves to | 1st order: $C + \Delta h$ | 2nd order: add $\tfrac12\Gamma h^2$ | Exact BSM |
|---|---|---|---|
| 102 ($h = +2$) | $10.4506 + 0.6368\times2 = 11.7243$ | $+\,\tfrac12(0.01876)(4) = 11.7618$ | 11.7611 |
| 98 ($h = -2$) | $10.4506 - 0.6368\times2 = 9.1769$ | $+\,\tfrac12(0.01876)(4) = 9.2144$ | 9.2151 |

Look at the gamma term: **$+0.0375$ in both cases.** $h^2$ is positive whether the stock goes up or down. If you hedge away the $\Delta h$ part (Part 5 and Part 9), the gamma term is what's left, and a long option makes it on a move in *either* direction. That is the whole reason traders care about gamma.

### Two variables: price and time

An option depends on $S$ and $t$. The two-variable second-order expansion, for a stock move $h$ and a time step $k$, has every first- and second-order combination of $h$ and $k$:

$$C(S+h,\ t+k) \approx C + \frac{\partial C}{\partial S}h + \frac{\partial C}{\partial t}k + \tfrac12\frac{\partial^2C}{\partial S^2}h^2 + \frac{\partial^2C}{\partial S\,\partial t}hk + \tfrac12\frac{\partial^2 C}{\partial t^2}k^2$$

In Greek letters, with the last two terms dropped:

$$C(S+h,\ t+k) \approx C + \Delta\,h + \Theta\,k + \tfrac12\Gamma\,h^2$$

**Why drop $hk$ and $k^2$ but keep $h^2$?** Because of how big a stock move is over a short time. From Section 1.5, the typical move over time $k$ is proportional to $\sqrt{k}$. So $h \sim \sqrt{k}$ (the symbol $\sim$ means "is roughly proportional to"). Then:

| Term | Size | $k = 0.01$ | $k = 0.0001$ |
|---|---|---|---|
| $k$ | $k$ | 0.01 | 0.0001 |
| $h^2$ | $(\sqrt k)^2 = k$ | 0.01 | 0.0001 |
| $hk$ | $\sqrt k \cdot k = k^{3/2}$ | 0.001 | 0.000001 |
| $k^2$ | $k^2$ | 0.0001 | 0.00000001 |

$h^2$ stays the **same size as $k$** however small the step. $hk$ and $k^2$ become a smaller and smaller fraction of $k$: at $k = 0.0001$, $hk$ is 1% of $k$ and $k^2$ is 0.01%. In the limit of tiny steps they vanish. Part 2.2 makes this precise as $(dW)^2 = dt$. Part 3 (Itô's lemma) is exactly this expansion.

---

# Part 2: Randomness Through Time

## 2.1 From a coin-flip walk to Brownian motion

**The problem.** We need a model where the stock price wiggles randomly at every instant, not just once a day. We'll build it from the simplest random process there is: a coin-flip walk.

### Step 1: a coin-flip walk

Start at 0. Each step, flip a coin: heads, move $+1$; tails, move $-1$.

One example path with flips H, H, T, H:

```text
step:      0   1   2   3   4
position:  0   1   2   1   2
```

Each step has mean $\tfrac12(+1) + \tfrac12(-1) = 0$ and variance $\tfrac12(1)^2 + \tfrac12(-1)^2 - 0^2 = 1$. The steps are independent, so variances add (Section 1.5). After 4 steps the position has variance 4 and standard deviation 2.

### Step 2: shrink the steps, keep the variance

We want a walk over a time interval $[0, t]$, with more and more steps packed in. Say $t = 1$ and we take $n$ steps, each lasting $\Delta t = \frac{1}{n}$. How big should each step be?

We want the total variance at time 1 to stay at 1, however many steps we take. With $n$ independent steps each of size $\pm s$, the total variance is $n\,s^2$. Set $n\,s^2 = 1$ and solve: $s = \frac{1}{\sqrt n} = \sqrt{\Delta t}$.

| Steps $n$ | $\Delta t = 1/n$ | Step size $s = \sqrt{\Delta t}$ | Total variance $n s^2$ |
|---|---|---|---|
| 4 | 0.25 | 0.5 | $4 \times 0.25 = 1$ |
| 100 | 0.01 | 0.1 | $100 \times 0.01 = 1$ |
| 10,000 | 0.0001 | 0.01 | $10{,}000 \times 0.0001 = 1$ |

**Why step size $\sqrt{\Delta t}$ and not $\Delta t$?** Try steps of size $\Delta t$ instead. With $n = 100$: total variance $= 100 \times (0.01)^2 = 0.01$. With $n = 10{,}000$: $10{,}000 \times (0.0001)^2 = 0.000001$. The randomness disappears as the steps get finer. Only $\sqrt{\Delta t}$ keeps a fixed amount of randomness per unit of time. **This is where all the square roots in option math come from.**

### Step 3: the limit is Brownian motion

Instead of $\pm$ coin flips, let each step be normal: $\Delta W_i \sim \mathcal{N}(0, \Delta t)$, which means $\Delta W_i = \sqrt{\Delta t}\,Z_i$. (With many steps it barely matters which you use. By the Central Limit Theorem a sum of many small coin flips is approximately normal anyway.) Add up the steps:

$$W_t = \sum_{i=1}^{n}\Delta W_i$$

Let $n \to \infty$. The limit is **Brownian motion** (also called a **Wiener process**), $W_t$. Its defining properties:

1. **Starts at zero:** $W_0 = 0$.
2. **Normal with variance $t$:** $W_t \sim \mathcal{N}(0, t)$, or equivalently $W_t = \sqrt{t}\,Z$.
3. **No memory:** increments over non-overlapping time intervals are independent. Past wiggles say nothing about future ones.
4. **Continuous but jagged:** no jumps, but so wiggly that it has no slope anywhere.

Some numbers. $W_1 \sim \mathcal N(0,1)$, so $P(W_1 > 1) = 1 - N(1) = 1 - 0.8413 = 0.1587$. $W_4 \sim \mathcal N(0, 4)$, standard deviation $\sqrt4 = 2$. Waiting 4 times as long makes the spread twice as big.

We write $dW$ for the increment over an infinitesimally short time $dt$. It has mean 0, variance $dt$, and typical size $\sqrt{dt}$.

### Why $\sqrt{dt}$ matters: noise beats drift over short horizons

For small numbers, $\sqrt{dt}$ is much **bigger** than $dt$. One trading day is $dt = \frac{1}{252} = 0.00397$ years, and $\sqrt{0.00397} = 0.0630$, about 16 times bigger.

Take a stock with expected return $\mu = 10\%$ a year and volatility $\sigma = 20\%$. Drift grows with $T$; noise grows with $\sqrt{T}$:

| Horizon $T$ | Expected drift $\mu T$ | Typical noise $\sigma\sqrt{T}$ | Noise ÷ drift |
|---|---|---|---|
| 1 day ($1/252$) | 0.04% | 1.26% | 32× |
| 1 year | 10% | 20% | 2× |
| 4 years | 40% | 40% | 1× |
| 25 years | 250% | 100% | 0.4× |

**High level:** over a day, the expected return is buried under noise 32 times its size. That's why daily stock charts look like pure randomness, and why (as Part 5 shows) the drift $\mu$ ends up irrelevant to option pricing. Over decades, drift wins.

## 2.2 The surprising rule $(dW)^2 = dt$

**The problem.** In ordinary calculus, $(dx)^2$ is negligible next to $dx$. If $dx = 0.001$, then $(dx)^2 = 0.000001$, and you throw it away. With Brownian motion that fails: $(dW)^2$ is the same size as $dt$. This fact is the one genuinely new rule in stochastic calculus, so let's establish it carefully.

### Compare a smooth path with a Brownian path

Split $[0, 1]$ into $n$ steps of length $\Delta t = \frac1n$ and add up the **squared** step sizes.

**Smooth path, $f(t) = t$.** Each step changes $f$ by exactly $\Delta t$. The sum of squares is

$$\sum_{i=1}^{n}(\Delta t)^2 = n\,(\Delta t)^2 = n \cdot \frac{1}{n^2} = \frac{1}{n}$$

which goes to 0. For $n = 100$ it's 0.01. For $n = 10{,}000$ it's 0.0001.

**Brownian path.** Each step $\Delta W_i$ is about $\sqrt{\Delta t}$ in size, so its square is about $\Delta t$, and adding $n$ of those gives about $n\,\Delta t = 1$. It doesn't go to 0. Let's make that precise.

### The sum of squares $Q$: its mean

Over $[0, t]$, define

$$Q = \sum_{i=1}^{n}(\Delta W_i)^2$$

Each $\Delta W_i$ has mean 0 and variance $\Delta t$. Rearranging the variance formula $\operatorname{Var}(X) = E[X^2] - (E[X])^2$ gives $E[X^2] = \operatorname{Var}(X) + (E[X])^2$. So:

$$E[(\Delta W_i)^2] = \Delta t + 0^2 = \Delta t$$

Expectations add, so adding up $n$ of these:

$$E[Q] = n\,\Delta t = t$$

### Its variance

Write $\Delta W_i = \sqrt{\Delta t}\,Z_i$ with $Z_i$ standard normal. Squaring: $(\Delta W_i)^2 = \Delta t\,Z_i^2$.

First the variance of $Z_i^2$. We need $E[Z^4] = 3$, a standard fact about the normal distribution (it comes from integrating $z^4\,n(z)$ by parts). Then:

$$\operatorname{Var}(Z_i^2) = E[(Z_i^2)^2] - (E[Z_i^2])^2 = E[Z_i^4] - 1^2 = 3 - 1 = 2$$

Next, multiplying a random variable by a constant $c$ multiplies its variance by $c^2$. Here $c = \Delta t$:

$$\operatorname{Var}\big((\Delta W_i)^2\big) = \operatorname{Var}(\Delta t\,Z_i^2) = (\Delta t)^2 \cdot 2$$

The steps are independent, so variances add:

$$\operatorname{Var}(Q) = n \cdot 2(\Delta t)^2 = 2\,(n\,\Delta t)\,\Delta t = 2t\,\Delta t$$

### Plug in numbers ($t = 1$)

| Steps $n$ | $\Delta t$ | $E[Q]$ | $\operatorname{Var}(Q) = 2\Delta t$ | SD of $Q$ | One simulated $Q$ |
|---|---|---|---|---|---|
| 4 | 0.25 | 1 | 0.5 | 0.707 | 0.119 |
| 100 | 0.01 | 1 | 0.02 | 0.141 | 0.963 |
| 10,000 | 0.0001 | 1 | 0.0002 | 0.014 | 0.995 |

(The last column is one random run on a computer. With 4 steps, $Q$ can land far from 1. With 10,000 it's pinned near 1.)

As $\Delta t \to 0$, the variance of $Q$ goes to 0. A random quantity with zero variance isn't random anymore: it equals its mean, $t$.

**Conclusion:** the sum of squared Brownian increments over $[0, t]$ is exactly $t$. In shorthand for one infinitesimal step:

$$\boxed{(dW)^2 = dt}$$

### The multiplication table

We'll meet three kinds of products. Their sizes, using $dW \sim \sqrt{dt}$, with an example where $dt = 0.0001$ (so $\sqrt{dt} = 0.01$):

| Product | Size | Example | Keep it? |
|---|---|---|---|
| $(dt)^2$ | $dt^2$ | 0.00000001 | No: vanishes next to $dt$ |
| $dt\cdot dW$ | $dt^{3/2}$ | 0.000001 | No: vanishes next to $dt$ |
| $(dW)^2$ | $dt$ | 0.0001 | **Yes: it equals $dt$** |

**High level:** randomness that's too small to see in a single step adds up to something definite over many steps. This little table is the whole engine of stochastic calculus.

## 2.3 Geometric Brownian motion (GBM): the BSM stock model

**The problem.** Brownian motion $W_t$ wiggles around 0 and can go negative. A stock price can't, and it should move in *percentage* terms. GBM fixes both.

BSM assumes the stock follows

$$dS = \mu S\,dt + \sigma S\,dW$$

Read it term by term:

- $dS$: change in the stock price over the next instant.
- $\mu S\,dt$: **drift**, the expected part. The stock's expected return is $\mu$ per year, so over $dt$ it expects to gain the fraction $\mu\,dt$ of its price, which is $\mu S\,dt$ in dollars.
- $\sigma S\,dW$: **noise**, the random part. A random shock $dW$, scaled by volatility $\sigma$, and by $S$ so the shock is a *percentage* of the price.

Divide both sides by $S$ to see it in return terms:

$$\frac{dS}{S} = \mu\,dt + \sigma\,dW$$

In words: the return over the next instant = expected return × time + volatility × random shock.

### One day with numbers

$S = 100$, $\mu = 0.10$, $\sigma = 0.20$, one trading day $dt = \frac{1}{252}$. Then $dW = \sqrt{dt}\,Z = 0.0630\,Z$.

- Drift: $\mu S\,dt = 0.10 \times 100 \times \frac{1}{252} = 0.0397$
- Noise: $\sigma S\,dW = 0.20 \times 100 \times 0.0630\,Z = 1.26\,Z$

So tomorrow's price change is $dS = 0.0397 + 1.26\,Z$.

| Random draw | $dS$ | Tomorrow's price |
|---|---|---|
| $Z = +1$ | $0.0397 + 1.26 = 1.30$ | 101.30 |
| $Z = 0$ | $0.0397$ | 100.04 |
| $Z = -1.5$ | $0.0397 - 1.89 = -1.85$ | 98.15 |

Again the drift (4 cents) is tiny next to the noise (\$1.26 per unit of $Z$).

### Why multiply the noise by $S$?

It's called *geometric* because the randomness is proportional to the price. Compare a \$10 stock and a \$1000 stock, both with 20% vol. One day's typical move is $1.26\%$ of the price for each: \$0.126 for the cheap stock and \$12.60 for the expensive one. If we left out the $S$, both would move about \$1.26 a day: a 12.6% daily swing for the \$10 stock and a 0.13% swing for the \$1000 stock. That's not how stocks behave. Percentage moves are what's comparable across stocks.

**High level:** GBM says the stock's *percentage* return is a little predictable drift plus a lot of Brownian noise. Section 3.3 will show this makes the price lognormal, which is the setup from Section 1.4.

---

# Part 3: Itô's Lemma

## 3.1 The problem

An option's value $V$ depends on the stock price $S$ and time $t$: $V = V(S, t)$. We know how $S$ moves (GBM). How does $V$ move?

In ordinary calculus you'd use the chain rule, which keeps only first-order terms. With randomness that gives the wrong answer. Here's a concrete example of it failing.

**Example: $V = S^2$, with no drift.** Take $\mu = 0$, $\sigma = 20\%$, $S = 100$, and one day. From Section 2.3, the stock's typical one-day move is $h = 1.26$. Make it simple: the stock goes up 1.26 or down 1.26 with equal chance.

- Ordinary chain rule: $dV = 2S\,dS$. The average $dS$ is 0, so this predicts an average $dV$ of **0**.
- Actual values: $(100 + 1.26)^2 = 10{,}253.56$ and $(100 - 1.26)^2 = 9{,}749.61$. Their average is $\frac{10{,}253.56 + 9{,}749.61}{2} = 10{,}001.59$. Compared with $100^2 = 10{,}000$, the average change is **+1.59**.

Where does the 1.59 come from? Expand: $(100 \pm h)^2 = 10{,}000 \pm 200h + h^2$. The $\pm 200h$ parts cancel on average. The $h^2$ part doesn't, because it's positive either way: $h^2 = 1.26^2 = 1.59$. The ordinary chain rule throws away $h^2$ as too small. Section 2.2 showed it isn't: $h^2$ is about $\sigma^2S^2\,dt$, the same size as $dt$.

**Itô's lemma** is the Taylor expansion of Section 1.6, keeping that second-order term.

## 3.2 Derivation

**Step 1. Taylor-expand.** Expand $V(S + dS,\ t + dt)$ around $(S, t)$ to second order (Section 1.6, with $h = dS$ and $k = dt$):

$$dV = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial S}dS + \frac{1}{2}\frac{\partial^2 V}{\partial S^2}(dS)^2 + \frac{\partial^2 V}{\partial S\,\partial t}dS\,dt + \frac{1}{2}\frac{\partial^2 V}{\partial t^2}(dt)^2 + \dots$$

Now decide which terms survive, using the multiplication table from Section 2.2.

**Step 2. Compute $(dS)^2$.** Substitute $dS = \mu S\,dt + \sigma S\,dW$ and expand with $(a + b)^2 = a^2 + 2ab + b^2$, where $a = \mu S\,dt$ and $b = \sigma S\,dW$:

$$(dS)^2 = \underbrace{\mu^2S^2(dt)^2}_{a^2} + \underbrace{2\mu\sigma S^2\,dt\,dW}_{2ab} + \underbrace{\sigma^2S^2(dW)^2}_{b^2}$$

Apply the table: $(dt)^2 \to 0$, $dt\,dW \to 0$, $(dW)^2 = dt$. Only the last term survives:

$$(dS)^2 = \sigma^2 S^2\,dt$$

**Check with one-day numbers** ($S = 100$, $\mu = 0.10$, $\sigma = 0.20$, from Section 2.3: $a \approx 0.0397$, $b \approx 1.26$ for a one-standard-deviation day):

| Piece | Value |
|---|---|
| $a^2 = (0.0397)^2$ | 0.0016 |
| $2ab = 2(0.0397)(1.26)$ | 0.1000 |
| $b^2 = (1.26)^2$ | 1.5873 |

Even over a whole day, $b^2$ is 94% of the total. Over shorter steps, the other two shrink away completely. And $\sigma^2S^2\,dt = 0.04 \times 10{,}000 \times \frac{1}{252} = 1.5873$, matching $b^2$.

**Step 3. The remaining terms.** $dS\,dt$ is $(\mu S\,dt + \sigma S\,dW)\,dt = \mu S\,(dt)^2 + \sigma S\,dt\,dW$. Both pieces vanish. $(dt)^2$ vanishes. Higher-order terms are smaller still.

**Step 4. Keep what survives.** Replace $(dS)^2$ with $\sigma^2S^2\,dt$:

$$\boxed{dV = \frac{\partial V}{\partial t}dt + \frac{\partial V}{\partial S}dS + \frac{1}{2}\sigma^2S^2\frac{\partial^2 V}{\partial S^2}dt}$$

That is **Itô's lemma** for a function of a GBM. Compared with ordinary calculus, the only new thing is the last term.

### Check it on $V = S^2$

Derivatives: $\frac{\partial V}{\partial t} = 0$ (no $t$ in it), $\frac{\partial V}{\partial S} = 2S$, $\frac{\partial^2 V}{\partial S^2} = 2$. Plug into Itô:

$$dV = 0 + 2S\,dS + \tfrac12\sigma^2S^2 \cdot 2\,dt = 2S\,dS + \sigma^2S^2\,dt$$

With $\mu = 0$ the average $dS$ is 0, so the average $dV$ is $\sigma^2S^2\,dt = 0.04 \times 10{,}000 \times \frac{1}{252} = 1.59$. That's exactly the +1.59 from the up/down example in 3.1. ✓

**High level:** curvature in $V$ (a nonzero second derivative) combined with randomness in $S$ produces a *predictable* drift in $V$, of size $\frac12\sigma^2S^2\frac{\partial^2V}{\partial S^2}$ per unit time. It's the same convexity effect as the $+\tfrac12 b^2$ in Section 1.4. For an option, $\frac{\partial^2V}{\partial S^2}$ is gamma, and this term becomes the gamma profit in Part 9.

## 3.3 Application: solving GBM, and volatility drag

**The problem.** GBM, $dS = \mu S\,dt + \sigma S\,dW$, tells us how $S$ changes each instant. We want a formula for $S_T$ itself, the price at expiry. The trick is to look at $\ln S$ instead of $S$.

### Step 1: Itô on $\ln S$

Let $f(S) = \ln S$. Its derivatives:

$$\frac{\partial f}{\partial t} = 0, \qquad \frac{\partial f}{\partial S} = \frac{1}{S}, \qquad \frac{\partial^2 f}{\partial S^2} = \frac{d}{dS}\left(S^{-1}\right) = -S^{-2} = -\frac{1}{S^2}$$

Plug these into Itô's lemma:

$$d(\ln S) = 0\cdot dt + \frac{1}{S}\,dS + \frac{1}{2}\sigma^2S^2\left(-\frac{1}{S^2}\right)dt$$

In the last term $S^2 \cdot \frac{1}{S^2} = 1$:

$$d(\ln S) = \frac{dS}{S} - \frac{1}{2}\sigma^2\,dt$$

Substitute GBM in return form, $\frac{dS}{S} = \mu\,dt + \sigma\,dW$:

$$d(\ln S) = \mu\,dt + \sigma\,dW - \frac{1}{2}\sigma^2\,dt$$

Group the $dt$ terms:

$$d(\ln S) = \left(\mu - \tfrac{1}{2}\sigma^2\right)dt + \sigma\,dW$$

### Step 2: add up from 0 to $T$

The right side has constant coefficients, so adding it up over $[0, T]$ is easy:

- The left side: adding up all the little changes in $\ln S$ gives the total change, $\ln S_T - \ln S_0$. (The same telescoping as in Section 1.2: every middle value cancels.)
- $\left(\mu - \tfrac12\sigma^2\right)dt$ adds up to $\left(\mu - \tfrac12\sigma^2\right)T$, because the $dt$'s add up to $T$.
- $\sigma\,dW$ adds up to $\sigma W_T$, because the Brownian steps add up to $W_T - W_0 = W_T$.

$$\ln S_T - \ln S_0 = \left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma W_T$$

### Step 3: solve for $S_T$

Replace $W_T$ with $\sqrt{T}\,Z$ (Section 2.1). Add $\ln S_0$ to both sides, then exponentiate. On the right, $e^{\ln S_0 + (\ldots)} = S_0\,e^{(\ldots)}$:

$$\boxed{S_T = S_0\exp\!\left[\left(\mu - \tfrac{1}{2}\sigma^2\right)T + \sigma\sqrt{T}\,Z\right]}$$

($\exp[x]$ is just another way to write $e^x$, easier to read when $x$ is long.)

**What this says:** the log return over $[0, T]$ is normal, with mean $\left(\mu - \tfrac12\sigma^2\right)T$ and standard deviation $\sigma\sqrt{T}$. So the price is lognormal, exactly the setup of Section 1.4.

### Step 4: numbers

$S_0 = 100$, $\mu = 0.10$, $\sigma = 0.20$, $T = 1$.

1. $\tfrac12\sigma^2 = \tfrac12(0.04) = 0.02$
2. Mean log return: $\mu - \tfrac12\sigma^2 = 0.10 - 0.02 = 0.08$
3. Standard deviation of log return: $\sigma\sqrt T = 0.20$

So $S_T = 100\,e^{0.08 + 0.20Z}$.

- **Median** price (the $Z = 0$ outcome, since $e^x$ keeps order): $100\,e^{0.08} = 108.33$.
- **Mean** price, using Section 1.4 with $a = 0.08$ and $b = 0.20$: $a + \tfrac12 b^2 = 0.08 + 0.02 = 0.10$, so $E[S_T] = 100\,e^{0.10} = 110.52$.

**Sanity check, in general.** With $a = \left(\mu - \tfrac12\sigma^2\right)T$ and $b = \sigma\sqrt T$:

$$a + \tfrac12 b^2 = \mu T - \tfrac12\sigma^2T + \tfrac12\sigma^2T = \mu T$$

So $E[S_T] = S_0\,e^{\mu T}$. The *average* price grows at the expected return $\mu$, as GBM intended. The $-\tfrac12\sigma^2$ from Itô and the $+\tfrac12 b^2$ convexity bonus cancel exactly.

### Volatility drag

The mean price grows at $\mu$, but the *median*, the typical outcome, grows at only $\mu - \tfrac12\sigma^2$. The gap $\tfrac12\sigma^2$ is called **volatility drag**:

| Volatility $\sigma$ | Drag $\tfrac12\sigma^2$ per year |
|---|---|
| 20% | 2% |
| 40% | 8% |
| 80% | 32% |

**Check with the example from Section 1.2.** The stock goes up 10%, then down 10%, ending at 99. In log terms that's $\ln(1.10) + \ln(0.90) = 0.09531 - 0.10536 = -0.01005$. Now use the drag formula: the per-day returns are $\pm 0.10$, so per-day $\sigma = 0.10$, and drag per day is $\tfrac12(0.10)^2 = 0.005$. Over two days, that's $2 \times 0.005 = 0.010$ of lost log return. The formula predicts $-0.0100$; the actual answer is $-0.01005$. ✓ (The tiny gap is the higher-order terms the formula drops.) The average simple return was zero, but volatility alone cost 1%.

**High level:** volatility costs compounded growth. The more a price swings, the further its typical path falls behind its average. Sinclair returns to this when he discusses leveraged ETFs (Ch. 13 in the 2nd edition), where daily rebalancing makes the drag severe.

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

Use an **indicator** $\mathbf 1_{\lbrace S_T > K\rbrace }$, which equals 1 if $S_T > K$ and 0 otherwise. Then

$$\max(S_T - K, 0) = (S_T - K)\,\mathbf 1_{\lbrace S_T > K\rbrace } = S_T\mathbf 1_{\lbrace S_T > K\rbrace } - K\,\mathbf 1_{\lbrace S_T > K\rbrace }$$

Take expectations. Expectation is linear, and $E[\mathbf 1_A] = P(A)$:

$$E^{\mathbb Q}[\max(S_T-K,0)] = \underbrace{E^{\mathbb Q}\!\left[S_T\,\mathbf 1_{\lbrace S_T>K\rbrace }\right]}_{\text{Piece A}} - K\,\underbrace{P^{\mathbb Q}(S_T > K)}_{\text{Piece B}}$$

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

$$E^{\mathbb Q}\!\left[S_T\,\mathbf 1_{\lbrace S_T>K\rbrace }\right] = \int_{-d_2}^{\infty} S_0\exp\!\left[\left(r-\tfrac12\sigma^2\right)T + \sigma\sqrt T z\right]\frac{1}{\sqrt{2\pi}}e^{-z^2/2}\,dz$$

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

$$E^{\mathbb Q}\!\left[S_T\,\mathbf 1_{\lbrace S_T>K\rbrace }\right] = S_0e^{rT}N(d_1)$$

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

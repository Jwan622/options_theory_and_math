# options_theory_and_math

Personal study notes for learning options theory (Black-Scholes-Merton, volatility trading) and the math underneath it. The reader has taken calculus and statistics but wants every idea built up slowly. The main companion text is Euan Sinclair, *Volatility Trading* (2nd ed., Wiley, 2013).

## Layout

```text
math/             general math and statistics lessons (variance, correlation, e and ln, Taylor series, ...)
options_theory/   options-specific lessons (bsm_primer.md, ...)
scripts/          tooling (check_math.py: markup checker for lessons)
```

- One lesson per Markdown file, named in `snake_case.md`.
- Cross-link related lessons with relative links, e.g. `../math/taylor_series.md` from `options_theory/`.
- When a math lesson has an options application, end it with a section tying it to `options_theory/bsm_primer.md`, and vice versa.

## How to write math in this repo

The reader's main complaint about textbooks is skipped steps. These rules exist to prevent that. Follow them for every lesson and every edit.

### 1. Motivate before you formalize

Open each concept with **the problem** it solves, in plain words, before any notation. The reader should know why they're about to see an equation before they see it.

### 2. Concrete before abstract

Show a small numeric example first, then the pattern, then the general formula. Example: compound \$1 monthly for a year in a table, *then* write $\left(1 + \frac{r}{n}\right)^n$.

### 3. Define every term and symbol before using it

Never assume the reader knows a word, symbol or Greek letter. If a symbol has two meanings (e.g. $\Delta$ as "change in" vs. the Greek delta), say so explicitly.

### 4. One step per line, with the reason

In a derivation, each line does one thing, and the text says what and why:

```text
Bad:   x + 4 = 10  →  x = 6

Good:  x + 4 = 10
       Subtract 4 from both sides:
       x + 4 - 4 = 10 - 4
       x = 6
```

- Name the rule being used ("use $\ln(ab) = \ln a + \ln b$", "expand $(a+b)^2 = a^2 + 2ab + b^2$", "divide by $\sigma\sqrt T$, which is positive, so the inequality keeps its direction").
- Never write "it can be shown", "clearly", "obviously" or "after some algebra". Show it.
- When a step uses a fact from elsewhere, point to it ("from Section 1.4", "see `variance_covariance.md`").
- If a fact genuinely can't be proved at this level (e.g. $E[Z^4] = 3$), say that it's being taken as given and where it comes from.

### 5. Plug in numbers, step by step

After a formula, work at least one example with real numbers, showing each intermediate value. Number the steps when there are several. Use tables when comparing several inputs.

### 6. Check results

- Verify a derived formula numerically whenever possible ("check: $90.48 \times e^{0.10} = 100.00$ ✓").
- Compute every number in a lesson with a script (e.g. a short Python one-off in a scratch directory) before writing it down. Don't do arithmetic in your head.
- Reuse running examples across lessons so numbers can be cross-checked. The standard option example is $S = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$: $C = 10.4506$, $P = 5.5735$, $\Delta = 0.6368$, $\Gamma = 0.01876$, vega $= 37.52$ per 1.00 vol, $\Theta = -6.414$ per year.

### 7. Say what it means

End each concept with a short **High level:** paragraph: what the result says in plain words, and why a trader would care.

### 8. Every number must be traceable

The reader should be able to recompute any number on the page from things shown earlier. If they can't see where a number came from, a step is missing, even if the math is correct.

- Before using a rule to produce numbers, derive the rule. Example: before showing $1.5^2 = 2.25$ for semiannual compounding, show that paying interest at rate $i$ turns balance $B$ into $B + Bi = B(1 + i)$, so each period multiplies by $(1 + i)$.
- When a process runs over several periods, track it in a table with one row per period: starting value, what changed and why, ending value.
- Write every case in the same form, even the trivial one, so the pattern is visible. Write $\left(1 + \frac11\right)^1 = 2$, not just $1 \times 2 = 2$, when the next cases are $\left(1 + \frac12\right)^2$ and $\left(1 + \frac14\right)^4$.

### 9. Read formulas term by term

When a formula appears (especially one quoted from a book), go through it piece by piece: what each symbol is, its units, and its sign.

- **Explain every sign.** Readers get stuck on "why is that a minus?" Say why: e.g. in $C - \Delta S$ the minus is there because the position is *short* $\Delta$ shares.
- Use underbraces or a table to label the parts of a long expression, e.g. option change / short-stock change / financing.
- Spell out notation the first time it appears: $\sum$, $\lim$, $k!$, $\exp[\cdot]$, $\sim$, $\partial$, $E[\cdot]$, $\operatorname{Var}$.
- Say what the time step and units are: per year vs. per day, $\Delta t = 1/252$, vol points vs. decimals.
- When a book writes something compressed (drops a $\Delta t$, writes $C(S_{t+1})$ for $C(S_{t+1}, t+\Delta t)$), say what the full version is.

### 10. Toy cases before the general case

- Show a two-outcome version before a continuous one (e.g. $Z = \pm1$ before a normal $Z$, a one-step binomial tree before Black-Scholes).
- After an algebraic identity, check it with one set of numbers (e.g. completing the square: plug in $b = 0.2$, $z = 1$, and confirm both sides give $-0.30$).

### 11. Approximations: say what's dropped, how big it is, and where it breaks

- Name the terms being dropped and show their size with numbers (a table of $k$, $h^2$, $hk$, $k^2$ for shrinking $k$ works well).
- Compare the approximation with the exact value in a table.
- Include a case where the approximation fails (e.g. a delta-gamma estimate for a \$20 move), so the reader knows its limits.

### 12. Integration by parts, substitutions and other techniques

State the rule first, then the specific choices, then check them. For integration by parts: write $\int u\,dv = [uv] - \int v\,du$, give $u$, $du$, $dv$ and $v$ explicitly, and verify $\frac{dv}{ds}$ by differentiating. For a substitution, say what changes in the limits.

### 13. Build every tool from small cases before stating it

Don't hand the reader a general theorem or formula and then use it. Do the small cases by hand first, find the pattern, then state the general version.

- Example: before the binomial theorem, multiply out $(1+y)^2$ and $(1+y)^3$ line by line, and explain where the coefficients 1, 3, 3, 1 come from (counting ways to pick brackets).
- Derive formulas by the reasoning that produces them, not by notation. Example: get $\binom{n}{k} = \frac{n(n-1)\cdots(n-k+1)}{k!}$ by counting ordered picks and dividing out the double counting, checked by listing all six pairs for $\binom42$.
- Use the lightest form that does the job. If only the product form of $\binom nk$ is needed, don't introduce $\frac{n!}{k!(n-k)!}$ as well.

### 14. One new thing at a time, with a plan for long arguments

- Introduce one concept, symbol or technique per paragraph. Don't define a notation and use it inside a formula in the same sentence.
- Before a multi-step proof, say the plan in a sentence or two ("multiply it out into pieces, then watch each piece as $n$ grows").
- Split long sections into numbered subsections (3.1, 3.2, …) so each has one job.
- Do each general derivation once with numbers first, then repeat the identical steps with symbols, using the same step numbers.

### 15. Close the loop

When a new tool is built, use it to reproduce a number the reader already saw. Example: the binomial expansion of $\left(1 + \frac14\right)^4$ adds up to 2.4414, the same as the quarterly compounding table. That's what convinces the reader the tool is right and connects it to what they know.

### 16. Lesson shape

For a substantial lesson: Learning Goal → sections (problem → example → derivation → numbers → high level) → connection to options → Recap → Check Your Understanding (questions with answers right below) → Vocabulary.

## When the reader is confused

- If the reader says they don't understand a passage, find the specific missing step: usually an unexplained number, sign, or rule. Rewrite that section of the lesson file itself; don't only answer in chat. Then commit and push.
- If they quote a passage from Sinclair or another book, explain it line by line, map the book's notation onto this repo's notation, and add the explanation to the relevant lesson.
- If they paste text copied from a rendered page, expect it to look garbled: rendered math copies as doubled or split-up characters, which isn't a rendering bug. Raw `$...$` in the paste *is* a real failure. Find that exact span in the file and fix it (rephrase, shorten, or move it to display math), even if no rule explains why it failed. If you spot a new pattern, add it to the formatting rules below and to `scripts/check_math.py`.
- When the reader says a passage is unclear, the fix is usually more structure (numbered subsections, a plan, small cases first, a table) rather than more words.
- Keep changes scoped to what was asked, and keep the running examples consistent across files.

## Markdown and LaTeX formatting rules

Lessons use GitHub-flavored Markdown with LaTeX math. These rules keep the math rendering in GitHub, VS Code and the Claude app's file panel.

- Inline math: `$...$`. Display math: `$$...$$` on its own line, with blank lines around it.
- **Never put `$` math directly next to a quote mark.** `"$S$"` renders as raw text in some viewers. Rephrase instead.
- Literal dollar amounts are written `\$100`. Never write `\$$x$` (an escaped dollar touching math): use "an amount $X$" instead.
- Use `\lbrace` / `\rbrace` rather than `\{` / `\}` inside math.
- **Keep inline math short** (a symbol or a short expression). Anything with nested fractions, factorials of expressions like $(n-k)!$, sums or several operators goes in display math on its own line. Long or dense inline spans are the ones that have shown up as raw `$...$` in the Claude app's file panel.
- Say "read as k factorial", not `read "$k$ factorial"`: no quote marks around math.
- Prefer tables and numbered steps over paragraphs that pack several formulas into one sentence.
- Code blocks tagged `text` are fine for ASCII diagrams and short pseudo-calculations.
- **Run `python3 scripts/check_math.py` after every edit.** It checks for unbalanced `$$` and inline `$`, math touching quote marks, `\$$`, and `\{`. Fix everything it reports before committing.

## Workflow

- Before committing, run `python3 scripts/check_math.py` and verify any new numbers with a script.
- When you finish a change, commit and push to `main` on GitHub (`origin`). The owner has asked for this as standing practice.
- End commit messages with the attribution line the harness provides.

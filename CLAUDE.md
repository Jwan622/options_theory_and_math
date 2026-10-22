# options_theory_and_math

Personal study notes for learning options theory (Black-Scholes-Merton, volatility trading) and the math underneath it. The companion text is Euan Sinclair, *Volatility Trading* (2nd ed., Wiley, 2013).

## Layout

```text
math/             general math and statistics lessons (variance, correlation, e and ln, Taylor series, ...)
options_theory/   options-specific lessons (bsm_primer.md, ...)
scripts/          check_math.py: markup checker for lessons
```

- One lesson per Markdown file, named in `snake_case.md`.
- Cross-link related lessons with relative links (e.g. `../math/taylor_series.md`). A math lesson with an options use ends with a section tying it to `options_theory/bsm_primer.md`, and vice versa.

## The reader

They've taken calculus and statistics, but textbooks lose them because steps get skipped. They read slowly and stop at the first thing they can't reconstruct. Corrections they've made so far show where explanations break:

| What they asked | What was missing |
|---|---|
| "Is that a minus sign? Why?" (in $C - \Delta S$) | The reason for a sign |
| "What's the upside-down L? What's a Taylor expansion?" | A symbol and a concept used before being defined |
| "Where do the numbers come from?" (1.5, 1.25 in compounding) | The rule that produces the numbers, $B(1+i)$ |
| "Isn't $100\%/n$ a percent, not a decimal?" | A unit conversion that felt too trivial to show |
| "Two different formulas here: add interest, or multiply by $1 + \frac1n$?" | Showing that two forms are the same thing |
| "Write this clearer" (binomial theorem) | Structure: a plan, small cases first, one idea per subsection |
| "I see dollar-sign stuff" | Math that didn't render |

Expect more of the same. Each one is a missing step, not a wrong result.

## How to teach the math

### Before the math

1. **Start with the problem.** Say in plain words what question the concept answers before any notation.
2. **Give the plan** before a multi-step argument, in a sentence or two ("multiply it out into pieces, then watch each piece as $n$ grows").
3. **Define every word, symbol and Greek letter before it's used.** Spell out notation the first time it appears: $\sum$, $\lim$, $k!$, $\exp[\cdot]$, $\sim$, $\partial$, $E[\cdot]$, $\operatorname{Var}$. Flag symbols with two meanings (e.g. $\Delta$ as "change in" vs. the Greek delta).
4. **One new thing at a time.** One concept, symbol or technique per paragraph. Split long sections into numbered subsections (3.1, 3.2, …), each with one job.

### Building it up

5. **Small cases, then the pattern, then the general rule.** Never hand over a theorem and then use it. Example: multiply out $(1+y)^2$ and $(1+y)^3$ by hand, explain the coefficients 1, 3, 3, 1, and only then state the binomial theorem.
6. **Two-outcome toy versions before continuous ones**: $Z = \pm1$ before a normal $Z$, a one-step binomial tree before Black-Scholes.
7. **Derive a rule before using it to make numbers**, by the reasoning that produces it. Examples: show $B + Bi = B(1+i)$ before compounding with 1.5; get $\binom nk$ by counting ordered picks and dividing out double counting. Use the lightest form that does the job.
8. **Numbers first, then symbols.** Do a derivation once with real numbers, then repeat the identical steps in symbols with the same step numbers.

### Every step

9. **One step per line, with the reason.** Name the rule, e.g. use the log rule $\ln(ab) = \ln a + \ln b$, or divide by $\sigma\sqrt T$, which is positive, so the inequality keeps its direction. Never write "clearly", "it can be shown" or "after some algebra".

   ```text
   Bad:   x + 4 = 10  →  x = 6

   Good:  x + 4 = 10
          Subtract 4 from both sides:
          x + 4 - 4 = 10 - 4
          x = 6
   ```

10. **No step is too small to show.** Percent to decimal ($100\% = \frac{100}{100} = 1$), $e^{-x} = \frac{1}{e^x}$, factoring out a common term: if it changes the form of something, show it.
11. **Explain every sign and unit.** Why is it a minus? Per year or per day? Decimal or vol points? What is $\Delta t$?
12. **When two forms are equivalent, show they're equal, side by side.** E.g. a table with an add column (start + interest) and a multiply column (start × $(1+i)$) that match row by row.
13. **Read formulas term by term**, especially ones quoted from a book. Label the parts (underbraces or a table), and when the book compresses something (drops a $\Delta t$, writes $C(S_{t+1})$ for $C(S_{t+1}, t + \Delta t)$), give the full version.
14. **Techniques: state the rule, then the choices, then check them.** For integration by parts, write $\int u\,dv = [uv] - \int v\,du$, give $u$, $du$, $dv$, $v$, and differentiate $v$ to verify. For a substitution, say what happens to the limits.
15. **Point to where facts come from** ("from Section 1.4", "see `variance_covariance.md`"). If something can't be proved at this level (e.g. $E[Z^4] = 3$), say it's taken as given.

### Numbers

16. **Every number must be traceable.** The reader should be able to recompute any number from what's shown above it.
17. **Track multi-period processes in a table**, one row per period: start, what changed and why, end.
18. **Write every case in the same form**, including the trivial one: $\left(1 + \frac11\right)^1 = 2$ alongside $\left(1 + \frac12\right)^2$ and $\left(1 + \frac14\right)^4$.
19. **Check results numerically.** After an identity, plug in one set of numbers. After a formula, verify it (e.g. $90.48 \times e^{0.10} = 100.00$ ✓). Compute every number with a script, never in your head.
20. **Close the loop.** Use each new tool to reproduce a number the reader already saw (the binomial expansion of $\left(1 + \frac14\right)^4$ gives 2.4414, matching the compounding table).
21. **Reuse the running example** so numbers cross-check between files: $S = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ gives $C = 10.4506$, $P = 5.5735$, $\Delta = 0.6368$, $\Gamma = 0.01876$, vega $= 37.52$ per 1.00 vol, $\Theta = -6.414$ per year.

### After the math

22. **Say what it means.** End each concept with a short **High level:** paragraph in plain words, saying why a trader would care.
23. **For approximations**, name what's dropped and show its size with numbers, compare with the exact value in a table, and include a case where it breaks (e.g. delta-gamma for a \$20 move).
24. **Lesson shape:** Learning Goal → sections (problem → example → derivation → numbers → high level) → connection to options → Recap → Check Your Understanding (answers right below each question) → Vocabulary.

## When the reader is confused

- Find the specific missing step (usually an unexplained number, sign, conversion or rule) and **fix the lesson file itself**, not just the chat. Then commit and push.
- If a passage is unclear overall, the fix is usually **more structure** (a plan, numbered subsections, small cases first, a table), not more words.
- If they quote Sinclair or another book, explain it line by line, map its notation onto this repo's, and add the explanation to the relevant lesson.
- Text pasted from a rendered page always looks garbled (math copies as doubled or split-up characters), which is not a bug. But raw `$...$` in a paste **is** a real rendering failure: find that exact span and fix it, even if no rule explains it, and record any new pattern below and in `scripts/check_math.py`.
- Keep changes scoped to what was asked.

## Markdown and LaTeX formatting

Lessons must render in GitHub, VS Code and the Claude app's file panel.

- Inline math `$...$`; display math `$$...$$` on its own line with blank lines around it.
- **Keep inline math short.** Anything with nested fractions, factorials of expressions like $(n-k)!$, sums, or several operators goes in display math. Dense inline spans are what have rendered as raw `$...$` in the file panel.
- **No quote marks touching math.** Write "read as k factorial", not `read "$k$ factorial"`.
- Literal dollars: `\$100`. Never `\$$x$`; write `an amount $X$` instead.
- `\lbrace` / `\rbrace`, not `\{` / `\}`.
- Prefer tables and numbered steps over sentences packed with formulas. `text` code blocks are fine for ASCII diagrams.

## Workflow

1. Verify every new number with a script.
2. Run `python3 scripts/check_math.py` and fix everything it reports.
3. Commit and push to `main` on GitHub (`origin`) when a change is done. The owner wants this every time, without asking.

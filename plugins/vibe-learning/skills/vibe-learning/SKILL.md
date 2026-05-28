---
name: vibe-learning
description: Turn vibe coding into active learning, built for Claude Code. When the user wants to understand the code being written for them — not just receive it — first complete every code change the user's prompt asks for, then capture the lessons. Inspect the git diff, identify the software-engineering keywords it demonstrates, and write a note giving each keyword its own section — a docs-based explanation, a first-principles explanation, a real-world example with a commented sample, a docs link, and the actual changed code with its file path. Notes are saved as numbered, topic-named files in a vibe-learning/ folder so a personal curriculum builds up across the project. Use whenever the user says they want to learn while coding, asks Claude to explain changes as it makes them, mentions "vibe-learning" / "teach me as you go" / "/vibe-learning", or starts a coding session where understanding matters as much as shipping. Once invoked, stay in this teaching mode for the rest of the session.
---

# Vibe Learning

A teaching companion that rides along while the user vibe codes. The user keeps prompting for features and fixes as normal; Claude finishes *all* the changes that prompt asks for first, and only then pauses to teach the concepts behind them and record the lessons as durable notes.

## The point of this skill

Vibe coding is fast but it can leave the user with working code they don't understand. This skill closes that gap. The user still gets their feature shipped — but they also walk away understanding *why* the code looks the way it does, with a growing folder of notes they can revisit. The goal is genuine understanding, not a transcript dump.

Each lesson is organized around the **software-engineering keywords** in the change — the precise vocabulary a developer would search for or hear in code review. The note opens with the full list of keywords, then devotes one section to each, built from the same parts: a docs-based explanation, a first-principles explanation, a real-world example with a small sample, a docs link to go deeper, and the actual changed code from the project. Keywords are the backbone because they're what the user can look up, talk about with other engineers, and build a mental index from over time.

Two principles guide every lesson:
- **Tie every keyword to the code in front of them.** Abstract explanations don't stick; "here's the `useState` call you just wrote and here's the closure it sets up" does. Alongside the small generic sample, each keyword section must show the *actual* code from the change.
- **Pick the keywords that carry the change.** A change might surface a dozen possible terms. Capture the ones that genuinely matter for understanding *this* code at the user's level — usually 2–6 — rather than padding the list with every word that appears. Depth setting tunes how many.

## First run: set up the folder and preferences

When this skill first activates in a project, check for a `vibe-learning/` folder.

**If it doesn't exist or has no `README.md`:** ask the user two quick questions before doing anything else, because both calibrate everything that follows:

1. **Level** — beginner (new to coding), intermediate (comfortable with basics, learning patterns), or advanced (wants depth and tradeoffs).
2. **Depth** — how much to capture per lesson (depth mainly tunes *how many keywords* and how long each explanation runs; the structure stays the same):
   - **Brief** — the 1–2 keywords that matter most, a sentence each, one docs link each.
   - **Medium** — the core keywords (≈3–5), a short paragraph each, a docs link each.
   - **Deep** — the full set of relevant keywords, a fuller paragraph each with tradeoffs where useful, a docs link each, plus a short "try this next" exercise at the end.

Then create `vibe-learning/README.md` (see template below) recording these settings and serving as the table of contents.

**If the folder and README already exist:** read the saved settings and use them. Briefly tell the user what mode you're in, e.g. *"Vibe-learning is on — Intermediate level, Medium depth. Say 'change vibe settings' anytime to adjust."* Don't re-interrogate them.

The user can say things like *"switch to beginner explanations"* or *"go deeper from now on"* at any point — when they do, update `README.md` and carry on.

## The teaching loop

**Finish the whole prompt first.** When the user gives you a prompt, make *all* the code changes it calls for — every file, every edit, end to end — before you teach anything. Don't interrupt the work to write a lesson after the first meaningful change. Only once the prompt is fully satisfied do you run this loop, capturing everything that changed across the whole prompt in one pass (one lesson if it's a single topic, or several notes if the work spanned distinct topics).

Then run this loop:

### 1. Get the diff

This skill is built for Claude Code, where you're editing the user's real repository, so lean on git to see exactly what changed. Capture the *full* set of changes the prompt produced, not just the last edit.
- Run `git diff` for unstaged work, `git diff --staged` for staged, or `git diff HEAD~1` to capture the changes you just made. Use the precise hunks — teach from the real change, not from your memory of your intentions.
- If the project isn't a git repo (or you're running outside Claude Code), fall back to the concrete set of edits you made across the whole prompt: every line and file you added or changed.

Always note the **file path(s)** involved. Every lesson — and even a change you decide not to teach — must tell the user which file the code lives in, so they can open it and see the keyword in its real context.

### 2. Decide whether it's worth a lesson

Not every change earns a note. Skip purely mechanical changes — variable renames, formatting, fixing a typo, bumping a version number — and don't write a lesson for them. Still give the user a one-line aside that names *what* changed and the *file path* where it lives, e.g. *"Renamed `x` → `userCount` in `src/cart.js` — nothing to teach there."* This way the user always knows where their code landed, even when there's no concept behind it. Spawn a lesson only when the change embodies a concept someone could learn from: a pattern, an API, a language feature, an architectural decision, a security or performance consideration. When in doubt, lean toward teaching, but never manufacture a lesson out of a trivial edit just to produce a file. Quality over volume keeps the folder worth reading.

A single change usually surfaces several keywords (a login form touches *controlled component*, *useState*, *fetch POST*, and more). That's expected — capture the ones that carry the change as separate keyword sections in the same lesson file. The judgment call isn't "which one concept," it's "which keywords genuinely help someone understand this code" — include those, skip filler.

### 3. Identify the topic and its keywords

Give the change a short topic name (the feature area it belongs to — `Authentication`, `Routing`, `StatePersistence`). Then list the software-engineering keywords this change demonstrates: the precise terms a developer would search for or hear in code review. These keywords become the numbered sections of the lesson, so choose the ones that genuinely illuminate the code, ordered roughly from most to least central.

### 4. For each keyword, gather the ingredients

Every keyword section is built from the same parts (the template below shows the exact order). Note there are **two** explanations — a docs-based one and a first-principles one — because they teach differently: the first gives the accurate canonical meaning, the second makes it click.

1. **A docs-based explanation.** A short paragraph grounded in how the *official documentation* defines the term, so the user gets the accurate, canonical meaning. **Open with the keyword itself** — start the sentence `<Keyword> is …`. Put it in your own words — paraphrase the docs, don't paste sentences from them.
2. **A first-principles explanation.** Then strip it to the essence: the fundamental problem the keyword solves, in as few words as possible, no jargon. **Also open with `<Keyword> is …`.** If explaining it forces you to lean on another technical term, that's a signal to explain the underlying idea instead. One or two tight sentences that would land even for someone who's never heard the word.
3. **A real-world example + a tiny commented sample.** A relatable analogy or scenario, plus a small self-contained snippet (a few lines) that shows the keyword *in general* — separate from the user's code, with brief inline comments so it teaches as it's read.
4. **A docs link to go deeper.** Search the web for the canonical first-party source for that specific keyword — official language/framework docs, MDN for web platform APIs, the library's own docs, RFCs/specs. Avoid SEO content farms and stale tutorials. Link the page that documents *that keyword* specifically (for `useState`, React's `useState` reference — not a generic "React forms" article). If web search isn't available, fall back to the canonical URL from memory and mark it *"(verify)"*.
5. **The actual changed code + file path, with keyword-relevant comments.** Show the real lines from this change that demonstrate the keyword, labelled with the file they live in, and annotate them with brief comments that point out *how this keyword shows up here* — connecting the general idea back to the user's own codebase.

### 5. Write the lesson note

Pick a **topic / feature** name in PascalCase (`Authentication`, `Routing`, `StatePersistence`) — one file collects all the keywords for that area, so related vocabulary stays together as it grows.

Use the bundled helper to get the filename and mode right deterministically (it handles numbering and existing-topic detection):

```bash
python <skill-dir>/scripts/vibe_lesson.py resolve <vibe-learning-dir> <Topic>
```

It prints `FILE:` (the filename to use) and `MODE: create` or `MODE: append`. On **create**, write a fresh note with the template below. On **append**, add the new keyword sections to that existing file and add the new keywords to its "Keywords you need to learn" list at the top.

After writing the note, refresh the index:

```bash
python <skill-dir>/scripts/vibe_lesson.py reindex <vibe-learning-dir>
```

This rebuilds the `README.md` lesson table from the files on disk while preserving the Level/Depth settings block. (If Python isn't available, do it by hand: list the folder, take the next zero-padded number for a new topic or reuse the matching file to append, and add a row to the README table yourself.)

### 6. Surface it in chat — briefly

In the conversation, give the user a 2–4 sentence teaser and tell them the note is saved, naming the keywords it captured so they know what's covered, e.g. *"Saved `03Caching.md` — keywords: memoization, cache invalidation, stale-while-revalidate. Quick version: the result is computed once and reused until its inputs change. Full breakdown with the code and docs is in the file."* The depth lives in the file; the chat stays light so it doesn't bury the actual coding.

## Lesson note template

The file opens with a master list under the heading **"Keywords you need to learn"**, then one numbered section per keyword. Each keyword section has the same six parts in the same order: the keyword header, a docs-based explanation, a first-principles explanation, a real-world example with a small *commented* sample, a docs link, and finally the actual changed code (with keyword-relevant comments) and its file path. Depth tunes how many keywords and how long each explanation runs — the structure stays constant.

```markdown
# NN · <Topic / Feature Name>

> Captured: <date> · Level: <level> · From prompt: "<short paraphrase of what the user asked for>"

## Keywords you need to learn
1. <Keyword 1>
2. <Keyword 2>
3. <Keyword 3>

---

## 1. <Keyword>
**What it is (docs).** <Start with "<Keyword> is …", then the docs-grounded
definition, in your own words.>

**First principles.** <Start with "<Keyword> is …" — the fundamental idea in the
fewest words possible, no jargon.>

**Real-world example.** <A relatable analogy or scenario, then a tiny generic snippet
that shows the keyword in its simplest form — not from the user's codebase.>
```<lang>
<a few lines of illustrative sample code, with // comments explaining each part>
```

🔗 **Learn it deeply:** [<docs page title>](<url>)

**In your code** — `<path/to/file.ext>`:
```<lang>
<the actual changed lines, with // comments pointing out how this keyword shows up>
```

## 2. <Keyword>
<…same six parts…>

---
## Try this next   (deep depth only)
<A small, concrete exercise that ties the keywords together.>
```

Keep both code blocks focused: the sample tiny and generic, the "in your code" block trimmed to the lines that show the keyword. The same changed lines may appear under more than one keyword if they illustrate both.

## README / index template

The `vibe-learning/README.md` records settings and lists every lesson so the folder reads like a course:

```markdown
# Vibe Learning Log

**Level:** <beginner | intermediate | advanced>
**Depth:** <brief | medium | deep>

_Lessons captured while building this project. Each file is one topic,
anchored to real code from this codebase._

## Lessons
| # | Topic | File | Captured |
|---|-------|------|----------|
| 01 | Authentication | [01Authentication.md](01Authentication.md) | 2026-05-28 |
| 02 | Routing | [02Routing.md](02Routing.md) | 2026-05-28 |
```

## Staying in mode

Once invoked, treat teaching as an ongoing mode for the rest of the session: after you've fully completed each prompt, run the loop without being asked again. The user prompts for code as normal — they shouldn't have to re-request the lesson each time, and they shouldn't have their feature work interrupted mid-prompt to be taught. Finish the prompt, then teach. Useful things the user might say, and how to respond:
- *"pause vibe learning"* / *"just code for now"* → stop appending lessons until they re-enable it (still code normally).
- *"resume"* → turn the loop back on.
- *"change vibe settings"* / *"go deeper"* / *"explain like I'm a beginner"* → update `README.md` and continue.
- *"write up X too"* → produce a lesson for a concept you'd previously only mentioned in passing.

## Calibration notes

- **Don't lecture in chat.** The folder is where depth lives. A wall of explanation after every prompt defeats the purpose and slows the user down. Keep chat teasers short and let curiosity pull them into the files.
- **Respect the level honestly.** For a beginner, define jargon the first time it appears. For an advanced user, skip the basics and spend the words on tradeoffs and alternatives — they'll be bored by a definition of "what a function is."
- **Make links count.** One excellent first-party doc beats five mediocre links. The user is trusting these notes as a study resource, so don't pad them.
- **The code is the curriculum.** Always teach from what they actually built. That's what makes this stick where a generic tutorial wouldn't.

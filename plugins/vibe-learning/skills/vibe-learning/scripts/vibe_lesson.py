#!/usr/bin/env python3
"""
vibe_lesson.py — helper for the vibe-learning skill.

Two jobs, both deterministic so the model doesn't have to eyeball them:

  resolve <folder> <Topic>
      Decide the lesson filename and whether to CREATE or APPEND.
      - If a file like NN<Topic>.md already exists, returns it in APPEND mode
        (new keywords get added to the existing topic file).
      - Otherwise returns a new NN<Topic>.md, numbered one past the current
        highest, zero-padded to two digits, in CREATE mode.

  reindex <folder>
      Rewrite the "## Lessons" table in <folder>/README.md by scanning every
      NN*.md lesson, reading its title and "Captured" date. Preserves the
      Level/Depth settings block at the top of the README if it's already there.

Stdlib only — no third-party dependencies. Usage examples:

    python vibe_lesson.py resolve ./vibe-learning Authentication
    python vibe_lesson.py reindex ./vibe-learning
"""

import os
import re
import sys

LESSON_RE = re.compile(r"^(\d{2,})(.+)\.md$")          # 01Authentication.md -> ("01", "Authentication")
TITLE_RE = re.compile(r"^#\s+(.*)$")                    # "# 01 · Authentication"
CAPTURED_RE = re.compile(r"Captured:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})")


def lesson_files(folder):
    """Return [(number:int, topic:str, filename:str), ...] sorted by number."""
    out = []
    for name in os.listdir(folder):
        if name.lower() == "readme.md":
            continue
        m = LESSON_RE.match(name)
        if m:
            out.append((int(m.group(1)), m.group(2), name))
    out.sort(key=lambda t: t[0])
    return out


def resolve(folder, topic):
    os.makedirs(folder, exist_ok=True)
    existing = lesson_files(folder)
    # Existing file for this exact topic? -> append.
    for num, t, name in existing:
        if t.lower() == topic.lower():
            print(f"FILE: {name}")
            print("MODE: append")
            return
    # New topic -> next number.
    next_num = (existing[-1][0] + 1) if existing else 1
    name = f"{next_num:02d}{topic}.md"
    print(f"FILE: {name}")
    print("MODE: create")


def _read_title_and_date(path):
    """Pull a display topic (after the '·' if present) and the Captured date."""
    topic, date = None, ""
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                if topic is None:
                    m = TITLE_RE.match(line.strip())
                    if m:
                        heading = m.group(1)
                        topic = heading.split("·", 1)[1].strip() if "·" in heading else heading.strip()
                        continue
                if not date:
                    m = CAPTURED_RE.search(line)
                    if m:
                        date = m.group(1)
                if topic is not None and date:
                    break
    except OSError:
        pass
    return topic, date


def _settings_block(readme_path):
    """Return the lines before '## Lessons' (title + settings), or a default."""
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as fh:
            text = fh.read()
        head = text.split("## Lessons", 1)[0].rstrip()
        if head.strip():
            return head + "\n\n"
    return (
        "# Vibe Learning Log\n\n"
        "**Level:** <set on first run>\n"
        "**Depth:** <set on first run>\n\n"
        "_Lessons captured while building this project. "
        "Each file is one topic, anchored to real code from this codebase._\n\n"
    )


def reindex(folder):
    readme = os.path.join(folder, "README.md")
    # Read the settings block FIRST — opening the file for write truncates it.
    block = _settings_block(readme)
    rows = []
    for num, topic_from_name, name in lesson_files(folder):
        title, date = _read_title_and_date(os.path.join(folder, name))
        topic = title or topic_from_name
        rows.append(f"| {num:02d} | {topic} | [{name}]({name}) | {date} |")
    table = (
        "## Lessons\n"
        "| # | Topic | File | Captured |\n"
        "|---|-------|------|----------|\n"
        + ("\n".join(rows) if rows else "")
        + "\n"
    )
    with open(readme, "w", encoding="utf-8") as fh:
        fh.write(block + table)
    print(f"Reindexed {len(rows)} lesson(s) into {readme}")


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    cmd = argv[1]
    if cmd == "resolve" and len(argv) == 4:
        resolve(argv[2], argv[3])
    elif cmd == "reindex" and len(argv) == 3:
        reindex(argv[2])
    else:
        print(__doc__)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

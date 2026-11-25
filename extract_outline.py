import json, re
from collections import OrderedDict

pages = json.load(open('data/pages.json'))
lines = []
for pg in pages:
    for ln in pg['text'].split('\n'):
        s = re.sub(r'\s+', ' ', ln.strip())
        if s:
            lines.append((pg['pdf_page'], s))

pat_part = re.compile(r'^Part\s+([A-D])\s*:\s*(.+)$')
pat_art = re.compile(r'^Article\s+(\d+)\s*[-–]\s*(.+)$')
pat_sec = re.compile(r'^([ABCD])\.\s*(\d+(?:\.\d+)*)\s*[-–]?\s*(.+)$')

items = []  # (page, kind, key, title)
for pg, s in lines:
    if pg <= 3:
        continue
    m = pat_part.match(s)
    if m:
        items.append((pg, 'part', m.group(1), m.group(2).strip()))
        continue
    m = pat_art.match(s)
    if m:
        title = m.group(2).strip()
        if len(title) < 120 and not title.lower().startswith('the '):
            items.append((pg, 'article', m.group(1), title))
            continue
    m = pat_sec.match(s)
    if m:
        title = m.group(3).strip()
        num = m.group(2)
        if len(title) <= 110 and not title.endswith('.') and len(num.split('.')) >= 2:
            # reject the known false positive on p73
            if pg == 73 and s.startswith('A.1.3 - Objective and the A.1.4'):
                continue
            items.append((pg, 'sec', m.group(1) + '.' + num, title))

# de-duplicate consecutive identical keys on same page
clean = []
for it in items:
    if clean and clean[-1][1:] == it[1:]:
        continue
    clean.append(it)
items = clean

# build body: text from after heading line to next item heading line
# map each item to its index in the full line list
starts = {}
for idx, (pg, s) in enumerate(lines):
    pass

# Instead rebuild with positions
pos_items = []
for pg, s in lines:
    if pg <= 3:
        continue
    m = pat_part.match(s)
    if m:
        pos_items.append((pg, 'part', m.group(1), m.group(2).strip(), s)); continue
    m = pat_art.match(s)
    if m and len(m.group(2).strip()) < 120 and not m.group(2).strip().lower().startswith('the '):
        pos_items.append((pg, 'article', m.group(1), m.group(2).strip(), s)); continue
    m = pat_sec.match(s)
    if m and len(m.group(3).strip()) <= 110 and not m.group(3).strip().endswith('.') and len(m.group(2).split('.')) >= 2:
        if pg == 73 and s.startswith('A.1.3 - Objective and the A.1.4'):
            continue
        pos_items.append((pg, 'sec', m.group(1) + '.' + m.group(2), m.group(3).strip(), s))

# locate line index for each heading (first occurrence at/after previous)
cursor = 0
located = []
for pg, kind, key, title, raw in pos_items:
    found = None
    for i in range(cursor, len(lines)):
        if lines[i][0] == pg and lines[i][1] == raw:
            found = i
            break
    if found is None:
        for i in range(0, len(lines)):
            if lines[i][0] == pg and lines[i][1] == raw:
                found = i
                break
    located.append((found, pg, kind, key, title, raw))
    if found is not None:
        cursor = found + 1

# assemble
sections = []
for n, (idx, pg, kind, key, title, raw) in enumerate(located):
    if idx is None:
        continue
    end = len(lines)
    for idx2, pg2, kind2, key2, title2, raw2 in located[n+1:]:
        if idx2 is not None and idx2 > idx:
            end = idx2
            break
    body_lines = []
    for i in range(idx + 1, end):
        p2, s2 = lines[i]
        # stop if a page header repeats (Page N Version 1.0) — keep content across pages
        if re.match(r'^Page \d+ Version 1\.0$', s2):
            continue
        body_lines.append((p2, s2))
    # build paragraphs: join lines; start new paragraph on bullets, numbered items, or line ending with '.' followed by capital? keep simple: join all, but preserve bullet/number blocks
    paras = []
    cur = ''
    for p2, s2 in body_lines:
        is_block = bool(re.match(r'^[•\-]\s+', s2)) or bool(re.match(r'^\d+\)\s+', s2)) or bool(re.match(r'^[a-z]\.\s+', s2)) or bool(re.match(r'^Sample \d', s2))
        if is_block:
            if cur.strip():
                paras.append(cur.strip())
            cur = s2
        else:
            cur = (cur + ' ' + s2).strip() if cur else s2
    if cur.strip():
        paras.append(cur.strip())
    # clean up common artifacts
    text = '\n'.join(paras)
    sections.append({'kind': kind, 'key': key, 'title': title, 'page': pg, 'text': text})

json.dump(sections, open('data/sections_auto.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(sections), Counter(s['kind'] for s in sections))
print('parts', [(s['key'], s['title'], s['page']) for s in sections if s['kind']=='part'])
print('articles', len([s for s in sections if s['kind']=='article']))
for s in sections:
    if s['kind']=='article' and s['key'] in ('3','14'):
        print(s['key'], s['title'], s['page'])

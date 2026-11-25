# -*- coding: utf-8 -*-
"""Phase 3 validation: compare curated B.3 official wording against the page-extracted text."""
import json, re, sys
from b3_rules_a import B3_RULES_A
from b3_rules_b import B3_RULES_B
from b3_rules_c import B3_RULES_C
from b3_checks_a import CHECKS_A
from b3_checks_b import CHECKS_B

B3 = B3_RULES_A + B3_RULES_B + B3_RULES_C
CHECKS = CHECKS_A + CHECKS_B
auto = {s['key']: s for s in json.load(open('data/sections_auto.json')) if s['kind']=='sec'}

def norm(t):
    t = t.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
    t = t.replace('–','-').replace('—','-').replace('•',' ')
    t = re.sub(r'[^\w\s.%°]', ' ', t)
    t = re.sub(r'\s+', ' ', t).lower().strip()
    return t

def toks(t): return norm(t).split()

problems=[]
for r in B3:
    if r['id'] not in auto:
        problems.append(f"{r['id']}: missing from auto extraction"); continue
    a = auto[r['id']]['text']
    cur = ' '.join(r['body'])
    at, ct = toks(a), toks(cur)
    # token coverage: how many curated tokens appear in auto (multiset)
    from collections import Counter
    ca, cc = Counter(at), Counter(ct)
    missing = cc - ca
    extra = ca - cc
    ratio = sum((cc & ca).values()) / max(1, sum(cc.values()))
    if ratio < 0.985:
        problems.append(f"{r['id']}: token coverage {ratio:.3f}; missing={list(missing.items())[:8]}; extra={list(extra.items())[:8]}")
    if not r['body']:
        problems.append(f"{r['id']}: empty body")
    if not r.get('plain'): problems.append(f"{r['id']}: no plain layer")
    if not r.get('engineering'): problems.append(f"{r['id']}: no engineering layer")
    if not (17 <= r['page'] <= 36): problems.append(f"{r['id']}: page {r['page']} outside 17-36")

# checks
ids={r['id'] for r in B3}
seen=set()
for c in CHECKS:
    if c['id'] in seen: problems.append(f"duplicate check {c['id']}")
    seen.add(c['id'])
    if c['rule'] not in ids: problems.append(f"{c['id']}: unknown rule {c['rule']}")
    if c['eval']!='none' and (c['min'] is None and c['max'] is None): problems.append(f"{c['id']}: numeric eval without threshold")
    if c['eval']=='none' and c['min'] is not None: problems.append(f"{c['id']}: threshold on manual check")
    if not c['criterion'] or not c['method'] or not c['evidence']: problems.append(f"{c['id']}: missing criterion/method/evidence")

# rule coverage by checks
no_checks=[r['id'] for r in B3 if not any(c['rule']==r['id'] for c in CHECKS)]
print('B.3 rules:',len(B3),'checks:',len(CHECKS))
print('Rules with no direct check (parents expected):', no_checks)
print('Coverage: every B.3 rule has a check or is a parent:', all((r['id'] in [c['rule'] for c in CHECKS]) or r.get('kind')=='parent' for r in B3))
print('Problems:',len(problems))
for p in problems: print(' -',p)

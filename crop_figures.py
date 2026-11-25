# -*- coding: utf-8 -*-
"""Crop the numbered figures out of the rulebook PDF into static/img/.

Each 'Figure B-n:' caption block is paired with the image block directly above it,
then that region is rendered at 3x and saved as fig-B-nn.png.
"""
import os, re, json
import pymupdf

PDF = '/home/user/uploads/1788782546573-BAJA_SAEINDIA_Chennai_2026_Rulebook_ICE_V01_1Sep2026.pdf'
OUT = 'static/img'
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(PDF)
made = []
for pno in range(len(doc)):
    page = doc[pno]
    try:
        boxes = [page.get_image_bbox(i) for i in page.get_images(full=True)]
    except Exception:
        boxes = []
    for b in page.get_text('blocks'):
        txt = b[4].strip()
        m = re.match(r'^Figure\s*B-?\s*(\d+)\s*:', txt)
        if not m: continue
        num = int(m.group(1))
        cap_top = b[1]
        # the figure sits above its caption; tolerate small bbox overlap (<=15pt)
        # and reject images that are far above (a different figure's leftovers)
        above = [x for x in boxes
                 if x.y1 <= cap_top + 15 and x.y0 < cap_top and (cap_top - x.y1) <= 45]
        if not above:
            continue
        box = max(above, key=lambda x: x.y1)
        pad = 3
        clip = pymupdf.Rect(box.x0 - pad, box.y0 - pad, box.x1 + pad, box.y1 + pad) & page.rect
        if clip.width < 60 or clip.height < 40:
            continue
        pix = page.get_pixmap(matrix=pymupdf.Matrix(3, 3), clip=clip)
        name = f'fig-B-{num:02d}.png'
        pix.save(os.path.join(OUT, name))
        made.append({'figure': f'B-{num}', 'page': pno + 1, 'file': name,
                     'w': pix.width, 'h': pix.height})
print(f'cropped {len(made)} figures')
for m in made: print(' ', m['figure'], 'p', m['page'], m['file'], m['w'], 'x', m['h'])
json.dump(made, open('data/figures.json', 'w'), indent=1)
json.dump(made, open('static/figures.json', 'w'), indent=1)

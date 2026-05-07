import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "자동화글_테스트")
BODY_DIR = r"C:\학원_temp"
SITE_URL = "https://perf.kr"

# ── 본문 문장 로딩 ──
print("본문 문장 로딩 중...", flush=True)
_all_sentences = []
_body_files = [f for f in os.listdir(BODY_DIR) if f.endswith('.txt')]
_total_files = len(_body_files)
for _i, _fname in enumerate(_body_files[:3], 1):
    with open(os.path.join(BODY_DIR, _fname), encoding='utf-8') as _f:
        _content = _f.read()
    for _line in _content.split('\n'):
        for _s in _line.split('.'):
            _s = _s.strip()
            if 10 < len(_s) <= 200:
                _all_sentences.append(_s)
print(f"문장 {len(_all_sentences)}개 로딩 완료", flush=True)

def make_body():
    result = []
    total = 0
    while total < 500:
        s = _all_sentences[random.randint(0, len(_all_sentences)-1)]
        if total + len(s) <= 600:
            result.append(s)
            total += len(s)
        elif total == 0:
            continue
        else:
            break
    return '. '.join(result) + '.'

def read_keywords(filename):
    path = os.path.join(BASE_DIR, filename)
    result = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                result.append(line)
    return result

def read_regions(filename):
    path = os.path.join(BASE_DIR, filename)
    seen = set()
    regions = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            col1 = parts[0].strip()
            col2 = parts[1].strip() if len(parts) >= 2 else '상담'
            if col1 not in seen:
                seen.add(col1)
                regions.append((col1, col2))
    return regions

main_keywords  = read_keywords('메인키워드.txt')
grade_keywords = read_keywords('학년키워드.txt')
combo_keywords = read_keywords('학년조합키워드.txt')
regions        = read_regions('지역키워드.txt')

def location_img_path(location):
    img = os.path.join(BASE_DIR, '학원위치', f'{location}.webp')
    if os.path.exists(img):
        return f'../../학원위치/{location}.webp'
    return '../../학원위치/상담.webp'

def keyword_variations(parts):
    no_space = ''.join(parts)
    all_space = ' '.join(parts)
    variations = [no_space, all_space]
    if len(parts) == 3:
        variations.append(parts[0] + ' ' + parts[1] + parts[2])
        variations.append(parts[0] + parts[1] + ' ' + parts[2])
    while len(variations) < 4:
        variations.append(all_space)
    return ', '.join(variations)

def make_html(keyword, loc_img, parts):
    spaced = ' '.join(parts)
    body = make_body()
    desc = f'{spaced} 1:1 개별지도로 취약점을 끝까지 파헤칩니다. {spaced} 완벽 일대일 밀착 케어를 경험하세요.'
    canonical = f'{SITE_URL}/자동화글/{keyword}/'
    kw_meta = keyword_variations(parts)
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1.0"/>
  <title>{spaced}</title>
  <meta name="description" content="{desc}"/>
  <meta name="keywords" content="{kw_meta}"/>
  <meta name="robots" content="index, follow"/>
  <link rel="canonical" href="{canonical}"/>
  <link rel="preload" as="image" href="../../1.webp"/>
  <meta property="og:type" content="website"/>
  <meta property="og:title" content="{spaced}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:image" content="{SITE_URL}/와와.webp"/>
  <meta property="og:url" content="{canonical}"/>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    body{{background:#111;font-family:-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic','맑은 고딕',system-ui,sans-serif}}
    .wrap{{max-width:720px;margin:0 auto;padding:24px 16px}}
    .imgs img{{width:100%;display:block;border-radius:10px;margin-bottom:16px}}
    .seo{{margin-top:12px;font-size:0.72rem;color:#666;line-height:1.8}}
    .seo h1{{font-size:0.8rem;color:#555;font-weight:400;margin-bottom:6px}}
    @media(max-width:600px){{
      .wrap{{padding:0}}
      .imgs img{{border-radius:0;margin-bottom:8px}}}}
  </style>
</head>
<body>
  <div class="wrap">
    <div class="imgs">
      <img src="../../1.webp" alt="{spaced}"/>
      <img src="../../2.webp" alt="{spaced}" loading="lazy"/>
      <img src="{loc_img}" alt="{spaced} 학원 위치" loading="lazy"/>
    </div>
    <div class="seo">
      <h1>{spaced}</h1>
      <p>{spaced}<br>{body}</p>
    </div>
  </div>
</body>
</html>'''

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 랜덤 3개 조합 생성
combos = []

for region, location in regions:
    for kw in main_keywords:
        combos.append(('타입1', region, location, kw, ''))

for region, location in regions:
    for grade in grade_keywords:
        for combo in combo_keywords:
            combos.append(('타입2', region, location, grade, combo))

samples = random.sample(combos, 3)

for s in samples:
    t = s[0]
    region, location = s[1], s[2]
    loc_img = location_img_path(location)

    if t == '타입1':
        keyword = f'{region}{s[3]}'
        parts = [region, s[3]]
    else:
        keyword = f'{region}{s[3]}{s[4]}'
        parts = [region, s[3], s[4]]

    folder = os.path.join(OUTPUT_DIR, keyword)
    os.makedirs(folder, exist_ok=True)
    html = make_html(keyword, loc_img, parts)
    with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    # 본문 미리보기
    body_preview = make_body()
    print(f'[{t}] {keyword}')
    print(f'     본문 미리보기: {body_preview[:80]}...')
    print()

print(f'자동화글_테스트 폴더에서 확인하세요: {OUTPUT_DIR}')

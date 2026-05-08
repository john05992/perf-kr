import os
import random
from urllib.parse import quote

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "교육정보_테스트")
BODY_DIR = r"C:\학원_temp"
SITE_URL = "https://perf.kr"
CLOUD = "dg9uf6vh6"

def cld(public_id, keyword, alt_suffix):
    t = quote(f"{keyword} {alt_suffix}", safe='')
    return f"https://res.cloudinary.com/{CLOUD}/image/upload/l_text:NanumGothic_40:{t},co_white,g_south,y_20/f_webp/{public_id}"

# 본문 문장 로딩 (테스트용 3파일만)
print("본문 문장 로딩 중...", flush=True)
_all_sentences = []
_body_files = [f for f in os.listdir(BODY_DIR) if f.endswith('.txt')]
for _fname in _body_files[:3]:
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

def make_desc(keyword):
    result = []
    total = 0
    while total < 150:
        s = _all_sentences[random.randint(0, len(_all_sentences)-1)]
        chunk = f'{keyword} {s}'
        if total + len(chunk) <= 200:
            result.append(chunk)
            total += len(chunk)
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

def make_html(keyword, parts):
    spaced = ' '.join(parts)
    body = make_body()
    desc = make_desc(spaced)
    canonical = f'{SITE_URL}/교육정보/{keyword}/'
    kw_meta = keyword_variations(parts)
    img1 = cld('%EC%99%80%EC%99%80_ftoait', spaced, '실제 내부')
    img2 = cld('1_xn96yh', spaced, '수업 방식')
    img3 = cld('2_vljm9h', spaced, '수업 후기')
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
  <link rel="preload" as="image" href="{img1}"/>
  <meta property="og:type" content="website"/>
  <meta property="og:title" content="{spaced}"/>
  <meta property="og:description" content="{desc}"/>
  <meta property="og:image" content="{img1}"/>
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
      <img src="{img1}" alt="{spaced} 실제 내부"/>
      <img src="{img2}" alt="{spaced} 수업 방식" loading="lazy"/>
      <img src="{img3}" alt="{spaced} 수업 후기" loading="lazy"/>
    </div>
    <div class="seo">
      <h1>{spaced}</h1>
      <p>{spaced}<br>{body}</p>
    </div>
  </div>
</body>
</html>'''

main_keywords  = read_keywords('메인키워드.txt')
grade_keywords = read_keywords('학년키워드.txt')
combo_keywords = read_keywords('학년조합키워드.txt')
regions        = read_regions('지역키워드.txt')

combos = []
for region, location in regions:
    for kw in main_keywords:
        combos.append(('타입1', region, kw, ''))
for region, location in regions:
    for grade in grade_keywords:
        for combo in combo_keywords:
            combos.append(('타입2', region, grade, combo))

samples = random.sample(combos, 3)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\n=== 테스트 3개 생성 -> {OUTPUT_DIR} ===\n")
for s in samples:
    t, region = s[0], s[1]
    if t == '타입1':
        keyword = f'{region}{s[2]}'
        parts = [region, s[2]]
    else:
        keyword = f'{region}{s[2]}{s[3]}'
        parts = [region, s[2], s[3]]

    folder = os.path.join(OUTPUT_DIR, keyword)
    os.makedirs(folder, exist_ok=True)
    html = make_html(keyword, parts)
    with open(os.path.join(folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[{t}] {' '.join(parts)}")
    print(f"     canonical: {SITE_URL}/교육정보/{keyword}/")
    print(f"     img1: https://res.cloudinary.com/{CLOUD}/image/upload/.../{' '.join(parts)} 실제 내부")
    print()

print(f"완료! 교육정보_테스트 폴더 열어서 index.html 확인해봐.")

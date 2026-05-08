import os
import re
import random
from urllib.parse import quote

BASE = r"C:\Users\tlsdy\OneDrive\바탕 화면\프리미엄 과외\교육정보"
CLOUD = "dg9uf6vh6"

def insert_keyword_once(html, keyword):
    p_m = re.search(r'(<p>.*?<br>)(.*?)(</p>)', html, re.DOTALL)
    if not p_m:
        return html
    prefix, body, suffix = p_m.group(1), p_m.group(2), p_m.group(3)
    positions = [m.start() for m in re.finditer(r'\. ', body)]
    if not positions:
        return html
    pos = random.choice(positions)
    new_body = body[:pos+2] + f'{keyword}은 ' + body[pos+2:]
    return html[:p_m.start()] + prefix + new_body + suffix + html[p_m.end():]

def cld(public_id, keyword, alt_suffix):
    t = quote(f"{keyword} {alt_suffix}", safe='')
    return f"https://res.cloudinary.com/{CLOUD}/image/upload/l_text:NanumGothic_40:{t},co_white,g_south,y_20/f_webp/{public_id}"

def process(folder_path):
    html_path = os.path.join(folder_path, 'index.html')
    with open(html_path, encoding='utf-8') as f:
        html = f.read()

    # 키워드 추출 (title 태그에서)
    m = re.search(r'<title>(.*?)</title>', html)
    if not m:
        return False
    keyword = m.group(1)

    img1 = cld('%EC%99%80%EC%99%80_ftoait', keyword, '실제 내부')
    img2 = cld('1_xn96yh', keyword, '수업 방식')
    img3 = cld('2_vljm9h', keyword, '수업 후기')

    # 위치사진 경로 추출 (기존 HTML에서)
    loc_m = re.search(r'<img src="(../../학원위치/[^"]+)"', html)
    loc_img = loc_m.group(1) if loc_m else '../../학원위치/상담.webp'

    # canonical/og:url: 자동화글 → 교육정보
    html = html.replace('https://perf.kr/자동화글/', 'https://perf.kr/교육정보/')

    # preload
    html = re.sub(r'<link rel="preload" as="image" href="[^"]*"/>',
                  f'<link rel="preload" as="image" href="{img1}"/>', html)

    # og:image
    html = re.sub(r'<meta property="og:image" content="[^"]*"/>',
                  f'<meta property="og:image" content="{img1}"/>', html)

    # imgs 블록 교체 (Cloudinary 3장 + 위치사진)
    new_imgs = (
        f'<div class="imgs">\n'
        f'      <img src="{img1}" alt="{keyword} 실제 내부"/>\n'
        f'      <img src="{img2}" alt="{keyword} 수업 방식" loading="lazy"/>\n'
        f'      <img src="{img3}" alt="{keyword} 수업 후기" loading="lazy"/>\n'
        f'      <img src="{loc_img}" alt="{keyword} 학원 위치" loading="lazy"/>\n'
        f'    </div>'
    )
    html = re.sub(r'<div class="imgs">.*?</div>', new_imgs, html, flags=re.DOTALL)

    # 본문에 키워드 한 번 랜덤 삽입
    html = insert_keyword_once(html, keyword)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return True

folders = [d for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d))]
total = len(folders)
success = 0

print(f"총 {total}개 파일 수정 시작...", flush=True)

for i, folder_name in enumerate(folders):
    if process(os.path.join(BASE, folder_name)):
        success += 1
    if (i + 1) % 100 == 0:
        print(f"  {i+1}/{total} 완료...", flush=True)

print(f"\n완료! {success}/{total}개 수정됨")
print("이제 자동화글 폴더명을 교육정보로 바꾸면 돼.")

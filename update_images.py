import os
import re
from PIL import Image

IM_DIR  = r"C:\Users\tlsdy\OneDrive\바탕 화면\사이트\perf.kr\im"
EDU_DIR = r"C:\Users\tlsdy\OneDrive\바탕 화면\사이트\perf.kr\교육정보"

# ── Step 1: PNG → WebP 변환 ──────────────────────────────────────────────────
print("=== PNG → WebP 변환 ===")
for i in range(1, 18):
    png_path  = os.path.join(IM_DIR, f"{i}.png")
    webp_path = os.path.join(IM_DIR, f"{i}.webp")
    if not os.path.exists(png_path):
        print(f"  {i}.png 없음 - 스킵")
        continue
    img = Image.open(png_path).convert("RGB")
    img.save(webp_path, "WEBP", quality=85, method=6)
    before = os.path.getsize(png_path) // 1024
    after  = os.path.getsize(webp_path) // 1024
    print(f"  {i}.png {before}KB → {i}.webp {after}KB")

# ── Step 2: imgs div 교체 ────────────────────────────────────────────────────
print("\n=== HTML 파일 수정 ===")

LOC_RE = re.compile(
    r'<img\s[^>]*src="([^"]*\ud559\uc6d0\uc704\uce58[^"]*)"[^>]*/>', re.IGNORECASE
)
IMGS_RE = re.compile(r'<div class="imgs">.*?</div>', re.DOTALL)
PRELOAD_RE = re.compile(r'<link rel="preload" as="image" href="[^"]*"/>')

def build_imgs_div(loc_src, loc_alt):
    tags = ['    <div class="imgs">']
    for i in range(1, 18):
        lazy = '' if i <= 2 else ' loading="lazy"'
        tags.append(f'      <img src="../../im/{i}.webp" alt=""{lazy}/>')
    tags.append(f'      <img src="{loc_src}" alt="{loc_alt}" loading="lazy"/>')
    tags.append('    </div>')
    return '\n'.join(tags)

processed = 0
skipped   = 0
errors    = 0
folders   = os.listdir(EDU_DIR)
total     = len(folders)

for idx, folder in enumerate(folders):
    folder_path = os.path.join(EDU_DIR, folder)
    html_path   = os.path.join(folder_path, 'index.html')

    if not os.path.isfile(html_path):
        skipped += 1
        continue

    try:
        with open(html_path, encoding='utf-8') as f:
            content = f.read()

        # 위치사진 src / alt 추출
        loc_match = LOC_RE.search(content)
        if loc_match:
            loc_src = loc_match.group(1)
            # alt 추출
            full_tag = loc_match.group(0)
            alt_m = re.search(r'alt="([^"]*)"', full_tag)
            loc_alt = alt_m.group(1) if alt_m else "학원 위치"
        else:
            loc_src = "../../학원위치/학원위치.webp"
            loc_alt = "학원 위치"

        new_div = build_imgs_div(loc_src, loc_alt)

        # imgs div 교체
        new_content = IMGS_RE.sub(new_div, content)

        # preload → im/1.webp 로 교체
        new_content = PRELOAD_RE.sub(
            '<link rel="preload" as="image" href="../../im/1.webp"/>',
            new_content
        )

        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        processed += 1
        if processed % 20000 == 0:
            print(f"  진행: {processed}/{total} ({processed*100//total}%)")

    except Exception as e:
        errors += 1
        if errors <= 5:
            print(f"  오류 ({folder}): {e}")

print(f"\n완료! 처리: {processed}개 / 스킵: {skipped}개 / 오류: {errors}개")

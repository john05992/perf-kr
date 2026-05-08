import os
import re
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "자동화글")
TEST_DIR = os.path.join(BASE_DIR, "자동화글_desc테스트")

def get_sentences_from_body(body_text):
    sentences = []
    for s in body_text.split('.'):
        s = s.strip()
        if len(s) > 10:
            sentences.append(s)
    return sentences

def make_desc(keyword, sentences):
    if len(sentences) < 4:
        pool = sentences * 4
    else:
        pool = sentences
    picked = random.sample(pool, min(4, len(pool)))
    return '. '.join(f'{keyword} {s}' for s in picked) + '.'

def update_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        html = f.read()

    # 제목 추출
    title_match = re.search(r'<title>(.*?)</title>', html)
    if not title_match:
        return False
    keyword = title_match.group(1).strip()

    # 본문 추출 (<br> 이후 텍스트)
    body_match = re.search(r'<br>(.*?)</p>', html, re.DOTALL)
    if not body_match:
        return False
    body_text = body_match.group(1).strip()

    sentences = get_sentences_from_body(body_text)
    if not sentences:
        return False

    new_desc = make_desc(keyword, sentences)

    # meta description 교체
    html = re.sub(
        r'<meta name="description" content=".*?"/>',
        f'<meta name="description" content="{new_desc}"/>',
        html
    )
    # og:description 교체
    html = re.sub(
        r'<meta property="og:description" content=".*?"/>',
        f'<meta property="og:description" content="{new_desc}"/>',
        html
    )

    os.makedirs(os.path.join(TEST_DIR, folder), exist_ok=True)
    out_path = os.path.join(TEST_DIR, folder, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return new_desc

# 처음 100개에서 랜덤 3개
import itertools
pool = [e.name for e in itertools.islice(os.scandir(OUTPUT_DIR), 100) if e.is_dir()]
samples = random.sample(pool, 3)

for folder in samples:
    filepath = os.path.join(OUTPUT_DIR, folder, 'index.html')
    result = update_file(filepath)
    if result:
        print(f'[{folder}]')
        print(f'  새 description: {result[:120]}...')
        print()
    else:
        print(f'[{folder}] 실패')

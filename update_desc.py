import os
import re
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "자동화글")

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

    title_match = re.search(r'<title>(.*?)</title>', html)
    if not title_match:
        return False
    keyword = title_match.group(1).strip()

    body_match = re.search(r'<br>(.*?)</p>', html, re.DOTALL)
    if not body_match:
        return False
    body_text = body_match.group(1).strip()

    sentences = get_sentences_from_body(body_text)
    if not sentences:
        return False

    new_desc = make_desc(keyword, sentences)

    html = re.sub(
        r'<meta name="description" content=".*?"/>',
        f'<meta name="description" content="{new_desc}"/>',
        html
    )
    html = re.sub(
        r'<meta property="og:description" content=".*?"/>',
        f'<meta property="og:description" content="{new_desc}"/>',
        html
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return True

count = 0
errors = 0
for folder in os.scandir(OUTPUT_DIR):
    if not folder.is_dir():
        continue
    filepath = os.path.join(folder.path, 'index.html')
    if not os.path.exists(filepath):
        continue
    try:
        update_file(filepath)
        count += 1
    except Exception:
        errors += 1
    if count % 1000 == 0 and count > 0:
        print(f'{count}개 완료...', flush=True)

print(f'\n완료! {count}개 수정, {errors}개 오류')

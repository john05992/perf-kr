import requests
import time

SITE_ID = "254723115"
ACCESS_TOKEN = input("토큰 입력: ").strip()

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# 테스트 글 1개
post_data = {
    "title": "망포동 영어과외",
    "content": """<p>망포동 영어과외 전문 1:1 개별지도로 취약점을 끝까지 파헤칩니다.</p>
<p>망포동 영어과외 완벽 일대일 밀착 케어를 경험하세요.</p>
<p>망포동 영어과외 학생 맞춤형 커리큘럼으로 성적을 올립니다.</p>""",
    "status": "publish",
    "format": "standard"
}

url = f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE_ID}/posts/new"
response = requests.post(url, headers=headers, json=post_data)

print(f"상태코드: {response.status_code}")
data = response.json()
if response.status_code == 200:
    print(f"성공! URL: {data.get('URL')}")
else:
    print(f"실패: {data}")

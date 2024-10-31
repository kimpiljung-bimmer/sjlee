import requests
from bs4 import BeautifulSoup
from github import Github
import os

# 1. Dead by Daylight 패치노트 URL
url = "https://forums.bhvr.com/dead-by-daylight/kb/patchnotes"  # 실제 패치노트 URL을 입력합니다.

# 2. GitHub 액세스 토큰 및 레포지토리 정보
GITHUB_TOKEN = "your_github_token"  # GitHub Personal Access Token
REPO_NAME = "yourusername/dbd-patch-notes"  # 'username/repository_name' 형식

# 3. 기존 패치노트 파일 읽기
def load_existing_notes():
    with open("patch-notes.md", "r", encoding="utf-8") as file:
        return file.read()

# 4. 새로운 패치노트 가져오기
def fetch_patch_notes():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 페이지에서 패치노트를 파싱하는 로직을 작성합니다 (HTML 구조에 따라 변경).
    patch_notes = soup.find("div", {"class": "patch-notes"}).text
    return patch_notes

# 5. GitHub에 패치노트 업데이트
def update_github_repo(new_notes):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file_path = "patch-notes.md"

    # 기존 파일의 내용을 불러와 비교
    contents = repo.get_contents(file_path)
    repo.update_file(contents.path, "Update patch notes", new_notes, contents.sha)

# 메인 프로세스
existing_notes = load_existing_notes()
new_notes = fetch_patch_notes()

if new_notes != existing_notes:
    with open("patch-notes.md", "w", encoding="utf-8") as file:
        file.write(new_notes)
    update_github_repo(new_notes)
    print("패치노트가 업데이트되었습니다.")
else:
    print("새로운 패치노트가 없습니다.")

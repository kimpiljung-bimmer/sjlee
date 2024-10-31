import requests
from bs4 import BeautifulSoup
from github import Github
import os

# 1. Dead by Daylight 패치노트 URL
url = "https://forums.bhvr.com/dead-by-daylight/kb/patchnotes"

# 2. GitHub 액세스 토큰 및 레포지토리 정보
GITHUB_TOKEN = os.getenv("SJLEE")  # 개인적으로 설정한 토큰으로 변경하세요
REPO_NAME = "sjlee/"  # 레포지토리 이름

# 3. 기존 패치노트 파일 읽기
def load_existing_notes():
    if os.path.exists("patch-notes.md"):
        with open("patch-notes.md", "r", encoding="utf-8") as file:
            return file.read()
    return ""

# 4. 새로운 패치노트 가져오기
def fetch_patch_notes():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 패치노트 HTML 구조에 맞게 수정 (구조에 따라 id나 class명 확인 필요)
    patch_notes_section = soup.find("div", {"class": "PageBody"})  # 정확한 클래스 이름은 확인 필요
    if patch_notes_section:
        patch_notes = patch_notes_section.get_text(separator="\n").strip()
    else:
        patch_notes = "패치노트를 찾을 수 없습니다."
    
    return patch_notes

# 5. GitHub에 패치노트 업데이트
def update_github_repo(new_notes):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    file_path = "patch-notes.md"

    # GitHub의 기존 파일 내용 가져오기
    try:
        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, "Update patch notes", new_notes, contents.sha)
    except Exception as e:
        print(f"파일 업데이트 중 오류 발생: {e}")

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

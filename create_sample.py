import os

# sample 폴더 및 하위 폴더 경로 설정 (ZIP 백업 시 하위 폴더 구조 테스트용)
base_dir = "sample"
sub_dir = os.path.join(base_dir, "sub_folder")

os.makedirs(sub_dir, exist_ok=True)

# 생성할 테스트 파일 목록 (경로: 파일 내용)
files_to_create = {
    # 다양한 확장자 테스트용
    os.path.join(base_dir, "memo.txt"): "일반 텍스트 메모 파일입니다.\n",
    os.path.join(base_dir, "data.csv"): "이름,나이,지역\n홍길동,25,서울\n김철수,30,부산\n",
    os.path.join(base_dir, "report.pdf"): "테스트용 더미 PDF 파일입니다.\n",
    os.path.join(base_dir, "photo.jpg"): "테스트용 더미 JPG 파일입니다.\n",
    os.path.join(base_dir, "music.mp3"): "테스트용 더미 MP3 파일입니다.\n",
    os.path.join(base_dir, "README"): "확장자가 없는 파일 분류 테스트용입니다.\n",

    # 중복 파일 검색 테스트용 (내용이 완전히 동일한 텍스트 파일 2개)
    os.path.join(base_dir, "duplicate_1.txt"): "중복 파일 검색 테스트용 동일한 내용입니다.\n",
    os.path.join(base_dir, "duplicate_2.txt"): "중복 파일 검색 테스트용 동일한 내용입니다.\n",

    # ZIP 백업 시 하위 폴더 유지 확인용
    os.path.join(sub_dir, "sub_note.txt"): "하위 폴더 안에 있는 테스트 파일입니다.\n",
}

for file_path, content in files_to_create.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"테스트 폴더 생성 완료: {os.path.abspath(base_dir)}")
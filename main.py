import os
import shutil
import hashlib
import zipfile
from datetime import datetime


def get_valid_folder_path():
    """사용자로부터 유효한 폴더 경로를 입력받는 함수"""
    # Windows에서 경로 복사 시 붙는 큰따옴표(")나 공백을 제거합니다.
    folder_path = input("대상 폴더 경로를 입력하세요: ").strip().strip('"').strip("'")

    if not folder_path or not os.path.isdir(folder_path):
        print("[오류] 존재하지 않는 폴더 경로입니다. 다시 확인해주세요.")
        return None

    return os.path.abspath(folder_path)


# ==========================================
# 기능 1: 폴더 내 파일 목록 조회
# ==========================================
def list_files(folder_path):
    """지정된 폴더 바로 아래에 있는 파일 목록과 크기를 출력합니다."""
    print(f"\n[파일 목록] 경로: {folder_path}")
    print("-" * 50)

    items = os.listdir(folder_path)
    file_count = 0

    for item in items:
        item_path = os.path.join(folder_path, item)
        # 하위 폴더는 제외하고 파일만 출력합니다.
        if os.path.isfile(item_path):
            file_size = os.path.getsize(item_path)
            print(f"- {item} ({file_size:,} bytes)")
            file_count += 1

    if file_count == 0:
        print("폴더 내에 파일이 없습니다.")
    else:
        print("-" * 50)
        print(f"총 {file_count}개의 파일이 있습니다.")


# ==========================================
# 기능 2: 확장자별 파일 분류
# ==========================================
def organize_by_extension(folder_path):
    """폴더 내 파일들을 확장자 이름의 하위 폴더로 분류하여 이동합니다."""
    confirm = input("폴더 내 파일들을 확장자별 하위 폴더로 이동할까요? (y/n): ").strip().lower()
    if confirm != "y":
        print("작업을 취소했습니다.")
        return

    moved_count = 0
    skipped_count = 0

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        # 파일인 경우에만 분류를 진행합니다.
        if os.path.isfile(item_path):
            # 확장자를 분리합니다. (예: '.txt' -> 'txt')
            _, ext = os.path.splitext(item)
            if ext:
                folder_name = ext[1:].lower()
            else:
                folder_name = "확장자없음"

            target_dir = os.path.join(folder_path, folder_name)
            os.makedirs(target_dir, exist_ok=True)

            target_path = os.path.join(target_dir, item)

            # 같은 이름의 파일이 이미 있으면 덮어쓰지 않고 건너뜁니다.
            if os.path.exists(target_path):
                print(f"[건너뜀] 이미 동일한 이름의 파일이 있습니다: {target_path}")
                skipped_count += 1
            else:
                shutil.move(item_path, target_path)
                print(f"[이동] {item} -> {folder_name}\\{item}")
                moved_count += 1

    print(f"\n분류 완료! (이동: {moved_count}개, 건너뜀: {skipped_count}개)")


# ==========================================
# 기능 3: 파일 해시를 이용한 중복 파일 검색
# ==========================================
def calculate_file_hash(file_path):
    """파일 내용을 읽어 SHA-256 해시값을 계산합니다."""
    sha256 = hashlib.sha256()
    # 대용량 파일도 메모리 부담 없이 읽을 수 있도록 64KB씩 나누어 읽습니다.
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            sha256.update(chunk)
    return sha256.hexdigest()


def find_duplicate_files(folder_path):
    """하위 폴더를 포함하여 해시값이 같은 중복 파일을 찾습니다. (삭제하지 않음)"""
    print(f"\n[중복 파일 검색 중...] 대상: {folder_path}")
    hash_map = {}

    # os.walk로 하위 폴더 내 모든 파일까지 검사합니다.
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                file_hash = calculate_file_hash(file_path)
                if file_hash in hash_map:
                    hash_map[file_hash].append(file_path)
                else:
                    hash_map[file_hash] = [file_path]
            except OSError as e:
                print(f"[읽기 실패] {file_path} ({e})")

    # 같은 해시값을 가진 파일이 2개 이상인 경우만 출력합니다.
    duplicates = [paths for paths in hash_map.values() if len(paths) > 1]

    if not duplicates:
        print("중복된 파일이 없습니다.")
    else:
        print(f"\n총 {len(duplicates)}개의 중복 그룹을 찾았습니다. (파일은 삭제되지 않습니다)")
        for idx, paths in enumerate(duplicates, start=1):
            print(f"\n[중복 그룹 {idx}]")
            for path in paths:
                print(f"  - {path}")


# ==========================================
# 기능 4: 지정 폴더 ZIP 백업
# ==========================================
def backup_folder_to_zip(folder_path):
    """지정한 폴더 전체를 날짜/시간이 포함된 ZIP 파일로 백업합니다."""
    parent_dir = os.path.dirname(folder_path)
    folder_name = os.path.basename(folder_path) or "backup"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{folder_name}_backup_{timestamp}.zip"

    # 기본적으로 대상 폴더의 상위 폴더에 백업 파일을 생성합니다.
    zip_path = os.path.join(parent_dir, zip_filename)

    print(f"\n[백업 시작] 생성될 파일: {zip_path}")

    file_count = 0
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 혹시 백업 대상 폴더 안에 ZIP 파일이 생성된 경우 자기 자신은 제외합니다.
                if os.path.abspath(file_path) == os.path.abspath(zip_path):
                    continue

                # ZIP 내부 경로 구조를 유지하기 위해 상대 경로를 계산합니다.
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)
                file_count += 1

    print(f"백업 완료! 총 {file_count}개의 파일이 압축되었습니다.")
    print(f"저장 위치: {zip_path}")


# ==========================================
# 메인 메뉴 실행
# ==========================================
def main():
    while True:
        print("\n==============================")
        print("      Smart File Manager")
        print("==============================")
        print("1. 폴더 내 파일 목록 조회")
        print("2. 확장자별 파일 분류")
        print("3. 중복 파일 검색 (해시 비교)")
        print("4. 지정 폴더 ZIP 백업")
        print("0. 종료")
        print("==============================")

        choice = input("원하는 기능의 번호를 입력하세요: ").strip()

        if choice == "0":
            print("프로그램을 종료합니다.")
            break
        elif choice in ("1", "2", "3", "4"):
            folder_path = get_valid_folder_path()
            if folder_path is None:
                continue

            if choice == "1":
                list_files(folder_path)
            elif choice == "2":
                organize_by_extension(folder_path)
            elif choice == "3":
                find_duplicate_files(folder_path)
            elif choice == "4":
                backup_folder_to_zip(folder_path)
        else:
            print("[오류] 0~4 사이의 올바른 번호를 입력해주세요.")


if __name__ == "__main__":
    main()
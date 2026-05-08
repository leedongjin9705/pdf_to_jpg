import os
from pdf2image import convert_from_path
from PIL import Image

def pdf_to_single_image(pdf_path, output_path, poppler_path=None):
    try:
        print(f"\n[작업 시작] '{os.path.basename(pdf_path)}' 변환 중...")
        images = convert_from_path(pdf_path, poppler_path=poppler_path)
        
        if not images:
            print(f"⚠️ '{os.path.basename(pdf_path)}'에서 추출할 페이지가 없습니다.")
            return

        # 이미지 병합 로직
        widths, heights = zip(*(i.size for i in images))
        max_width = max(widths)
        total_height = sum(heights)

        new_im = Image.new('RGB', (max_width, total_height), (255, 255, 255))

        y_offset = 0
        for im in images:
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

        # 결과 저장 (JPG)
        new_im.save(output_path, 'JPEG', quality=95)
        print(f"✅ 완료: '{os.path.basename(output_path)}' 생성됨")

    except Exception as e:
        print(f"❌ '{os.path.basename(pdf_path)}' 처리 중 오류 발생: {e}")

# ==========================================
# 설정 부분
# ==========================================

# 1. Poppler 경로
poppler_dir = r"C:\Users\user\Downloads\Release-26.02.0-0\poppler-26.02.0\Library\bin"

# 2. 작업할 폴더 경로
base_dir = r"C:\Users\user\Downloads\RD\RD\Update (All TA) _업로드 요청 파일"

# 폴더 내의 모든 파일을 확인하여 .pdf로 끝나는 파일만 처리
files = os.listdir(base_dir)
pdf_files = [f for f in files if f.lower().endswith('.pdf')]

if not pdf_files:
    print("폴더 내에 PDF 파일이 없습니다. 경로를 확인해주세요.")
else:
    print(f"총 {len(pdf_files)}개의 PDF 파일을 찾았습니다. 변환을 시작합니다.")
    
    for filename in pdf_files:
        full_pdf_path = os.path.join(base_dir, filename)
        
        # 출력 파일명 설정 (예: '보고서.pdf' -> '보고서.jpg')
        output_filename = os.path.splitext(filename)[0] + ".jpg"
        full_output_path = os.path.join(base_dir, output_filename)
        
        # 변환 함수 실행
        pdf_to_single_image(full_pdf_path, full_output_path, poppler_path=poppler_dir)

    print("\n✨ 모든 작업이 끝났습니다!")
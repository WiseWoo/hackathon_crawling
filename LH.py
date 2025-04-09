import argparse
import boto3

# argparse로 CLI 인자 받기
parser = argparse.ArgumentParser()
parser.add_argument('--s3_bucket', type=str, required=True, help='S3 버킷 이름')
parser.add_argument('--s3_key_prefix', type=str, default='lh-notices', help='S3 내 저장 경로 prefix')
parser.add_argument('--aws_access_key', type=str, required=True, help='AWS Access Key')
parser.add_argument('--aws_secret_key', type=str, required=True, help='AWS Secret Key')
parser.add_argument('--aws_region', type=str, default='ap-northeast-2', help='AWS 리전')
args = parser.parse_args()

# boto3 S3 클라이언트 초기화
s3 = boto3.client('s3',
                  aws_access_key_id=args.aws_access_key,
                  aws_secret_access_key=args.aws_secret_key,
                  region_name=args.aws_region)


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import os
import time

download_dir = os.path.abspath("/Users/wisewoo/Hack/")
os.makedirs(download_dir, exist_ok=True)

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
options.add_argument('--headless')

prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# 랜딩 페이지 캘린더 페이지로 이동
driver.get("https://apply.lh.or.kr/lhapply/apply/sc/list.do?mi=1312")
time.sleep(7)

# 임대만 선택
select_cal = Select(driver.find_element(By.ID, "calSrchType"))
select_cal.select_by_value("01")  # 임대주택
time.sleep(1)

# 접수 하는것만 선택
select_recv = Select(driver.find_element(By.ID, "srchPanSs"))
select_recv.select_by_visible_text("접수")
time.sleep(1)

# 검색 버튼 클릭
driver.find_element(By.ID, "btnSah").click()
time.sleep(5)

# 오늘 날짜 기반 셀렉터 생성
today = datetime.datetime.today()
year = str(today.year)[2:]
month = f"{today.month:02d}"
day = f"{today.day:02d}"
selector_prefix = f"#\\32 0{year}{month}{day}"
calendar_selector = f"{selector_prefix} > a.btn_more.hash"

# 오늘 날짜의 버튼 클릭
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, calendar_selector))).click()
time.sleep(2)

# 팝업 안에서 공고 리스트 긁기
popup = wait.until(EC.presence_of_element_located((By.ID, 'popSchleMore')))
notice_items = popup.find_elements(By.CSS_SELECTOR, "li")

for idx in range(1, len(notice_items)+1):
    try:
        a_tag = notice_items[idx].find_element(By.CSS_SELECTOR, "dl > dt > a")
        href = a_tag.get_attribute("href")

        # 직접 링크 클릭이 아니라, 링크를 새로 여는 방식으로 처리 (팝업 클릭 안 함)
        driver.execute_script("window.open(arguments[0]);", href)
        driver.switch_to.window(driver.window_handles[-1])

        # 페이지 로딩 대기
        time.sleep(6)

        # 공고 pdf 다운로드: "공고" + ".pdf" 포함된 a 태그 클릭
        download_links = driver.find_elements(By.CSS_SELECTOR, "a")
        for link in download_links:
            text = link.text.strip()
            if "공고" in text and ".pdf" in text:
                link.click()
                time.sleep(5)

				# S3 업로드
				pdf_path = os.path.join(download_dir, text)
        s3_key = f"{args.s3_key_prefix}/{pdf_path}"
        s3.upload_file(pdf_path, args.s3_bucket, s3_key)
        print(f"✅ S3 업로드 완료: s3://{args.s3_bucket}/{s3_key}")
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

    except:
        pass
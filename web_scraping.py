from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def login_to_movacal(driver):
    print("ログインを待機中...")
    try:
        driver.get("https://s2.movacal.net/23.6/?pid=top&first_access=1731050023&patient_id=")
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.ID, "patient_search_top"))
        )
        print("ログイン完了。")
        return True
    except Exception as e:
        print(f"ログインに失敗しました: {e}")
        return False

def navigate_to_receipt(driver):
    try:
        receipt_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#tNavi li.no5 a"))
        )
        receipt_link.click()
        return True
    except TimeoutException:
        print("レセプトリンクが見つかりませんでした。")
        return False

def navigate_to_facility_list(driver):
    try:
        facility_list_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '施設別一覧')]"))
        )
        facility_list_link.click()
        return True
    except TimeoutException:
        print("施設別一覧リンクが見つかりませんでした。")
        return False

def navigate_to_qkan_cloud(driver):
    try:
        qkan_cloud_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//li[@class='tablist' and contains(text(), '給管帳連携')]"))
        )
        qkan_cloud_tab.click()
        return True
    except TimeoutException:
        print("給管帳連携タブが見つかりませんでした。")
        return False

def select_month_on_page(driver, selected_month):
    try:
        wait = WebDriverWait(driver, 10)
        month_select = wait.until(EC.presence_of_element_located((By.NAME, "month")))
        select = Select(month_select)
        select.select_by_value(selected_month)
        # URLの変更を待つ
        wait.until(EC.url_contains(f"month={selected_month}"))
        print(f"{selected_month}の月が選択されました。")
        # ページが完全に読み込まれるのを待つ
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list_table")))
    except Exception as e:
        print(f"月の選択に失敗しました: {e}")

def extract_patient_data_with_pagination(driver):
    all_patient_data = []
    page_number = 1
    while True:
        print(f"ページ {page_number} のデータを抽出中...")
        try:
            wait = WebDriverWait(driver, 10)
            table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "list_table")))
            rows = table.find_elements(By.TAG_NAME, "tr")[1:] # ヘッダー行をスキップ
            if not rows:
                print("テーブルにデータがありません。")
                break
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 5:
                    patient_data = {
                        "氏名": cells[1].text,
                        "生年月日": cells[2].text,
                        "要介護度": cells[3].text,
                        "サービス": cells[4].text
                    }
                    all_patient_data.append(patient_data)
            next_page = driver.find_elements(By.XPATH, "//a[contains(text(), '次へ')]")
            if next_page:
                next_page[0].click()
                wait.until(EC.staleness_of(table))
                page_number += 1
            else:
                print("全てのページのデータを抽出しました。")
                break
        except Exception as e:
            print(f"データの抽出中にエラーが発生しました: {e}")
            print(f"現在のURL: {driver.current_url}")
            print(f"ページソース: {driver.page_source[:500]}...")
            break
    return all_patient_data

def normalize_patient_data(patient_data):
    normalized_data = []
    for patient in patient_data:
        services = patient["サービス"].split()
        for service in services:
            normalized_patient = patient.copy()
            normalized_patient["サービス"] = service
            normalized_data.append(normalized_patient)
    return normalized_data

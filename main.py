from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.web_scraping import (
    login_to_movacal,
    navigate_to_receipt,
    navigate_to_facility_list,
    navigate_to_qkan_cloud,
    select_month_on_page,
    extract_patient_data_with_pagination,
)
from src.gui import select_month_gui
from src.file_operations import save_to_excel
def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    try:
        selected_month = select_month_gui()
        if selected_month is None:
            print("ユーザーが操作をキャンセルしました。")
            return
        if login_to_movacal(driver):
            if navigate_to_receipt(driver):
                if navigate_to_facility_list(driver):
                    if navigate_to_qkan_cloud(driver):
                        select_month_on_page(driver, selected_month)
                        patient_data = extract_patient_data_with_pagination(driver)
                        save_to_excel(patient_data, "患者リスト.xlsx")
                        print("患者リストがExcelファイルとして保存されました。")
                        input("処理が完了しました。Enterキーを押すとブラウザが閉じます...")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        driver.quit()
if __name__ == "__main__":
    main()

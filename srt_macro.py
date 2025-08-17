# edit date : 2024-07-15
# version : 2.0.0

import time
import random
import webbrowser
import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_macro(member_number, password, arrival, departure, standard_date, standard_time, from_train_number, to_train_number, try_waitlist):
    """SRT 예매 매크로를 실행합니다."""

    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    reserved = False

    yield "--------------- Start SRT Macro ---------------"

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        yield "웹 드라이버를 성공적으로 초기화했습니다."
    except Exception as e:
        yield f"웹 드라이버 초기화 실패: {e}"
        return

    try:
        driver.get('https://etk.srail.co.kr/cmc/01/selectLoginForm.do')
        driver.implicitly_wait(15)
        yield "로그인 페이지로 이동했습니다."

        driver.find_element(By.ID, 'srchDvNm01').send_keys(member_number)
        driver.find_element(By.ID, 'hmpgPwdCphd01').send_keys(password)
        yield "회원번호와 비밀번호를 입력했습니다."

        wait = WebDriverWait(driver, 10)
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div[4]/div/div[2]/form/fieldset/div[1]/div[2]/div[2]/div/div[2]/input")))
        login_button.click()
        driver.implicitly_wait(5)
        yield "로그인 버튼을 클릭했습니다."

        driver.get('https://etk.srail.kr/hpg/hra/01/selectScheduleList.do')
        driver.implicitly_wait(5)
        yield "기차 조회 페이지로 이동했습니다."

        dep_stn = driver.find_element(By.ID, 'dptRsStnCdNm')
        dep_stn.clear()
        dep_stn.send_keys(arrival)

        arr_stn = driver.find_element(By.ID, 'arvRsStnCdNm')
        arr_stn.clear()
        arr_stn.send_keys(departure)
        
        Select(driver.find_element(By.ID,"dptDt")).select_by_value(standard_date)
        Select(driver.find_element(By.ID, "dptTm")).select_by_visible_text(standard_time)
        yield f"{arrival}에서 {departure}로 가는 {standard_date} {standard_time}시 기차편을 조회합니다."

        driver.find_element(By.XPATH, "//input[@value='조회하기']").click()
        driver.implicitly_wait(5)

    except Exception as e:
        yield f"초기 설정 중 오류가 발생했습니다: {e}"
        driver.quit()
        return


    while st.session_state.get('running', False) and not reserved:
        try:
            for i in range(from_train_number, to_train_number + 1):
                if not st.session_state.get('running', False):
                    break
                
                try:
                    standard_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(7)").text
                    if "예약하기" in standard_seat:
                        yield f"{i}번째 기차에서 예약 가능한 좌석을 발견했습니다. 예약을 시도합니다."
                        driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[7]/a/span").click()
                        driver.implicitly_wait(3)

                        if driver.find_elements(By.ID, 'isFalseGotoMain'):
                            reserved = True
                            yield "🎉 예약 성공! 10초 후 예약 내역 페이지가 열립니다."
                            webbrowser.get(chrome_path).open("https://etk.srail.kr/hpg/hra/02/selectReservationList.do?pageId=TK0102010000")
                            st.session_state.running = False
                            break
                        else:
                            yield "잔여석이 없어 예약에 실패했습니다. 다시 시도합니다."
                            driver.back()
                            driver.implicitly_wait(5)
                except Exception:
                    pass # 예약하기 버튼이 없으면 다음으로

                if try_waitlist:
                    try:
                        standby_seat = driver.find_element(By.CSS_SELECTOR, f"#result-form > fieldset > div.tbl_wrap.th_thead > table > tbody > tr:nth-child({i}) > td:nth-child(8)").text
                        if "신청하기" in standby_seat:
                            yield f"{i}번째 기차에서 예약 대기를 발견했습니다. 대기를 신청합니다."
                            driver.find_element(By.XPATH, f"/html/body/div[1]/div[4]/div/div[3]/div[1]/form/fieldset/div[6]/table/tbody/tr[{i}]/td[8]/a/span").click()
                            driver.implicitly_wait(3)

                            if driver.find_elements(By.ID, 'isFalseGotoMain'):
                                reserved = True
                                yield "🎉 예약 대기 성공! 10초 후 예약 내역 페이지가 열립니다."
                                webbrowser.get(chrome_path).open("https://etk.srail.kr/hpg/hra/02/selectReservationList.do?pageId=TK0102010000")
                                st.session_state.running = False
                                break
                            else:
                                yield "예약 대기 신청에 실패했습니다. 다시 시도합니다."
                                driver.back()
                                driver.implicitly_wait(5)
                    except Exception:
                        yield f"{i}번째 기차는 예약 및 대기 신청이 불가능합니다."
                        pass
            
            if not reserved:
                # 서버 부하 및 차단 위험을 줄이기 위해 최소 3초 이상 랜덤 대기
                sleep_time = random.uniform(3, 7)
                yield f"조회된 모든 기차에 잔여석이 없습니다. {sleep_time:.1f}초 후(랜덤) 새로고침합니다."
                time.sleep(sleep_time)
                submit = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/div[2]/form/fieldset/div[2]/input")
                driver.execute_script("arguments[0].click();", submit)
                driver.implicitly_wait(10)

        except Exception as e:
            yield f"오류 발생: {e}. 페이지를 새로고침하고 다시 시도합니다."
            try:
                driver.refresh()
                driver.implicitly_wait(5)
            except Exception as refresh_e:
                yield f"새로고침 실패: {refresh_e}. 매크로를 종료합니다."
                st.session_state.running = False
                break
    
    if not st.session_state.get('running', False):
        yield "매크로가 중지되었습니다."
    
    driver.quit()
    yield "웹 드라이버를 종료했습니다."
import re
import time
from typing import List
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Crawl.function.action import click_button
from Crawl.function.download_process import download_to_local, move_location
from Crawl.function.fill_form import multi_check, scroll_select, filter_region, click_with_list
from Crawl.function.fill_calendar import find_from_date_vs_to_date, fill_date, calculate_month_vs_year

## Open main Web
def open_web(url: str, edge) -> None:
    """
    Send user name vs password then login

    Args:
        url: str
            link web

    Returns:
        None
    """

    edge.get(f"{url}")
    time.sleep(3)
    

def login(user: str, pw: str, edge) -> bool:
    """
    Send user name vs password then login

    Args:
        user: str
            user name 
        pw: str
            password of user account

    Returns:
        bool
    """
    try:
        WebDriverWait(edge, 20).until(
            EC.presence_of_element_located((By.ID, "txtUserid"))
        )
    finally:
        user_name = edge.find_element("id","txtUserid")
        pass_wd = edge.find_element("id","txtPasswd")
        user_name.send_keys(user)
        pass_wd.send_keys(pw)
        edge.find_element(By.ID,"btnLogin").click()
        del user_name
        del pass_wd

def turn_off_caution_if_exist(edge) -> None:
    """
    Whenever having many account login or login in many MAC, this caution happen

    Returns:
        None
    """
    time.sleep(1.7)
    try:
        WebDriverWait(edge, 5).until(
            EC.presence_of_element_located((By.ID, "SYS_ASCX_btnContinue"))
        )
    except:
        pass
    finally:
        click_button(id="SYS_ASCX_btnContinue",edge=edge)

def change_user_account(account: str, edge) -> None:
    """
    Send user name vs password then login

    Args:
        account: str
            id of role using in web

    Returns:
        None
    """
    turn_off_caution_if_exist(edge = edge)
    while True:
        try:
            time.sleep(2.7)
            click_button(id = "btnChangePosition", edge=edge)
            # click_button(id = "SYS_ASCX_drpNewPosition", edge = edge )
            elem = edge.find_element("id","SYS_ASCX_drpNewPosition")
            select = Select(elem)
            ## Choose user having value HQR64354
            select.select_by_value(account)
            click_button(id="SYS_ASCX_btnConfirm",edge=edge)
            break
        except:
            pass

def find_index_by_text(text_value: str, edge) -> str:
    """
    select search button on a row that having text needed
    
    Args:
        text_value: str
            name of row

    Returns:
        None
    """
    time.sleep(1.7)
    run_time=0
    while True:
        try:
            time.sleep(0.5)
            run_time += 0.5
            index_select = edge.find_element(By.XPATH, f"//span[contains(text(), '{text_value}')]")
            row_no = re.findall(r'\d+', index_select.get_attribute("id"))[0]
            break
        except:
            if run_time > 2:
                row_no = None
                break
            pass
    return row_no

def access_to_report(child_1: str, child_2: str, child_3: str, edge) -> None:
    """
    Download file to local
    
    Args:
      child_1: str
        navigation child 1 in report menu
      child_2: str
        navigation child of child 1
      child_3: str
        navigation child of child 2

    Returns:
      None
    """
    time.sleep(1.7)
    while True:
        try:
            time.sleep(2.7)
            edge.find_element(By.ID, f"{child_1}").click()
            edge.find_element(By.ID, f"{child_2}").click()
            edge.find_element(By.ID, f"{child_3}").click()
            break
        except:
            try:
                child_1_1 = edge.find_element(By.ID, f"{child_1}")
                child_1_2 = child_1_1.find_element(By.ID, f"{child_1}")
                child_1_2.find_element(By.ID, f"{child_1}").click()
                child_1_2.find_element(By.ID, f"{child_2}").click()
                child_1_2.find_element(By.ID, f"{child_3}").click()
            except:
                pass
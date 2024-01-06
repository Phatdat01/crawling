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
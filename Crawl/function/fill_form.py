import re
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Crawl.function.action import click_button

## search
def filter_region(value: str, edge) -> None:
    """
    Click to a button needed.
    
    Args:
        lst_of_click: List[str]
            list of multi tag to define button

    Returns:
        None
    """

    list_filter = edge.find_elements(By.XPATH, "//input[@placeholder='Enter keywords']")
    for fil in list_filter:
        try: 
            fil.send_keys(value)
        except:
            pass
      
## When item having multi tag
def click_with_list(lst_of_click: List[str], edge) -> None:
    """
    Click to a button needed.
    
    Args:
        lst_of_click: List[str]
            list of multi tag to define button

    Returns:
        None
    """

    for item in lst_of_click:
        try:
            time.sleep(0.1)
            item.click()
            break
        except:
            pass


## Check all box (filter if having filter)
def multi_check(edge) -> None:
    """
    Click all check box

    Returns:
        None
    # """
    # try:
    #     WebDriverWait(edge, 10).until(
    #         EC.presence_of_element_located((By.ID, "ui-multiselect-all"))
    #     )
    # finally:
    #     click_with_list(lst_of_click = edge.find_elements(By.CLASS_NAME, "ui-multiselect-all"), edge =edge)
    #     click_with_list(lst_of_click = edge.find_elements(By.CLASS_NAME, "ui-multiselect-close"), edge = edge)
    while True:
        try:
            time.sleep(0.7)
            click_with_list(lst_of_click = edge.find_elements(By.CLASS_NAME, "ui-multiselect-all"), edge =edge)
            click_with_list(lst_of_click = edge.find_elements(By.CLASS_NAME, "ui-multiselect-close"), edge = edge)
            break
        except:
            pass

def scroll_select(id: str, select_value: str, edge) -> None:
    """
    Download file to local
    
    Args:
        id: id
            id of element
        select_value: str
            name choose by visible text

    Returns:
        None
    """
    time.sleep(1.3)
    try:
        WebDriverWait(edge, 20).until(
            EC.presence_of_element_located((By.ID, id))
        )
    except:
        print("Error")
    finally:
        scroll = edge.find_element(By.ID, id)
        select = Select(scroll)
        select.select_by_visible_text(select_value)

def fill_info_hdr(edge) -> None:
    time.sleep(2.7)
    try:
        WebDriverWait(edge,10).until(
            EC.presence_of_element_located((By.ID, "pag_FW_SYS_INTF_JOB_btn_Add_Value"))
        )
    finally:
        while True:
            try:
                click_button(id="pag_FW_SYS_INTF_JOB_btn_Add_Value", edge = edge)
                time.sleep(2.3)
                try:
                    WebDriverWait(edge,10).until(
                        EC.presence_of_element_located((By.ID, "pag_FW_SYS_INTF_JOB_NewGeneral_JOB_DESC_Value"))
                    )
                finally:
                    print(edge.find_elements(By.ID, "pag_FW_SYS_INTF_JOB_NewGeneral_JOB_DESC_Value"))
                edge.find_element(By.ID, "pag_FW_SYS_INTF_JOB_NewGeneral_JOB_DESC_Value").send_keys("1")
                time.sleep(1)
                edge.find_element(By.ID, "pag_FW_SYS_INTF_JOB_NewGeneral_JOB_TIMEOUT_Value").send_keys("00")
                time.sleep(2)
                scroll_select(
                    id = "pag_FW_SYS_INTF_JOB_NewGeneral_JOB_TYPE_Value", 
                    select_value = "Export",
                    edge=edge
                )
                time.sleep(2.3)
                scroll_select(
                    id = "pag_FW_SYS_INTF_JOB_NewGeneral_EXE_TYPE_Value", 
                    select_value = "Manual/Ad hoc",
                    edge = edge
                )
                time.sleep(2.1)
                click_button(id = "pag_FW_SYS_INTF_JOB_RootNew_btn_Next_Value", edge = edge)
                time.sleep(2)
                click_button(id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_INTF_ID_SelectButton", edge = edge)
                break
            except:
                pass
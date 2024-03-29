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

def fix_navigation(edge) -> None:
    time.sleep(3)
    try:
        WebDriverWait(edge,50).until(
            EC.presence_of_element_located((By.ID, "li_more_nav_ROOT_tab_Main_nav_more_li"))
        )
    finally:
        child1s = edge.find_elements(By.ID,"li_more_nav_ROOT_tab_Main_nav_more_li")
        if len(child1s)>1:
            time.sleep(2)
        child1s = edge.find_elements(By.ID,"li_more_nav_ROOT_tab_Main_nav_more_li")
        for child1 in child1s:
            child1.click()   

def process_claim_section(text_value: str, downloads_path: str, date_flag: bool, edge) -> None:
    """
    Process 2 source on option 4
    
    Args:
      id: id
        id of element
    downloads_path: str
        path to take download file on local
    date_flag: bool
        date text calendar or scroll calendar

    Returns:
      None
    """
    time.sleep(2.7)
    source_name_list = ["CL02_PROMOTION_CLAIM_FOC","CL04_CRM"]
    date_now = datetime.now()
    text_of_date = datetime.strftime(date_now, "%Y%m%d")
    # click to source
    row_no = find_index_by_text(text_value=text_value,edge=edge)
    if row_no:
        click_button(
                id = f"pag_RPT_Overview_grd_ReportList_ctl{row_no}_btn_GoToReport_Value", 
                edge = edge
            )
    # fill month vs year
    if date_flag:
        # with date field is text calendar
        date_of_from_date, date_of_to_date = find_from_date_vs_to_date(date_now = date_now)
        fill_date(id = "pag_RPT_Filter_grd_RPT_ctl02_Control_dat_Value",input_date = date_of_from_date, edge = edge)
        fill_date(id = "pag_RPT_Filter_grd_RPT_ctl03_Control_dat_Value",input_date = date_of_to_date, edge = edge)
        click_button(id="pag_RPT_Filter_grd_RPT_ctl04_Control_drp_Value_ms",edge = edge)
        multi_check(edge)
    else:
        # with scroll date
        select_month, select_year = calculate_month_vs_year(date_now = date_now)
        time.sleep(1)
        scroll_select(id = "pag_RPT_Filter_grd_RPT_ctl02_Control_drp_Value", select_value = select_year, edge = edge)
        time.sleep(1)
        scroll_select(id = "pag_RPT_Filter_grd_RPT_ctl03_Control_drp_Value", select_value = select_month, edge = edge)
    time.sleep(1.9)
    click_button("pag_RPT_Filter_btn_Generate_Report_Value",edge = edge)
    # download file
    time.sleep(1)
    download_to_local(id = "rvrMain_ctl05_ctl04_ctl00_ButtonImg", edge = edge)
    # move file
    move_location(
        downloads_path = downloads_path, 
        text_of_date = text_of_date, 
        source_name_list = source_name_list,
        add_text = "",
        region = "", 
        edge = edge
    )

def fill_kc(region: str, downloads_path: str, date_now, add_text: str, source_name_list: List[str], edge) -> None:
    time.sleep(1.7)
    while True:
        try:
            time.sleep(1)
            text_of_date = datetime.strftime(date_now, "%Y%m%d")
            date_of_from_date, date_of_to_date = find_from_date_vs_to_date(date_now = date_now)
            if region == "GT" and date_of_to_date.day == 15:
                date_of_to_date = date_of_to_date - timedelta(days = 1)
            fill_date(id="pag_RPT_Filter_grd_RPT_ctl02_Control_dat_Value",input_date=date_of_from_date, edge=edge)
            # fill to date
            fill_date(id="pag_RPT_Filter_grd_RPT_ctl03_Control_dat_Value",input_date=date_of_to_date, edge=edge)
            time.sleep(1)
            click_button(id = "pag_RPT_Filter_grd_RPT_ctl04_Control_drp_Value_ms", edge = edge)
            if region:
                time.sleep(1)
                click_with_list(lst_of_click = edge.find_elements(By.CLASS_NAME, "ui-multiselect-none"), edge = edge)
                time.sleep(1)
                filter_region(value = region, edge = edge)
            time.sleep(2)
            multi_check(edge = edge)
            time.sleep(2)
            click_button(id="pag_RPT_Filter_grd_RPT_ctl05_Control_drp_Value_ms", edge = edge)
            multi_check(edge = edge)
            time.sleep(1)
            scroll_select(
                id = "pag_RPT_Filter_grd_RPT_ctl07_Control_drp_Value",
                select_value = "Confirmed",
                edge = edge
            )
            click_button(id = "pag_RPT_Filter_btn_Generate_Report_Value", edge = edge)
            ## Download file
            download_to_local(id = "rvrMain_ctl05_ctl04_ctl00_Button", edge = edge)
            move_location(
                downloads_path=downloads_path, 
                text_of_date=text_of_date, 
                source_name_list=source_name_list, 
                add_text=add_text, 
                region=region, 
                edge=edge
            )
            break
        except:
            pass

# For round 5
def kc_total(downloads_path: str, date_now, region_list: List[str], edge) -> None:
    """
    For work with OPI section, but still nothing
    
    Args:
        downloads_path: str
            link the the save when download
        text_of_date: str
            use for find folder move to
        file_name: str
            file name architecture
        region_list: List[str]
            region name list of file
    Returns:
        None
    """

    time.sleep(1.7)
    source_name_list = ["VN08_DIST_PROMOTION"]
    row_no = find_index_by_text(text_value = "Khuyến mãi Nhà Phân Phối (Promotion)", edge = edge)
    click_button(
                id = f"pag_RPT_Overview_grd_ReportList_ctl{row_no}_btn_GoToReport_Value", 
                edge = edge
            )
    if region_list == []:
        fill_kc(
            region = "", 
            downloads_path = downloads_path, 
            add_text = "", 
            date_now = date_now,
            source_name_list = source_name_list, 
            edge = edge
        )
    else:
        for region in region_list:
            fill_kc(
                region = region, 
                downloads_path = downloads_path, 
                add_text = f"_R3_", 
                date_now = date_now,
                source_name_list = source_name_list, 
                edge = edge
            )

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


def access_hdr_sec(text_value: str, edge) -> None:
    """
    Choose ar hdr or invoice to open
    
    Args:
        id: id
            id of hdr
        flag: bool
            ar or invoice

    Returns:
        None
    """
    time.sleep(0.7)
    while True:
        try:
            time.sleep(2)
            row_no = find_index_by_text(text_value = text_value, edge = edge)
            if row_no:
                click_button(
                    id = f"pop_Dynamic_grd_Main_ctl{row_no}_DynCol_INTF_ID_Value", 
                    edge = edge
                )
                break
            else:
                page = 2
                while True:
                    click_button(id=f"pop_Dynamic_grd_Main_GridListPagerList_Go_{page}", edge = edge)
                    time.sleep(2)
                    row_no = find_index_by_text(text_value = text_value, edge = edge)
                    if row_no:
                        click_button(
                            id = f"pop_Dynamic_grd_Main_ctl{row_no}_DynCol_INTF_ID_Value", 
                            edge = edge
                        )
                        break
                    page += 1
                break
        except:
            break
    time.sleep(2)
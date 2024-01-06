import os
import time
from typing import List
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Crawl.function.action import click_button
from Crawl.function.fill_form import multi_check, scroll_select
from Crawl.function.download_process import download_to_local, move_location
from Crawl.function.fill_calendar import find_from_date_vs_to_date, fill_date
from Crawl.function.access import find_index_by_text, access_to_report, kc_total, fix_navigation

def opi(downloads_path: str,date_now, region_list: List[str], edge) -> None:
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
    time.sleep(2.7)
    source_name_list = ["VN04_OFF_PUR_INV_OPI"]
    row_no = find_index_by_text(text_value = "Offtake-Inventory-Purchase: Off-Pur-Inv (OPI)", edge = edge)
    text_of_date = datetime.strftime(date_now,"%Y%m%d")
    click_button(
                id = f"pag_RPT_Overview_grd_ReportList_ctl{row_no}_btn_GoToReport_Value", 
                edge = edge
            )

    for region in region_list:
        while True:
            try:
                time.sleep(2)
                date_of_from_date, date_of_to_date = find_from_date_vs_to_date(date_now = date_now)
                if region == "GT" and date_of_to_date.day == 15:
                    date_of_to_date = date_of_to_date - timedelta(days = 1)
                fill_date(id="pag_RPT_Filter_grd_RPT_ctl02_Control_dat_Value",input_date=date_of_from_date, edge=edge)
                fill_date(id="pag_RPT_Filter_grd_RPT_ctl03_Control_dat_Value",input_date=date_of_to_date, edge=edge)
                croll=edge.find_element(By.ID, "pag_RPT_Filter_grd_RPT_ctl04_Control_drp_Value")
                select=Select(croll)
                select.select_by_index(region_list.index(region))
                time.sleep(0.7)
                try:
                    WebDriverWait(edge,10).until(
                        EC.presence_of_element_located((By.ID, "pag_RPT_Filter_grd_RPT_ctl05_Control_drp_Value_ms"))
                    )
                finally:
                    for i in range(2):
                        time.sleep(0.5)
                        scroll_select(
                            id = "pag_RPT_Filter_grd_RPT_ctl11_Control_drp_Value",
                            select_value = "Confirmed",
                            edge = edge
                        )
                        click_button(id = "pag_RPT_Filter_grd_RPT_ctl05_Control_drp_Value_ms", edge = edge)
                        time.sleep(1)
                        multi_check(edge = edge)
                time.sleep(0.9)
                print(edge.find_elements(By.ID,"pag_RPT_Filter_grd_RPT_ctl06_Control_drp_Value_ms"))
                click_button(id = "pag_RPT_Filter_grd_RPT_ctl06_Control_drp_Value_ms", edge = edge)
                multi_check(edge = edge)
                time.sleep(1.3)
                click_button(id = "pag_RPT_Filter_grd_RPT_ctl07_Control_drp_Value_ms", edge = edge)
                multi_check(edge = edge)
                click_button(id = "pag_RPT_Filter_grd_RPT_ctl08_Control_drp_Value_ms", edge = edge)
                multi_check(edge = edge)
                time.sleep(2.3)
                click_button(id = "pag_RPT_Filter_btn_Generate_Report_Value", edge = edge)
                ## Download file
                download_to_local(id = "rvrMain_ctl05_ctl04_ctl00_Button", edge = edge)
                # move_to_location(downloads_path, text_of_date, file_name, region)
                time.sleep(1.3)
                move_location(
                    downloads_path = downloads_path, 
                    text_of_date = text_of_date, 
                    source_name_list = source_name_list, 
                    add_text = "_R3_", 
                    region = region, 
                    edge = edge
                )
                break
            except:
                pass

def promotion_vs_opi(downloads_path: str, edge) -> None:
    """
    Action Crawl Data Round 3
    
    Args:
        downloads_path: str
            where the file is download
        file_names: str
            name of file
        region_list: str
            List of regions
        sections: str
            Name of section to download

    Returns:
        None
    """   
    REGION_LIST = ["ECOM","GT","MT","TRADER"]
    date_now = datetime.now()
    fix_navigation(edge = edge)
    access_to_report(
        child_1 = "li_more_nav_ROOT_tab_Main_nav_more_li",
        child_2 = "li_ROOT_tab_Main_itm_Report_li",
        child_3 = "li_pag_ReportRoot_tab_Inventory_itm_KC_Report_li",
        edge = edge
    )  

    kc_total(
        downloads_path = downloads_path, 
        date_now = date_now,
        region_list = REGION_LIST,
        edge = edge
    )
    click_button(id = "pag_RPT_Filter_btn_Back_Value", edge = edge)    
    opi(
        downloads_path = downloads_path,
        date_now = date_now,
        region_list = REGION_LIST,
        edge = edge
    )
    click_button(id = "pag_RPT_Filter_btn_Back_Value", edge = edge)
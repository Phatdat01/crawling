import os
import glob
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Crawl.function.action import click_button
from Crawl.function.download_process import download_ar
from Crawl.function.fill_form import scroll_select, fill_info_hdr
from Crawl.function.fill_calendar import fill_date, find_from_date_vs_to_date
from Crawl.function.access import access_to_report, access_hdr_sec, kc_total, fix_navigation


def access_invoice_dtl(downloads_path: str, text_of_date: str, edge) -> None:
    time.sleep(1)
    access_hdr_sec(text_value = "EXP_AR_INVOICE_DTL", edge=edge)
    # status
    time.sleep(2)
    scroll_select(id="pag_FW_SYS_INTF_JOB_DTL_PopupNew_FILE_TYPE_Value",select_value="D - Delimited", edge=edge)
    click_button(id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_FLD_SEPARATOR_STD_Value_0", edge = edge)
    time.sleep(1)
    scroll_select(
        id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl13_dyn_Field_drp_Value",
        select_value = "Invoiced",
        edge=edge
    )
    date_now = datetime.now()
    date_of_from_date, date_of_to_date = find_from_date_vs_to_date(date_now=date_now)
    fill_date(id="pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl15_dyn_Field_dat_Value",input_date=date_of_from_date, edge=edge)
    fill_date(id="pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl16_dyn_Field_dat_Value",input_date=date_of_to_date, edge=edge)
    time.sleep(2)
    download_ar(downloads_path=downloads_path, text_of_date=text_of_date, edge=edge)

def invoice_details_vs_promotion(downloads_path: str, edge) -> None:
    """
    Action Crawl Data Round 5

    Returns:
        None
    """   
    date_now = datetime.now()
    text_of_date = datetime.strftime(date_now,"%Y%m%d")
    REGION_LIST = ["ECOM","GT","MT","TRADER"]
    time.sleep(3)
    fix_navigation(edge = edge)
    access_to_report(
        child_1="li_more_nav_ROOT_tab_Main_nav_more_li",
        child_2="li_ROOT_tab_Main_itm_SysAdminSetup_li",
        child_3="li_pag_Sys_Root_tab_Detail_itm_Job_AR_li",
        edge=edge
    )  

    fill_info_hdr(edge = edge)
    access_invoice_dtl(downloads_path=downloads_path, text_of_date=text_of_date, edge=edge)
    
    if not os.path.exists(f"source/{dir}/VN08_DIST_PROMOTION.csv"):  
        # edge.find_element(By.XPATH, "//*[@id='li_more_nav_ROOT_tab_Main_nav_more_li']//*[@id='li_more_nav_ROOT_tab_Main_nav_more_li']//*[@id='li_more_nav_ROOT_tab_Main_nav_more_li']").click()
        fix_navigation(edge=edge)
        time.sleep(2)
        access_to_report(
            child_1 = "li_more_nav_ROOT_tab_Main_nav_more_li",
            child_2 = "li_ROOT_tab_Main_itm_Report_li",
            child_3 = "li_pag_ReportRoot_tab_Inventory_itm_KC_Report_li",
            edge = edge
        )  
        time.sleep(1.7)
        kc_total(
            downloads_path = downloads_path, 
            date_now = date_now, 
            region_list = [], 
            edge = edge
        )
        click_button(id = "pag_RPT_Filter_btn_Back_Value", edge = edge)


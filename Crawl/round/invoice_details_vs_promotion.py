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


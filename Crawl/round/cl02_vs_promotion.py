import os
import time
from datetime import datetime

from Crawl.function.action import click_button
from Crawl.function.access import access_to_report, process_claim_section, kc_total, fix_navigation
from Crawl.function.fill_calendar import find_from_date_vs_to_date, fill_date, calculate_month_vs_year

def cl02_vs_promotion(downloads_path: str, edge) -> None:
    """
    Action Crawl Data Round 1

    Returns:
        None
    """
    date_now = datetime.now()
    fix_navigation(edge=edge)
    access_to_report(
        child_1 = "li_more_nav_ROOT_tab_Main_nav_more_li",
        child_2 = "li_ROOT_tab_Main_itm_Report_li",
        child_3 = "li_pag_ReportRoot_tab_Inventory_itm_Claims_li",
        edge = edge
    )  
    # Source 1
    process_claim_section(text_value = "BẢNG KÊ CHI TIẾT HÓA ĐƠN", downloads_path = downloads_path, date_flag= True, edge = edge)
    click_button(id = "pag_RPT_Filter_btn_Back_Value", edge = edge)
    dir = sorted(os.listdir("source"))[-1]
    if not os.path.exists(f"source/{dir}/VN08_DIST_PROMOTION.csv"):
        fix_navigation(edge=edge)
        access_to_report(
            child_1 = "li_more_nav_ROOT_tab_Main_nav_more_li",
            child_2 = "li_ROOT_tab_Main_itm_Report_li",
            child_3 = "li_pag_ReportRoot_tab_Inventory_itm_KC_Report_li",
            edge = edge
        )  
        time.sleep(2)
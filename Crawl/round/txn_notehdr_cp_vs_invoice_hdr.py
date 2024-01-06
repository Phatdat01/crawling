import glob
import time
from datetime import datetime
from selenium.webdriver.support.select import Select

from Crawl.function.action import click_button
from Crawl.function.download_process import download_ar
from Crawl.function.fill_form import scroll_select, fill_info_hdr
from Crawl.function.fill_calendar import fill_date, find_from_date_vs_to_date
from Crawl.function.access import access_to_report, access_hdr_sec, fix_navigation

def txn_notehdr_cp_vs_invoice_hdr(downloads_path: str, edge) -> None:
    """
    Action Crawl Data Round hdr ar vs invoice

    Returns:
        None
    """   
    text_of_date = datetime.strftime(datetime.now(),"%Y%m%d")
    fix_navigation(edge = edge)
    access_to_report(
        child_1="li_more_nav_ROOT_tab_Main_nav_more_li",
        child_2="li_ROOT_tab_Main_itm_SysAdminSetup_li",
        child_3="li_pag_Sys_Root_tab_Detail_itm_Job_AR_li",
        edge=edge
    )  
    fill_info_hdr(edge=edge)
    # Access to ar hdr
    access_hdr(
        status_id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl10_dyn_Field_drp_Value",
        select_value_status_id = "Confirmed",
        from_date_id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl13_dyn_Field_dat_Value",
        to_date_id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl14_dyn_Field_dat_Value",
        text_name_souce = "EXP_AR_CN_HDR",
        downloads_path = downloads_path, 
        text_of_date = text_of_date, 
        edge = edge
    )

    fill_info_hdr(edge=edge)
    # Access to invoiced hdr
    access_hdr(
        status_id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl13_dyn_Field_drp_Value",
        select_value_status_id = "Invoiced",
        from_date_id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl15_dyn_Field_dat_Value",
        to_date_id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_grd_DynamicFilter_ctl16_dyn_Field_dat_Value",
        text_name_souce = "EXP_AR_INVOICE_HDR",
        downloads_path = downloads_path, 
        text_of_date = text_of_date,  
        edge = edge
    )
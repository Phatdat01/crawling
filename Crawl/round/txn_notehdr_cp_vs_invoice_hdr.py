import glob
import time
from datetime import datetime
from selenium.webdriver.support.select import Select

from Crawl.function.action import click_button
from Crawl.function.download_process import download_ar
from Crawl.function.fill_form import scroll_select, fill_info_hdr
from Crawl.function.fill_calendar import fill_date, find_from_date_vs_to_date
from Crawl.function.access import access_to_report, access_hdr_sec, fix_navigation

def access_hdr(
    status_id: str,
    select_value_status_id: str,
    from_date_id: str,
    to_date_id: str,
    text_name_souce: str, 
    downloads_path: str, 
    text_of_date: str, 
    edge
) -> None:
    time.sleep(2.7)
    access_hdr_sec(text_value = text_name_souce, edge=edge)
    # status
    time.sleep(2)
    scroll_select(
        id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_FILE_TYPE_Value",
        select_value = "D - Delimited", 
        edge = edge
    )
    click_button(id = "pag_FW_SYS_INTF_JOB_DTL_PopupNew_FLD_SEPARATOR_STD_Value_0", edge = edge)
    time.sleep(1)
    scroll_select(
        id = status_id,
        select_value = select_value_status_id,
        edge=edge
    )
    time.sleep(1)
    date_now = datetime.now()
    date_of_from_date, date_of_to_date = find_from_date_vs_to_date(date_now=date_now)
    # fill from date
    fill_date(id = from_date_id,input_date = date_of_from_date, edge = edge)
    # fill to date
    time.sleep(1)
    fill_date(id = to_date_id, input_date = date_of_to_date, edge = edge)
    download_ar(downloads_path=downloads_path, text_of_date=text_of_date, edge=edge)

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
import os
import re
import glob
import time
import shutil
import pandas as pd
from typing import List
from datetime import datetime
from Crawl.function.action import click_button
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_latest_file(downloads_path: str) -> str:
    files = glob.glob(f"{downloads_path}/*.csv", recursive=False)
    files.sort(key=os.path.getmtime)
    file = files[-1].split("\\")[-1]
    return file

def download_ar(downloads_path: str, text_of_date: str, edge) -> None:
    while True:
        try:
            time.sleep(1.7)
            click_button(id="pag_FW_SYS_INTF_JOB_DTL_PopupNew_btn_Add_Value", edge=edge)
            time.sleep(1.7)
            click_button(id="pag_FW_SYS_INTF_JOB_RootNew_btn_Save_Value", edge=edge)
            time.sleep(1.7)
            click_button(id="TF_Prompt_btn_Ok_Value", edge=edge)
            time.sleep(5.9)
            try:
                WebDriverWait(edge,50).until(
                    EC.presence_of_element_located((By.ID, "pag_FW_SYS_INTF_STATUS_JOB_btn_Download_Value"))
                )
            finally:
                click_button(id="pag_FW_SYS_INTF_STATUS_JOB_btn_Download_Value", edge=edge)
            while True:
                try:
                    time.sleep(2.7)
                    while True:
                        files = glob.glob(f"{downloads_path}/*.zip", recursive=False)
                        if files:
                            break
                        time.sleep(1)
                    files.sort(key=os.path.getmtime)
                    zip_path = files[-1].replace("\\","/")
                    if os.path.exists(zip_path):
                        shutil.unpack_archive(zip_path, f"source/{text_of_date}")
                        time.sleep(3)
                        os.remove(zip_path)
                        edge.switch_to.window(edge.window_handles[-1])
                        edge.close()
                        edge.switch_to.window(edge.window_handles[0])
                    time.sleep(1)
                    try:
                        WebDriverWait(edge,50).until(
                            EC.presence_of_element_located((By.ID, "pag_FW_SYS_INTF_STATUS_JOB_btn_Back_Value"))
                        )
                    finally:
                        click_button(id="pag_FW_SYS_INTF_STATUS_JOB_btn_Back_Value",edge=edge)
                    break
                except:
                    break
            break
        except:
            break

def download_to_local(id: str, edge) -> None:
    """
    Download file to local
    
    Args:
        id: str
            id of button download

    Returns:
        None
    """

    # Download file
    while True:
        try:
            time.sleep(7)
            click_button(id = id,edge=edge)
            edge.find_element(By.XPATH, "//a[contains(text(),'CSV')]").click()
            break
        except:
            pass
    

def move_location(downloads_path: str, text_of_date: str, source_name_list: List[str], add_text: str, region: str, edge) -> None:
    """
    Move file to a storage
    
    Args:
        downloads_path: str
            where the file is download
        text_of_date: str
            region want to download
        add_text: str
            add to name of file
        region: str
            region want to download

    Returns:
        None
    """
    while True:
        time.sleep(2.7)
        target_file=""
        source_file = get_latest_file(downloads_path = downloads_path)
        for name in source_name_list:
            print(name)
            if name in source_file:
                # Replace integer example values " (1)." to "."
                target_file = re.sub(r" \(\d+\).csv", "", source_file)
                target_file = re.sub(r".csv", "", target_file)
                break
        if target_file:
            break
    while True:
        try:
            time.sleep(1.7)
            fi = pd.read_csv(f"{downloads_path}\\{source_file}", skiprows = 3,encoding = 'utf8')
            if "CL02_PROMOTION_CLAIM_FOC" in source_file:
                fi = fi.groupby(["Customer5"],as_index=False)["Customer10"].max()
                fi.columns = ["Program_ID","Total"]
                time.sleep(1)
            fi.to_csv(f"{downloads_path}\\{source_file}",encoding = 'utf-8-sig')
            time.sleep(2)
            shutil.move(f"{downloads_path}\\{source_file}", f"source/{text_of_date}/{target_file}{add_text}{region}.csv")
            ## Back to main reparing for download
            break
        except:
            pass
    time.sleep(1)
    click_button(id = "btnReportBack", edge = edge)
        
# def move_to_location(downloads_path: str, text_of_date: str, file_name: str, region: str, edge) -> None:
#     """
#     Move file to a storage
    
#     Args:
#         downloads_path: str
#             where the file is download
#         text_of_date: str
#             region want to download
#         file_name: str
#             name of file
#         region: str
#             region want to download

#     Returns:
#         None
#     """

#     while True:
#         try:
#             time.sleep(5)
#             file = os.listdir(downloads_path)[-1]
#             fi = pd.read_csv(f"{downloads_path}\{file}",skiprows = 3,encoding = 'utf8')
#             fi.to_csv(f"{downloads_path}\{file}",encoding = 'utf-8-sig')
#             shutil.move(f"{downloads_path}\{file}", f"./source/{text_of_date}/{file_name}{region}.csv")
#             ## Back to main reparing for download
#             click_button(id = "btnReportBack", edge = edge)
#             break
#         except:
#             pass

def create_source(date_now) -> None:
    text_of_date = datetime.strftime(date_now,"%Y%m%d")
    if not os.path.exists(f"source"):
        os.makedirs(f"source")
    if not os.path.exists(f"source/{text_of_date}"):
        os.makedirs(f"source/{text_of_date}")
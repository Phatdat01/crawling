import json
import time
from pathlib import Path
from datetime import datetime
from selenium import webdriver

from Crawl.function.download_process import create_source
from Crawl.round.promotion_vs_opi import promotion_vs_opi
from Crawl.round.crm_vs_promotion import crm_vs_promotion
from Crawl.round.cl02_vs_promotion import cl02_vs_promotion
from Crawl.function.access import open_web, login, change_user_account
from Crawl.round.invoice_details_vs_promotion import invoice_details_vs_promotion
from Crawl.round.txn_notehdr_cp_vs_invoice_hdr import txn_notehdr_cp_vs_invoice_hdr

DOWNLOAD_PATH = str(Path.home() / "Downloads")
FILE_NAME = "VN08_DIST_PROMOTION_R3_"

data = json.load(open('credentials.json'))
# edge = webdriver.Edge(f"{data.get('driver')}")

# selenium 3
# from selenium import webdriver
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# edge = webdriver.Edge(EdgeChromiumDriverManager().install())

# selenium 4
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
edge = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))


def crawl_data(status_login: bool, option: str) -> bool:
    """
    Crawl vs process data
    
    Args:
        option: int
            option in theme where 2 source to compare

    Returns:
        True
    """ 
    open_web(url=data.get('url'), edge = edge)
    print(status_login)
    if not status_login:
        login(
            user = data.get('name'),
            pw = data.get('pass'),
            edge = edge
        )
        change_user_account(account="HQR64354", edge = edge)
    else:
        pass
    time.sleep(2)
    date_now = datetime.now()
    create_source(date_now = date_now)
    if option == "TXN_NOTEHDR_CP vs INVOICE_HDR":
        txn_notehdr_cp_vs_invoice_hdr(downloads_path=DOWNLOAD_PATH,edge = edge)
    elif option == "Promotion vs OPI":
        promotion_vs_opi(downloads_path=DOWNLOAD_PATH,edge = edge)
    elif option == "CRM vs Promotion":
        crm_vs_promotion(downloads_path=DOWNLOAD_PATH, edge=edge)
    elif option == "CL02 vs Promotion":
        cl02_vs_promotion(downloads_path=DOWNLOAD_PATH, edge=edge)
    else:
        invoice_details_vs_promotion(downloads_path=DOWNLOAD_PATH, edge=edge)
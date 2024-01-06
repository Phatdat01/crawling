
import time
from typing import Tuple
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def calculate_month_vs_year(date_now) -> Tuple[str]:
    report_collect_date = date_now
    if date_now.day == 1:
        report_collect_date = date_now - timedelta(days=1)
    select_month = report_collect_date.month
    select_year = report_collect_date.year
    return str(select_month),str(select_year)

def find_from_date_vs_to_date(date_now) -> Tuple[str]:
    """
    Calculate from date vs to date depend on date now
    
    Args:
        date_now: Date
            current date

    Returns:
        None
    """

    # get the first day 
    date_of_from_date=date_now.replace(day=1)
    # Change to next month, then just subtract num of day
    next_month = date_now.replace(day=28) + timedelta(days=4)
    # date_of_to_date=next_month - timedelta(days=next_month.day)
    # temp take current day
    date_of_to_date=date_now
    # if current day is day 1, change to the previous month
    if date_now.day==1:
        date_of_to_date = date_of_from_date - timedelta(days=1)
        date_of_from_date =date_of_to_date.replace(day=1)
    return date_of_from_date, date_of_to_date

def fill_date(id: str, input_date, edge) -> None:
    """
    Fill to calendar with date in type text
    
    Args:
        id: str
            id of date field
        fill_date: str
            date to fill, architecture "%d%m%Y"

    Returns:
        None
    """    
    # time.sleep(1)
    try:
        WebDriverWait(edge, 20).until(
            EC.presence_of_element_located((By.ID, id))
        )
    finally:
        edit_date = edge.find_element(By.ID, id)
        edit_date.send_keys(datetime.strftime(input_date,'%d%m%Y'))
        edit_date.send_keys(Keys.ESCAPE)
        edit_date.send_keys(datetime.strftime(input_date, '%d%m%Y'))
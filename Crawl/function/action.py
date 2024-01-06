import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def click_button(id: str, edge) -> None:
    time.sleep(0.9)
    try:
        WebDriverWait(edge,50).until(
            EC.presence_of_element_located((By.ID, id))
        )
    finally:
        edge.find_element(By.ID, id).click()
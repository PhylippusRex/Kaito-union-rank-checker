import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def get_rank(username):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://yaps.kaito.ai/union")
    time.sleep(5)


    usernames = []
    last_height = driver.execute_script("return document.body.scrollHeight")


    while len(usernames) < 1000:
        cards = driver.find_elements(By.CSS_SELECTOR, "div.flex.flex-col.items-center.text-xs")
        for card in cards:
            handle = card.text.strip()
            if handle.startswith('@') and handle not in usernames:
                usernames.append(handle)
                if handle.lower() == username.lower():
                    driver.quit()
                    return len(usernames)


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


    driver.quit()
    return None


# Streamlit UI
st.title("Kaito Union Rank Checker")
user_input = st.text_input("Enter your X (Twitter) handle (include @):")


if st.button("Check Rank"):
    with st.spinner("Checking leaderboard..."):
        rank = get_rank(user_input.strip())
        if isinstance(rank, int):
            st.success(f"🏆 {user_input} is ranked #{rank}")
        elif rank is None:
            st.warning("❌ You're not in the top 1000.")
        else:
            st.error(rank)
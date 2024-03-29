
import os
import streamlit as st
import time
from pytz import timezone 
from datetime import datetime
import pandas as pd
import numpy as np
import json
#when we import hydralit, we automatically get all of Streamlit
import hydralit as hy
from source.process_data import check_url_is_valid
from source.crawl_with_selenium import selenium_read_img_in_json, selenium_save_image_list, delete_all_images_file, save_selenium_dataframe
from source.crawl_with_beautiful import initial_beautiful_soup, beautiful_save_image_list, beautiful_dataframe


from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

path = os.getcwd()
print(path)
origin_path = path.replace("/source", "")
data_path = origin_path + "/data/crawl_by_network"
selenium_image_path = data_path +  "/selenium_images"
print(data_path)
print(selenium_image_path)

# style
th_props = [
  ('font-size', '16px'),
  ('text-align', 'center'),
  ('font-weight', 'bold'),
  ('color', '#6d6d6d'),
  ('background-color', '#f7ffff')
  ]
                               
td_props = [
  ('font-size', '16px')
  ]
                                 
styles = [
  dict(selector="th", props=th_props),
  dict(selector="td", props=td_props)
  ]


st.set_page_config(
    page_title="Crawl all images og any website",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': "https://www.google.com",
        'Report a bug': "https://www.google.com",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

app = hy.HydraApp(title='Crawl all images of any website')
st.title('Crawl all images of any website')
st.info("Crawl all images of any website", icon="🚨")

# @st.experimental_singleton
# def get_driver():
#     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=Options)
# @st.experimental_singleton
# def installff():
#   os.system('sbase install geckodriver')
#   os.system('ln -s /home/appuser/venv/lib/python3.9/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

URL = ""
TIMEOUT = 20



def initial_selenium(url: str, path_file: str):
    # @st.experimental_memo 
    # def get_driver():
    #     return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # options = uc.ChromeOptions()
    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    # options.headless=True
    # options.add_argument('--headless')
    # options.add_argument('headless')
  
    # # Ignores any certificate errors if there is any
    # options.add_argument("--ignore-certificate-errors")
    # driver = uc.Chrome(options=options)
   

    # desired_capabilities = DesiredCapabilities.CHROME
    # desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
  
    # options = Options()
    # options.add_argument('--disable-gpu')
    # options.add_argument('--headless')
    # # options.add_argument("--ignore-certificate-errors")

    # driver = get_driver()
    desired_capabilities = DesiredCapabilities.FIREFOX
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
  
    st.title("Test Selenium")

    firefoxOptions = Options()
    firefoxOptions.add_argument("--headless")
    # firefoxOptions.add_argument('--disable-gpu')
    # firefoxOptions.add_argument("--ignore-certificate-errors")
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(
        options=firefoxOptions,
        service=service,
    )

    # Create the webdriver object and pass the arguments
    # options = webdriver.ChromeOptions()
  
    # # Chrome will start in Headless mode
    # options.add_argument('headless')
  
    # # Ignores any certificate errors if there is any
    # options.add_argument("--ignore-certificate-errors")
  
    # # Startup the chrome webdriver with executable path and
    # # pass the chrome options and desired capabilities as
    # # parameters.
    # # driver = webdriver.Chrome(chrome_options=options)
    # driver= webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # # driver = get_driver()
    
  
    # Send a request to the website and let it load
    driver.get(url)
  
    # Sleeps for 10 seconds
    time.sleep(10)
  
    # Gets all the logs from performance in Chrome
    logs = driver.get_log("performance")
    
    print(path_file)
    # Opens a writable JSON file and writes the logs in it
    with open("{path}/network_log.json".format(path=path_file), "w", encoding="utf-8") as f:
        print("json is writing")
        f.write("[")
  
        # Iterates every logs and parses it using JSON
        for log in logs:
            network_log = json.loads(log["message"])["message"]
  
            # Checks if the current 'method' key has any
            # Network related value.
            if("Network.response" in network_log["method"]
                    or "Network.request" in network_log["method"]
                    or "Network.webSocket" in network_log["method"]):
  
                # Writes the network log to a JSON file by
                # converting the dictionary to a JSON string
                # using json.dumps().
                f.write(json.dumps(network_log)+",")
        f.write("{}]")
  
    print("Quitting Selenium WebDriver")
    driver.quit()
    return True


def selenium_read_img_in_json(path_file: str):
    # Read the JSON File and parse it using
    # json.loads() to find the urls containing images.

    json_file_path = "{path}/network_log.json".format(path=path_file)
    with open(json_file_path, "r", encoding="utf-8") as f:
        logs = json.loads(f.read())
  
    # Iterate the logs
    images_url = []
    for log in logs:
  
        # Except block will be accessed if any of the
        # following keys are missing.
        try:
            # URL is present inside the following keys
            url = log["params"]["request"]["url"]
  
            # Checks if the extension is .png or .jpg
            if url[len(url)-4:] == ".png" or url[len(url)-4:] == ".jpg" or url[len(url)-4:] == ".svg" :
                print(url, end='\n\n')
                images_url.append(url)
        except Exception as e:
            pass

    return images_url


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

def get_now():
    now = datetime.now(timezone("Asia/Ho_Chi_Minh"))
    now_time =  now.strftime("%Y%m%d_%H%M%S")
    return now_time

def download_csv(df):
    csv = convert_df(df)
    now_time = get_now()

    st.download_button(
        label="👉 Download data as CSV",
        data=csv,
        file_name='{now_time}_gmail_file.csv'.format(now_time=now_time),
        mime='text/csv',
    )

def link_input_fnc():
    st.text_input("url or link of any website", key="name")

    # You can access the value at any point with:
    return st.session_state.name

def button_acction(url=None):

    if st.button('Crawl all images'):
        link_status = check_url_is_valid(url)
        if link_status is True:
            ## selenium crawl by network
            initial_selenium(url=url, path_file=data_path)
            images_list = selenium_read_img_in_json(path_file=data_path)
            delete_all_images_file(selenium_image_path)
            index_l, url_l, file_name_l, image_name_l, status_l = selenium_save_image_list(images_list, selenium_image_path)
            save_selenium_dataframe(data_path, index_l, url_l, file_name_l, image_name_l, status_l)
            print("crawl by selenium is sucessful")
            last_index = len(index_l) + 1
            
            ## beautiful crawl
            beautiful_images_list = initial_beautiful_soup(url=url)
            index_l, url_l, file_name_l, image_name_l, status_l = beautiful_save_image_list(last_index = last_index,images_list = beautiful_images_list, path_folder=selenium_image_path)
            beautiful_df = beautiful_dataframe(index_l, url_l, file_name_l, image_name_l, status_l)
            print("crawl by beautiful is sucessful")

            beautiful_df.to_csv("{data_path}/beautiful_df.csv".format(data_path=data_path), index=False)
            beautiful_df = pd.read_csv("{data_path}/beautiful_df.csv".format(data_path=data_path))
            selenium_df = pd.read_csv("{data_path}/selenium_df.csv".format(data_path=data_path))
            # print("exported is sucessful")
            
            df_new = pd.concat([selenium_df, beautiful_df])
            df_new.to_csv("{data_path}/final_df.csv".format(data_path=data_path))

            total_images = len(df_new['file_name'])
            st.text("total images:" + str(total_images))
             # show images grid
            filteredImages = list(selenium_image_path + "/" + df_new['file_name'])
            caption = list(df_new['image_name'])

            idx = 0 
            for _ in range(len(filteredImages)-1): 
                cols = st.columns(4) 
                
                if idx < len(filteredImages): 
                    cols[0].image(filteredImages[idx], width=150, caption=caption[idx])
                idx+=1
                
                if idx < len(filteredImages):
                    cols[1].image(filteredImages[idx], width=150, caption=caption[idx])
                idx+=1

                if idx < len(filteredImages):
                    cols[2].image(filteredImages[idx], width=150, caption=caption[idx])
                idx+=1 
                if idx < len(filteredImages): 
                    cols[3].image(filteredImages[idx], width=150, caption=caption[idx])
                    idx = idx + 1
                else:
                    break

            # table
            with st.expander("Table data"):
                # st.subheader(result)
            # Display the dataframe and allow the user to stretch the dataframe
            # across the full width of the container, based on the checkbox value
                st.table(df_new)
                download_csv(df_new)
        else:
            st.subheader("Invalid URL")

       
    else: 
        st.write(f'Click the button to process') 


# if __name__=='__main__':

@app.addapp()
def search():
    snow_mode = st.checkbox('Snow mode')
    if snow_mode:
        st.snow()
    with st.expander("Guideline"):
            st.subheader("The steps of tools:")
            st.text("1. You will input your links which you need to download all images with automations")
            st.text("2. We will waiting relax time to the system will be processed")
            st.text("3. All images is crawled which will display on below grid table")
            st.text("4. Finally, you can download all your images via .zip file")
            st.text("Thank you !!!")

    st.subheader("Input here")
    link_variable = link_input_fnc()
    st.subheader(link_variable)
    
    button_acction(url=link_variable)
    

@app.addapp()
def info():
    hy.info('Info')

#Run the whole lot, we get navbar, state management and app isolation, all with this tiny amount of work.
app.run()

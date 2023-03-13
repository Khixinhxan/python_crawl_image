from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
import json
from urllib.request import urlretrieve
import os, shutil
import pandas as pd

import streamlit as st

# @st.experimental_singleton
# def get_driver(options):
    # return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)



# def initial_selenium(url: str, path_file: str):
#     # options = uc.ChromeOptions()
#     # desired_capabilities = DesiredCapabilities.CHROME
#     # desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
#     # options.headless=True
#     # options.add_argument('--headless')
#     # options.add_argument('headless')
  
#     # # Ignores any certificate errors if there is any
#     # options.add_argument("--ignore-certificate-errors")
#     # driver = uc.Chrome(options=options)
   

#     desired_capabilities = DesiredCapabilities.CHROME
#     desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
  
#     # Create the webdriver object and pass the arguments
#     options = webdriver.ChromeOptions()
  
#     # Chrome will start in Headless mode
#     options.add_argument('headless')
  
#     # Ignores any certificate errors if there is any
#     options.add_argument("--ignore-certificate-errors")
  
#     # Startup the chrome webdriver with executable path and
#     # pass the chrome options and desired capabilities as
#     # parameters.
#     # driver = webdriver.Chrome(chrome_options=options)
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     # driver = get_driver(options)
    
  
#     # Send a request to the website and let it load
#     driver.get(url)
  
#     # Sleeps for 10 seconds
#     time.sleep(10)
  
#     # Gets all the logs from performance in Chrome
#     logs = driver.get_log("performance")
    
#     print(path_file)
#     # Opens a writable JSON file and writes the logs in it
#     with open("{path}/network_log.json".format(path=path_file), "w", encoding="utf-8") as f:
#         print("json is writing")
#         f.write("[")
  
#         # Iterates every logs and parses it using JSON
#         for log in logs:
#             network_log = json.loads(log["message"])["message"]
  
#             # Checks if the current 'method' key has any
#             # Network related value.
#             if("Network.response" in network_log["method"]
#                     or "Network.request" in network_log["method"]
#                     or "Network.webSocket" in network_log["method"]):
  
#                 # Writes the network log to a JSON file by
#                 # converting the dictionary to a JSON string
#                 # using json.dumps().
#                 f.write(json.dumps(network_log)+",")
#         f.write("{}]")
  
#     print("Quitting Selenium WebDriver")
#     driver.quit()
#     return True


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

def selenium_save_image(url: str, folder: str, file_name: str):
    try:
        urlretrieve("{url}".format(url=url), "{path}/{file_name}".format(path=folder, file_name=file_name))
        return True
    except Exception as e:
        return False
    

def selenium_save_image_list(images_url: list, path_folder: str ):
    x = 0
    url_l = []
    index_l = []
    file_name_l = []
    image_name_l = []
    status_l = []
    for i in images_url:
        if i is None:
            continue
        if "http" not in i:
            i = "https:" + i
        print(i)
        x = x+1
        image_name_temp = i.split('/').pop()
        image_name = None
        if ".svg" in i:
            file_name = str(x) + ".svg"
            image_name = image_name_temp.replace(".svg", "")
        if ".png" in i:
            file_name = str(x) + ".png"
            image_name = image_name_temp.replace(".png", "")
        if ".jpg" in i:
            file_name = str(x) + ".jpg"
            image_name = image_name_temp.replace(".jpg", "")

        url_l.append(i)
        index_l.append(x)
        file_name_l.append(file_name)
        image_name_l.append(image_name)
        status = selenium_save_image(url=i, folder=path_folder, file_name=file_name)
        status_l.append(status)
    
    return index_l, url_l, file_name_l, image_name_l, status_l

def delete_all_images_file(selenium_image_path: str) -> bool:
    if len(os.listdir(selenium_image_path)) == 0:
        print("folder is empty")
        return False
    for filename in os.listdir(selenium_image_path):
        file_path = os.path.join(selenium_image_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    print("delete all files")
    return True

def selenium_dataframe(index_l, url_l, file_name_l, image_name_l, status_l) -> pd.DataFrame():
    df = pd.DataFrame()
    df['id'] = index_l
    df['image_name'] = image_name_l
    df['file_name'] = file_name_l
    df['status'] = status_l
    df['url'] = url_l

    return df

def save_selenium_dataframe(data_path: str, index_l: list, url_l: list, file_name_l: list, image_name_l:list, status_l: list) -> bool:
    try:
        df = selenium_dataframe(index_l, url_l, file_name_l, image_name_l, status_l)
        df.to_csv("{data_path}/selenium_df.csv".format(data_path=data_path), index=False)
        return True
    except Exception as e:
        return False
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import time 
import pandas as pd

def initial_beautiful_soup(url: str) -> list:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }
    #Get every image from the website
    html_page = urlopen(url)
    # soup = BeautifulSoup(html_page, "html.parser")
    time.sleep(10)
    soup = BeautifulSoup(html_page, "html.parser")

    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))

    return images

def save_image(url: str, folder: str, file_name: str):
    try:
        urlretrieve("{url}".format(url=url), "{path}/{file_name}".format(path=folder, file_name=file_name))
        return True
    except Exception as e:
        return False

def beautiful_save_image_list(last_index: int, images_list: list, path_folder: str):
    folder = path_folder
    index_l, url_l, file_name_l, image_name_l, status_l = [], [], [], [], []
    last_index = 11
    for i in images_list:
        if i is None:
            continue
        if "http" not in i:
            i = "https:" + i
        print(i)
        last_index = last_index + 1
        image_name = i.split("?")[1]
        image_name_l.append(image_name)
        if ".svg" in i:
            file_name = str(last_index) + ".svg"
        if ".png" in i:
            file_name = str(last_index) + ".png"
        if ".jpg" in i:
            file_name = str(last_index) + ".jpg"
        
        index_l.append(last_index)
        url_l.append(i)
        file_name_l.append(file_name)
        status = save_image(url=i, folder=folder, file_name=file_name)
        status_l.append(status)
    
    return index_l, url_l, file_name_l, image_name_l, status_l

def beautiful_dataframe(index_l, url_l, file_name_l, image_name_l, status_l) -> pd.DataFrame():
    df = pd.DataFrame()
    df['id'] = index_l
    df['image_name'] = image_name_l
    df['file_name'] = file_name_l
    df['status'] = status_l
    df['url'] = url_l

    return df
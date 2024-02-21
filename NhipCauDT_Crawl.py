import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)

def Crawl_NhipCauDauTu(driver):

    link_List = ['https://nhipcaudautu.vn/kinh-doanh/', 'https://nhipcaudautu.vn/cong-nghe/',
                     'https://nhipcaudautu.vn/doanh-nhan/', 'https://nhipcaudautu.vn/chuyen-de/',
                     'https://nhipcaudautu.vn/tai-chinh/', 'https://nhipcaudautu.vn/bat-dong-san/',
                     'https://nhipcaudautu.vn/phong-cach-song/', 'https://nhipcaudautu.vn/the-gioi/',
                     'https://nhipcaudautu.vn/kieu-bao/']

    data = []
    driver.get("https://nhipcaudautu.vn/")
    current_datetime = datetime.datetime.now()
    for link in link_List:
        driver.get(link)
        time.sleep(3)
        box_list_xem_nhieu = driver.find_elements(By.CSS_SELECTOR, "#main_container > div.wrapper > div.section1 > div.row > div.col-md-4 > div.box_xemnhieu > div.warp > ul > li")
        topic = driver.find_element(By.CSS_SELECTOR, "#main_container > div.wrapper > h1").text
        position = "XEM NHIỀU"
        # Crawl các slide có trên các Topic
        list_slide = driver.find_elements(By.CSS_SELECTOR, "#main_container > div.wrapper > div.section1 > div.row > div.col-md-8 > div.slide_top > div.owl-carousel > div.owl-stage-outer > div.owl-stage > div.owl-item")
        for slide in list_slide:
            img_tag = slide.find_element(By.CSS_SELECTOR, "div > a > img")
            one_slide = slide.find_element(By.CSS_SELECTOR, "div > h3 > a")
            slide_title = img_tag.get_attribute("title")
            slide_href = one_slide.get_attribute("href")
            print(slide_title)
            print(slide_href)
            data.append({
                    "Topic" : topic,
                    "Position": None,
                    "News_Time": None,
                    "Crawl_Time": current_datetime,
                    "Title": slide_title,
                    "Link": slide_href,
                    "Short_Description": None
                    })
        # Crawl danh sách các tin tức được xem nhiều theo topic
        for xem_nhieu in box_list_xem_nhieu:
            tag_li_a = xem_nhieu.find_element(By.CSS_SELECTOR, "a")
            title_content = tag_li_a.text
            href_news = tag_li_a.get_attribute("href")
            print("Position: ", position)
            print("Time: ", current_datetime)
            print("Tittle: ", title_content)
            print("Link: ", href_news)
            data.append({
                "Topic": topic,
                "Position": position,
                "News_Time": None,
                "Crawl_Time": current_datetime,
                "Title": title_content,
                "Link": href_news,
                "Short_Description": None
            })
        # Crawl danh sách các tin tức mới theo topic
        list_new = driver.find_elements(By.CSS_SELECTOR,"#main_container > div.wrapper > div.section3 > div.col_md8 > div.container-post-wrap > div.row > div.col-xs-12 > article.post")
        for item in list_new:
            title = item.find_element(By.CSS_SELECTOR, "ul > li > div.media_body> div.entry-data > p > a")
            title_content = title.get_attribute("title")
            href_news = title.get_attribute("href")
            short_description = item.find_element(By.CSS_SELECTOR, "ul > li > div.media_body> div.entry-data > div.description").text
            print("Topic: ", topic)
            print("Time: ", current_datetime)
            print("Tittle: ", title_content)
            print("Short_Description: ", short_description)
            print("Link: ", href_news)
            data.append({
                "Topic": topic,
                "Position": None,
                "News_Time": None,
                "Crawl_Time": current_datetime,
                "Title": title_content,
                "Link": href_news,
                "Short_Description": short_description
            })


    #Chuyển danh sách data đã crawl được thành một dataframe
    df_crawl_data = pd.DataFrame(data)


    # Đọc dữ liệu hiện có từ tệp Excel (nếu tệp đã tồn tại)
    try:
        existing_data = pd.read_excel('Save_Data_Crawl.xlsx', sheet_name="Sheet1")
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Kiểm tra và thêm chỉ các hàng mới vào DataFrame hiện có
    if not existing_data.empty:
        # Lọc ra các hàng mới (chưa tồn tại trong DataFrame hiện có dựa trên check Link)
        new_data = df_crawl_data[~df_crawl_data['Link'].isin(existing_data['Link'])]
        #ọc ra các hàng mới (chưa tồn tại trong DataFrame hiện có dựa trên check Link and Title)
        #new_data = df_crawl_data[~df_crawl_data.apply(lambda row: (row['Link'], row['Title']) in existing_data[['Link','Title']].apply(tuple, axis=1), axis=1)]

        # Kết hợp DataFrame hiện có với dữ liệu mới
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        # Nếu không có dữ liệu hiện có, sử dụng toàn bộ dữ liệu crawl được
        combined_data = df_crawl_data

    # Xuất dữ liệu đã kết hợp vào tệp Excel
    combined_data.to_excel('Save_Data_Crawl.xlsx', index=False, sheet_name="Sheet1")

Crawl_NhipCauDauTu(driver)
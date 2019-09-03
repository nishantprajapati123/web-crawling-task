import requests
import sys
import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def today(driver, link):
    driver.get(link)
    place_name = driver.find_element_by_class_name(
        'today_nowcard-location').text
    place_time = driver.find_element_by_class_name(
        'today_nowcard-timestamp').text
    place_temp = driver.find_element_by_class_name('today_nowcard-temp').text
    place_phrase = driver.find_element_by_class_name(
        'today_nowcard-phrase').text
    place_feels = driver.find_element_by_class_name('today_nowcard-feels').text
    place_hilo = driver.find_element_by_class_name('today_nowcard-hilo').text
    place_right_now = driver.find_element_by_tag_name('tbody').text
    print(f'Place = {place_name}')
    print(f'Time = {place_time}')
    print(f'Temperature = {place_temp}')
    print(place_phrase)
    print(place_feels)
    print(place_hilo)
    print()
    print('Right now')
    print('----------')
    print(place_right_now)


def hourly(driver, link):
    driver.get(link)
    table = driver.find_elements_by_css_selector('.twc-table>tbody>tr')
    table_head = driver.find_element_by_tag_name(
        'thead').text.replace('\n', ' ')
    table_head = table_head.replace(' ', '\t')
    # print(table_head)
    # print(table)
    hr_table = list()
    hr_table.append(table_head[:5]+'DAY     '+table_head[5:])
    for row in table:
        trim = row.text.replace('\n', '\t')
        # trim.replace('\n','\t')
        hr_table.append(trim)
    # print hourly table
    place_name = driver.find_element_by_class_name('hourly-page-title').text
    print(place_name)
    print()
    for x in hr_table:
        print(x)


def monthly(driver, link):
    # driver.get("https://weather.com/weather/monthly/l/" + link[36:])
    driver.get(link)
    monthly_title = driver.find_element_by_class_name(
        'monthly-page-title').text
    print(monthly_title)
    monthly_days = driver.find_elements_by_css_selector(
        '.forecast-monthly__days>dt')
    monthly_date = driver.find_elements_by_css_selector('.date')
    monthly_main = driver.find_elements_by_css_selector('.temps>.hi')

    q, r, s = [], [], []

    for x in monthly_days:
        q.append(x.text)
    for y in monthly_main:
        r.append(y.text)
    for x in monthly_date:
        s.append(x.text)
    for i, j in zip(r, s):
        q.append(j+" --> "+i)

    mnt_data = np.array(q)
    mnt_data = mnt_data.reshape(6, 7)
    mnt_data = pd.DataFrame(mnt_data)
    df = mnt_data.to_string(header=False, index=False)
    print(df)


if __name__ == '__main__':
    place = sys.argv[1]
    # date = None
    forecast_type = 'today'
    if(len(sys.argv) == 3):
        forecast_type = sys.argv[2]


    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        # driver = webdriver.Chrome()

        url = f'https://weather.com/en-IN/search/enhancedlocalsearch?where={place}&loctypes=1/4/5/9/11/13/19/21/1000/1001/1003/&from=hdr'
        driver.get(url)

        # wait for DOM to appear
        element = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located(
            (By.CSS_SELECTOR, ".styles__resultsList__2-Km4 li a.styles__itemLink__23h5a")))
        places_option = dict()
        print(f'Available option for {place} are: ')
        for id, ele in enumerate(element):
            places_option[id+1] = ele.get_attribute('href')
            print((id+1), " -> " + ele.text)

        choice_of_place = int(input("Enter your choice: "))
        # print(places_option.keys())
        if choice_of_place in places_option.keys():
                # print(choice_of_place)
                # print(places_option[choice_of_place])
            if forecast_type == 'today':
                today(driver, places_option[choice_of_place])
            elif forecast_type == 'hourly':
                hr_link = places_option[choice_of_place]
                hr_link = hr_link[-13:]
                # print(hr_link)
                hourly(
                    driver, 'https://weather.com/en-IN/weather/hourbyhour/l/' + hr_link)
            elif forecast_type == 'monthly':
                mt_link = places_option[choice_of_place]
                mt_link = mt_link[-13:]

                monthly(
                    driver, 'https://weather.com/en-IN/weather/monthly/l/' + mt_link)
        else:
            print("Invalid choice")
        driver.quit()
    except Exception as e:
        print("Slow connection!")
        driver.quit()

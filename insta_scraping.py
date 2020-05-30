from selenium import webdriver
import time
import sys

#setting variables
public_post_url = sys.argv[1]
more_comments_count = sys.argv[2]

#path to the chromewebdriver
driver = webdriver.Chrome("C:/Users/JRSVa/Desktop/insta scrapper/chromedriver_win32/chromedriver.exe")
driver.get(public_post_url)

#wait 5s for page loading
time.sleep(5)

#if user not logined
try:
    close_button = driver.find_element_by_class_name('xqRnw')
    close_button.click()
except:
    pass


try:
    load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
    print("Found {}".format(str(load_more_comment)))
    i = 0
    while load_more_comment.is_displayed() and i < int(more_comments_count):
        #loadind more comments
        load_more_comment.click()

        #time to wait, it can be different, depending of network latency
        time.sleep(1.5)

        load_more_comment = driver.find_element_by_css_selector('.MGdpg > button:nth-child(1)')
        print("Found #{}".format(str(i)))
        i += 1
except Exception as e:
    print(e)
    pass



#getting the comments and usernames in to lists
user_names = []
user_comments = []
comment = driver.find_elements_by_class_name('gElp9 ')

for c in comment:
    container = c.find_element_by_class_name('C4VMK')
    name = container.find_element_by_class_name('_6lAjh').text
    content = container.find_element_by_tag_name('span').text
    content = content.replace('\n', ' ').strip().rstrip()
    user_names.append(name)
    user_comments.append(content)

user_names.pop(0)
user_comments.pop(0)

try:
    #generating excel file
    import pandas as pd

    data = pd.DataFrame({'user':user_names, 'user_comment':user_comments})
    data.to_excel('./comments_output.xlsx')
    driver.close()
except Exception as e:
    print("Error generating the excel file {}".format(str(e)))
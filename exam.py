from selenium import webdriver

B_URL = "./chromedriver.exe"
T_URL = "https://exam.msrit.edu/eresultseven/"
DEPT = "CS"
browser = webdriver.Chrome(executable_path=B_URL)
browser.implicitly_wait(20)
browser.get(T_URL)
cap = input("enter the captcha: ")

with open(f'#{DEPT}.csv', 'w+') as f:
    capt = browser.find_element_by_id("osolCatchaTxt0")
    capt.send_keys(cap)
    capt_click = browser.find_element_by_class_name("buttongo")
    element = browser.find_element_by_id("usn")
    for i in range(1, 200):
        element.clear()
        element.send_keys(f"1MS21{DEPT}{i:03}")
        capt_click.click()
        browser.implicitly_wait(20)
        try:
            name = browser.find_element_by_tag_name("h3")
            cgpa = browser.find_elements_by_tag_name("p")
            data = f'1MS21{DEPT}{i:03}, {name.text}, {float(cgpa[3].text):.2f}\n'
            f.write(data)
            print(f"{name.text}: {cgpa[3].text}")
        except Exception as e:
            print(e)
            break
        browser.back()
    browser.close()

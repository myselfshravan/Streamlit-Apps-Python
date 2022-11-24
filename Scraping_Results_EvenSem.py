from selenium import webdriver

B_URL = "./chromedriver.exe"
T_URL = "https://exam.msrit.edu/eresultseven/"
DEPT = "CY"
TOLERANCE = 5
browser = webdriver.Chrome(executable_path=B_URL)
browser.get(T_URL)
cap = input("Enter the captcha: ")

with open(f'#{DEPT}.csv', 'w+') as f:
    capt = browser.find_element_by_id("osolCatchaTxt0")
    capt.send_keys(cap)
    capt_click = browser.find_element_by_class_name("buttongo")
    element = browser.find_element_by_id("usn")
    tol = TOLERANCE
    for i in range(1, 200):
        element.clear()
        element.send_keys(f"1MS21{DEPT}{i:03}")
        capt_click.click()
        try:
            name = browser.find_element_by_tag_name("h3")
            cgpa = browser.find_elements_by_tag_name("p")

            data = f'1MS21{DEPT}{i:03}, {name.text}, {cgpa[3].text}\n'
            f.write(data)
            print(f"{i + 1} {name.text}: {cgpa[3].text}")
            tol = TOLERANCE
        except Exception as e:
            print(e)
            tol -= 1
            if tol == 0:
                break
        browser.back()
    browser.close()

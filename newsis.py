from selenium import webdriver

B_URL = "./chromedriver.exe"
T_URL = "https://parents.msrit.edu/parents_even2022/"
DEPT = "CS"
browser = webdriver.Chrome(executable_path=B_URL)
browser.implicitly_wait(20)
browser.get(T_URL)

username = browser.find_element_by_id("username")
dd = browser.find_element_by_id("dd")
mm = browser.find_element_by_id("mm")
yyyy = browser.find_element_by_id("yyyy")
login = browser.find_elements_by_tag_name("input")[6]
print("111")
    # for i in range(1, 2):
    #     element.clear()
    #     element.send_keys(f"1MS21{DEPT}{i:03}")
    #     capt_click.click()
    #     browser.implicitly_wait(20)
    #     try:
    #         name = browser.find_element_by_tag_name("h3")
    #         cgpa = browser.find_elements_by_tag_name("p")
    #         data = f'1MS21{DEPT}{i:03}, {name.text}, {float(cgpa[3].text):.2f}\n'
    #         f.write(data)
    #         print(f"{name.text}: {cgpa[3].text}")
    #     except Exception as e:
    #         print(e)
    #         break
    #     browser.back()
    # browser.close()

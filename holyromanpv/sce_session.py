import time
import requests
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from pyvirtualdisplay import Display
import pandas


def json2df(data):
    df = pandas.DataFrame(data['viewUsageDetails'], columns=['startDateTime', 'value'])
    df.rename(columns={'startDateTime': 'timestamp', 'value': 'power'}, inplace=True)
    df.power = pandas.to_numeric(df.power)
    df.timestamp = pandas.to_datetime(df.timestamp)
    df.set_index('timestamp', inplace=True)
    return df


class SCESession:
    
    def __init__(self, username=None, password=None, account=None, contract=None):
        self.display = Display(visible=0, size=(1920, 1080))  
        self.display.start()
        options = Options()
        options.headless = False
        options.add_argument("window-size=1920,1080")
        self.account = account
        self.contract = contract
        self.username = username
        self.password = password 
        self.headers = None
        self.session = requests.Session()
        self.driver = webdriver.Chrome(options=options, seleniumwire_options={'verify_ssl': False}) 
       
    def get_account_page(self):
        self.driver.get('https://www.sce.com/mysce/myaccount')
        self.close_popup()
                
    def login(self):
        self.driver.get('http://www.sce.com/mysce/login')
        #username_field = self.driver.find_element_by_id('userIDorEmail')        
        #username_field = self.driver.find_element_by_id('user ID or Email')
        username_field = self.driver.find_elements_by_id('userName')[1]
        #password_field = self.driver.find_element_by_id('passwordLogin')
        password_field = self.driver.find_elements_by_id('password')[1]
        #username_field.clear()
        #password_field.clear()        
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)        
        time.sleep(1)        
        buttons = self.driver.find_elements_by_class_name('sceButton__sceBtnSmPrimary__1SQ_u')
        submit = buttons[-1]
        submit.click()
        time.sleep(10)
        self.close_popup()
        return self.login_failed() == False
        
    def login_failed(self):
        fail_str = 'Sorry, your email and/or password was incorrect'
        failed = fail_str in self.driver.page_source
        return failed
        
    def close_popup(self):
        try:
            self.driver.find_element_by_id('Combined-Shape').click()
        except Exception as e:
            print('no_popup')         
            
    def get_headers(self):
        n_tries = 0
        while self.headers is None:
            try:
                self.get_headers_attempt()
            except Exception as e:
                print(e)
                print('Headers not grabbed. Retrying')
                self.get_account_page()                
                time.sleep(5)
            n_tries += 1
            if n_tries > 5:
                self.logout()
                self.quit()
                quit()
            
    def get_headers_attempt(self):     
        self.close_popup()
        self.driver.find_element_by_id('ThisPeriod').click()        
        time.sleep(1)
        self.close_popup()
        self.driver.find_element_by_id('Hourly').click()
        time.sleep(1)
        self.close_popup()
        #self.driver.find_element_by_id('openCalender').click()
        time.sleep(10)
        for request in self.driver.requests:
            if 'https://prodms.dms.sce.com/myaccount/v1/usage' in request.url:# and 'oktaUid' in request.headers:        
                self.headers = dict(request.headers)
        
    def make_requests_session(self):
        self.get_headers()
        self.session.headers = self.headers        
    
    def make_url(self, date):
        period = 60
        trunk = 'https://prodms.dms.sce.com/myaccount/v1/usage'
        query = '?'
        #query += 'serviceAccountNumber={account}&'
        query += 'contractNumber={contract}&'
        query += 'period={period}&'
        query += 'usageDemandIndicator=usage&'
        query += 'startDate={start}%2012:02&'
        query += 'endDate={end}%2012:02&'
        query += 'numberOfDays=4&'
        query += 'lastBillEndDate=2020-01-22&'
        query += 'nemFlag=N&'
        query += 'statementNumber=NA'
        #query = query.format(start=date, end=date, account=self.account, period=period)
        query = query.format(start=date, end=date, contract=self.contract, period=period)
        url = trunk + query
        return url
                       
    def download(self, date):
        failed = True
        n_tries = 1
        while failed:            
            try:
                data = self.download_attempt(date)                
                failed = False
            except Exception as e:  
                print(e)
                print('download failed. Trying again')
                self.make_requests_session()                
                time.sleep(5)
            n_tries += 1
            if n_tries > 5:
                self.logout()
                self.quit()                        
        return data   
    
    
    def download_attempt(self, date):    
        url = self.make_url(date)        
        self.session.options(url)
        time.sleep(2)
        ret = self.session.get(url)
        data = json2df(ret.json())
        return data
    
    def logout(self):
        try:                     
            self.get_account_page()
            self.driver.find_element_by_class_name('fa-user').click()
            time.sleep(5)
            self.driver.find_element_by_class_name('sceButton__sceBtnSmDefault__1hmG2').click()                
        except Exception as e: 
            print(str(e))
            print('could not log out')
        
    def quit(self):        
        self.driver.quit()
        self.display.stop()
     

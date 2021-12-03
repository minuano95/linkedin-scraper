# ------------
# Selenium imports

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver

# ------------

from bs4 import BeautifulSoup
from time import sleep
import requests
import csv
import re

# -------------


def get_linkedin_jobs(search_term):
    search_term = search_term.replace(' ', '%20')
    url = f'https://www.linkedin.com/jobs/search?keywords={search_term}'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(r'C:\Users\User\Downloads\chromedriver.exe', options=options)
    driver.get(url)
    
    fazer_login_btn = driver.find_element_by_css_selector('body > div.base-serp-page > header > nav > div > a.nav__button-secondary').click()
    email_input = driver.find_element_by_id('username').send_keys('linkedin_email')
    senha_input = driver.find_element_by_id('password').send_keys('linkedin_password')
    entrar_btn = driver.find_element_by_css_selector('#organic-div > form > div.login__form_action_container > button').click()

    page_html = driver.page_source

    soup = BeautifulSoup(page_html, 'html.parser')

    scrapped_offers = []

    for job_offer in soup.find_all('a', href=re.compile(r'/jobs/view/')):

        url = 'https://www.linkedin.com/' + job_offer.attrs['href']        
        
        if url not in scrapped_offers:
            print('-'*30)
            print(url)

            scrapped_offers.append(url)

            driver.get(url)
            sleep(1)

            while True:
                try:
                    ver_mais_btn = driver.find_element_by_id('ember48').click()
                    break
                except Exception as e:
                    pass

            sleep(1)
            page_html = driver.page_source
            soup = BeautifulSoup(page_html, 'html.parser')
            titulo_vaga = soup.find('h1', {'class': "t-24 t-bold"}).text.strip()
            contratante = soup.find('a', {'class': "ember-view t-black t-normal"}).text.strip()
            local_trabalho = soup.find('span', {'class': "jobs-unified-top-card__bullet"}).text.strip()
            tempo_postado = soup.find('span', {'class': 'jobs-unified-top-card__subtitle-secondary-grouping t-black--light'}).span.text.strip()[2:]# .text.strip()
            try:
                candidatos = soup.find('span', {'class': 'jobs-unified-top-card__applicant-count'}).text.strip()
            except AttributeError:
                candidatos = 0
            
            csv_file_writer(titulo_vaga,contratante,local_trabalho,tempo_postado,candidatos,url)

            print('-'*30)


def csv_file_writer(titulo_vaga,empregador,local,data_postado,candidatos,url):
    with open('job_offers.csv', 'a+', encoding='utf-8') as csv_file:
        job_offer = csv.writer(csv_file,)

        job_offer.writerow([titulo_vaga,empregador,local,data_postado,candidatos,url]) 


get_linkedin_jobs('desenvolvedor(a) python junior')
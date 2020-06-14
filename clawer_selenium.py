from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

import json
import os
import argparse
from multiprocessing import Process, Manager

import requests
import urllib
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import datetime
import time
import sys

urllib3.disable_warnings(InsecureRequestWarning)


def download_google_staticimages(config):
    t0 = time.time()
    # 검색할 url만들기
    searchword = config['keyword']
    searchurl = 'https://www.google.com/search?q=' + searchword + '&source=lnms&tbm=isch'
    maxcount = 200

    # 폴더 만들기
    if not os.path.exists(config["image_save_path"] + '\\' + searchword[1:-1]):
        os.mkdir(config["image_save_path"] + '\\' + searchword[1:-1])
    chromedriver = config['driver_path']

    # 브라우저 띄우고 인터럽트 안 걸리게하기
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')

    try:
        browser = webdriver.Chrome(chromedriver, options=options)
    except Exception as e:
        print(f'No found chromedriver in this environment.')
        print(f'Install on your machine. exception: {e}')
        sys.exit()

    browser.set_window_size(1280, 1024)
    browser.get(searchurl)
    time.sleep(1)

    print(f'Getting you a lot of images. This may take a few moments...')

    #
    element = browser.find_element_by_tag_name('body')

    # 스크롤 내리기 1
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    print(f'Reached end of page.')
    time.sleep(0.5)
    print(f'Retry')
    time.sleep(0.5)

    # 결과 더 보기 클릭
    browser.find_element_by_xpath('//input[@value="결과 더보기"]').click()

    # 스크롤 내리기 2
    for i in range(50):
        element.send_keys(Keys.PAGE_DOWN)
        time.sleep(0.3)

    try:
        browser.find_element_by_id('smb').click()
        for i in range(50):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)
    except:
        for i in range(10):
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.3)

    # 이미지 들어있는거 전부 찾기
    page_source = browser.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    images = soup.find_all('img')

    # 이미지 들어있는 주소 찾기
    urls = []
    for image in images:
        try:
            url = image['data-src']
            if not url.find('https://'):
                urls.append(url)
        except:
            try:
                url = image['src']
                if not url.find('https://'):
                    urls.append(image['src'])
            except Exception as e:
                print(f'No found image sources.')
                print(e)

    # 이미지 다운로드 받기
    count = 0
    if urls:
        for url in urls:
            # 다운로드 받을 이미지 최대개수 설정
            if count >= maxcount:
                break
            try:
                res = requests.get(url, verify=False, stream=True)
                rawdata = res.raw.read()
                with open(
                        os.path.join(config['image_save_path'] + '\\' + searchword[1:-1], 'img_' + str(count) + '.jpg'),
                        'wb') as f:
                    f.write(rawdata)
                    count += 1
            except Exception as e:
                print('Failed to write rawdata.')
                print(e)

    # 브라우저 종료
    browser.close()

    # 끝나는 시간 체크, 총 시간 출력, 사진 몇장 크롤링했는지 확인
    t1 = time.time()
    total_time = t1 - t0
    print(f'\n')
    print(f'Download completed. [Successful count = {count}].')
    print(f'Total time is {str(total_time)} seconds.')
    return count


import argparse
import os
import sys

root = os.getcwd()


class Config(object):
    params = {
        "root": root,
        "mode": "default",
        "keyword": "default",
        "epoch": 100,
        "learning_rate": 0.001,
        "batch_size": 8,
        "weight_decay": 0.0001,
        "driver_path": r'C:\Users\201810938\Documents\카카오톡 받은 파일\Recycle (1)\Recycle\chromedriver_win32\chromedriver.exe',
        "image_save_path": root ,
        "model_load_path": root + r"\5_class_model.tar",
        "model_save_path": root + r'\save_model',
        "image_folder": root + r"\trash",
        "test_image": r"_",
        "top3": [],
        "class_num": 5,
        "argumentation": False
    }


if __name__ == '__main__':
    mush_room_list = ['Psathyrella piluriformis', 'Albatrellus confluens', 'Macrocybe gigantea', 'Annulohypoxylon multiforme', 'Xylaria polymorpha (Pers.)Grev.',
                      'nocybe cookei', 'Hygrophorus arbustivus Fr.', 'Thelephora palmata', 'Amanita  caesareoides', 'Russula compacta Frost', 'Tricholoma ustale',
                      'Aporpium strigosum .', 'Nectria pallidula', 'Orbilia epipora', 'Ramaria stricta', 'Glaziella splendens', 'Paxillus atrotomentosus var. bambusinus',
                      'Lanopila nipponica', 'Laetiporus sulphureus', 'Asterophora lycoperdoides', 'Daedaleopsis confragosa', 'Clitocybe acromelalga', 'Tricholoma muscarium',
                      'Amanita virosa', 'Chlorophylum neomastoideum', 'Ciborinia camelliae', 'Steccherinum murashikinskyi', 'Cordyceps militaris', 'Ptychoverpa bohemica',
                      'Coprinopsis atramentaria', 'Aleuria aurantia', 'Daedalea dickinsii', 'Cyptotrama asprata', 'Agaricus abruptibulbus', 'Pholiota terrestris',
                      'Tricholoma myomyces', 'Lyopyllum shimeji', 'Hypochnicium geogenium', 'Lenzites styracina', 'Ischnoderma resinosum', 'Cortinarius meinhardii',
                      'Gyromitra esculanta', 'Amanita pantherina', 'Marasmiellus ramealis', 'Thelephora multipartita', 'Fomitopsis officinalis', 'Panaeolus papilionaceus',
                      'Fomes fomentarius', 'Phallus impudicus', 'Lycoperdon perlatum', 'Calvatia craniiformis', 'Marasmius crinis-equi', 'Mycena pura', 'Amanita esculenta',
                      'Phallus indusiatus', 'Macrolepiota dersa', 'Coprinus comatus', 'straeus hygrometricus', 'Microporus vernicipes', 'Lyophyllum semitale', 'Pisolithus arhizus',
                      'Ciborinia sp.', 'Auricularia auricula-judae', 'Chroogomphus rutilus', 'Sarcodon scabrosus', 'Russula emetica', 'Hebeloma crustuliniforme', 'Cudoniella clavus',
                      'Tremella fimbriata .', 'Gymnopilus liquiritiae', 'Entoloma omiense', 'Lepista nuda', 'Gymnopus confluens', 'Perenniporia minutissima', 'Laccaria tortilis',
                      'Pterula sublata', 'Inocybe calospora Quél', 'Stecherinum ochraceum', 'Gomphidius maculatus', 'Coprinellus domesticus', 'Mycena chlorophos', 'Boletus pulverulentus Opat',
                      'Retiboletus ornatipes', 'Hebeloma vinosophyllum', 'Cystidiophorus castaneus', 'Tremella pulvinaria', 'Amanita excelsa', 'Entoloma  clypeatum', 'Ampulloclitocybe clavipes',
                      'Lactarius volemus', 'Beauveria bassiana', 'Psathyrella ammophila', 'Amanita alboflavescens', 'Amanita spissacea', 'Mutinus borneensis', 'Rhodocollybia butyracea f. butyracea',
                      'Trametes kusanoana', 'Cordyceps sphecocephata', 'Polyporus alveolaris', 'Hygrophorous russula', 'Phellinus pomaceus', 'Heterobasidion insulare', 'Chlorociboria aeruginascens',
                      'Clavulina  coralloides', 'Agrocybe praecox', 'Entoloma violaceum', 'Agrocybe erebia', 'Porostereum crassum', 'Wolfiporia extensa', 'Bankera fuligeneoalba', 'Xylocoremium flabelliforme',
                      'Panellus stypticus', 'Amanita parcivolvata', 'Erythricium laetum', 'Ganoderma lucidum', 'Boletus fraternus', 'Entoloma quadratum', 'Hygrocybe miniata', 'Cantharellus cinnabarinus',
                      'Boletus erythropus', 'Laetiporus sulphureus var. miniatus', 'Phallus rugulosus', 'Clathrus ruber', 'Mutinus elegans', 'Suillus pictus', 'Podostroma cornu-damae',
                      'Ramaria formosa', 'Nectria episphaeria', 'Rhizopogon roseolus', 'Mycena erubescens', 'Amanita rubescens', 'Lactarius laeticolor', 'Amanita rubrovolvata', 'Clavulinopsis miyabeana',
                      'Thelephora penicillata', 'Squamanita umbonata', 'Pholiota squarrosa', 'Suillus luteus', 'Clitocybe candicans', 'Entoloma sericellum', 'Inocybe lacera',
                      'Peroneutypa scoparia', 'Pluteus aurantiorugosus', 'Armillaria mellea', 'Armillaria tabescens', 'Xerula pudens', 'Craterellus cornucopioodes']
    config = Config().params
    process_num = 5

    for i in range(0, len(mush_room_list), process_num):
        procs = []
        for mushroom in mush_room_list[i:i + process_num]:
            config['keyword'] = '"' + mushroom + '"'
            print(config['keyword'])
            proc = Process(target=download_google_staticimages, args=(config,))
            procs.append(proc)
            proc.start()
        for proc in procs:
            proc.join()
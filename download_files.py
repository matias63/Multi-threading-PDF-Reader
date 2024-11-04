# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:37:08 2019

@author: hewi
"""

#### IF error : "ModuleNotFOundError: no module named PyPDF2"
   # then uncomment line below (i.e. remove the #):
       
# pip install PyPDF2
# pip install pandas
# pip install openpyxl
# pip install xlsxwriter
# pip install requests


from numpy import save
import pandas as pd
import PyPDF2
from pathlib import Path
import shutil, os
import os.path
import urllib
import glob
import urllib.request
import requests

class NotAPdfError(Exception):
    pass
class MyError(Exception):
    pass


def check_link2():
    if df2.at[j,'Report Html Address'] != "":
        print("Link 2")
        if not pdf_url(df2.at[j,'Report Html Address']):
            raise NotAPdfError(f"URL {df2.at[j, 'Report Html Address']} is not a valid PDF.")
        else: 
            download(savefile,'Report Html Address')

def pdf_url(url):
     try:
         r = requests.get(url,timeout=2)
         content_type = r.headers.get('content-type')
         if 'application/pdf' in content_type:
             ext = '.pdf'
             return True
         else:
             return False
     except requests.RequestException as e:
        print(f"Error checking URL {url}: {e}")
        return False

def download(savefile,url_type ='Pdf_URL'):
    try:
        urllib.request.urlretrieve(df2.at[j,url_type], savefile)
        if os.path.isfile(savefile):
            with open(savefile, 'rb') as pdfFileObj:
                pdfReader = PyPDF2.PdfReader(pdfFileObj)
                if len(pdfReader.pages) > 0:
                    df2.at[j, 'pdf_downloaded'] = "yes"
                else:
                    df2.at[j, 'pdf_downloaded'] = "file_error"
        else:
            df2.at[j, 'pdf_downloaded'] = "404"
            print("not a file")
    except Exception as e:
        df2.at[j, 'pdf_downloaded'] = str(e)
        print(str(str(j)+" " + str(e)))           

###!!NB!! column with URL's should be called: "Pdf_URL" and the year should be in column named: "Pub_Year"

### File names will be the ID from the ID column (e.g. BR2005.pdf)

########## EDIT HERE:
    
### specify path to file containing the URLs
# list_pth = 'K:/TextMining/02 Analysis 8/10 TextMining Projects/CSR/CSR Train/02 Supporting Scripts/01 Scripts input/GRI_2017_2020_SAHO.xlsx'
list_pth = r'./input_files/GRI_2017_2020.xlsx'



###specify Output folder (in this case it moves one folder up and saves in the script output folder)
# 'K:/TextMining/02 Analysis 8/10 TextMining Projects/CSR/CSR Train/02 Supporting Scripts/03 Scripts output/'
pth = r'./downloaded_files/'
if not os.path.exists(pth):
    os.makedirs(pth)
###Specify path for existing downloads
# dwn_pth = 'K:/TextMining/02 Analysis 8/10 TextMining Projects/CSR/CSR Train/02 Supporting Scripts/03 Scripts output/dwn/'
dwn_pth = r'./downloaded_files/existing_files'
if not os.path.exists(dwn_pth):
    os.makedirs(dwn_pth)

### cheack for files already downloaded
dwn_files = glob.glob(os.path.join(dwn_pth, "*.pdf")) 
exist = [os.path.basename(f)[:-4] for f in dwn_files]

###specify the ID column name
ID = "BRnum"


##########

### read in file
df = pd.read_excel(list_pth, sheet_name=0, index_col=ID)

### filter out rows with no URL
non_empty = df.Pdf_URL.notnull() == True
df = df[non_empty]
df2 = df.copy()


#writer = pd.ExcelWriter(pth+'check_3.xlsx', engine='xlsxwriter', options={'strings_to_urls': False}) # didnt recognise option choise
# writer = pd.ExcelWriter(pth+'check_3.xlsx', engine='xlsxwriter')



with pd.ExcelWriter(pth+'check_3.xlsx', engine='xlsxwriter') as writer:
    ### filter out rows that have been downloaded
    df2 = df2[~df2.index.isin(exist)]

    ### loop through dataset, try to download file.
    # for j in df2.index:
    for j in df2.index:
        print(df2.at[j,'Pdf_URL'])
        # savefile = str(pth + "dwn/" + str(j) + '.pdf')
        savefile = str(pth + "existing_files/" + str(j) + '.pdf')
        try:
            # check first link
            if df2.at[j,'Pdf_URL'] != "":
                print("Link 1")
                if not pdf_url(df2.at[j,'Pdf_URL']): # if not the first link, check the second link
                    check_link2() 
                else: # else check link 1
                    download(savefile,'Pdf_URL') 
                    if   df2.at[j, 'pdf_downloaded'] != "yes" and df2.at[j,'Report Html Address'] != "": # if link 1 fails, check link 2
                        check_link2()
                        if   df2.at[j, 'pdf_downloaded'] != "yes": # if link 2 fails , raise error
                            raise MyError(f"{ID} has an unencoutered for error.")
                            df2.at[j, 'pdf_downloaded'] = "file_error" # set error in output file
            else:
                raise NotAPdfError(f"URL {df2.at[j, 'pdf_downloaded']} is not a valid PDF.")
                df2.at[j, 'pdf_downloaded'] = "Not_A_PDF_ERROR"    
                
        except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, Exception ) as e:
                    df2.at[j,"error"] = str(e)
                   

      






df2.to_excel(writer, sheet_name="dwn")
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



from math import e
from tabnanny import check
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
# import threading
from concurrent.futures import ThreadPoolExecutor
import openpyxl



class NotAPdfError(Exception):
    pass
class MyError(Exception):
    pass


### bug that produces the empty pdfs as well
# def tryAgain(amount,function,retries=0):
#     if retries > amount: return False
#     try:
#         if lambda x: function == True:
#             return True
#     except:
#         tryAgain(amount,function,retries+1)



            

def check_link2(savefile,j):
    if df2.at[j,'Report Html Address'] != "":
        print("try 2")
        # if not tryAgain(3,pdf_url(df2.at[j,'Report Html Address'])):
        if not is_url_pdf(df2.at[j,'Report Html Address']):
            df2.at[j, 'pdf_downloaded'] = "not downloadet"
            df2.at[j, 'error'] = f"URL {df2.at[j, 'Report Html Address']} is not a valid PDF."
            raise NotAPdfError(f"URL {df2.at[j, 'Report Html Address']} is not a valid PDF.")
        else: 
            download(savefile,'Report Html Address')

def is_url_pdf(url):
     try:
         r = requests.get(url,timeout=4)
         content_type = r.headers.get('content-type')
         if 'application/pdf' in content_type:
             ext = '.pdf'
             return True
         else:
             return False
     except requests.RequestException as e:
        # df2.at[j, 'pdf_downloaded'] = "not downloadet"
        df2.at[j, 'error'] = f"Error checking URL {url}: {e}"
        return False

def download(savefile,j,url_type ='Pdf_URL'):
    try:
        urllib.request.urlretrieve(df2.at[j,url_type], savefile)
        if os.path.isfile(savefile):
            with open(savefile, 'rb') as pdfFileObj:
                pdfReader = PyPDF2.PdfReader(pdfFileObj)
                if len(pdfReader.pages) > 0:
                    df2.at[j, 'pdf_downloaded'] = "yes"
                else:
                    df2.at[j, 'error'] = "file_error"
                    # df2.at[j, 'pdf_downloaded'] = "not downloadet"
        else:
            df2.at[j, 'error'] = "404"
            # df2.at[j, 'pdf_downloaded'] = "not downloadet"
            print("not a file")
    except Exception as e:
        # df2.at[j, 'pdf_downloaded'] = str(e)
        # df2.at[j, 'pdf_downloaded'] = str(e)

        print(str(str(j)+" " + str(e)))           


def download_pdf(df2,j):
        try:
            savefile = str(pth + "existing_files/" + str(j) + '.pdf')
            if df2.at[j,'pdf_downloaded'] != "not downloadet":
                # check first link
                if df2.at[j,'Pdf_URL'] != "": # if link 1 is not empty url string
                    print("Try 1")
                    # if not tryAgain(3, pdf_url(df2.at[j,'Pdf_URL'])):
                    if not is_url_pdf(df2.at[j,'Pdf_URL']): # if link 1 is not a valid url
                        check_link2(savefile,j)         # check link 2
                    else:
                        download(savefile,j,'Pdf_URL') # download link 1
                        if df2.at[j, 'pdf_downloaded'] != "yes" and df2.at[j,'Report Html Address'] != "": # if link 1 fails, check link 2
                            check_link2(savefile,j) # check link 2 and download if possible
                            if df2.at[j, 'pdf_downloaded'] == "":  # if pdf has not been downloaded, raise error
                                # df2.at[j, 'pdf_downloaded'] = "not downloadet"
                                df2.at[j, 'error'] = "file_error"
                                raise MyError(f"{ID} has an unencoutered for error.")
                else:
                    df2.at[j, 'error'] = "Not_A_PDF_ERROR"
                    # df2.at[j, 'pdf_downloaded'] = "not downloadet"

                    raise NotAPdfError(f"URL {df2.at[j, 'pdf_downloaded']} is not a valid PDF.")
            
        except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, Exception ) as e:
                    df2.at[j,"error"] = str(e)
                    print(df2.at[j,'Pdf_URL'])  
                    df2.at[j,"pdf_downloaded"] = "not downloadet"

# def check_existing_download_tries():
#     path = r'checked_links.xlsx'
#     current_dir = os.getcwd()
#     subfolder = r'downloaded_files'
#     path_to_xlsx = os.path.join(current_dir, subfolder, path)

#     if os.path.isfile(path_to_xlsx):
#         data = pd.read_excel(path_to_xlsx, engine='openpyxl')
#         looked_through_records = data[data['error'].notna()]['BRnum'].tolist()
#         return looked_through_records
#     else:
#         return []


    
### specify path to file containing the URLs

list_pth = r'./input_files/GRI_2017_2020.xlsx'



###specify Output folder (in this case it moves one folder up and saves in the script output folder)
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


### filter out rows that have been attempted to download
# not_working_links = check_existing_download_tries()
### filter out rows that have been downloaded
df2 = df2[~df2.index.isin(exist)]
# df2 = df2[~df2.index.isin(not_working_links)]
# print(not_working_links)

### loop through dataset, try to download file.
args = [(df2,j) for j in df2.index[0:20]]
 
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(download_pdf, df, j) for df,j in args]

for future in futures:
    future.result()
             

      
output_df = df2.copy()
# output_path = os.path.join(pth, 'checked_links.xlsx')
output_path = list_pth

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:

    df2.to_excel(writer, sheet_name="Sheet1")  



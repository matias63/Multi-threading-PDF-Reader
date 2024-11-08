# Multi-threading-PDF-Reader
Programmet downloader pdfer fra en exel fil placeret i input files og tjekker efter om filerne i linksne kan downloades, er downloadede allerede eller tidligere afprøvet. 
Dette registeres og indsættes som kollonne med fejlmeddelese i input filen 
alle filer ender i en mappe downloaded_files.
error typen: name 'j' is not defined betyder at den er fundet og derfor springes over fra at forsøge at downloade igen.
Filen er sat til at stoppe efter 25 pdf-links er forsøgt downloadet. dette kan ændres på linje 190.

## Programming Language: 
Python

## Installation
installer disse packages for at køre Multi-threading-PDF-Reader

openpyxl==3.1.5
packaging==24.1
pandas==2.2.3
PyPDF2==3.0.1
requests==2.32.3
XlsxWriter==3.2.0



## kørsel:
(pt. er filen der downloades fra hardcoded ind, så dette behøves ikke at oplyses.
Filen kører til den stoppes.

python .\download_files.py

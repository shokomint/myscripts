#!/bin/sh
PDF_GET="/Users/shoko/Develop/myscripts/shuin_QandA.py"
PDF_CONV="/Users/shoko/Develop/pdfminer.six/tools/pdf2txt.py"
PDF_DIR="/Users/shoko/Develop/myscripts/shuin_downloads/"
TXT="/Users/shoko/Downloads/q_and_a.txt"

python3 ${PDF_GET} -d $1 > ${TXT} 
python3 ${PDF_CONV} -V "${PDF_DIR}q_$1.pdf" >> ${TXT}
python3 ${PDF_CONV} -V "${PDF_DIR}a_$1.pdf" >> ${TXT}


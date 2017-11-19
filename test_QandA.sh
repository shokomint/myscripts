#!/bin/sh

PYTHON=python3
SHU_PDF_GET="/Users/shoko/Develop/myscripts/shuin_QandA.py"
SAN_PDF_GET="/Users/shoko/Develop/myscripts/sanin_QandA.py"
SHU_PDF_DIR="/Users/shoko/Develop/myscripts/shuin_downloads/"
SAN_PDF_DIR="/Users/shoko/Develop/myscripts/sanin_downloads/"

PDF_CONV="/Users/shoko/Develop/pdfminer.six/tools/pdf2txt.py"
TXT="/Users/shoko/Downloads/q_and_a.txt"

ARG_TYPE=$1
ARG_QNUM=$2
if [ ${ARG_TYPE} == "shu" ]; then

	${PYTHON} ${SHU_PDF_GET} -d ${ARG_QNUM} > ${TXT} 

	if [ -f "${SHU_PDF_DIR}q_${ARG_QNUM}.pdf" ]; then
		${PYTHON} ${PDF_CONV} -V "${SHU_PDF_DIR}q_${ARG_QNUM}.pdf" >> ${TXT}
	fi
	if [ -f "${SHU_PDF_DIR}a_${ARG_QNUM}.pdf" ]; then
		${PYTHON} ${PDF_CONV} -V "${SHU_PDF_DIR}a_${ARG_QNUM}.pdf" >> ${TXT}
	fi

elif [ ${ARG_TYPE} = "san" ]; then
	${PYTHON} ${SAN_PDF_GET} -d ${ARG_QNUM} #> ${TXT} 
	
	if [ -f "${SAN_PDF_DIR}q_${ARG_QNUM}.pdf" ]; then
		echo "${SAN_PDF_DIR}q_${ARG_QNUM}.pdf"
		${PYTHON} ${PDF_CONV} -V "${SAN_PDF_DIR}q_${ARG_QNUM}.pdf" #>> ${TXT}
	fi
	if [ -f "${SAN_PDF_DIR}a_${ARG_ARG_QNUM}.pdf" ]; then
		${PYTHON} ${PDF_CONV} -V "${SAN_PDF_DIR}a_${ARG_QNUM}.pdf" #>> ${TXT}
	fi

else
	echo "error"
fi

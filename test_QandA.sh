#!/bin/sh

PYTHON=python3
PERL=perl
SHU_PDF_GET="/Users/shoko/Develop/myscripts/shuin_QandA.py"
SAN_PDF_GET="/Users/shoko/Develop/myscripts/sanin_QandA.py"
SHU_PDF_DIR="/Users/shoko/Develop/myscripts/shuin_downloads/"
SAN_PDF_DIR="/Users/shoko/Develop/myscripts/sanin_downloads/"

PDF_CONV="/Users/shoko/Develop/pdfminer.six/tools/pdf2txt.py"
TXT_CONV1="/Users/shoko/Develop/myscripts/conv_QandA.py"
TXT_CONV2="/Users/shoko/Develop/myscripts/conv_QandA.pl"
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

    ${PYTHON} ${TXT_CONV1} -f ${TXT} 

    ${PERL} ${TXT_CONV2} ${TXT}

elif [ ${ARG_TYPE} = "san" ]; then
	${PYTHON} ${SAN_PDF_GET} -n ${ARG_QNUM} 
	
else
	echo "error"
fi

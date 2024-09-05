from typing import Optional, Union
from abc import ABC, abstractmethod

from pdfminer.high_level import extract_text
# https://github.com/pdfminer/pdfminer.six
# https://pdfminersix.readthedocs.io/en/latest/tutorial/highlevel.html


class CvParseInterface(ABC):
    @staticmethod
    @abstractmethod
    def cv_pdf_to_text():
        pass

class CvParser(CvParseInterface): 
    @staticmethod
    def cv_pdf_to_text(path_to_pdf_cv: str, dst_text: Optional[str]) -> str:
        '''
        If dst_text not None when saved to dst_text
        '''
        text = extract_text(path_to_pdf_cv)

        if dst_text is not None:
             with open(dst_text, 'w') as file:
                file.write(text)

        return text







if __name__ == "__main__":

    pdf_list = [
        "data/CV_NaumtsevAleksandr.pdf",
        "data/Savin_Back_Go.pdf"
    ]


    text = CvParser.cv_pdf_to_text(
        path_to_pdf_cv = pdf_list[1],
        dst_text="data/text_Savin_Back_Go.txt"
    )

    


   




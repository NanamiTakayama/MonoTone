# -*- coding: utf-8 -*-
#https://dev.classmethod.jp/beginners/python-py-googletrans/

from googletrans import Translator

def transe():
    translator = Translator()
    print(translator.translate('flower,rainbow,test,pencil,右',src='en' ,dest='ja'))



if __name__ == '__main__':
    transe()

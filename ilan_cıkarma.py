# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

def removesatir(string): ##SAYFADAN GELEN VERİDEKİ SATIRLARI KALDIRIR
    string=string.replace('\n','')
    return string

def remove_ilk_bosluk(string): ##SAYFADAN GELEN VERİDEKİ İLK BOŞLUĞU KALDIRIR
    string=string.strip()
    return string

def sayfa_sayısı(s): ##İLAN ARARKEN KAÇ SAYFA İLAN OLDUĞUNU BULUR.
    r = requests.get(s)
    print(s)
    source = BeautifulSoup(r.content, "html.parser")
    numaralar = []
    dizi=[]
    numara = source.find_all('ul', class_='he-pagination__links')
    for n in numara: ##VERİYİ EKLER
        numaralar.append(n.text)
    if(len(numaralar)==0): ##İLAN 1 SAYFA İSE.....
        return  1
    for rakam in numaralar[0]: ##VERİDEKİ SAYI PARÇALARINI TEK TEK DİZİYE EKLER
        dizi.append(rakam)
    if(5<len(dizi)<10): ##DİZİNİN BOYUTU 5 İLE 10 ARASINDA İSE SAYFA SAYISI SON ELEMAN OLUR
        sayi=dizi[len(dizi)-1]
        return sayi
    sayi = ''
    for i in range(8, len(dizi)): ###EĞER VERİ 12345...99 FORMATINDA İSE 99 U BULUR VE EKLER
        sayi = sayi + dizi[i]
    if(len(dizi)==5): #EĞER VERİ 12345 İSE YAPAR
        sayi=6
    if(len(dizi)==2):
        return 2
    return sayi

def ilan_bulma(tur,sehir):
    if(tur=='konut'):           #SADECE KONUT KATEGORİSİNDE LİNK FARKLI
        s='https://www.hepsiemlak.com/'+sehir+'-satilik'
    else:
        s = 'https://www.hepsiemlak.com/'+sehir+'-satilik/' +tur
    page=int(sayfa_sayısı(s))
    p=open('dosya.txt', 'a', encoding="utf-8")
    for sayfa in range(2,page+2):
        print('SAYFA SAYISI:',page)
        a = str(sayfa)
        print(s,'ALINDI')
        r = requests.get(s)
        source = BeautifulSoup(r.content,"html.parser")
        jobs=source.find_all('div',class_='list-view-content')
        liste=[]
        for i in jobs:
            liste.append(i.text)

        for i in range(0,len(liste)):
            string=liste[i]
            Tr2Eng = str.maketrans('çğıöşüIÜÖŞÇĞ', "cgiosuiuoscg")
            string=string.translate(Tr2Eng)

            with open('file.txt', 'w', encoding="utf-8") as f:
                f.write(string)
                f.close()
            dosya=open('file.txt','r', encoding="utf-8")
            satirlar=[]
            satirlar_2=[]
            for i in dosya:
                satirlar.append(remove_ilk_bosluk(i))

            for y in range(0,len(satirlar)):
                satirlar_2.append(removesatir(satirlar[y]))
            x=''

            for i in range(0,len(satirlar_2)):
                x=x +'   '+ satirlar_2[i]
            p.write(str(remove_ilk_bosluk(x)))###TÜM İLAN BİLGİLERİ
            p.write('\n')
        if (tur == 'konut'):
            s = 'https://www.hepsiemlak.com/'+sehir+'-satilik?page=' + a
        else:
            s = 'https://www.hepsiemlak.com/'+sehir+'-satilik/' + tur + '?page=' + a

turler=['konut','isyeri', 'arsa','devremulk','turistik-isletme']
sehir=input(('LÜTFEN İLAN ARAMAK İSTEDİĞİNİZ EGE VEYA MARMARA BÖLGESİNDEN BİR ŞEHİR GİRİNİZ:'))
Tr2Eng = str.maketrans('çğıöşü',"cgiosu")
sehir=sehir.translate(Tr2Eng)
f = open('dosya.txt', 'w', encoding="utf-8")
f.write('########################################################'+'KONUT'+ '######################')
f.write('\n')
f.close()
ilan_bulma(turler[0],sehir)
for i in range(1,len(turler)):
    p = open('ilanlar.txt', 'a', encoding="utf-8")
    p.write('####################################################'+ turler[i]+ '###############################################################################################')
    p.write('\n')
    p.close()
    ilan_bulma(turler[i],sehir)

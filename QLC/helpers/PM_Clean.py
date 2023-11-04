import re
import string

def cleanbath(num):
    num = num.replace('Bathrooms:','').replace(' ','')
    try:
        return int(num)
    except:
        return num

def cleanref(num):
    num = num.replace('Ref:','').replace(' ','')
    try:
        return int(num)
    except:
        return num

def cleansize(num):
    num = num.replace('Size:','').replace('sqm','').replace(' ','')
    try:
        return int(num)
    except:
        return num
    
def cleanprice(num):
    num = num.replace('€','').replace(' per ','/').replace(',','')
    try:
        return int(num)
    except:
        return num
    
def cleanfeat(feat):
    feat = feat.replace('\r','')
    return feat

def cleandescr(descr):
    descr = descr.replace('Property description\n\t\t','')
    end = descr.index('\t\t\n')
    return descr[:end]
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re

import time
# from geopy.geocoders import Nominatim
# from geopy.exc import (GeocoderTimedOut,
#                         GeocoderQueryError,
#                         GeocoderQuotaExceeded,
#                         ConfigurationError,
#                         GeocoderParseError
#                         )

def clean_text(x):
    x = x.replace('(','').replace(')','').replace('[','').replace(']','').replace('@','')
    x = x.replace('!','').replace('#','').replace('?','').replace('/','').replace('.','')
    x = x.replace('£','').replace('$','').replace('%','').replace('&','').replace('*','')
    
    return x
                                                                           
def calc_Bedrooms(df,listings_type):
    prop_no_Beds = []
    
    if listings_type == 'rent':
        
        for prop in df['Heading']:
            Bool = False
            
            # 0-9 Bedrooms
            for i in range(0,9):
                if '{} Bedroom'.format(i) in prop:
                    # check whether greater than 10
                    for j in range(10,30):
                        if '{} Bedroom'.format(j) in prop:
                            prop_no_Beds.append(int('{}'.format(j)))
                            Bool = True
                    # Case less than 10        
                    if Bool == False:
                        prop_no_Beds.append(int('{}'.format(i)))
                        Bool = True
            # Case no bedroom
            if Bool == False:
                prop_no_Beds.append(np.nan)
                
        
    if listings_type == 'sale':      
        for prop in df['Heading']:        
            Bool = False
            for i in range(0,9):
                if '{} Bedroom'.format(i) in prop:
                    for j in range(10,50):
                        if '{} Bedroom'.format(j) in prop:
                            prop_no_Beds.append(int('{}'.format(j)))
                            Bool = True
                    if Bool == False:
                        prop_no_Beds.append(int('{}'.format(i))) 
                        Bool = True
            if Bool == False:
                prop_no_Beds.append(np.nan)
                
    return prop_no_Beds

# Clean text in features
def clean_Feats(df):
    feats = df['Features'].values
    for i in range(0, len(feats)):
        try:
            text = ''.join(feats[i])
            feats[i] = re.split(r'\W+', text)
        except:
            pass
    return feats

# Create checklist for feature
def extract_FeatList(df,feat):
    df1 = df['Features'].fillna('N/A')
    featlist = []
    filter_list = [feat in ''.join(y).lower() for y in [x for x in df1]]
    for y in filter_list:
        if y==True:
            featlist.append(1)
        else:
            featlist.append(0)
    return featlist

def extract_Feats(df,feat):
#df[feat]
    feat_list = extract_FeatList(df,feat)
    df['Town View'] = feat_list(df,'Town View','town view')
    df['Sea View'] = feat_list(df,'Sea View','sea view')
    df['Valley View'] = feat_list(df,'Valley View','valley view')
    df['Finished'] = feat_list(df,'Finish','finish')
    df['Furnished'] = feat_list(df,'Furnish','furnish')
    df['Garage'] = feat_list(df,'Garage','garage')
    df['Terrace'] = feat_list(df,'Terrace','terrace')
    df['Balcony'] = feat_list(df,'Balcony','balcony')
    df['Pool'] = feat_list(df,'Pool','pool')
    df['Parking'] = feat_list(df,'Parking','parking')
    df['Garden'] = feat_list(df,'Garden','garden')
    df['Yard'] = feat_list(df,'Yard','yard')
    
def extract_PropType(df):
    prop_type = []
    for prop in df['Heading']:
        if 'Office' in prop:
            prop_type.append('Office')

        elif 'Apartment' in prop:
            if 'Block of Apartments' in prop:
                prop_type.append('Block of Apartments')
            else:
                prop_type.append('Apartment')

        elif 'Penthouse' in prop:
            prop_type.append('Penthouse')

        elif 'Maisonette' in prop:
            prop_type.append('Maisonette')  

        elif 'Garage' in prop:
            prop_type.append('Garage')

        elif 'Villa' in prop:
            if 'Semi-Detached Villa' in prop:
                prop_type.append('Semi-Detached Villa')
            elif 'Detached Villa' in prop:
                prop_type.append('Detached Villa')
            elif 'Village House' in prop:
                prop_type.append('Village House')
            else:
                prop_type.append('Villa')

        elif 'Commercial Property' in prop:
            prop_type.append('Commercial Property')

        elif 'Land' in prop:
            if 'Farm Land' in prop: #none for rent
                prop_type.append('Farm Land')
            else:
                prop_type.append('Land')

        elif 'Shop' in prop:
            prop_type.append('Shop')

        elif 'Plot' in prop:  #none for rent
            prop_type.append('Plot')

        elif 'House' in prop:
            if 'Farm House' in prop:
                prop_type.append('Farm House')
            elif 'Terraced House' in prop:
                prop_type.append('Terraced House')
            elif 'Town House' in prop:
                prop_type.append('Town House')
            elif 'House of Character' in prop:
                prop_type.append('House of Character')
            elif 'Country House' in prop: #none for rent
                prop_type.append('Country House')
            elif 'Semi-Detached House' in prop: #none for rent
                prop_type.append('Semi-Detached House')
            elif 'Village House' in prop:
                pass
            elif 'Guest House' in prop:
                prop_type.append('Guest House')
            else:
                prop_type.append('House')

        elif 'Site' in prop:  #none for rent
            prop_type.append('Site')

        elif 'Palazzo' in prop:
            prop_type.append('Palazzo')

        elif 'Bungalow' in prop:
            if 'Semi-Detached Bungalow' in prop:
                prop_type.append('Semi-Detached Bungalow')
            elif 'Terraced Bungalow' in prop:
                prop_type.append('Terraced Bungalow')
            else:
                prop_type.append('Bungalow')

        elif 'Warehouse' in prop:
            prop_type.append('Warehouse')

        elif 'Showroom' in prop:
            prop_type.append('Showroom')

        elif 'Restaurant' in prop:
            prop_type.append('Restaurant')

        elif 'Residential Development' in prop: #none for rent
            prop_type.append('Residential Development')

        elif 'Factory' in prop:
            prop_type.append('Factory')

        elif 'Commercial Development' in prop:
            prop_type.append('Commercial Development')

        elif 'Industrial Building' in prop:
            prop_type.append('Industrial Building')

        elif 'Studio' in prop:
            prop_type.append('Studio')

        elif 'Cafe' in prop:
            prop_type.append('Cafe')

        elif 'Retail Property' in prop:
            prop_type.append('Retail Property')

        elif 'Storage' in prop:
            prop_type.append('Storage')

        elif 'Pub' in prop:
            prop_type.append('Pub')

        elif 'Healthcare Facility' in prop:
            prop_type.append('Healthcare Facility')

        elif 'Industrial Development' in prop:  #none for rent
            prop_type.append('Industrial Development')

        elif 'Cottage' in prop:
            prop_type.append('Cottage')

        elif 'Leisure Facility' in prop:
            prop_type.append('Leisure Facility')

        elif 'Bar' in prop:
            prop_type.append('Bar')

        elif 'Hotel' in prop:
            prop_type.append('Hotel')

        elif 'Duplex' in prop:
            prop_type.append('Duplex')

        elif 'Airspace' in prop:
            prop_type.append('Airspace')

        elif 'Parking' in prop:        
            prop_type.append('Parking')

        else:
            prop_type.append(np.nan)

    return prop_type

def HL_Type(df):
    Residential = ['Apartment', 'Penthouse', 'Maisonette', 'Villa', 'House', 'Bungalow',                      'Cottage', 'Duplex', 'Palazzo', 'Residential']
    Commercial = ['Office', 'Garage', 'Shop', 'Warehouse', 'Showroom', 'Restaurant',                         'Commercial', 'Factory', 'Industrial', 'Cafe', 'Retail', 'Pub',                             'Healthcare', 'Bar', 'Hotel']
    Other = ['Land', 'Site', 'Plot', 'Airspace'] 

    prop_type = []
    for prop in df['Type']:
        if prop in Residential:
            prop_type.append('Residential')

        elif prop in Commercial:
            prop_type.append('Commercial')

        elif prop in Other:
            prop_type.append('Other')
        
        else:
            prop_type.append(np.nan)

    return prop_type


def extract_Locality(df):
    # can use .replace() method as well
    prop_loc = []
    # Split heading into array of words
    props = np.array([x.split() for x in df['Heading']], dtype=object)
    for i in range(0,len(df['Heading'])):
        if 'Venera' in props[i][-1]:
            prop_loc.append('Santa Venera')
        
        elif 'Tuffieha' in props[i][-1]:
            prop_loc.append('Ghajn Tuffieha')
            
        elif 'Gwann' in props[i][-1]:
            prop_loc.append('San Gwann')
            
        elif 'Julian' in props[i][-1]:
            prop_loc.append('St Julians')
            
        elif 'Giorni' in props[i][-1]:
            prop_loc.append('Ta Giorni')
            
        elif 'Ridge' in props[i][-1]:
            prop_loc.append('High Ridge')
            
        elif 'Ic-Caghaq' in props[i][-1]:
            prop_loc.append('Bahar ic-Caghaq')
            
        elif 'il-Bajda' in props[i][-1]:
            prop_loc.append('Blata il-Bajda')
            
        elif 'Xbiex' in props[i][-1]:
            prop_loc.append("Ta' Xbiex")
            
        elif 'Lucija' in props[i][-1]:
            prop_loc.append('Santa Lucija')
                            
        elif 'Cambridge' in props[i][-1]:
            prop_loc.append('Fort Cambridge')
                            
        elif 'Point' in props[i][-1]:
            prop_loc.append('Tigne Point')
                            
        elif 'Andrews' in props[i][-1]:
            prop_loc.append('St Andrews')
                            
        elif 'Bay' in props[i][-1]:
            prop_loc.append(props[i][-3] + ' '+ props[i][-2] + ' ' + props[i][-1])
                            
        elif 'Targa' in props[i][-1]:
            prop_loc.append('San Pawl tat Targa')
            
        elif 'Guardamangia' in props[i][-1]: 
            prop_loc.append('Gwardamanga')
            
        elif 'Chambray' in props[i][-1]:
            prop_loc.append('Fort Chambray')
        
        elif 'Lawrenz' in props[i][-1]:
            prop_loc.append('San Lawrenz')
                            
        else:
            # Reason for this method
            prop_loc.append(props[i][-1])
                            
        prop_loc[i] = clean_text(prop_loc[i])

    prop_loc
    return prop_loc
                            
def HL_Locality(df):
    prop_loc = []
    for loc in df['Locality']:
        if loc in ['Tigne Point', 'Fort Cambridge']:
            prop_loc.append('Sliema')
                 
        elif loc in ['Pendergardens', 'Portomaso', "St Julian's", 'Paceville', 'Mercury', 'Ta Giorni']:
            prop_loc.append('St Julians')
               
        elif loc in ['Birguma', 'San Pawl tat Targa']:
            prop_loc.append('Naxxar')          
        else:
            prop_loc.append(loc)
    return prop_loc


def clean_Price(df, listings_type):
    prices = []
    
    if listings_type == 'rent':
        for rp in df['Price']:
            try:    
                if 'month' in rp:
                    if rp.find('\t\t') != -1:
                        #select string up to /month
                        rp = int(rp[:rp.find('/month\t')])
                        prices.append(int(rp))
                    else:
                        rp = int(rp.replace('/month',''))
                        prices.append(int(rp))    

                elif 'year' in rp:
                    if rp.find('\t\t') != -1:
                        rp = int(rp[:rp.find('/year\t')])
                        prices.append(int(rp/12))
                    else:
                        rp = int(rp.replace('/year',''))
                        prices.append(int(rp/12))

                elif 'week' in rp:
                    if rp.find('\t\t') != -1:
                        rp = int(rp[:rp.find('/week\t')])
                        prices.append(int((52*rp)/12))
                    else:
                        rp = int(rp.replace('/month',''))
                        prices.append(int((52*rp)/12))

                elif 'day' in rp:
                    if rp.find('\t\t') != -1:
                        rp = int(rp[:rp.find('/day\t')])
                        prices.append(int(31*rp))
                    else:
                        rp = int(rp.replace('/day',''))
                        prices.append(int(31*rp))
                elif 'Price on Request':
                    prices.append(np.nan)

            except:
                prices.append(np.nan)
                pass
       
    elif listings_type == 'sale':
        for sp in df['Price']:
            try:    
                if 'Price on Request' in str(sp):
                    prices.append(np.nan)
                else:
                    prices.append(int(sp))

            except:
                prices.append(np.nan)
                pass

    return prices


def price_SQM(df):
    pricePerSqm = df['Price']/df['Size']
    return pricePerSqm
       
def price_Bed(df):
    pricePerBed = df['Price']/df['No_Beds']
    return pricePerBed
               
               
def clean_agencies(df):    
    agencies = []
    for branch in df['Branch']:
        if ('Frank Salt' in branch):
            agencies.append('Frank Salt')
        elif ('REMAX' in branch) or ('RE/MAX' in branch) or ('Remax' in branch):
            agencies.append('REMAX')
        elif 'Ben Estates' in branch:
            agencies.append('Ben Estates')
        elif 'Zanzi' in branch:
            agencies.append('Zanzi Homes')
        else:
            agencies.append(branch)
    return agencies

               

# def latlon_locality(loc):
#     geolocator = Nominatim(user_agent="my_app")
#     if loc == 'San Pawl tat Targa':
#         return (35.92135993118856, 14.439146496791702)
#     elif loc == 'Fort Cambridge':
#         return (35.9100966,14.5061214)
#     elif loc == 'Mtahleb':
#         return (35.88084057821896, 14.353329317329878)

#     else:
#         try:
#             location = geolocator.geocode("{}, Malta".format(loc))
#             return (location.latitude, location.longitude)
#         except:
#             time.sleep(10)
#             latlon_locality(loc)
        






































































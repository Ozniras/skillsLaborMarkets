import numpy as np
import pandas as pd

def complIndexClean(df=None,
                   commodityCode='commoditycode',
                   error='XXXX',
                   dataLevel=['exporter', 'eci']):
    """
    Takes the complexity index files provided by Harvard MIT 
    (already pre-processed to use only one year)
    Eliminates 'errors' (XXXX values)
    Returns one value (of Economic Complexity Index) per country
    """
    
    # Delete some errors (?)
    df[commodityCode] = df[commodityCode][df[commodityCode].astype(str) != error].astype(int)
    # Data is at product level, eci is constant at country (exporter) level
    return df[dataLevel].drop_duplicates()

def countryMerger():
    """
    Merges iso2 and iso3 to LI country_sk via iso2 (aka country_code)
    """
    iso = pd.read_csv('../00_originalData/isoConversions.csv', keep_default_na=False, na_values='')
    iso[iso['country'] == 'Congo, (Kinshasa)'] = 'Congo, Dem. Rep.'
    iso[iso['country'] == 'Congo (Brazzaville)'] = 'Congo, Rep'
    iso[iso['country'] == 'Cape Verde'] = 'Cabo Verde'
    iso[iso['country'] == 'Gambia'] = 'Gambia, The'
    iso[iso['country'] == 'Sao Tome and Principe'] = 'São Tomé and Principe'
    iso[iso['country'] == 'Tanzania, United Republic of'] = 'Tanzania'
    
     
    
    liCountry = pd.read_csv('../00_originalData/li_country.tsv', sep='\t')[['country_sk', 'country_code']]
    liCountry.rename(columns={'country_code' : 'iso2'}, inplace=True)
    liCountry['iso2'] = liCountry['iso2'].str.upper()
    
    # by using inner, we get rid of country_sk = 169, LI's the "not elsewhere classified"
    return pd.merge(iso, liCountry, on='iso2', how='inner').drop(['iso2', 'isoUN_M49'], axis=1)

def skillPenToOutcome(skillPen=None, 
                      outcome=None, 
                      outcomeFields=['eci']):
    """
    Adds outcome fields (ECI, or [GDPPC2016, EMPL]) to skill penetration matrix
    """
    # Get mapping with iso3, iso3, and country_sk
    isoMapping = countryMerger().set_index('country_sk') 
    
    # Add skills matrix
    temp = pd.merge(isoMapping, skillPen, right_index=True, left_index=True, how='inner')
    
    # Add outcome variables
    outcomeFields.extend(['iso3'])
    return pd.merge(temp.reset_index(), outcome[outcomeFields], on='iso3', how='inner'
                   ).set_index('country_sk').drop('iso3', axis=1) # indexed by country_sk
    
    

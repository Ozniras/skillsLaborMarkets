import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def setup(mapFile=None, 
          mapKeys=None, 
          econFile=None, 
          econKeys={'countryKey':None, 'cityKey':None, 'yearKey':None, 'rankingKey':None, 'yearForEconData':None}, 
          skillData=None, 
          skillKeys={'parentKey':None, 'penetrationKey':None},
          inDoubt='first'):
    '''Eliminate duplicates keys-for-merge in mapping file from LinkedIn and 
    in Oxford Economics Competitive Cities data (keep first).
    Then merge LinkedIn skill data (by country and city) with Oxford Economics 
    Competitive Cities data being mapping file from LinkedIn'''
    
    print('Duplicated cities in city file by {0}:\n'.format(mapKeys))
    print(mapFile[mapFile[mapKeys].duplicated(keep=False)])
    mapFileReady = mapFile.drop_duplicates(subset=mapKeys, keep=inDoubt).copy()
    
    econFileYear = econFile[econFile[econKeys['yearKey']] == econKeys['yearForEconData']].copy()
    print('\nDuplicated cities in economic characteristics by {0}:\n'.format(econKeys['cityKey']))
    print(econFileYear[econFileYear[econKeys['cityKey']].duplicated(keep=False)])
    econFileYear.drop_duplicates(subset=econKeys['cityKey'], keep=inDoubt, inplace=True)
    
    skillPen = skillData.set_index(mapKeys)[[skillKeys['parentKey'], skillKeys['penetrationKey']]].pivot(columns=skillKeys['parentKey']).fillna(0)[skillKeys['penetrationKey']]
    
    df = pd.merge(pd.merge(skillPen, mapFileReady.set_index(mapKeys), left_index=True, right_index=True, how='inner', validate='m:1').reset_index(), econFileYear[[econKeys['countryKey'], econKeys['cityKey'], econKeys['rankingKey']]], left_on='city_OE', right_on='City', validate='1:1', how='inner').set_index(mapKeys)
    
    return df

def selecter(db=None, 
             topBottom=2,
             fieldsToDrop=['country_sk', 'region_sk', 'iso2c', 'city_OE', 'city_LinkedIn'], 
             countryField='Country', 
             cityField='City', 
             rankingField='city_gdp_capita'):
    
    keeper = db.reset_index().drop(fieldsToDrop, axis=1).groupby(
        countryField).filter(
        lambda x: x[cityField].count() >= topBottom * 2).sort_values(
        [countryField, rankingField], ascending=False)
    header = keeper.groupby(countryField).head(topBottom)
    tailer = keeper.groupby(countryField).tail(topBottom)
    keeper = header.append(tailer).reset_index().sort_values([countryField, rankingField], ascending=False).set_index([countryField, cityField])
    return header, tailer, keeper

def graph(header=None, 
          tailer=None, 
          countryField='Country', 
          cityField='City', 
          rankingKey='city_gdp_capita'):
    x = tailer.drop([cityField, rankingKey, countryField], axis=1).mean(axis=0).T.sort_index()
    y = header.drop([cityField, rankingKey, countryField], axis=1).mean(axis=0).T.sort_index()
    plt.plot(x, y, 'r.')
    line = np.linspace(0, max(plt.ylim()[1], plt.xlim()[1]), 500)
    plt.plot(line, line, 'k-')
    for i in range(len(x.index)):
        plt.text(x[i], y[i], x.index[i], fontsize=8);
    fig = plt.gcf()
    fig.set_size_inches(11.7, 8.3)
    plt.xlabel('Pen rate in low ranked')
    plt.ylabel('Pen rate in high ranked')
    plt.title('Differences in skill penetration between cities ranked by {}'.format(rankingKey))
    plt.savefig('../city_' + rankingKey + '.png', bbox_inches='tight')
    plt.show()

def differences(header=None, tailer=None, number=None, countryField='Country', cityField='City', rankingKey='city_gdp_capita'):
    
    x = tailer.set_index(cityField).T.drop([rankingKey, countryField], axis=0).mean(axis=1).sort_index()
    y = header.set_index(cityField).T.drop([rankingKey, countryField], axis=0).mean(axis=1).sort_index()
    diffSkills = (y - x).sort_values(ascending=False)
    print('FOR NUMBER OF CITIES AT TOP AND AT BOTTOM = {0}\n'.format(number))
    print('Number of positive differences: {0}'.format(str(len(diffSkills[diffSkills > 0]))))
    print('Number of negative differences: {0}'.format(str(len(diffSkills[diffSkills < 0]))))
    print('Number of no differences: {0}'.format(str(len(diffSkills[diffSkills == 0]))))
    print('\nTop 10 positive differences:')
    print(diffSkills.head(10))
    print('\nTop 10 negative differences:')
    print(diffSkills.tail(10))
    print('\nSkills with a diff of at least 1% in abs:')
    print(diffSkills[np.abs(diffSkills) > 0.01])
    return diffSkills

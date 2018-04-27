import numpy as np
import pandas as pd

def imposeSkillsLimit(df=None, 
                skillName='std_skill_name', 
                level1='country_sk',
                level1count='member_ct',
                skillLevel='industry_sk', 
                skillCount='skill_member_ct',
                threshold=0.001):
    """ 
    Expects a df with skill name, SKILL member count at some sub-national level (eg country and industry, then skill), 
    and member counts at the same sub-national level (eg country and industry), but repeated for each skill
    Aggregates at two levels: country and industry or city
    Returns dataframe of skills (as in skillName) with GLOBAL pen rates (penRate) of at least threshold
    """
    df = df.copy() # Do NOT alter original dataframe
    skillTotals = df.groupby(skillName).agg({skillCount : 'sum'}).rename({skillCount : 'penRate'}, axis=1)
    memTotal = df.groupby([level1, skillLevel]).agg({level1count : 'max'}).sum().rename({level1count : 'penRate'})
    penRate = skillTotals / memTotal
    toReturn = penRate.loc[penRate['penRate'] >= threshold, :].reset_index()
    print('\nSkill with minimum number of global members given threshold:')
    print(toReturn['penRate'].min() * memTotal)
    return toReturn

def skillsLimit(df=None,
          skillName='std_skill_name',
          level1='country_sk',
          level1count='member_ct',
          skillLevel='industry_sk',
          skillCount='skill_member_ct',
          threshold=0.001,
          penRate='penRate'):
    
    skillsKeep = imposeSkillsLimit(df=df,
          skillName=skillName,
          level1=level1,
          level1count=level1count,
          skillLevel=skillLevel,
          skillCount=skillCount,
          threshold=threshold)
    
    df = df.copy()
    df = pd.merge(df, skillsKeep, on=skillName, how='inner')
    return df.drop(penRate, axis=1)
    
def createCountryPenRates(df=None,
                         skillName='std_skill_name',
                         level1='country_sk',
                         level1count='member_ct',
                         skillCount='skill_member_ct',
                         penRate='penRate'):
    """
    Expects a df with skill name, SKILL member count at some sub-national level (eg country and industry, then skill), 
    and member counts at the same sub-national level (eg country and industry), but repeated for each skill
    Returns dataframe of penetration rates for country x skills, with 0 for NaN
    """
    skillTotal = df.groupby([level1, skillName]).agg({skillCount : 'sum'})
    memTotal = df.groupby(level1).agg({level1count: 'max'})
    countrySkillPen = memTotal.join(skillTotal, how='inner')
    countrySkillPen[penRate] = countrySkillPen[skillCount] / countrySkillPen[level1count]
    countrySkillPen.drop([level1count, skillCount], axis=1, inplace=True)
    countrySkillPen.reset_index(inplace=True)
    return countrySkillPen.set_index(level1)[[skillName, penRate]].pivot(
        columns=skillName).fillna(0)[penRate]

def readLimitMergeSkills(baseFile=None,
                        skillName='std_skill_name',
                        level1='country_sk',
                        level1count='member_ct',
                        skillLevel='industry_sk',
                        skillCount='skill_member_ct',
                        threshold=0.001):
    """
    Limit skills used to some global penetration MINIMUM threshold
    """
    # Read and show
    li = pd.read_csv(baseFile, sep='\t')
    print('Original file\n')
    print(li.head())
    print("\nNumber of individual skills without censoring (beyond LI's rule of 30)")
    print(li[skillName].drop_duplicates().shape)
        
    #Limit to skills with global pen ratesof at least 0.1%
    li = skillsLimit(df=li,
                     skillName=skillName,
                     level1=level1,
                     level1count=level1count,
                     skillLevel=skillLevel,
                     skillCount=skillCount,
                     threshold=threshold)

    print('\nSkills after limiting to ', str(threshold))
    print(li[skillName].drop_duplicates().shape)
        
    return createCountryPenRates(df=li,
                                 skillName=skillName,
                                 level1=level1,
                                 level1count=level1count,
                                 skillCount=skillCount)

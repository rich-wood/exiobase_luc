# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 19:31:52 2021

@author: Richard Wood

This script generates multipliers from deforestation data, using EXIOBASE 3

The script uses data available at:
https://zenodo.org/record/4250532
but allocated to EXIOBASE3 industries

EXIOBASE3 is available at:
https://zenodo.org/record/4588235
Note, v3.8.2 is used in the generation of results in this script.

This is an update to work at:
https://doi.org/10.1016/j.gloenvcha.2019.03.002
https://doi.org/10.1016/j.jclepro.2018.12.313  

You must set the directory for the exiobase data with
exio3_folder, or you can uncomment text to use the autodownload function

Requires pandas, numpy and pymrio to run.
Pymrio available at: https://github.com/konstantinstadler/pymrio
    
"""
import pandas as pd
import pymrio 
import numpy as np

# All data on deforestation emissions is assumed available in this working directory, but EXIOBASE 3 data needs locating
# set location of exiobase data (if you have not downloaded EXIOBASE3 yet, see commented text below for autodownload)
exio3_folder = "F:/indecol/Projects/MRIOs/EXIOBASE3/EXIOBASE_3_8_2/"


# there is a idscrepancy in codes vs names in some files, so load the full classification for renaming later
EX2i=pd.read_csv('EXIOBASE20i.txt',index_col=0,usecols=[1,3],header=None,sep='\t')
EX2i_dict=dict(EX2i.iloc[:, -1] )

# load deforestation data, both single year and all years for checking
df2018= pd.read_csv("OutputExiobaseStructured.csv",header=0, index_col=[0,1],usecols=[0,1,3,4,5])
df_allyears= pd.read_csv("OutputExiobaseAllYears.csv",header=0, index_col=[0,1])
# rename allyears to full names for consistency with exio3
df_allyears.rename(EX2i_dict,axis=0,inplace=True)




for yr in range(2005,2019):
#for yr in range(2018,2019):
    
    # if you need to download exio3, run this:
        # exio_meta = pymrio.download_exiobase3(
        #   storage_folder=exio3_folder, system="ixi", years=[yr] )

# parse exiobase and just calc L and x (no other calcs needed)        
    exio3 = pymrio.parse_exiobase3(path=exio3_folder + 'IOT_'+ str(yr) +'_ixi.zip')
    L=pymrio.calc_L(exio3.A)
    x=pymrio.calc_x_from_L(L, exio3.Y.sum(axis=1))

# obtain the relevant data for specific year
    df_yr=df_allyears.loc[df_allyears['Year'] == yr]
    # reindex (and transpose) so that matrix multiplication can be later performed
    df_yr_full=df_yr.reindex_like(df2018).fillna(0).T
    
    # calculate intensities (notation: s):
    s=pymrio.calc_S(df_yr_full, x)
    # calculate multipliers (notation: m):
    #m_df=(s).dot(L) # run with dataframes
    m=pymrio.calc_M(s, L) #using pymrio, checked that same result as m_df
    m.to_csv('Multipliers_'+ str(yr) +'.csv')
    
    #exio3.Y shows final demand disaggregated by category (columns), we are just interested in total final demand for each region, so sum over categories.
    Ycnt=exio3.Y.groupby(axis=1,level=0,sort=False).agg(sum)
    #note that sort=False above is essential for calc_accounts to work properly later.
    D_cba_cnt=pymrio.calc_e(m,Ycnt)
    
    D_cba_cnt.to_csv('Footprints_Country_'+ str(yr) +'.csv')
    
    
    #note you have to ensure that the region order in columns of Ycnt is the same as in s for this to work, otherwise do it the long-hand way (see D_cba_sec below).
    [D_cba, D_pba, D_imp, D_exp]=pymrio.calc_accounts(s,L,Ycnt,163)
    
    
    D_cba.to_csv('Footprints_Sector_'+ str(yr) +'.csv')
    
    
    if yr == 2018:
        # test for 2018 data (ensure same answer across both versions of extension data)
        s2018=pymrio.calc_S(df2018.T, x)
        # check both methods (numpy vs pandas)
        m2018_np=np.dot(s2018,L) #test with numpy
        m2018_df=s2018.dot(L) # run with dataframes
        sum(sum(abs(m2018_np-m2018_df.values))) # answer should be zero if no problems        
        sum(sum(abs(m2018_np-m.values))) # answer should be zero if no problems - there is a small residual
        m2018_df.to_csv('Multipliers_2018src.csv')
    
    
    
    # now run with disaggregated stressors by origin country/sector - need to diagonalise the extensions, and thus loop over each extension.
    for dftype in df_yr_full.index:    
        
        # firstly just check the product level results
        # multiply each multiplier by the Y block, showing region/sector of origin of final production in rows, and region of consumption in columns
        D_cba_sec_disagg=Ycnt.multiply(m.loc[dftype],axis=0)
        D_cba_sec= D_cba_sec_disagg.groupby(level=1,sort=False).agg(sum)
        #should give the same result as that generated in D_cba - now just used for checking and not written out
        
        
        
        # diagonalise the stressor intensities, one at a time
        s_diag = pd.DataFrame(
            index=s.columns,
            columns=s.columns,
            data=np.diag(s.loc[dftype])        )
        
        # remove zero rows (no deforestation occurs in that sector region combo)
        tmp_indx= (s_diag!= 0).any(axis=1)
        s_diag_nz=s_diag.loc[tmp_indx]

        # calculate disaggregated multipliers
        m_disagg_df=s_diag_nz.dot(L)
        
        #save disaggregated data after dropping zero rows
        m_disagg_df.to_csv('Multipliers_origin_'+ str(yr) +'_'+dftype +'.csv')
        
        #now lets calculate the footprints including the sector/region of origin by using the diagonalised s.
        # note you have to ensure that the region order in columns of Ycnt is the same as in s for this to work, otherwise do it the long-hand way (see D_cba_sec above).
        [D_cba_origin, D_pba_origin, D_imp_origin, D_exp_origin]=pymrio.calc_accounts(s_diag_nz,L,Ycnt,163)
        
        
        #save the footprints by sector/region of origin
        D_cba_origin.to_csv('Footprints_origin_'+ str(yr) +'_'+dftype +'.csv')

        

                
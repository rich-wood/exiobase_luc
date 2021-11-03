# exiobase_luc
Short code to generate multipliers from land use change data on deforestation with the EXIOBASE dataset.
Sector and Region codes are per the EXIOBASE dataset, see below.

Output files:

Footprints_Country_XXXX
- reports footprints by region (corresponding to the Consumption Based Accounts of each region for each year (XXXX)
- units are specified in the naming of each row in the files

Footprints_Sector_XXXX
- reports footprints by sector and region (corresponding to the Consumption Based Accounts of each region and the sector of final demand) for each year (XXXX)
- a disaggregation of Footprints_Country_XXXX
- units are specified in the naming of each row in the files

Footprints_origin_XXXX_YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
- reports footprints by both sector and region of origin AND sector and country of final demand (corresponding to a disaggregation of the Consumption Based Accounts of each region and the sector of final demand) for each year (XXXX)
- a disaggregation of Footprints_Sector_XXXX
- the rows show where the emissions or land use change occurs (e.g. land use change in Brazil that ends up in goods finally consumed in Norway would show Brazil in the rows, and Norway in the columns).
- there is a different file for each type of land use change or emission (YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY). 
- the name of the land use change/emission and corresponding unit is embedded in the file name.


Multipliers_XXXX
- reports footprint multipliers by sector and region of final production 
- unit of the multiplier are constructed by the unit specified in the row name for the numerator, and MEURO (million euro - the native unit of EXIOBASE) in the denomiator. Eg. for Deforestation area, the multiplier unit is ha/MEURO
- multipliers show the supply-chain impacts up to the point of final consumption. 
- if multipliers are multiplied by values of final demand, then you obtain footprints.

Multipliers_origin_XXXX_YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
- as per Multipliers_XXXX, but with the sector and region of origin of the emission/land use change identified.
- a pure disaggregation of Multipliers_XXXX
- there is a different file for each type of land use change or emission (YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY). 
- the name of the land use change/emission and corresponding unit numerator of the multiplier is embedded in the file name.
- units of all multipliers are per MEURO as per Multipliers_XXXX



The script uses data available at:
https://zenodo.org/record/4250532
but allocated to EXIOBASE3 industries
EXIOBASE3 is available at:
https://zenodo.org/record/4588235
Note, v3.8.2 is used in the generation of results in this script.
This is an update to work at:
https://doi.org/10.1016/j.gloenvcha.2019.03.002
https://doi.org/10.1016/j.jclepro.2018.12.313  

import pandas as pd
import pygris as py # Gets coordinates for tracts

incomeCols = {
'B19001_006E':'25k-29kEst','B19001_006M':'25k-29kMar',
'B19001_007E':'30k-34kEst','B19001_007M':'30k-34kMar',
'B19001_008E':'35k-39kEst','B19001_008M':'35k-39kMar',
'B19001_009E':'40k-44kEst','B19001_009M':'40k-44kMar',
'B19001_002M':'Under10kMar','B19001_002E':'Under10kEst',
'B19001_003M':'10k-14kMar','B19001_003E':'10k-14kEst',
'B19001_004M':'15k-19kMar','B19001_004E':'15k-19kEst',
'B19001_005M':'20k-24kMar','B19001_005E':'20k-24kEst',
'B19001_001M':'TotalMar','B19001_001E':'TotalEst',
'B19001_014M':'100k-124kMar','B19001_014E':'100k-124kEst',
'B19001_015M':'125k-149kMar','B19001_015E':'125k-149kEst',
'B19001_016M':'150k-199kMar','B19001_016E':'150k-199kEst',
'B19001_017E':'Above200kEst','B19001_017M':'Above200kMar',
'B19001_010M':'45k-49kMar','B19001_010E':'45k-49kEst',
'B19001_011M':'50k-59kMar','B19001_011E':'50k-59kEst',
'B19001_012M':'60k-74kMar','B19001_012E':'60k-74kEst',
'B19001_013M':'75k-99kMar','B19001_013E':'75k-99kEst',
'NAME':'tractName','GEO_ID':'geoid','year':'Year'
}

raceCols = {
'B03002_001E':'TotalEst','B03002_001M':'TotalMar',
'B03002_005E':'NotHispNativeORalaskanEst','B03002_005M':'NotHispNativeORalaskanMar',
'B03002_004E':'NotHispBlackEst','B03002_004M':'NotHispBlackMar',
'B03002_003E':'NotHispWhiteEst','B03002_003M':'NotHispWhiteMar',
'B03002_002E':'NotHispTotalEst','B03002_002M':'NotHispTotalMar',
'B03002_009E':'NotHispTwoPlusEst','B03002_009M':'NotHispTwoPlusMar',
'B03002_008E':'NotHispOtherRaceEst','B03002_008M':'NotHispOtherRaceMar',
'B03002_007E':'NotHispNativeHaWaiiORPacificEst','B03002_007M':'NotHispNativeHaWaiiORPacificMar',
'B03002_006E':'NotHispAsianEst','B03002_006M':'NotHispAsianMar',
'B03002_011E':'NotHisp2plusRacesNOsomeOtherEst','B03002_011M':'NotHisp2plusRacesNOsomeOtherMar',
'B03002_010E':'NotHisp2RacesOneBeingSomeOtherEst','B03002_010M':'NotHisp2RacesOneBeingSomeOtherMar',
'B03002_015E':'HispNativeORalaskanEst','B03002_015M':'HispNativeORalaskanMar',
'B03002_014E':'HispBlackEst','B03002_014M':'HispBlackMar',
'B03002_013E':'HispWhiteEst','B03002_013M':'HispWhiteMar',
'B03002_012E':'HispTotalEst','B03002_012M':'HispTotalMar',
'B03002_019E':'HispTwoPlusEst','B03002_019M':'HispTwoPlusMar',
'B03002_018E':'HispOtherRaceEst','B03002_018M':'HispOtherRaceMar',
'B03002_017E':'HispNativeHaWaiiORPacificEst','B03002_017M':'HispNativeHaWaiiORPacificMar',
'B03002_016E':'HispAsianEst','B03002_016M':'HispAsianMar',
'B03002_021E':'Hisp2plusRacesNOsomeOtherEst','B03002_021M':'Hisp2plusRacesNOsomeOtherMar',
'B03002_020E':'Hisp2RacesOneBeingSomeOtherEst','B03002_020M':'Hisp2RacesOneBeingSomeOtherMar',
'NAME':'Name','GEO_ID':'geoid','year':'Year'
}

sexbyageCols = {
'B01001_001E':'TotalEst','B01001_001M':'TotalMar',
'B01001_002E':'MTotalEst','B01001_002M':'MTotalMar',
'B01001_003E':'MUnder5Est','B01001_003M':'MUnder5Mar',
'B01001_004E':'M5-9Est','B01001_004M':'M5-9Mar',
'B01001_005E':'M10-14Est','B01001_005M':'M10-14Mar',
'B01001_006E':'M15-17Est','B01001_006M':'M15-17Mar',
'B01001_007E':'M18-19Est','B01001_007M':'M18-19Mar',
'B01001_008E':'M20Est','B01001_008M':'M20Mar',
'B01001_009E':'M21Est','B01001_009M':'M21Mar',
'B01001_010E':'M22-24Est','B01001_010M':'M22-24Mar',
'B01001_011E':'M25-29Est','B01001_011M':'M25-29Mar',
'B01001_012E':'M30-34Est','B01001_012M':'M30-34Mar',
'B01001_013E':'M35-39Est','B01001_013M':'M35-39Mar',
'B01001_014E':'M40-44Est','B01001_014M':'M40-44Mar',
'B01001_015E':'M45-49Est','B01001_015M':'M45-49Mar',
'B01001_016E':'M50-54Est','B01001_016M':'M50-54Mar',
'B01001_017E':'M55-59Est','B01001_017M':'M55-59Mar',
'B01001_018E':'Male60-61Est','B01001_018M':'M60-61Mar',
'B01001_019E':'M62-64Est','B01001_019M':'M62-64Mar',
'B01001_020E':'M65-66Est','B01001_020M':'M65-66Mar',
'B01001_021E':'M67-69Est','B01001_021M':'M67-69Mar',
'B01001_022E':'M70-74Est','B01001_022M':'M70-74Mar',
'B01001_023E':'M75-79Est','B01001_023M':'M75-79Mar',
'B01001_024E':'M80-84Est','B01001_024M':'M80-84Mar',
'B01001_025E':'M85AboveEst','B01001_025M':'M85AboveMar',
'B01001_026E':'FTotalEst','B01001_026M':'FTotalMar',
'B01001_027E':'FUnder5Est','B01001_027M':'FUnder5Mar',
'B01001_028E':'F5-9Est','B01001_028M':'F5-9Mar',
'B01001_029E':'F10-14Est','B01001_029M':'F10-14Mar',
'B01001_030E':'F15-17Est','B01001_030M':'F15-17Mar',
'B01001_031E':'F18-19Est','B01001_031M':'F18-19Mar',
'B01001_032E':'F20Est','B01001_032M':'F20Mar',
'B01001_033E':'F21Est','B01001_033M':'F21Mar',
'B01001_034E':'F22-24Est','B01001_034M':'F22-24Mar',
'B01001_035E':'F25-29Est','B01001_035M':'F25-29Mar',
'B01001_036E':'F30-34Est','B01001_036M':'F30-34Mar',
'B01001_037E':'F35-39Est','B01001_037M':'F35-39Mar',
'B01001_038E':'F40-44Est','B01001_038M':'F40-44Mar',
'B01001_039E':'F45-49Est','B01001_039M':'F45-49Mar',
'B01001_040E':'F50-54Est','B01001_040M':'F50-54Mar',
'B01001_041E':'F55-59Est','B01001_041M':'F55-59Mar',
'B01001_042E':'F60-61Est','B01001_042M':'F60-61Mar',
'B01001_043E':'F62-64Est','B01001_043M':'F62-64Mar',
'B01001_044E':'F65-66Est','B01001_044M':'F65-66Mar',
'B01001_045E':'F67-69Est','B01001_045M':'F67-69Mar',
'B01001_046E':'F70-74Est','B01001_046M':'F70-74Mar',
'B01001_047E':'F75-79Est','B01001_047M':'F75-79Mar',
'B01001_048E':'F80-84Est','B01001_048M':'F80-84Mar',
'B01001_049E':'F85PlusEst','B01001_049M':'F85PlusMar',
'NAME':'Name','GEO_ID':'geoid','year':'Year'
}

files = {'income.csv': incomeCols, 'race.csv':raceCols, 'sexage.csv':sexbyageCols}

# Gets the coordinates
def coordsSearch(year):
    tracts = py.tracts('17', '031', year=year)
    geoid = [col for col in tracts.columns if col.upper().startswith(('GEOID', 'CTIDFP'))][0]
    lat = [col for col in tracts.columns if col.startswith('INTPTLAT')][0]
    lon = [col for col in tracts.columns if col.startswith('INTPTLON')][0]
    tractsF = tracts[[geoid,lat,lon]].copy()
    tractsF.columns = ['key', 'Y', 'X']
    return tractsF

coords = []
for year in range(2009, 2024):
    accuYear = 2000 if year < 2010 else year #2009 is not available in census and is based on year 2000s coordinates which is available
    currentCoords = coordsSearch(accuYear)
    currentCoords['Year'] = str(year)
    coords.append(currentCoords)
allCoords = pd.concat(coords)

# Drops all rows with nan if any / Empty columns / Adds coordinates
for file, colNames in files.items():
    cleanFile = file.replace('.csv', '_clean.csv')
    current = pd.read_csv(file, dtype=str)

    emptyCols = [col for col in current.columns if col.endswith(('EA', 'MA'))]
    current = current.drop(columns=emptyCols)
    current = current.dropna()

    current = current.rename(columns=colNames)

    current['key'] = current['geoid'].str[-11:]
    current = current.merge(allCoords, how='left', on=['key', 'Year'])
    current = current.drop(columns='key')

    current.to_csv(cleanFile, index=False)
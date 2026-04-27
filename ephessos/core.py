from astropy.time import Time
from astropy.table import vstack
import numpy as np
import pandas as pd
from datetime import datetime

def ephessos(designation=None, epoch=None, eccentricity=None, node=None, arg_perihelion=None, inclination=None, mean_anomaly=None, semimajor_axis=None, mean_motion=None, perihelion_distance=None, perihelion_date=None, H_mag=None, G_slope=None, mjd_start=58849.0, mjd_end=61042.0, step_size="1d", verbose=False):
    # Example of a HTTP API Request to Horizons: 
    request_url = "https://ssd.jpl.nasa.gov/api/horizons.api?format=text&"
    # request_url = "https://ssd.jpl.nasa.gov/api/horizons.api?"
    # 00433   10.38  0.15 K25BL 310.55432  178.92978  304.27008   10.82847  0.2228360  0.55977529   1.4581210  0 E2025-YE5 16519  59 1893-2025 0.52 M-v 3Ek MPCORBFIT  1804    (433) Eros               20251222
    """
    OBJECT = df.iloc[0]["Designation"] # 	Name of user input object
    EPOCH = df.iloc[0]["Epoch"] 	  	# Julian Day number (JDTDB) of osculating elements
    ECLIP = "J2000" 	  	# Reference ecliptic frame of elements: J2000 or B1950. J2000 assumes the IAU76/80 J2000 obliquity of 84381.448 arcsec relative to the ICRF reference frame. B1950 assumes FK4/B1950 obliquity of 84404.8362512 arcsec.
    EC =  str(df.iloc[0]["Eccentricity"]) # 	  	Eccentricity
    QR = 	# au 	Perihelion distance (see note above)
    TP = 	#   	Perihelion Julian Day number (see note above)
    OM =  str(df.iloc[0]["Node"])	# deg 	Longitude of ascending node wrt ecliptic
    W =   str(df.iloc[0]["Arg_Perihelion"])	# deg 	Argument of perihelion wrt ecliptic
    IN =  str(df.iloc[0]["Inclination"])	# deg 	Inclination wrt ecliptic
    MA =  str(df.iloc[0]["Mean_Anomaly"])	# deg 	Mean anomaly (see note above)
    A =   str(df.iloc[0]["Semimajor_Axis"])	# au 	Semi-major axis (see note above)
    N =	  str(df.iloc[0]["Mean_Motion"]) # deg/d 	Mean motion (see note above)
    """
    OBJECT = designation # 	Name of user input object
    EPOCH = str(epoch) 	  	# Julian Day number (JDTDB) of osculating elements
    ECLIP = "J2000" 	  	# Reference ecliptic frame of elements: J2000 
    EC =  str(eccentricity) # 	  	Eccentricity
    QR =  str(perihelion_distance)	# au 	Perihelion distance (see note above)
    TP =  str(perihelion_date)	#   	Perihelion Julian Day number (see note above)
    OM =  str(node)	# deg 	Longitude of ascending node wrt ecliptic
    W =   str(arg_perihelion)	# deg 	Argument of perihelion wrt ecliptic
    IN =  str(inclination)    # deg 	Inclination wrt ecliptic
    MA =  str(mean_anomaly)	# deg 	Mean anomaly (see note above)
    A =   str(semimajor_axis)	# au 	Semi-major axis
    N =	  str(mean_motion) # deg/d 	Mean motion (see note above)
    H = str(H_mag) # Absolute magnitude
    G = str(G_slope) # Slope parameter
    
    # HEOE = ';TEST,2460400.5,1.5,0.2,10.5,45.0,30.0,20240401,1.0,J2000'
    
    # Process time range for ephemeris query
    from astropy.time import Time
    t_start = Time(mjd_start, format='mjd')
    t_end = Time(mjd_end, format='mjd')

    if verbose: 
        print("--designation="+designation+" --epoch="+str(epoch)+" --eccentricity="+str(eccentricity)+" --node="+str(node)+", --arg_perihelion="+str(arg_perihelion)+" --inclination="+str(inclination)+" --mean_anomaly="+str(mean_anomaly)+" --semimajor_axis="+str(semimajor_axis)+" --mean_motion="+str(mean_motion)+" --mjd_start="+str(mjd_start)+" --mjd_end="+str(mjd_end)+" --step_size="+step_size)

    """
    # request_url = request_url + "&COMMAND='1'"
    """

    if eccentricity is None and node is None and arg_perihelion is None and inclination is None and mean_anomaly is None and semimajor_axis is None:
        request_url = request_url + "COMMAND='" + OBJECT + "'" 
    else:
        request_url = request_url + "COMMAND=';'" 
    #if designation is not None: request_url = request_url + "&OBJECT="+OBJECT
    #if epoch is not None: request_url = request_url + "&EPOCH=2461000.83333"#+EPOCH
    if epoch is not None: request_url = request_url + "&EPOCH="+EPOCH
    request_url = request_url + "&ECLIP="+ECLIP
    if eccentricity is not None: request_url = request_url + "&EC="+EC 
    if node is not None: request_url = request_url + "&OM="+OM 
    if arg_perihelion is not None: request_url = request_url + "&W="+W 
    if inclination is not None: request_url = request_url + "&IN="+IN 
    if mean_anomaly is not None: request_url = request_url + "&MA="+MA 
    if semimajor_axis is not None: request_url = request_url + "&A="+A 
    if perihelion_distance is not None: request_url = request_url + "&QR="+QR 
    if perihelion_date is not None: request_url = request_url + "&TP="+TP
    if H_mag is not None: request_url = request_url + "&H="+H
    if G_slope is not None: request_url = request_url + "&G="+G 
    # request_url = request_url + "&N="+N 

    # request_url = request_url + "&COMMAND='499'"
    request_url = request_url + "&OBJ_DATA='YES'" 
    request_url = request_url + "&MAKE_EPHEM='YES'" 
    request_url = request_url + "&EPHEM_TYPE='OBSERVER'" 
    request_url = request_url + "&CENTER='500@32'"  # 500@32 is the sun & Earth-Moon Barycenter L2 (SEMB-L2)
    request_url = request_url + "&START_TIME='" + t_start.isot + "'" 
    request_url = request_url + "&STOP_TIME='"+ t_end.isot + "'" 
    request_url = request_url + "&STEP_SIZE='" + step_size + "'"
    request_url = request_url + "&CSV_FORMAT='YES'" 
    request_url = request_url + "&QUANTITIES='1,2,3,4,5,6,7,8,9,10,19,20,23,24,25,27,29'"
    # request_url = request_url.replace(",", "%3B")

    import urllib.request
    if verbose: print(request_url)
    
    request_url = request_url.replace(";","%3B")    

    fp = urllib.request.urlopen(request_url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()
    
    #this provides some insight if the query is not working.  It would be good to include a graceful exit within this if statement in the future.
    if len(mystr) < 1000:
        print("Error: Horizons query returned a short response. Check the request URL and parameters.")
        print("Request URL:", request_url)
        print("Response:")
        print(mystr)
   
    lines_horizons_query = np.array(mystr.split('\n'))
    id_start_of_table = np.where(lines_horizons_query == '$$SOE')[0][0]
    id_end_of_table = np.where(lines_horizons_query == '$$EOE')[0][0]
    id_column_names = id_start_of_table - 2
    horizons_column_names = lines_horizons_query[id_column_names]
    horizons_data_table = lines_horizons_query[id_start_of_table+1:id_end_of_table]
    n_rows = len(lines_horizons_query[id_start_of_table+1:id_end_of_table])

    csv_table_list = []
    # csv_table_list = csv_table_list + [horizons_column_names.split(',')]

    for i in range(n_rows):
        csv_table_list = csv_table_list + [horizons_data_table[i].split(',')]

    # print(csv_table_list)

    horizons_dataframe = pd.DataFrame(np.array(csv_table_list), columns=horizons_column_names.split(','))

    ra_icrf = np.zeros(len(horizons_dataframe), dtype=object)
    dec_icrf = np.zeros(len(horizons_dataframe), dtype=object)
    date_hms = np.zeros(len(horizons_dataframe), dtype=object)
    mjd = np.zeros(len(horizons_dataframe))

    time_column_name = horizons_dataframe.columns[0]

    for i in range(len(horizons_dataframe)):
        ra_icrf[i] = horizons_dataframe[" R.A._(ICRF)"].iloc[i][1:].replace(" ",":")
        dec_icrf[i] = horizons_dataframe[" DEC__(ICRF)"].iloc[i][1:].replace(" ",":")
        date_hms[i] = translate_horizons_date_to_date_hms(horizons_dataframe[time_column_name].iloc[i])[1:]
        mjd[i] = Time(date_hms[i], format='iso').mjd    

    print(date_hms)

    from astropy.coordinates import SkyCoord  # High-level coordinates
    coords = SkyCoord(ra_icrf, dec_icrf, unit=(u.hourangle, u.deg))
    horizons_dataframe["RA_deg_ICRF"] = coords.ra.deg
    horizons_dataframe["DEC_deg_ICRF"] = coords.dec.deg
    horizons_dataframe["MJD"] = mjd
    return(horizons_dataframe)


def translate_horizons_date_to_date_hms(horizons_date):
    # Example input: "2025-Jan-22 00:00"
    # Convert to ISO format: "2025-01-22T00:00:00"
    date_hms = horizons_date.replace("Jan","01").replace("Feb","02").replace("Mar","03").replace("Apr","04").replace("May","05").replace("Jun","06").replace("Jul","07").replace("Aug","08").replace("Sep","09").replace("Oct","10").replace("Nov","11").replace("Dec","12")
    return date_hms





def read_mpc_nea_file(file_path, verbose=False):
    # Define the exact character ranges based on the MPC schema
    # Note: pandas uses 0-based indexing and the 'stop' value is exclusive
    col_specification = [
        (0, 7),     # Designation
        (8, 13),    # H (Absolute Mag)
        (14, 19),   # G (Slope Parameter)
        (20, 25),   # Epoch
        (26, 35),   # Mean Anomaly
        (37, 46),   # Argument of Perihelion
        (48, 57),   # Longitude of Ascending Node
        (59, 68),   # Inclination
        (70, 79),   # Eccentricity
        (80, 91),   # Mean Daily Motion
        (92, 103),  # Semimajor Axis
        (105, 106), # Uncertainty (U)
        (107, 116), # Reference
        (117, 122), # Num observations
        (123, 126), # Num oppositions
        (127, 131), # First year / Arc
        (132, 136), # Last year / 'days'
        (137, 141), # r.m.s residual
        (142, 145), # Perturbers (Coarse)
        (146, 149), # Perturbers (Precise)
        (150, 160), # Computer Name
        (161, 165), # Flags (Hex)
        (166, 174), # Numerical ID
        (175, 194), # Readable Designation
        (194, 202)  # Last Observation Date
    ]

    column_names = [
        "Designation", "H", "G", "Epoch", "Mean_Anomaly", "Arg_Perihelion", 
        "Node", "Inclination", "Eccentricity", "Mean_Motion", "Semimajor_Axis", 
        "Uncertainty", "Ref", "Obs_Count", "Opp_Count", "First_Obs", "Last_Obs_Arc",
        "RMS_Resid", "Pert_Coarse", "Pert_Precise", "Comp_Name", "Flags", "Num_ID",
        "Full_Name", "Last_Obs_Date"
    ]

    # Read the file
    # Replace 'NEA.txt' with the path to your downloaded file
    df = pd.read_fwf(
        file_path, 
        colspecs=col_specification, 
        names=column_names, 
        header=None
    )

    # Optional: Convert numeric columns that might have been read as strings
    df['H'] = pd.to_numeric(df['H'], errors='coerce')
    df['Semimajor_Axis'] = pd.to_numeric(df['Semimajor_Axis'], errors='coerce')
    #df[['ID', 'Name']] = df['Full_Name'].str.extract(r'(\(.*\))\s+(.*)')
    df["Designation"] = df["Designation"].astype(str)

    # Preview the first few rows
    if verbose:
        print(df.head())
    return(df)

def read_mpc_comet_file(file_path, verbose=False):
    # Define the exact character ranges based on the MPC schema
    # Note: pandas uses 0-based indexing and the 'stop' value is exclusive
    col_specification = [
        (0, 4),    # Periodic number
        (4, 5),    # Orbit type (C, P, D, etc.)
        (5, 12),   # Designation (packed)
        (14, 18),  # Perihelion Year
        (19, 21),  # Perihelion Month
        (21, 29),  # Perihelion Day
        (30, 39),  # Perihelion distance q (AU)
        (41, 49),  # Eccentricity e
        (51, 59),  # Argument of perihelion (deg)
        (61, 69),  # Longitude of ascending node (deg)
        (71, 79),  # Inclination (deg)
        (81, 85),  # Epoch Year
        (86,87),  # Epoch Month
        (88, 89),  # Epoch Day
        (91, 95),  # Absolute Magnitude H
        (96, 100), # Slope Parameter G
        (102, 158) # Comet Name
    ]

    column_names = [
        'number', 'type', 'designation', 'peri_year', 'peri_month', 'peri_day', 
        'q', 'e', 'arg_peri', 'node', 'inclination', 'epoch_year', 'epoch_month', 'epoch_day', 
        'H', 'G', 'name'
    ]

    # Read the file
    df = pd.read_fwf(
        file_path, 
        colspecs=col_specification, 
        names=column_names, 
        header=None
    )

    #fix up some time colmns that have missing values.  This is a bit of a hack, but it allows us to convert the columns to integers without losing data.  We can improve this in the future by adding a column that indicates whether the value was imputed or not.
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)

    df[['ID', 'shortName']] = df.name.str.split(r"\(", expand=True)
    df.replace({'shortName': r'\)'}, '', regex=True, inplace=True)
    df['peri_year'] = df['peri_year'].astype(int)
    df['peri_month'] = df['peri_month'].astype(int)
    df['peri_day'] = df['peri_day'].astype(int)
    df['peri_jd'] = df.apply(lambda row: Time(datetime(row['peri_year'], row['peri_month'], row['peri_day']), scale='utc').jd, axis=1)

    # fill in missing epochs with the most common value
    most_common_epoch_year = df['epoch_year'].mode()[0]
    most_common_epoch_month = df['epoch_month'].mode()[0]
    most_common_epoch_day = df['epoch_day'].mode()[0]   
    df.fillna({'epoch_year': most_common_epoch_year, 'epoch_month': most_common_epoch_month, 'epoch_day': most_common_epoch_day}, inplace=True   )
    
    df['epoch_year'] = df['epoch_year'].astype(int)
    df['epoch_month'] = df['epoch_month'].astype(int)
    df['epoch_day'] = df['epoch_day'].astype(int)
    df['epoch_jd'] = df.apply(lambda row: Time(datetime(row['epoch_year'], row['epoch_month'], row['epoch_day']), scale='utc').jd, axis=1) 

    if verbose:
        print(df.head())

    return(df)
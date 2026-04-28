from astropy.table import vstack
import numpy as np
import pandas as pd
from astropy.time import Time
from astropy import units as u
import ephessos as ep
import os
ephessos_dir = os.path.dirname(ep.__file__)

def ephessos(sso_search=None, designation="Default", epoch=None, eccentricity=None, perihelion_distance=None, perihelion_date=None, node=None, arg_perihelion=None, inclination=None, mean_anomaly=None, semimajor_axis=None, mean_motion=None, H_mag=None, G_slope=None, obs_center="500@32", mjd_start=58849.0, mjd_end=61042.0, step_size="1d", quantities='1,2,3,4,5,6,7,8,9,10,19,20,23,24,25,27,29', verbose=False):
    """
    ephessos is a function that queries the JPL Horizons API for ephemeris data based on user-provided orbital elements and time range. The function constructs a request URL with the specified parameters, sends the request to the Horizons API, and processes the response to extract the relevant ephemeris data. The resulting data is returned as a pandas DataFrame containing the requested quantities for each time step within the specified range. The function also includes error handling and verbose output options for debugging and user feedback.
        :param str designation: Name of the object to query (default is "Default")
        :param str epoch: Julian Day number (JDTDB) of osculating elements (default is None)
        :param float eccentricity: Eccentricity of the orbit (default is None)
        :param float perihelion_distance: Perihelion distance in au (default is None)
        :param float perihelion_date: Perihelion date as a Julian Day number (default is None)
        :param float node: Longitude of ascending node wrt ecliptic in degrees (default is None)
        :param float arg_perihelion: Argument of perihelion wrt ecliptic in degrees (default is None)
        :param float inclination: Inclination wrt ecliptic in degrees (default is None)
        :param float mean_anomaly: Mean anomaly in degrees (default is None)
        :param float semimajor_axis: Semi-major axis in au (default is None)
        :param float mean_motion: Mean motion in deg/d (default is None)
        :param float H_mag: Absolute magnitude (default is None)
        :param float G_slope: Slope parameter (default is None)
        :param float mjd_start: Start time in Modified Julian Date (default is 58849.0)
        :param float mjd_end: End time in Modified Julian Date (default is 61042.0)
        :param str step_size: Step size for ephemeris query (default is "1d")
        :param str quantities: Comma-separated list of quantities to request from the Horizons API (default is '1,2,3,4,5,6,7,8,9,10,19,20,23,24,25,27,29')
        :param bool verbose: If True, prints the request URL and parameters for debugging (default is False)
    """

    if sso_search is None:
        ephessos_out = _ephessos(designation=designation, epoch=epoch, 
                                 eccentricity=eccentricity, perihelion_distance=perihelion_distance, 
                                 perihelion_date=perihelion_date, node=node, 
                                 arg_perihelion=arg_perihelion, inclination=inclination, 
                                 mean_anomaly=mean_anomaly, semimajor_axis=semimajor_axis, 
                                 mean_motion=mean_motion, 
                                 H_mag=H_mag, G_slope=G_slope, 
                                 obs_center=obs_center, mjd_start=mjd_start, mjd_end=mjd_end, 
                                 step_size=step_size, quantities=quantities, verbose=verbose)
        return(ephessos_out)
    
    if sso_search is not None:
        import pandas 
        if isinstance(sso_search, pandas.DataFrame):
            from tqdm import tqdm
            ephessos_df_list = [] 
            for i in tqdm(range(len(sso_search))):
                # print(cone_search.iloc[i])
                designation = sso_search.iloc[i]['Designation']
                epoch = sso_search.iloc[i]['Epoch']
                eccentricity = sso_search.iloc[i]['Eccentricity']
                node = sso_search.iloc[i]['Node']
                arg_perihelion = sso_search.iloc[i]['Arg_Perihelion']
                inclination = sso_search.iloc[i]['Inclination']
                mean_anomaly = sso_search.iloc[i]['Mean_Anomaly']
                semimajor_axis = sso_search.iloc[i]['Semimajor_Axis']
                mean_motion = sso_search.iloc[i]['Mean_Motion']
                H_mag = sso_search.iloc[i]['H']
                G_slope = sso_search.iloc[i]['G']

                ephessos_df = ep.core.ephessos(designation=designation, epoch=epoch, 
                                               eccentricity=eccentricity, 
                                               node=node, 
                                               arg_perihelion=arg_perihelion, inclination=inclination, 
                                               mean_anomaly=mean_anomaly, semimajor_axis=semimajor_axis, 
                                               mean_motion=mean_motion, H_mag=H_mag, 
                                               G_slope=G_slope, obs_center=obs_center,
                                               mjd_start=mjd_start, mjd_end=mjd_end, 
                                               step_size=step_size, 
                                               quantities=quantities, verbose=False)
    
                ephessos_df_list.append(ephessos_df)
            return(ephessos_df_list)
    


def _ephessos(designation="Default", epoch=None, eccentricity=None, perihelion_distance=None, perihelion_date=None, node=None, arg_perihelion=None, inclination=None, mean_anomaly=None, semimajor_axis=None, mean_motion=None, H_mag=None, G_slope=None, obs_center="500@32", mjd_start=58849.0, mjd_end=61042.0, step_size="1d", quantities='1,2,3,4,5,6,7,8,9,10,19,20,23,24,25,27,29', verbose=False):
    """
    This is an auxiliary function to ease the input in the main ephessos one
    """

    from astropy.time import Time
    from astropy import units as u

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
    if epoch == "K25BL":
        EPOCH = Time('2025-11-21T00:00:00', format='isot', scale='tt').jd
    else:
        EPOCH = Time(epoch, format='isot', scale='tt').jd

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
    #if epoch is not None: request_url = request_url + "&EPOCH="+str(EPOCH)
    if epoch is not None: request_url = request_url + "&EPOCH="+str(EPOCH)
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
    request_url = request_url + "&CENTER='" + obs_center + "'"  # 500@32 is the sun & Earth-Moon Barycenter L2 (SEMB-L2) 
    request_url = request_url + "&START_TIME='" + t_start.isot + "'" 
    request_url = request_url + "&STOP_TIME='"+ t_end.isot + "'" 
    request_url = request_url + "&STEP_SIZE='" + step_size + "'"
    request_url = request_url + "&CSV_FORMAT='YES'"
    request_url = request_url + "&QUANTITIES='"+ quantities + "'"  
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

    horizons_column_names_list = horizons_column_names.split(',')
    horizons_column_names_filtered = []
    for horizon_column_name in horizons_column_names_list:
        horizons_column_names_filtered.append(horizon_column_name.replace(" ",""))
    horizons_dataframe = pd.DataFrame(np.array(csv_table_list), columns=horizons_column_names_filtered)

    ra_icrf = np.zeros(len(horizons_dataframe), dtype=object)
    dec_icrf = np.zeros(len(horizons_dataframe), dtype=object)
    date_hms = np.zeros(len(horizons_dataframe), dtype=object)
    mjd = np.zeros(len(horizons_dataframe))

    time_column_name = horizons_dataframe.columns[0]

    for i in range(len(horizons_dataframe)):
        ra_icrf[i] = horizons_dataframe["R.A._(ICRF)"].iloc[i][1:].replace(" ",":")
        dec_icrf[i] = horizons_dataframe["DEC__(ICRF)"].iloc[i][1:].replace(" ",":")
        date_hms[i] = translate_horizons_date_to_date_hms(horizons_dataframe[time_column_name].iloc[i])[1:]
        mjd[i] = Time(date_hms[i], format='iso').mjd    

    # print(date_hms)

    from astropy.coordinates import SkyCoord  # High-level coordinates
    coords = SkyCoord(ra_icrf, dec_icrf, unit=(u.hourangle, u.deg))
    horizons_dataframe["RA_deg_ICRF"] = coords.ra.deg
    horizons_dataframe["DEC_deg_ICRF"] = coords.dec.deg
    horizons_dataframe["MJD"] = mjd
    horizons_dataframe["Designation"] = designation
    return(horizons_dataframe)


def translate_horizons_date_to_date_hms(horizons_date):
    """
    translate_horizons_date_to_date_hms translates the date format provided by the Horizons API (e.g., "2025-Jan-22 00:00") into a standard ISO format (e.g., "2025-01-22T00:00:00"). This function replaces the month abbreviations with their corresponding numeric values and formats the date string accordingly.
        :param str horizons_date: Date string from the Horizons API (e.g., "2025-Jan-22 00:00")
        :returns: Date string in ISO format (e.g., "2025-01-22T00:00:00")
        :rtype: str
    """
    # Example input: "2025-Jan-22 00:00"
    # Convert to ISO format: "2025-01-22T00:00:00"
    date_hms = horizons_date.replace("Jan","01").replace("Feb","02").replace("Mar","03").replace("Apr","04").replace("May","05").replace("Jun","06").replace("Jul","07").replace("Aug","08").replace("Sep","09").replace("Oct","10").replace("Nov","11").replace("Dec","12")
    return date_hms





def read_mpc_nea_file(file_path, verbose=False):
    """
    read_mpc_nea_file reads the MPCORB.DAT file from the Minor Planet Center and parses it into a pandas DataFrame. The function defines the exact character ranges for each column based on the MPC schema and uses pandas' read_fwf function to read the fixed-width formatted file. It also converts certain columns to numeric types and ensures that the Designation column is treated as a string. This function is specifically designed for reading the Near-Earth Asteroids (NEA) subset of the MPCORB.DAT file, which may have a different structure or content compared to the full MPCORB.DAT file.
        :param str file_path: Path to the MPCORB.DAT file
        :returns: DataFrame containing the parsed MPCORB.DAT data for Near-Earth Asteroids
        :rtype: pandas.DataFrame
    """
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
    if verbose: print(df.head())
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



def read_mpcorb_file(file_path, skiprows=43):
    """
    read_mpcorb_file reads the MPCORB.DAT file from the Minor Planet Center and parses it into a pandas DataFrame. The function defines the exact character ranges for each column based on the MPC schema and uses pandas' read_fwf function to read the fixed-width formatted file. It also converts certain columns to numeric types and ensures that the Designation column is treated as a string. The skiprows parameter allows skipping the header lines of the MPCORB.DAT file, which typically contain metadata and comments.
        :param str file_path: Path to the MPCORB.DAT file
        :param int skiprows: Number of header lines to skip (default is 43)
        :returns: DataFrame containing the parsed MPCORB.DAT data
        :rtype: pandas.DataFrame
    """

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

    # Read the file, skipping the header (first 43 lines)
    df = pd.read_fwf(
        file_path, 
        colspecs=col_specification, 
        names=column_names, 
        header=None,
        skiprows=skiprows
    )

    # Optional: Convert numeric columns that might have been read as strings
    df['H'] = pd.to_numeric(df['H'], errors='coerce')
    df['Semimajor_Axis'] = pd.to_numeric(df['Semimajor_Axis'], errors='coerce')
    df["Designation"] = df["Designation"].astype(str)

    return df



def get_last_modification_time(file_path):
    """
    get_last_modification_time checks the last modification time of a file and calculates the time difference between now and the last modification time. It returns a dictionary containing the time difference (Delta), the last modification time, and the current time. This function is useful for determining if a cached file is still valid or if it needs to be updated.
        :param str file_path: Path to the file to check
        :returns: Dictionary containing the time difference, last modification time, and current time
        :rtype: dict
    """
    import os
    import time
    import datetime
    from astropy.time import Time

    if os.path.exists(file_path):
        modification_time = Time(datetime.datetime.fromtimestamp(os.path.getmtime(file_path)))
        # print(modification_time)
        now_time = Time.now()
        # print(now_time)
        delta_t  = now_time - modification_time

    else:
        print("File does not exist.")
    
    return({"Delta": delta_t, "Modification Time": modification_time, "Now Time": now_time})


def download_file(url, verbose=True):
    """
    Downloads the file described as an url address.
        :param str url: Url of the file to be downloaded
        :returns: Local path of the downloaded file
        :rtype: str
    """
    import requests
    # From: https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    from tqdm import tqdm 
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        total_size = int(r.headers.get('content-length', 0))
        with open(local_filename, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, disable=not verbose) as pbar:
                for chunk in r.iter_content(chunk_size=1048576):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
    return(local_filename)

# If needed. Download the MPCORB.DAT file and read it into a table


def get_last_mpcorb():
    """
    get_last_mpcorb checks if the MPCORB.DAT file exists in the cache and if it is less than a day old. If it exists and is recent, it uses the cached file. If it does not exist or is old, it downloads the latest MPCORB.DAT.gz file from the Minor Planet Center, saves it to the cache, and then reads it into a DataFrame. The function returns the path to the uncompressed MPCORB.DAT file that can be read into a DataFrame.

    :returns: Path to the uncompressed MPCORB.DAT file
    :rtype: str
    """
    # Check if file exists in cache, if not download it and move it to the cache
    import gzip
    import shutil
    
    # If the file exists ... 
    mpcorb_cache_path = os.path.join(ep.core.ephessos_dir, "MPCORB.DAT.gz")
    if os.path.exists(mpcorb_cache_path):
        last_modification_time = get_last_modification_time(mpcorb_cache_path)
        if last_modification_time["Delta"].sec < 3600*24:  # If the file is less than a one day old, use it
            print(f"Using Minor Planet Center cached file: Last: {last_modification_time['Modification Time'].isot}")
            with gzip.open(mpcorb_cache_path, 'rb') as f_in:
                with open(mpcorb_cache_path.replace(".gz",""), 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)    
                    return(f_out.name)
        else:
            return(download_MPCORB())
                       
    # If not, or if the file is old 
    else:
        return(download_MPCORB())
   
def download_MPCORB():
    import gzip
    import shutil
    
    mpcorb_cache_path = os.path.join(ep.core.ephessos_dir, "MPCORB.DAT.gz")
    mpcorb_url = "https://www.minorplanetcenter.net/iau/MPCORB/MPCORB.DAT.gz"
    download_file(mpcorb_url, verbose=True)
    os.rename("MPCORB.DAT.gz", mpcorb_cache_path)
    # print(os.path.join(ep.core.ephessos_dir, "MPCORB.DAT.gz"))
    with gzip.open(mpcorb_cache_path, 'rb') as f_in:
        with open(mpcorb_cache_path.replace(".gz",""), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)    
            return(f_out.name)
            

def cone_search(ra, dec, mjd, search_radius, observatory=None, verbose=False):
    """
    cone_search performs a cone search around the given RA, Dec, and epoch with the specified search radius to find potential matches in the MPCORB.DAT file. It uses the pympc library to perform the initial cone search and then cross-references the results with the MPCORB.DAT file to find corresponding entries.
        :param float ra: Right Ascension in degrees
        :param float dec: Declination in degrees
        :param float epoch: Epoch in Julian Date
        :param float search_radius: Search radius in arcseconds
        :returns: DataFrame containing the matching entries from MPCORB.DAT
        :rtype: pandas.DataFrame
    """
    # if epoch == "K25BL":
    #    EPOCH = Time('2025-11-21T00:00:00', format='isot', scale='tt').mjd
    #else:
    #    EPOCH = Time(epoch, format='isot', scale='tt').mjd

    # Get the path to the latest MPCORB.DAT file
    last_mpcorb = ep.core.get_last_mpcorb()

    # Perform the cone search using pympc to get potential matches
    import pympc

    # If the mpcorb_xephem.csv file is older than one day, update it 
    import tempfile
    xephem_filepath = os.path.join(tempfile.gettempdir(), "mpcorb_xephem.csv")
    if os.path.exists(xephem_filepath):
        last_modification_time = get_last_modification_time(xephem_filepath)
        if last_modification_time["Delta"].sec > 3600*24:  # If the file is less than a one day old, use it
            print("Updating MPCORB catalogue...")
            pympc.update_catalogue()
    else: 
        print("Downloading MPCORB catalogue...")
        pympc.update_catalogue()

    matches = pympc.minor_planet_check(ra=ra, dec=dec, epoch=mjd, search_radius=search_radius, observatory=observatory)

    if verbose: print(matches)
    if len(matches) == 0:
        print("No matches found in cone search.")
        return(pd.DataFrame())  # Return an empty DataFrame if no matches are found
    # Find the corresponding entries in MPCORB.DAT for the matches found by pympc
    return(find_sso_in_mpcorb(matches, last_mpcorb))


def find_sso_in_mpcorb(matches, last_mpcorb):
    """
    find_sso_in_mpcorb finds the corresponding entries in MPCORB.DAT for the matches found by pympc.
    :param pandas.DataFrame matches: DataFrame containing the matches found by pympc
    :param str last_mpcorb: Path to the latest MPCORB.DAT file
    :returns: DataFrame containing the matching entries from MPCORB.DAT
    :rtype: pandas.DataFrame
    """

    # Find the line inside MPCORB.DAT that corresponds to the object of interest
    temp_last_mpcorb = last_mpcorb.replace(".DAT", "_temp.DAT")

    sso_matches = []
    from tqdm import tqdm 
    for i in tqdm(range(len(matches["name"]))):
        os.system('grep "' + str(matches["name"][i]) + '" ' + last_mpcorb + ' > ' + temp_last_mpcorb)
        # Read the temporary file containing the single SSO into a DataFrame
        sso_matches.append(ep.core.read_mpcorb_file(file_path=temp_last_mpcorb, skiprows=0))

    import pandas as pd
    return(pd.concat(sso_matches))
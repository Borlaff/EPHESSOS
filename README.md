# EPHESSOS

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Borlaff/EPHESSOS">
    <img src="https://raw.githubusercontent.com/Borlaff/EPHESSOS/main/media/ephessos_logo.png" alt="EPHESSOS_logo" width="700">
  </a>
  <p align="center">
    <h2 align="center">Ephemeris for Solar System Objects with JPL/Horizons</h2>
    <br />
    <a href="https://github.com/Borlaff/EPHESSOS">View Demo</a>
    ·
    <a href="https://github.com/Borlaff/EPHESSOS/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Borlaff/EPHESSOS/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>


[![PyPI version](https://badge.fury.io/py/ephessos.svg)](https://pypi.org/project/ephessos/)
[![License: BSD](https://img.shields.io/badge/License-BSD-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

EPHESSOS is a [NASA Ames Research Center](https://www.nasa.gov/space-science-and-astrobiology-at-ames/) Python library for querying ephemeris data of solar system objects from NASA's JPL Horizons system. It provides an easy interface to query positional and observational data for asteroids, comets, and planets. EPHESSOS allows to provide custom orbital elements to JPL/Horizons and retrieve the ephemerides from their server, and to perform positional queries on the Minor Planet Center database. 

## Features

- Query JPL Horizons using orbital elements or object designations
- Parse MPC NEA (Near-Earth Asteroid) data files
- Retrieve comprehensive ephemeris data including RA, Dec, distance, and more
- Support for custom time ranges and step sizes
- Integration with Astropy for astronomical calculations

## Installation

Install EPHESSOS using pip:

```bash
pip install ephessos
```

Or from source:

```bash
git clone https://github.com/Borlaff/EPHESSOS.git
cd EPHESSOS
pip install .
```

## Quick Start

Here's a simple example showing how to query the ephemeris of asteroid (433) Eros:

```python
import ephessos as ep
from astropy.time import Time

# Define time range
mjd_start = Time('2024-01-01T00:00:00', format='isot', scale='utc').mjd
mjd_end = Time('2024-01-15T00:00:00', format='isot', scale='utc').mjd

# Query Horizons for Eros (designation: 00433)
eros_data = ep.core.ephessos(
    designation="00433",
    mjd_start=mjd_start,
    mjd_end=mjd_end,
    step_size="1d",
    verbose=True
)

print(eros_data.head())
```

This will return a pandas DataFrame containing ephemeris data including:
- Right Ascension (RA) and Declination (Dec) in degrees
- Distance from observer
- Magnitude and other observational quantities
- Modified Julian Date (MJD)

## Advanced Usage

### Reading MPC Data Files

EPHESSOS can parse MPC-formatted NEA files:

```python
# Read MPC NEA data
nea_table = ep.core.read_mpc_nea_file("path/to/nea.txt")

# Query ephemeris for the first object
first_object = nea_table.iloc[0]
data = ep.core.ephessos(
    designation=first_object["Designation"],
    epoch=first_object["Epoch"],
    eccentricity=first_object["Eccentricity"],
    node=first_object["Node"],
    arg_perihelion=first_object["Arg_Perihelion"],
    inclination=first_object["Inclination"],
    mean_anomaly=first_object["Mean_Anomaly"],
    semimajor_axis=first_object["Semimajor_Axis"],
    mean_motion=first_object["Mean_Motion"],
    mjd_start=mjd_start,
    mjd_end=mjd_end,
    step_size="1d"
)
```

## Cone searches

EPHESSOS can search targets in a given area and time, and retrieve the information from the Minor Planet Center. Here is one example of a cone search for Solar System Objects around a certain location of the sky within a given period (one month):

```python
# H2 Cone Search
# This notebook is dedicated to develop the cone_search and detector_search function in EPHESSOS
import ephessos as ep
from astropy.time import Time
import astropy.units as u

# Let's define a location 
ra = 230.028
dec = -11.774

# How long are you staring at that location?
now = Time(60000, format="mjd") # Time.now()
mjd = now.mjd #

# Let's find out what asteroids pass around 5 arcminutes of the center
# during a month of observations 
start = now - 15*24*60*60*u.s #  
end = now + 15*24*60*60*u.s #
search_radius = 5*60 # 5 arcminutes

# ephessos needs Modified Julian Dates as input
mjd_start = start.mjd
mjd_end = end.mjd

cone_search = ep.core.cone_search(ra=ra, dec=dec, mjd=mjd, search_radius=search_radius, observatory=273, verbose=True)
ephessos_df = ep.core.ephessos(sso_search=cone_search, mjd_start=mjd_start, mjd_end=mjd_end, step_size="1h")


# Let's plot the results! 
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8,8))

circ = plt.Circle((ra,dec), color="firebrick", linewidth=2, linestyle="--", fill=False, facecolor=None, label="Search radius")
ax.add_patch(circ)

for i in range(len(ephessos_df)):
    ax.plot(ephessos_df[i]["RA_deg_ICRF"], ephessos_df[i]["DEC_deg_ICRF"], label=ephessos_df[i]["Designation"].iloc[0])

ax.scatter(ra, dec, marker="+", s=100, color="firebrick", label="Pointing")
ax.set_ylabel("Declination (degrees)")
ax.set_xlabel("Right ascension (degrees)")
ax.legend()
plt.savefig("H2_cone_search.png", dpi=300)
```

<br />
<div align="center">
  <a href="https://github.com/Borlaff/EPHESSOS">
    <img src="https://raw.githubusercontent.com/Borlaff/EPHESSOS/main/notebooks/H2_cone_search.png" alt="EPHESSOS cone search example" width="700">
  </a>
</div>


## Command Line Interface

EPHESSOS also provides a command-line interface through the `ephessos` executable, which allows you to query ephemeris data directly from the terminal without writing Python code.

### Basic Usage

After installation, you can use the `ephessos` command to generate ephemeris data. You must provide the orbital elements and time range:

```bash
 ephessos --designation=433 --epoch=2461000.5 --eccentricity=0.222836 --node=304.27008 --arg_perihelion=178.92978 --inclination=10.82847 --mean_anomaly=310.55432 --semimajor_axis=1.458121 --mean_motion=0.55977529 --mjdstart=58849.0 --mjdend=61042.0 --step_size=1d --output="eros_ephem.csv"
```

### Required Parameters

- `--designation`: Object designation (e.g., "00433" for Eros)
- `--epoch`: Julian Date of the osculating elements
- `--eccentricity`: Orbital eccentricity
- `--node`: Longitude of the ascending node (degrees)
- `--arg_perihelion`: Argument of perihelion (degrees)
- `--inclination`: Orbital inclination (degrees)
- `--mean_anomaly`: Mean anomaly (degrees)
- `--semimajor_axis`: Semi-major axis (AU)
- `--mean_motion`: Mean motion (degrees/day)
- `--mjdstart`: Start time as Modified Julian Date
- `--mjdend`: End time as Modified Julian Date

### Optional Parameters

- `--step_size`: Time step for ephemeris (default: "1d" for 1 day)
  - Examples: "1d", "12h", "6h", "1h", "30m"
- `--output`: Output CSV filename (default: "horizons_ephemeris.csv")
- `--verbose`: Enable verbose output

The output will be a CSV file containing columns for:
- Date/time information
- Right Ascension and Declination (ICRF)
- Apparent magnitude
- Distance from observer and Sun
- And other ephemeris quantities

### Converting Dates to MJD

To convert calendar dates to Modified Julian Dates for use with `--mjdstart` and `--mjdend`, you can use online converters or Python:

```python
from astropy.time import Time
t = Time('2024-01-01T00:00:00', format='isot', scale='utc')
print(f"MJD: {t.mjd}")
```

## Contributing

Contributions are welcome! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

## License

EPHESSOS is licensed under the BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Citation

If you use EPHESSOS in your research, please cite:

```
Borlaff, A. S., & Dotson, J. (2026). EPHESSOS: Ephemeris for Solar System Objects with JPL/Horizons.
```

## Contact

- **Authors**: Alejandro S. Borlaff, Jessie Dotson
- **Email**: a.s.borlaff@nasa.gov, jessie.dotson@nasa.gov
- **Repository**: [https://github.com/Borlaff/EPHESSOS](https://github.com/Borlaff/EPHESSOS)

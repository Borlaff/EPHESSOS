# EPHESSOS
Ephemeris for Solar System Objects with JPL/Horizons

[![PyPI version](https://badge.fury.io/py/ephessos.svg)](https://pypi.org/project/ephessos/)
[![License: BSD](https://img.shields.io/badge/License-BSD-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

EPHESSOS is a Python library for querying ephemeris data of solar system objects from NASA's JPL Horizons system. It provides an easy interface to retrieve positional and observational data for asteroids, comets, and planets.

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
eros_data = ep.core.sso_query_to_horizons(
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
data = ep.core.sso_query_to_horizons(
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


## Documentation

Full documentation is available at: [https://ephessos.readthedocs.io/](https://ephessos.readthedocs.io/)

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

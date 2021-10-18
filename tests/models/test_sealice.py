import numpy as np
from opendrift.readers import reader_netCDF_CF_generic
from opendrift.models.sealice import SeaLice
from datetime import timedelta


def test_sealice():
    o = SeaLice(loglevel=30)
    reader_arome = reader_netCDF_CF_generic.Reader(
        o.test_data_folder() +
        '2Feb2016_Nordic_sigma_3d/AROME_MetCoOp_00_DEF_20160202_subset.nc')
    o.add_reader([reader_arome])
    lat = 67.711251
    lon = 13.556971  # Lofoten
    o.seed_elements(lon,
                    lat,
                    radius=5000,
                    number=1000,
                    time=reader_arome.start_time)
    o.run(steps=24, time_step=3600)
    np.testing.assert_almost_equal(o.elements.lon.max(), 15.864, 2)


def test_sealice_larc():
    o = SeaLice(loglevel=30)
    reader_arome = reader_netCDF_CF_generic.Reader(
        o.test_data_folder() +
        '2Feb2016_Nordic_sigma_3d/AROME_MetCoOp_00_DEF_20160202_subset.nc')
    o.add_reader([reader_arome])
    reader_light = reader_netCDF_CF_generic.Reader(
        'https://opendap.larc.nasa.gov/opendap/hyrax/POWER/daily/power_801_daily_allsky_sfc_sw_dwn_lst.nc',
        standard_name_mapping={
            'ALLSKY_SFC_SW_DWN': 'surface_net_downward_radiative_flux'
        })
    o.add_reader(reader_light)
    lcts = timedelta(hours=1).total_seconds()  #seeding time-steps
    length = timedelta(days=10)
    lat = 67.711251
    lon = 13.556971  # Lofoten
    o.set_config('lice:seeding_time_step', lcts)
    o.set_config('general:use_auto_landmask', False)
    o.set_config('general:duration', length.total_seconds())
    o.seed_elements(lon,
                    lat,
                    radius=5000,
                    number=1000,
                    time=reader_arome.start_time,
                    particle_biomass=2000,
                    z=-5)
    o.run(time_step=lcts, duration=length)
    np.testing.assert_almost_equal(o.elements.lon.max(), 15.864, 2)

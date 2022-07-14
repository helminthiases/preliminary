import numpy as np


class Config:

    def __init__(self):
        """

        """

    @staticmethod
    def interval():

        return np.linspace(start=2000, stop=2017, num=18)

    @staticmethod
    def missing():

        return ['site_id', 'longitude', 'latitude', 'year',
                'hk_prevalence', 'asc_prevalence', 'tt_prevalence']

"""
Module: features
"""
import os
import pathlib
import glob

import pandas as pd
import dask

import config


class Features:
    """
    Number of missing observations
    """

    def __init__(self):
        """

        """
        
        configurations = config.Config()

        # fields for missing data analysis
        self.missing = configurations.missing()

        # Data Source
        source = os.path.join(str(pathlib.Path(os.getcwd()).parent), 'infections', 'warehouse',
                              'data', 'ESPEN', 'experiments', 'baseline')
        self.paths = glob.glob(pathname=os.path.join(source, '*.csv'))

    @staticmethod
    @dask.delayed
    def __read(path: str):
        """

        :param path:
        :return:
        """

        try:
            return pd.read_csv(filepath_or_buffer=path)
        except OSError as err:
            raise Exception(err.strerror) from err

    @staticmethod
    @dask.delayed
    def __coordinates(data: pd.DataFrame) -> float:
        """
        The number of missing coordinate points, i.e., the number of cases whereby
        either the longitude or latitude value is missing.

        :param data:
        :return:
        """

        condition = data['longitude'].isna() | data['latitude'].isna()
        return sum(condition)

    @dask.delayed
    def __numbers(self, data: pd.DataFrame) -> pd.Series:
        """

        :return:
        """

        values: pd.Series = data.copy()[self.missing].isna().sum(axis=0)
        return values

    @staticmethod
    @dask.delayed
    def __integrate(numbers: pd.Series, coordinates: float, country: str, observations: int):

        series = numbers.copy()
        series.loc['coordinates'] = coordinates
        series.loc['iso2'] = country
        series.loc['N'] = observations

        return series

    def exc(self):
        """

        :return:
        """

        computations = []
        for path in self.paths:

            data = self.__read(path=path)
            numbers = self.__numbers(data=data)
            coordinates = self.__coordinates(data=data)
            values = self.__integrate(numbers=numbers, coordinates=coordinates,
                                      country=pathlib.Path(path).stem, observations=data.shape[0])

            computations.append(values)

        dask.visualize(computations, filename=os.path.join(os.getcwd(), 'src', 'missing', 'data'),
                       format='pdf')
        calculations = dask.compute(computations, scheduler='processes')[0]

        return pd.concat(objs=calculations, axis=1).transpose()

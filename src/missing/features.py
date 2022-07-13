"""
Module: features
"""
import glob
import os
import pathlib

import dask
import pandas as pd

import config
import src.functions.directories
import src.functions.streams


class Features:
    """
    Number of missing observations
    """

    def __init__(self, storage: str, source: str):
        """

        :param storage:
        :param source:
        """

        configurations = config.Config()
        self.missing = configurations.missing()

        # streams
        self.streams = src.functions.streams.Streams()

        # storage
        self.storage = storage
        src.functions.directories.Directories().create(self.storage)

        # data file paths
        self.paths = glob.glob(pathname=os.path.join(source, '*.csv'))

    @staticmethod
    @dask.delayed
    def __read(path: str) -> pd.DataFrame:
        """

        :param path:
        :return:
        """

        try:
            return pd.read_csv(filepath_or_buffer=path)
        except OSError as err:
            raise Exception(err.strerror) from err

    @dask.delayed
    def __states(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Is a cell value missing?

        :param data:
        :return:
        """

        # Missing? Including cases whereby either the longitude or latitude value
        # is missing.
        frame = data.copy()[self.missing].isna()
        frame.loc[:, 'coordinates'] = data['longitude'].isna() | data['latitude'].isna()

        return frame

    @dask.delayed
    def __write(self, data: pd.DataFrame, name: str):
        """

        :param data:
        :param name:
        :return:
        """

        self.streams.write(data=data, path=os.path.join(self.storage, f'{name}.csv'))

        return data

    @dask.delayed
    def __numbers(self, data: pd.DataFrame):
        """
        Counts the number of missing values per field.

        :return:
        """

        values = data.copy().sum(axis=0)

        return values

    @staticmethod
    @dask.delayed
    def __integrate(numbers: pd.Series, country: str, observations: int) -> pd.Series:
        """

        :param numbers:
        :param country:
        :param observations:
        :return:
        """

        series = numbers.copy()
        series.loc['iso2'] = country
        series.loc['N'] = observations

        return series

    def exc(self):
        """

        :return:
        """

        computations = []
        for path in self.paths:
            name = pathlib.Path(path).stem
            data = self.__read(path=path)
            states = self.__states(data=data)
            states = self.__write(data=states, name=name)
            numbers = self.__numbers(data=states)
            values = self.__integrate(numbers=numbers, country=name, observations=data.shape[0])
            computations.append(values)

        dask.visualize(computations, filename=os.path.join(os.getcwd(), 'src', 'missing', 'data'),
                       format='pdf')
        calculations = dask.compute(computations, scheduler='processes')[0]

        return pd.concat(objs=calculations, axis=1).transpose()

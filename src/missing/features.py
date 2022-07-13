"""
Module: features
"""
import os
import pathlib
import glob

import pandas as pd
import dask

import config
import src.functions.streams
import src.functions.directories


class Features:
    """
    Number of missing observations
    """

    def __init__(self, storage: str, source: str):
        """

        """
        
        configurations = config.Config()

        # fields for missing data analysis
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
    def __read(path: str):
        """

        :param path:
        :return:
        """

        try:
            return pd.read_csv(filepath_or_buffer=path)
        except OSError as err:
            raise Exception(err.strerror) from err

    @dask.delayed
    def __states(self, data: pd.DataFrame, name: str) -> pd.DataFrame:

        frame = data.copy()[self.missing].isna()
        frame.loc[:, 'coordinates'] = frame['longitude'].isna() | frame['latitude'].isna()
        frame = frame.copy().astype(dtype='int32')

        self.streams.write(data=frame, path=os.path.join(self.storage, f'{name}.csv'))

        return frame

    @dask.delayed
    def __numbers(self, data: pd.DataFrame) -> pd.Series:
        """

        :return:
        """

        values: pd.Series = data.copy().isna().sum(axis=0)
        return values

    @staticmethod
    @dask.delayed
    def __integrate(numbers: pd.Series, country: str, observations: int):

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

            data = self.__read(path=path)
            frame = self.__states(data=data, name=pathlib.Path(path).stem)
            numbers = self.__numbers(data=frame)
            values = self.__integrate(numbers=numbers, country=pathlib.Path(path).stem,
                                      observations=data.shape[0])
            computations.append(values)

        dask.visualize(computations,
                       filename=os.path.join(os.getcwd(), 'src', 'missing', 'data'),
                       format='pdf')
        calculations = dask.compute(computations, scheduler='processes')[0]

        return pd.concat(objs=calculations, axis=1).transpose()

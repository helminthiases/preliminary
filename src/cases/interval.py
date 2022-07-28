import glob
import os
import pathlib

import dask
import pandas as pd

import config
import src.functions.streams


class Interval:

    def __init__(self):
        """

        """

        configurations = config.Config()

        # WASH data time interval
        self.interval = configurations.interval()

    @staticmethod
    @dask.delayed
    def __read(path: str):
        """

        :param path:
        :return:
        """

        try:
            return pd.read_csv(filepath_or_buffer=path, usecols=['iso2', 'year'])
        except OSError as err:
            raise Exception(err.strerror) from err

    @dask.delayed
    def __interval(self, data: pd.DataFrame) -> dict:
        """
        The number & fraction of observations that were measured within the WASH time interval.

        :param data:
        :return:
        """

        condition = data['year'].isin(self.interval)
        interval = {'complete_iin': sum(condition),
                    'complete_iif': sum(condition) / data.shape[0]}
        return interval

    @staticmethod
    @dask.delayed
    def __integrate(interval: dict, country: str, observations: int):
        """

        :param interval:
        :param country:
        :param observations:
        :return:
        """

        series = pd.Series(data=interval)
        series.loc['iso2'] = country
        series.loc['complete'] = observations

        return series

    def exc(self, integration: pd.DataFrame, source, storage):
        """

        :param integration: Counts of raw & usable observations → per infection type, and per country.
        :param source: The location of the data files
        :param storage: Storage directory for the combination of WASH interval counts & <integration>
        :return:
        """

        # Paths
        paths = glob.glob(pathname=source)

        computations = []
        for path in paths:
            data = self.__read(path=path)
            interval = self.__interval(data=data)
            values = self.__integrate(interval=interval, country=pathlib.Path(path).stem, observations=data.shape[0])
            computations.append(values)

        calculations = dask.compute(computations, scheduler='processes')[0]

        interval = pd.concat(objs=calculations, axis=1).transpose()
        interval = interval.merge(integration, how='left', on='iso2')
        message = src.functions.streams.Streams().write(data=interval,
                                                        path=os.path.join(storage, 'interval.csv'))

        return message

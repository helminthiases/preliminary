import glob
import os
import pathlib

import dask
import pandas as pd

import config


class Features:

    def __init__(self):
        """

        """

        configurations = config.Config()

        # WASH data time interval
        self.interval = configurations.interval()

        # Data Source
        source = os.path.join(str(pathlib.Path(os.getcwd()).parent), 'infections', 'warehouse',
                              'data', 'ESPEN', 'networks', 'graphs')
        self.paths = glob.glob(pathname=os.path.join(source, '*.csv'))

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
    def __interval(self, data: pd.DataFrame) -> float:
        """
        The percentage of observations that were measured within the WASH time interval.

        :param data:
        :return:
        """

        condition = data['year'].isin(self.interval)
        return sum(condition) / data.shape[0]

    @staticmethod
    @dask.delayed
    def __integrate(interval: float, country: str, observations: int):

        series = pd.Series(data={'complete_in_interval': interval})
        series.loc['iso2'] = country
        series.loc['complete'] = observations

        return series

    def exc(self):

        computations = []
        for path in self.paths:
            data = self.__read(path=path)
            interval = self.__interval(data=data)
            values = self.__integrate(interval=interval, country=pathlib.Path(path).stem, observations=data.shape[0])

            computations.append(values)

        dask.visualize(computations, filename=os.path.join(os.getcwd(), 'src', 'interval', 'data'),
                       format='pdf')
        calculations = dask.compute(computations, scheduler='processes')[0]

        return pd.concat(objs=calculations, axis=1).transpose()

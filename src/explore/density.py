import os

import dask.dataframe
import pandas as pd

import src.functions.streams


class Density:

    def __init__(self, storage):
        """

        :param storage:
        """

        self.storage = storage

        self.fields = ['iso2', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'identifier',
                       'p_density']

    def __read(self, path):
        """
        Reading-in and merging the set of enhanced, and inspected, STH experiments
        data files.  Only relevant fields are read.

        :param path:
        :return:
        """

        try:
            frame = dask.dataframe.read_csv(urlpath=path, usecols=self.fields, encoding='utf-8')
        except OSError as err:
            raise Exception(err.strerror) from err

        lines: pd.DataFrame = frame.compute()
        lines.reset_index(drop=True, inplace=True)

        return lines

    def __write(self, data):
        """

        :param data:
        :return:
        """

        return src.functions.streams.Streams().write(
            data=data, path=os.path.join(self.storage, 'density.csv'))

    @staticmethod
    def __density(data):
        """

        :param data:
        :return:
        """

        condition = data[['p_density']].notna().values
        lines = data.copy().loc[condition, :]

        return lines

    @staticmethod
    def __prevalence(data):
        """

        :param data:
        :return:
        """

        lines = data.melt(id_vars=['iso2', 'year', 'identifier', 'p_density'],
                          value_vars=['hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                          var_name='infection',
                          value_name='prevalence')

        condition = lines[['prevalence']].notna().values
        lines = lines.copy().loc[condition, :]

        return lines

    def exc(self, path):
        """

        :param path:
        :return:
        """

        lines = self.__read(path=path)
        lines = self.__density(data=lines)
        lines = self.__prevalence(data=lines)

        message = self.__write(data=lines)

        return message

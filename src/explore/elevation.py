import os

import dask.dataframe
import pandas as pd

import src.functions.streams


class Elevation:

    def __init__(self, storage):
        """

        :param storage:
        """

        self.storage = storage

        self.fields = ['iso2', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence',
                       'identifier', 'elevation']

    def __read(self, path):
        """
        Reading-in and merging the set of enhanced, and inspected, STH experiments
        data files.  Only relevant fields are read.

        :param path:
        :return:
        """

        try:
            return dask.dataframe.read_csv(urlpath=path, usecols=self.fields, encoding='utf-8')
        except OSError as err:
            raise Exception(err.strerror) from err

    def __write(self, data):
        """

        :param data:
        :return:
        """

        return src.functions.streams.Streams().write(
            data=data, path=os.path.join(self.storage, 'elevation.csv'))

    def exc(self, path):
        """

        :param path:
        :return:
        """

        frame = self.__read(path=path)

        lines: pd.DataFrame = frame.compute()
        lines.reset_index(drop=True, inplace=True)
        lines = lines.melt(id_vars=['iso2', 'year', 'identifier', 'elevation'],
                           value_vars=['hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                           var_name='infection',
                           value_name='prevalence')

        condition = lines[['prevalence']].notna().values
        lines = lines.copy().loc[condition, :]

        message = self.__write(data=lines)

        return message

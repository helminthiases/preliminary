import sys
import os
import logging
import pathlib

import pandas as pd
import dask.dataframe

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
            return dask.dataframe.read_csv(urlpath=path, usecols=self.fields, encoding='utf-8')
        except OSError as err:
            raise Exception(err.strerror) from err

    def __write(self, data):
        """

        :param data:
        :return:
        """

        return src.functions.streams.Streams().write(
            data=data, path=os.path.join(self.storage, 'density.csv'))

    def exc(self, path):

        frame = self.__read(path=path)

        lines: pd.DataFrame = frame.compute()
        lines.reset_index(drop=True, inplace=True)
        lines = lines.melt(id_vars=['iso2', 'year', 'identifier', 'p_density'],
                           value_vars=['hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                           var_name='infection',
                           value_name='prevalence')

        message = self.__write(data=lines)

        return message

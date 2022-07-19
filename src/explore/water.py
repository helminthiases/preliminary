import os.path

import dask.dataframe
import pandas as pd

import src.functions.streams


class Water:

    def __init__(self, storage):
        """

        """

        self.storage = storage
        self.fields = ['iso2', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'identifier',
                       'improved_water', 'unpiped_water', 'surface_water', 'piped_water', 'unimproved_water']

    def __read(self, path):
        """

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
            data=data, path=os.path.join(self.storage, 'water.csv'))

    @staticmethod
    def __access(data):
        """

        :param data:
        :return:
        """

        lines = data.melt(id_vars=['iso2', 'year', 'identifier', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                          value_vars=['improved_water', 'unpiped_water', 'surface_water', 'piped_water', 'unimproved_water'],
                          var_name='water_facility',
                          value_name='access_percentage')

        condition = lines[['access_percentage']].notna().values
        lines = lines.copy().loc[condition, :]

        return lines

    @staticmethod
    def __prevalence(data):
        """

        :param data:
        :return:
        """

        lines = data.melt(id_vars=['iso2', 'year', 'identifier', 'water_facility', 'access_percentage'],
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
        lines = self.__access(data=lines)
        lines = self.__prevalence(data=lines)
        message = self.__write(data=lines)

        return message

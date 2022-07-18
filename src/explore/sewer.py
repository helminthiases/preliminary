import os.path

import pandas as pd
import dask.dataframe

import src.functions.streams


class Sewer:

    def __init__(self, storage):
        """

        """

        self.storage = storage
        self.fields = ['iso2', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'identifier',
                       'improved_sewer', 'unpiped_sewer', 'surface_sewer', 'piped_sewer', 'unimproved_sewer']

    def __read(self, path):
        """

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
            data=data, path=os.path.join(self.storage, 'sewer.csv'))

    def exc(self, path):
        """

        :param path:
        :return:
        """

        frame = self.__read(path=path)

        lines: pd.DataFrame = frame.compute()
        lines.reset_index(drop=True, inplace=True)
        lines = lines.melt(id_vars=['iso2', 'year', 'identifier', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                           value_vars=['improved_sewer', 'unpiped_sewer', 'surface_sewer', 'piped_sewer', 'unimproved_sewer'],
                           var_name='sewage_facility',
                           value_name='access_percentage')

        message = self.__write(data=lines)

        return message
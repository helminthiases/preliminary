import os

import pandas as pd

import src.functions.streams


class Integrate:

    def __init__(self, storage: str):
        """

        """

        self.storage = storage

    def __write(self, data):
        return src.functions.streams.Streams().write(
            data=data, path=os.path.join(self.storage, 'cases.csv'))

    @staticmethod
    def __fractions(data):
        """

        :param data:
        :return:
        """

        # melt
        frame = data.melt(id_vars=['iso2', 'N'],
                          value_vars=['hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'sth_prevalence'],
                          value_name='infection', var_name='exist')

        # fractions
        frame.loc[:, 'exist_fraction'] = frame['exist'].div(frame['N'], fill_value=0).values

        # NaN
        frame['exist'].where(frame['exist'].notna(), 0, inplace=True)

        return frame

    def exc(self, raw: pd.DataFrame, exists: pd.DataFrame):
        """

        :param raw:
        :param exists:
        :return:
        """

        # merge
        frame = raw.merge(exists, how='left', on='iso2')

        # fractions
        frame = self.__fractions(data=frame)

        return self.__write(data=frame)

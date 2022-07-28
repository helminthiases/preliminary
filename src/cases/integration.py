import os

import pandas as pd

import src.functions.streams


class Integration:

    def __init__(self, storage: str):
        """

        :param storage:
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
                          value_name='exist', var_name='infection')

        # fractions
        frame.loc[:, 'exist_fraction'] = frame['exist'].div(frame['N'], fill_value=0).values

        # NaN
        frame['exist'].where(frame['exist'].notna(), 0, inplace=True)

        return frame

    def exc(self, experiments: pd.DataFrame, exists: pd.DataFrame):
        """

        :param experiments:
        :param exists:
        :return:
        """

        # merge
        frame = experiments.merge(exists, how='left', on='iso2')

        # fractions
        frame = self.__fractions(data=frame)

        self.__write(data=frame)

        return frame

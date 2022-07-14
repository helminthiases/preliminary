import os
import logging

import pandas as pd

import src.functions.directories
import src.functions.streams


class Prevalence:

    def __init__(self, storage: str):
        """

        :param storage:
        """

        self.storage = storage
        src.functions.directories.Directories().create(self.storage)

        # instances
        self.streams = src.functions.streams.Streams()

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def __fractions(data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        frame = data.copy()
        quotients = frame[['hk_missing', 'asc_missing', 'tt_missing']].div(frame['N'], axis='index')
        frame.loc[:, ['hk_missing_fraction', 'asc_missing_fraction', 'tt_missing_fraction']] = quotients.values

        return frame

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # numbers
        # numbers = data.copy()[['iso2', 'N', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence']]
        # self.streams.write(data=numbers, path=os.path.join(self.storage, 'prevalenceNumbers.csv'))

        # percentages
        # fractions = self.__fractions(data=numbers)
        # self.streams.write(data=fractions, path=os.path.join(self.storage, 'prevalenceFractions.csv'))

        frame = data.copy()[['iso2', 'N', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence']]
        frame.rename(columns={'hk_prevalence': 'hk_missing', 'asc_prevalence': 'asc_missing',
                              'tt_prevalence': 'tt_missing'}, inplace=True)
        frame = self.__fractions(data=frame)
        self.streams.write(data=frame, path=os.path.join(self.storage, 'prevalence.csv'))

import os
import logging

import pandas as pd

import src.functions.streams


class Prevalence:

    def __init__(self, storage: str):
        """

        :param storage:
        """

        self.storage = storage

        # instances
        self.streams = src.functions.streams.Streams()

        # logging
        logging.basicConfig(level=logging.INFO,
                            format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                            datefmt='%Y-%m-%d %H:%M:%S')
        self.logger = logging.getLogger(__name__)

    def __fractions(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        frame = data.copy()
        frame.loc[:, ['hk_prevalence', 'asc_prevalence', 'tt_prevalence']] = \
            frame[['hk_prevalence', 'asc_prevalence', 'tt_prevalence']].div(frame['N'], axis='index')

        self.logger.info(frame.head())

        return frame

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # numbers
        numbers = data.copy()[['iso2', 'N', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence']]
        self.streams.write(data=numbers, path=os.path.join(self.storage, 'prevalenceNumbers.csv'))

        # percentages
        fractions = self.__fractions(data=numbers)
        self.streams.write(data=fractions, path=os.path.join(self.storage, 'prevalenceFractions.csv'))

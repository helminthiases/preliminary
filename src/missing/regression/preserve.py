import os

import pandas as pd

import src.functions.directories
import src.functions.streams


class Preserve:

    def __init__(self):
        """

        """

        self.storage = os.path.join(os.getcwd(), 'warehouse', 'missing', 'regression')
        directories = src.functions.directories.Directories()
        directories.cleanup(path=self.storage)
        directories.create(path=self.storage)

    def exc(self, estimates: pd.DataFrame):
        """

        :param estimates:
        :return:
        """

        frame = estimates.loc[~(estimates['variable'] == 'const'), :]
        message = src.functions.streams.Streams().write(
            data=frame, path=os.path.join(self.storage, 'estimates.csv'))

        return message

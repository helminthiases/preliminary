import os
import logging

import pandas as pd

import src.functions.streams
import src.functions.directories


class SpatioTemporal:

    def __init__(self, storage: str):
        """

        :param storage: storage directory
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

    def exc(self, data: pd.DataFrame):
        """

        :param data:
        :return:
        """

        # numbers & fractions
        frame = pd.melt(data, id_vars=['iso2', 'N'],
                        value_vars=['site_id', 'latitude', 'longitude', 'year', 'coordinates'],
                        var_name='feature', value_name='missing_number')
        frame.loc[:, 'missing_fraction'] = frame['missing_number'].div(frame['N'])

        self.streams.write(data=frame, path=os.path.join(self.storage, 'spatiotemporal.csv'))

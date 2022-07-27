import logging
import os
import sys

import pandas as pd


def main():
    """

    :return:
    """

    # per country, and w.r.t. complete cases, determine the number of observations
    # that lie within the IHME WASH years
    frame = src.interval.features.Features().exc()
    logger.info(frame.info())

    # for reference purposes, get the original number of observations per
    # country, i.e., the counts prior to the removal of incomplete cases
    try:
        complete = pd.read_csv(filepath_or_buffer=os.path.join(root, 'warehouse', 'cases', 'cases.csv'),
                               usecols=['iso2', 'N'])
    except OSError as err:
        raise Exception(err.strerror) from err
    logger.info(complete)

    # merge
    frame = frame.merge(complete, how='left', on='iso2')

    # preserve
    message = src.functions.streams.Streams().write(data=frame, path=os.path.join(storage, 'interval.csv'))
    logger.info(message)


if __name__ == '__main__':

    # path
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # classes
    import src.interval.features
    import src.functions.directories
    import src.functions.streams

    # Storage
    storage = os.path.join(os.getcwd(), 'warehouse', 'interval')
    src.functions.directories.Directories().create(path=storage)

    main()

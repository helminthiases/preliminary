import logging
import os
import pathlib
import sys

import dask.dataframe
import pandas as pd


def main():
    """

    :return:
    """

    logger.info('prevalence & water')

    # Reading-in and merging the set of enhanced, and inspected, STH experiments
    # data files.  Only relevant fields are read.
    frame = dask.dataframe.read_csv(urlpath=path, usecols=fields, encoding='utf-8')
    lines: pd.DataFrame = frame.compute()
    lines.reset_index(drop=True, inplace=True)
    logger.info(lines.shape)

    # Writing to a single file
    src.functions.streams.Streams().write(data=lines, path=os.path.join(storage, 'water.csv'))


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

    # hub
    hub = pathlib.Path(root).parent

    # source
    path = os.path.join(hub, 'spatial', 'warehouse', 'features', 'elevation', '*.csv')
    fields = ['iso2', 'longitude', 'latitude', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'identifier',
              'improved_water', 'unpiped_water', 'surface_water', 'piped_water', 'unimproved_water', 'elevation']

    # storage
    storage = os.path.join(root, 'warehouse', 'explore', 'access')

    # classes
    import src.functions.directories
    import src.functions.streams

    directories = src.functions.directories.Directories()
    directories.cleanup(path=storage)
    directories.create(path=storage)

    main()

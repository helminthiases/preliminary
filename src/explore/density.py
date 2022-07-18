import sys
import os
import logging
import pathlib

import pandas as pd
import dask.dataframe


def main():
    """

    :return:
    """

    logger.info('prevalence & population density')

    # Reading-in and merging the set of enhanced, and inspected, STH experiments
    # data files.  Only relevant fields are read.
    frame = dask.dataframe.read_csv(urlpath=path, usecols=fields, encoding='utf-8')
    lines: pd.DataFrame = frame.compute()
    lines.reset_index(drop=True, inplace=True)
    lines = lines.melt(id_vars=['iso2', 'year', 'identifier', 'p_density'],
                       value_vars=['hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                       var_name='infection',
                       value_name='prevalence')
    logger.info(lines.shape)
    logger.info(lines.head())

    # Writing to a single file
    src.functions.streams.Streams().write(data=lines, path=os.path.join(storage, 'density.csv'))


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
    fields = ['iso2', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'identifier',
              'p_density']

    # storage
    storage = os.path.join(root, 'warehouse', 'explore', 'misc')

    # classes
    import src.functions.directories
    import src.functions.streams

    directories = src.functions.directories.Directories()
    directories.cleanup(path=storage)
    directories.create(path=storage)

    main()
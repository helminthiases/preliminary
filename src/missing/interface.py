import logging
import os
import sys

import pandas as pd


def main():
    """

    :return:
    """

    frame = src.missing.features.Features().exc()
    logger.info(frame.head())

    # prevalence features
    prevalence = pd.melt(frame, id_vars=['iso2', 'N'],
                         value_vars=['hk_prevalence', 'asc_prevalence', 'tt_prevalence'],
                         var_name='geohelminth', value_name='missing_fraction')
    try:
        prevalence.to_csv(path_or_buf=os.path.join(storage, 'prevalence.csv'),
                          header=True, index=False, encoding='utf-8')
    except OSError as err:
        raise Exception(err.strerror)

    # space & time features
    spatiotemporal = pd.melt(frame, id_vars=['iso2', 'N'],
                             value_vars=['site_id', 'latitude', 'longitude', 'year', 'coordinates'],
                             var_name='feature', value_name='missing_fraction')
    try:
        spatiotemporal.to_csv(path_or_buf=os.path.join(storage, 'spatiotemporal.csv'),
                              header=True, index=False, encoding='utf-8')
    except OSError as err:
        raise Exception(err.strerror)


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
    import src.missing.features
    import src.functions.directories

    # Storage
    storage = os.path.join(os.getcwd(), 'warehouse', 'missing')
    src.functions.directories.Directories().create(path=storage)

    main()

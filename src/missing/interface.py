import logging
import os
import sys
import pathlib
import pandas as pd
import glob


def main():
    """

    :return:
    """

    # The focus herein is ESPEN STH experiments missing data analysis.  The data is
    # stored in the files of:
    source = os.path.join(str(pathlib.Path(os.getcwd()).parent), 'infections', 'warehouse',
                          'data', 'ESPEN', 'experiments', 'baseline')

    # This function determines the missing state of each value of the fields of interest.  In general, the
    # fields in question are the geographic coordinates fields, the geohelminth prevalence fields, and
    # the year fields
    frame = src.missing.features.Features(storage=os.path.join(storage, 'disaggregates'), source=source).exc()

    # Inventory of <disaggregates> files
    files = glob.glob(pathname=os.path.join(storage, 'disaggregates', '*.csv'))
    elements = [file.split('preliminary', 1)[1] for file in files]
    elements = [element.replace('\\', '/') for element in elements]
    elements = [HUB + element for element in elements]
    data = pd.DataFrame(data={'path': elements})
    data.to_csv(path_or_buf=os.path.join(storage, 'data.csv'), index=False, header=True, encoding='utf-8')

    # Counts & fractions for graphing
    src.missing.prevalence.Prevalence(
        storage=os.path.join(storage, 'aggregates')).exc(data=frame)
    src.missing.spatiotemporal.SpatioTemporal(
        storage=os.path.join(storage, 'aggregates')).exc(data=frame)

    # Null Regression
    # Focusing on the countries with the smallest number of missing data cells
    paths = [os.path.join(source, f'{name}.csv')
             for name in ['NG', 'TG', 'LR', 'CD', 'UG', 'KE', 'CI', 'ZM', 'MW', 'TZ', 'MG', 'SZ', 'ML', 'ER']]
    estimates = src.missing.regression.estimates.Estimates(paths=paths).exc()
    message = src.missing.regression.preserve.Preserve().exc(estimates=estimates)
    logger.info(message)


if __name__ == '__main__':

    # path
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))
    HUB = 'https://raw.githubusercontent.com/helminthiases/preliminary/master'

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # classes
    import src.functions.directories
    import src.missing.features
    import src.missing.prevalence
    import src.missing.spatiotemporal
    import src.missing.regression.estimates
    import src.missing.regression.preserve

    # storage
    storage = os.path.join(os.getcwd(), 'warehouse', 'missing')

    # directories
    directories = src.functions.directories.Directories()
    directories.cleanup(storage)
    directories.create(path=storage)

    main()

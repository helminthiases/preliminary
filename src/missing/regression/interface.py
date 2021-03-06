"""
interface
"""
import logging
import os
import sys
import pathlib


def main():
    """
    Null regression

    :return:
    """

    logger.info('pattern')

    # we are interested in the missing data of the raw data
    source = os.path.join(str(pathlib.Path(os.getcwd()).parent), 'infections', 'warehouse',
                          'data', 'ESPEN', 'experiments', 'baseline')

    # focusing on the countries with the smallest number of missing data cells
    paths = [os.path.join(source, f'{name}.csv') for name in ['NG', 'TG', 'LR', 'CD', 'UG', 'KE', 'CI', 'ZM', 'MW']]

    # null regression
    estimates = src.missing.regression.estimates.Estimates(paths=paths).exc()
    message = src.missing.regression.preserve.Preserve().exc(estimates=estimates)
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

    # class
    import src.missing.regression.estimates
    import src.missing.regression.preserve

    main()

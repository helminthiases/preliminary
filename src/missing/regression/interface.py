import os
import sys
import logging

import pandas as pd


def main():

    source = os.path.join(os.getcwd(), 'warehouse', 'missing', 'disaggregates')

    estimates = src.missing.regression.estimates.Estimates(source=source).exc()
    logger.info(pd.concat(estimates))


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
    import src.missing.regression.estimates

    main()

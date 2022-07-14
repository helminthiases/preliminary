import logging
import os
import sys


def main():

    # the location of the data files that encode data missing states
    source = os.path.join(os.getcwd(), 'warehouse', 'missing', 'disaggregates')

    # null regression
    estimates = src.missing.regression.estimates.Estimates(source=source).exc()
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

    # classes
    import src.missing.regression.estimates
    import src.missing.regression.preserve

    main()

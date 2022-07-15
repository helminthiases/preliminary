import logging
import os
import sys
import pathlib


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

    # Counts & fractions for graphing
    src.missing.prevalence.Prevalence(
        storage=os.path.join(storage, 'aggregates')).exc(data=frame)
    src.missing.spatiotemporal.SpatioTemporal(
        storage=os.path.join(storage, 'aggregates')).exc(data=frame)

    # The location of the data files that encode data missing states
    source = os.path.join(os.getcwd(), 'warehouse', 'missing', 'disaggregates')

    # Hence, null regression.
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

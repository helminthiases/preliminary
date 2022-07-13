import logging
import os
import sys
import pathlib


def main():
    """

    :return:
    """

    source = os.path.join(str(pathlib.Path(os.getcwd()).parent), 'infections', 'warehouse',
                          'data', 'ESPEN', 'experiments', 'baseline')

    frame = src.missing.features.Features(storage=os.path.join(storage, 'disaggregates'), source=source).exc()
    logger.info(frame.head())

    src.missing.prevalence.Prevalence(
        storage=os.path.join(storage, 'aggregates')).exc(data=frame)
    src.missing.spatiotemporal.SpatioTemporal(
        storage=os.path.join(storage, 'aggregates')).exc(data=frame)


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

    # storage
    storage = os.path.join(os.getcwd(), 'warehouse', 'missing')

    # directories
    directories = src.functions.directories.Directories()
    directories.cleanup(storage)
    directories.create(path=storage)

    main()

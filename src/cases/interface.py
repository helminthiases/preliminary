import glob
import logging
import os
import sys


def main():
    """

    :return:
    """

    logger.info('cases')

    # experiments: # of raw observations per country
    paths = glob.glob(pathname=os.path.join(hub, 'infections', 'warehouse', 'data',
                                            'ESPEN', 'experiments', 'baseline', '*.csv'))
    experiments = src.cases.experiments.Experiments().exc(paths=paths)
    logger.info(experiments.head())

    # exists: summary of number of usable observations per infection type, per country
    source = os.path.join(hub, 'infections', 'warehouse', 'data', 'ESPEN', 'experiments', 'reduced', '*.csv')
    exists = src.cases.exists.Exists().exc(source=source)
    logger.info(exists.head())

    # integrating experiments & exists
    message = src.cases.integration.Integration(storage=storage).exc(
        experiments=experiments, exists=exists)
    logger.info(message)


if __name__ == '__main__':

    # path
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # the hub
    hub = os.path.dirname(root)

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    # classes
    import src.cases.experiments
    import src.cases.exists
    import src.cases.integration
    import src.functions.streams
    import src.functions.directories

    # storage
    storage = os.path.join(root, 'warehouse', 'cases')
    directories = src.functions.directories.Directories()
    directories.cleanup(storage)
    directories.create(storage)

    main()

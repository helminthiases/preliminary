import glob
import logging
import os
import sys


def main():
    logger.info('cases')

    # experiments
    paths = glob.glob(pathname=os.path.join(hub, 'infections', 'warehouse', 'data',
                                            'ESPEN', 'experiments', 'baseline', '*.csv'))
    experiments = src.cases.experiments.Experiments().exc(paths=paths)

    # exists
    path = os.path.join(hub, 'infections', 'warehouse', 'data', 'ESPEN', 'networks', 'graphs', '*.csv')
    exists = src.cases.exists.Exists().exc(path=path)

    message = src.cases.integrate.Integrate(storage=storage).exc(experiments=experiments, exists=exists)
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
    import src.cases.integrate
    import src.functions.streams
    import src.functions.directories

    # storage
    storage = os.path.join(root, 'warehouse', 'cases')
    directories = src.functions.directories.Directories()
    directories.cleanup(storage)
    directories.create(storage)

    main()

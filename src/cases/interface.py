import logging
import os
import sys
import glob


def main():

    logger.info('main')

    # number of lines
    numerics = src.cases.numerics.Numerics()

    # raw
    paths = glob.glob(pathname=os.path.join(hub, 'infections', 'warehouse', 'data',
                                            'ESPEN', 'experiments', 'baseline', '*.csv'))
    miscellaneous = numerics.exc(paths=paths)
    logger.info(miscellaneous)

    # complete
    paths = glob.glob(pathname=os.path.join(hub, 'infections', 'warehouse', 'data',
                                            'ESPEN', 'networks', 'graphs', '*.csv'))
    complete = numerics.exc(paths=paths)
    logger.info(complete)


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
    import src.cases.numerics

    main()

import glob
import logging
import os
import sys


def main():
    logger.info('cases')

    # number of lines
    numerics = src.cases.numerics.Numerics()

    # raw
    paths = glob.glob(pathname=os.path.join(hub, 'infections', 'warehouse', 'data',
                                            'ESPEN', 'experiments', 'baseline', '*.csv'))
    raw = numerics.exc(paths=paths)

    # complete
    paths = glob.glob(pathname=os.path.join(hub, 'infections', 'warehouse', 'data',
                                            'ESPEN', 'networks', 'graphs', '*.csv'))
    complete = numerics.exc(paths=paths)
    complete.rename(columns={'N': 'complete'}, inplace=True)

    # merge
    frame = raw.merge(complete, how='left', on='iso2')
    frame.loc[:, 'complete_fraction'] = frame['complete'].div(frame['N'], fill_value=0).values
    logger.info(frame)

    # preserve
    message = src.functions.streams.Streams().write(
        data=frame, path=os.path.join(storage, 'complete.csv'))
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
    import src.cases.numerics
    import src.functions.streams
    import src.functions.directories

    # storage
    storage = os.path.join(root, 'warehouse', 'cases')
    directories = src.functions.directories.Directories()
    directories.cleanup(storage)
    directories.create(storage)

    main()

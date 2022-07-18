import logging
import os
import pathlib
import sys


def main():
    logger.info('explore')


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

    # hub
    hub = pathlib.Path(root).parent

    # source
    path = os.path.join(hub, 'spatial', 'warehouse', 'features', 'elevation', '*.csv')

    # storage
    storage = os.path.join(root, 'warehouse', 'explore')

    # classes
    import src.functions.directories
    import src.functions.streams

    directories = src.functions.directories.Directories()
    directories.cleanup(path=storage)
    directories.create(path=storage)

    main()

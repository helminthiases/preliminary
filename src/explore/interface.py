import logging
import os
import pathlib
import sys


def main():
    """

    :return:
    """

    logger.info('explore')

    message = src.explore.water.Water(storage=storage).exc(path=path)
    logger.info(message)

    message = src.explore.sewer.Sewer(storage=storage).exc(path=path)
    logger.info(message)

    message = src.explore.density.Density(storage=storage).exc(path=path)
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

    # hub
    hub = pathlib.Path(root).parent

    # source
    path = os.path.join(hub, 'spatial', 'warehouse', 'features', 'elevation', '*.csv')

    # storage
    storage = os.path.join(root, 'warehouse', 'explore')

    # classes
    import src.explore.sewer
    import src.explore.water
    import src.explore.density
    import src.functions.directories
    import src.functions.streams

    directories = src.functions.directories.Directories()
    directories.cleanup(path=storage)
    directories.create(path=storage)

    main()

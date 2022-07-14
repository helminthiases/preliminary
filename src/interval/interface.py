import logging
import os
import sys


def main():
    """

    :return:
    """

    frame = src.interval.features.Features().exc()
    logger.info(frame.info())

    message = src.functions.streams.Streams().write(data=frame, path=os.path.join(storage, 'interval.csv'))
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
    import src.interval.features
    import src.functions.directories
    import src.functions.streams

    # Storage
    storage = os.path.join(os.getcwd(), 'warehouse', 'interval')
    src.functions.directories.Directories().create(path=storage)

    main()

import os
import sys
import logging


def main():

    logger.info('regression')

    source = os.path.join(os.getcwd(), 'warehouse', 'missing', 'disaggregates')

    src.missing.regression.states.States(source=source).exc()


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
    import src.missing.regression.states

    main()

import logging
import os
import subprocess
import sys


def main():
    """

    :return:
    """

    logger.info('main')
    subprocess.run('python src/missing/interface.py', shell=True)
    subprocess.run('python src/missing/interface.py', shell=True)


if __name__ == '__main__':

    # path
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # hub
    hub = os.path.dirname(root)

    # logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger(__name__)

    main()

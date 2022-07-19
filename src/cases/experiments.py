import os
import pathlib

import dask
import pandas as pd


class Experiments:

    def __init__(self):
        """

        """

    @staticmethod
    @dask.delayed
    def __lines(path: str) -> pd.DataFrame:
        """

        :return:
        """

        with open(file=path, mode='r') as disc:
            count = sum(1 for _ in disc)
            disc.close()

        return pd.DataFrame(data={'iso2': pathlib.Path(path).stem, 'N': count}, index=[0])

    def exc(self, paths):
        """

        :return:
        """

        computation = []
        for path in paths:
            lines = self.__lines(path=path)
            computation.append(lines)

        dask.visualize(computation, filename=os.path.join(os.getcwd(), 'src', 'cases', 'data'), format='pdf')
        calculations = dask.compute(computation, scheduler='processes')[0]

        return pd.concat(calculations, ignore_index=True)

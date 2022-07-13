import os
import glob
import pathlib

import pandas as pd
import numpy as np
import dask

import src.missing.regression.glm


class States:

    def __init__(self, source):
        """

        """

        self.paths = glob.glob(pathname=os.path.join(source, '*.csv'))

        self.glm = src.missing.regression.glm.GLM()

        self.infections = ['hk_prevalence', 'asc_prevalence', 'tt_prevalence']

    @staticmethod
    @dask.delayed
    def __read(path: str):

        try:
            return pd.read_csv(filepath_or_buffer=path, header=0, encoding='utf-8', dtype=np.int32)
        except OSError as err:
            raise Exception(err.strerror) from err

    @dask.delayed
    def __glm(self, independent: list, dependent: str, name: str, data: pd.DataFrame):
        """

        :param independent:
        :param dependent:
        :param data:
        :return:
        """

        if data[dependent].sum() == 0:
            return pd.DataFrame()
        elif data[dependent].sum() == data.shape[0]:
            return pd.DataFrame()
        elif data[independent].values.sum() == 0:
            return pd.DataFrame()
        else:
            return self.glm.exc(independent=independent, dependent=dependent,
                                name=name, data=data)

    @staticmethod
    @dask.delayed
    def __integrate(time: pd.DataFrame, space: pd.DataFrame):

        frame = pd.concat([time, space], ignore_index=True, axis=0)

        return frame

    def exc(self):

        computation = []
        for path in self.paths:

            name = pathlib.Path(path).stem
            frame = self.__read(path=path)
            time = self.__glm(independent=['year'] + self.infections, dependent='coordinates', name=name, data=frame)
            space = self.__glm(independent=['coordinates'] + self.infections, dependent='year', name=name, data=frame)
            estimates = self.__integrate(time=time, space=space)

            computation.append(estimates)

        dask.visualize(computation, filename=os.path.join(os.getcwd(), 'src', 'missing', 'regression', 'data'),
                       format='pdf')
        calculations = dask.compute(computation, scheduler='processes')[0]

        return calculations

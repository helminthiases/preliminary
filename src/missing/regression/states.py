import os
import glob
import pathlib

import pandas as pd
import numpy as np

import src.missing.regression.glm


class States:

    def __init__(self, source):
        """

        """

        self.paths = glob.glob(pathname=os.path.join(source, '*.csv'))

        self.glm = src.missing.regression.glm.GLM()

        self.infections = ['hk_prevalence', 'asc_prevalence', 'tt_prevalence']

    @staticmethod
    def __read(path: str):

        try:
            return pd.read_csv(filepath_or_buffer=path, header=0, encoding='utf-8', dtype=np.int32)
        except OSError as err:
            raise Exception(err.strerror) from err

    def __glm(self, independent: list, dependent: str, name: str, data: pd.DataFrame):
        """

        :param independent:
        :param dependent:
        :param data:
        :return:
        """

        if data[[dependent]].values.sum() == 0:
            return pd.DataFrame()
        else:
            return self.glm.exc(independent=independent, dependent=dependent,
                                name=name, data=data)

    @staticmethod
    def __integrate(time: pd.DataFrame, space: pd.DataFrame):

        frame = pd.concat([time, space], ignore_index=True, axis=0)

        return frame

    def exc(self):

        for path in self.paths[:5]:

            name = pathlib.Path(path).stem

            frame = self.__read(path=path)
            time = self.__glm(independent=['year'] + self.infections, dependent='coordinates', name=name, data=frame)
            space = self.__glm(independent=['coordinates'] + self.infections, dependent='year', name=name, data=frame)
            estimates = self.__integrate(time=time, space=space)

            print(estimates)

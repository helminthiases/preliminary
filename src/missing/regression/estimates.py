"""
estimates
"""
import os
import pathlib

import pandas as pd
import dask

import src.missing.regression.glm


class Estimates:
    """
    The null regression estimates
    """

    def __init__(self, paths):
        """

        :param paths:
        """

        self.infections = ['hk_prevalence', 'asc_prevalence', 'tt_prevalence']

        # data source paths
        self.paths = paths

        # instances
        self.glm = src.missing.regression.glm.GLM()

    @dask.delayed
    def __read(self, path: str):
        """

        :param path:
        :return:
        """

        try:
            reference = pd.read_csv(filepath_or_buffer=path, header=0, encoding='utf-8',
                                    usecols=['iso2', 'year', 'longitude', 'latitude'] + self.infections)
        except OSError as err:
            raise Exception(err.strerror) from err

        reference.loc[:, 'coordinates'] = reference['longitude'].notna() & reference['latitude'].notna()
        reference.loc[:, 'period'] = reference['year'].isna()
        reference.loc[:, 'geography'] = reference['longitude'].isna() | reference['latitude'].isna()

        return reference

    @dask.delayed
    def __glm(self, independent: list, dependent: str, name: str, data: pd.DataFrame):
        """

        :param independent:
        :param dependent:
        :param data:
        :return:
        """

        return self.glm.exc(independent=independent, dependent=dependent,
                            name=name, data=data)

    @staticmethod
    @dask.delayed
    def __integrate(time: pd.DataFrame, space: pd.DataFrame):
        """

        :param time:
        :param space:
        :return:
        """

        frame = pd.concat([time, space], ignore_index=True, axis=0)

        return frame

    def exc(self):
        """

        :return:
        """

        computation = []
        for path in self.paths:

            name = pathlib.Path(path).stem
            frame = self.__read(path=path)
            time = self.__glm(independent=['year'] + self.infections, dependent='geography', name=name, data=frame)
            space = self.__glm(independent=['coordinates'] + self.infections, dependent='period', name=name, data=frame)
            estimates = self.__integrate(time=time, space=space)

            computation.append(estimates)

        dask.visualize(computation, filename=os.path.join(os.getcwd(), 'src', 'missing', 'regression', 'data'),
                       format='pdf')
        calculations = dask.compute(computation, scheduler='processes')[0]

        return pd.concat(calculations)

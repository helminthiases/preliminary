"""
Module: glm
"""
import numpy as np
import pandas as pd
import statsmodels.api as sma
import statsmodels.iolib as smi


class GLM:
    """
    GLM
    """

    def __init__(self):
        """

        """

        self.floats = ['coefficient', 'S.E.', 'z', 'p_value', '0.025', '0.975']

    @staticmethod
    def __estimates(outcome, predictors) -> list:
        """
        generalised linear modelling

        :param outcome:
        :param predictors:
        :return:
        """

        design = sma.add_constant(predictors, prepend=True)
        alg = sma.GLM(endog=outcome, exog=design.astype(float), missing='drop', family=sma.families.Binomial())
        model = alg.fit(use_t=True)
        summary = model.summary()

        return summary.tables

    def __coefficients(self, estimates: list):
        """

        :param estimates:
        :return:
        """

        coefficients: smi.SimpleTable = estimates[1]
        content: list = coefficients.data

        # excluding the labels row
        frame = pd.DataFrame(data=content[1:])

        # naming the fields
        frame.set_axis(['variable', 'coefficient', 'S.E.', 'z', 'p_value', '0.025', '0.975'],
                       axis='columns', inplace=True)

        # ensuring that all the fields, except the variables field, have float values
        frame.loc[:, self.floats] = frame[self.floats].astype(float)

        return frame

    @staticmethod
    def __settings(data: pd.DataFrame, coefficients: pd.DataFrame,
                   independent: list) -> pd.DataFrame:
        """

        :param data:
        :param coefficients:
        :param independent:
        :return:
        """

        # number of missing values per predictor
        variables = data[independent].isna().sum().to_frame()
        variables.reset_index(drop=False, inplace=True)
        variables.set_axis(labels=['variable', 'variable.nan'], axis=1, inplace=True)

        # merge
        frame = coefficients.merge(variables, how='left', on='variable')

        return frame

    def __extrema(self, independent: list):
        """

        :param independent:
        :return:
        """

        extrema = pd.DataFrame(data={'variable': ['const'] + independent})
        extrema.loc[:, self.floats] = np.NAN

        return extrema

    def exc(self, independent: list, dependent: str, name: str, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param independent:
        :param dependent:
        :param name:
        :param data:
        :return:
        """

        condition = data[independent].notna().sum() > 0
        reduced = sum(condition) != len(independent)

        if (data[dependent].sum() == 0) | (data[dependent].sum() == data.shape[0]):
            coefficients = self.__extrema(independent=independent)
        elif reduced:
            coefficients = self.__extrema(independent=independent)
        else:
            # the generalised linear model estimates
            estimates = self.__estimates(outcome=data[[dependent]],
                                         predictors=data[independent])
            # extracting & structuring the coefficient estimates
            coefficients = self.__coefficients(estimates=estimates)

        # the missing values counts
        coefficients = self.__settings(data=data, coefficients=coefficients, independent=independent)

        # finally
        coefficients.loc[:, 'reference'] = dependent
        coefficients.loc[:, 'reference.nan'] = data[[dependent]].values.sum()
        coefficients.loc[:, 'iso2'] = name

        return coefficients

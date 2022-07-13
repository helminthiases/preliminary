"""
Module: glm
"""
import pandas as pd
import statsmodels.api as sma
import statsmodels.iolib as smi


class GLM:

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

        design = sma.add_constant(predictors, prepend=False)
        alg = sma.GLM(endog=outcome, exog=design, family=sma.families.Binomial())
        model = alg.fit()
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
    def __settings(coefficients: pd.DataFrame, dependent: str, name: str) -> pd.DataFrame:
        """

        :param coefficients:
        :param dependent:
        :param name:
        :return:
        """

        frame = coefficients.copy()
        frame.loc[:, 'iso2'] = name
        frame.loc[:, 'reference'] = dependent

        return frame

    def exc(self, independent: list, dependent: str, name: str, data: pd.DataFrame) -> pd.DataFrame:
        """

        :param independent:
        :param dependent:
        :param name:
        :param data:
        :return:
        """

        # the generalised linear model estimates
        estimates = self.__estimates(outcome=data.copy()[[dependent]],
                                     predictors=data.copy()[independent])

        # extracting & structuring the coefficient estimates
        coefficients = self.__coefficients(estimates=estimates)
        coefficients = self.__settings(coefficients=coefficients,
                                       dependent=dependent,
                                       name=name)

        # the number of empty reference field cells
        coefficients.loc[:, 'reference.nan'] = data[[dependent]].values.sum()

        return coefficients

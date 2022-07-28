"""
Module: exists
"""
import pandas as pd
import dask.dataframe


class Exists:
    """
    Exists
    """

    def __init__(self):
        """

        """

        self.fields = ['iso2', 'year', 'hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'sth_prevalence', 'identifier']
        self.infections = ['hk_prevalence', 'asc_prevalence', 'tt_prevalence', 'sth_prevalence']

    def __read(self, source: str) -> pd.DataFrame:
        """

        :param source:
        :return:
        """

        try:
            frame = dask.dataframe.read_csv(urlpath=source, usecols=self.fields, encoding='utf-8')
        except OSError as err:
            raise Exception(err.strerror) from err

        lines: pd.DataFrame = frame.compute()

        return lines

    def exc(self, source: str)-> pd.DataFrame:
        """

        :param source:
        :return:
        """

        lines = self.__read(source=source)

        lines.loc[:, self.infections] = lines[self.infections].notna().values
        exists = lines.groupby(by='iso2').agg(hk_prevalence=('hk_prevalence', sum),
                                              asc_prevalence=('asc_prevalence', sum),
                                              tt_prevalence=('tt_prevalence', sum),
                                              sth_prevalence=('sth_prevalence', sum))
        exists.reset_index(drop=False, inplace=True)

        return exists

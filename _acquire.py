################################################################################
#
#
#
#       _acquire.py
#
#       Description: This file contains an Acquire class which can be used as a
#           parent class for data acquisition. Simply inherit the class and 
#           set the file_name, database_name, and sql fields to the relevant 
#           information.
#
#       Class:
#
#           Acquire
#
#       Class Fields:
#
#           file_name
#           database_name
#           sql
#
#       Class Methods:
#
#           __init__(self, file_name, database_name, sql)
#           get_data(self, use_cache = True, cache_data = True)
#           _load_data(self, use_cache = True, cache_data = True)
#           _pre_preparation(self, df)
#
#
################################################################################

import os
import pandas as pd

from get_db_url import get_db_url

################################################################################

class Acquire:
    '''
        A data acquisition class that can be used for acquiring data and cacheing it in 
        a csv file.
        
        Instance Methods
        ----------------
        __init__: Returns None
        get_data: Returns DataFrame
        _load_data: Return DataFrame
        _pre_preparation: Return DataFrame
    '''

    ################################################################################

    def __init__(self, file_name: str = '', database_name: str = '', sql: str = '') -> None:
        '''
            Parameters
            ----------
            file_name: str
                A .csv file name for cacheing data for quicker access.

            database_name: str
                The name of the database to load the data from.

            sql: str
                An SQL query with which to query the data from the database.
        '''

        self.file_name = file_name
        self.database_name = database_name
        self.sql = sql

    ################################################################################

    def get_data(self, use_cache: bool = True, cache_data: bool = True) -> pd.DataFrame:
        '''
            Acquire the data from either the database or csv file and perform 
            any pre preparation transformations that are defined.
        
            Parameters
            ---------- 
            use_cache: bool, default True
                If True the dataset will be retrieved from a csv file if one
                exists, otherwise, it will be retrieved from the MySQL database. 
                If False the dataset will be retrieved from the MySQL database
                even if the csv file exists.

            cache_data: bool, default True
                If True the dataset will be cached in a csv file.

            Returns
            -------
            DataFrame: A Pandas DataFrame containing data from the source provided.
        '''

        df = self._load_data(use_cache, cache_data)
        return self._pre_preparation(df)

    ################################################################################

    def _load_data(self, use_cache: bool = True, cache_data: bool = True) -> pd.DataFrame:
        '''
            Return a dataframe containing data from the database defined by 
            self.database_name.

            If a .csv file containing the data does not already exist the data 
            will be cached in a .csv file inside the current working directory. 
            Otherwise, the data will be read from the .csv file. The filename is 
            defined by self.file_name.

            Parameters
            ----------
            use_cache: bool, default True
                If True the dataset will be retrieved from a csv file if one
                exists, otherwise, it will be retrieved from the MySQL database. 
                If False the dataset will be retrieved from the MySQL database
                even if the csv file exists.

            cache_data: bool, default True
                If True the dataset will be cached in a csv file.

            Returns
            -------
            DataFrame: A Pandas DataFrame containing data from the source provided.
        '''

        # If the file is cached, read from the .csv file
        if os.path.exists(self.file_name) and use_cache:
            return pd.read_csv(self.file_name)
        
        # Otherwise read from the mysql database
        else:
            df = pd.read_sql(self.sql, get_db_url(self.database_name))

            # Cache the data in a .csv file, if that is what we want
            if cache_data:
                df.to_csv(self.file_name, index = False)

            return df

    ################################################################################

    def _pre_preparation(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
            Perform any necessary pre preparation transformations on the data 
            that either cannot be done in SQL or are simply easier with pandas. 
            This function must be overwritten in a child class otherwise it 
            does nothing.
        
            Parameters
            ----------
            df: DataFrame
                A pandas DataFrame acquired by the get_data function.
        
            Returns
            -------
            DataFrame: The acquired DataFrame with any defined transformations.
        '''

        return df
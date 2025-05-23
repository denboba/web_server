"""" This module contains the DataIngestor class with
  the functionality to ingest data from a csv file
 """
import logging

import pandas as pd


class DataIngestor:
    """ Data Ingestor class """

    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.df = None
        self.logger = logging.getLogger('webserver')

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily'
        ]

        self.questions_best_is_max = [
            'Percent of adults who achieve at least 150 minutes a week of \
             moderate-intensity aerobic physical '
            'activity or 75 minutes a week of vigorous-intensity aerobic \
            activity (or an equivalent combination)',
            'Percent of adults who achieve at least 150 minutes a week of\
             moderate-intensity aerobic physical '
            'activity or 75 minutes a week of vigorous-intensity aerobic\
             physical activity and engage in '
            'muscle-strengthening activities on 2 or more days a week',
            'Percent of adults who achieve at least 300 minutes a week of \
            moderate-intensity aerobic physical '
            'activity or 150 minutes a week of vigorous-intensity aerobic \
            activity (or an equivalent combination)',
            'Percent of adults who engage in muscle-strengthening \
            activities on 2 or more days a week',
        ]
        self.read_file()

    def read_file(self):
        """" a method to read the csv file safely"""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.logger.info("Read file %s", self.csv_path)
            return self.df
        except Exception as e:
            self.logger.error("Error reading file %s:%s", self.csv_path, str(e))
            raise

    def validate_question(self, question: str) -> bool:
        """"method to validate the question"""
        return question in self.questions_best_is_min or question in self.questions_best_is_max

    def states_mean(self, question: str, ):
        """"this method responsible for returning the states mean"""
        result = self.df[self.df['Question'] == question].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'], errors='coerce')
        average = result.groupby('LocationDesc')['Data_Value'].mean().dropna()
        sorted_states = average.sort_values().to_dict()
        return sorted_states

    def state_mean(self, question: str, state: str):
        """"this method responsible for returning the state mean"""
        result = self.df[(self.df['Question'] == question) &
                         (self.df['LocationDesc'] == state)].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'], errors='coerce')
        mean_value = result['Data_Value'].mean()
        return {state: mean_value} if mean_value is not None else {state: None}

    def best5(self, question: str):
        """"this method responsible for returning the best 5 states"""
        result = self.df[self.df['Question'] == question].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'], errors='coerce')
        average = result.groupby('LocationDesc')['Data_Value'].mean().dropna()
        if question in self.questions_best_is_min:
            return average.nsmallest(5).to_dict()
        return average.nlargest(5).to_dict()

    def worst5(self, question: str):
        """"this method responsible for returning the worst 5 states"""
        result = self.df[self.df['Question'] == question].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'], errors='coerce')
        average = result.groupby('LocationDesc')['Data_Value'].mean().dropna()
        if question in self.questions_best_is_min:
            return average.nlargest(5).to_dict()
        return average.nsmallest(5).to_dict()

    def global_mean(self, question: str):
        """"this method responsible for returning the global mean"""
        result = self.df[self.df['Question'] == question].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'], errors='coerce')

        global_mean_value = result['Data_Value'].mean()
        return {"global_mean": global_mean_value}

    def diff_from_mean(self, question: str):
        """""this method responsible for returning the diff from mean"""
        result = self.df[self.df['Question'] == question].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'], errors='coerce')
        state_means = result.groupby('LocationDesc')['Data_Value'].mean().dropna()
        global_mean_value = result['Data_Value'].mean()

        diff_dict = (global_mean_value - state_means).sort_values().to_dict()
        return diff_dict

    def state_diff_from_mean(self, question: str, state: str):
        """"this method responsible for returning the state diff from mean"""
        return {state: (self.global_mean(question)["global_mean"] -
                        self.state_mean(question, state)[state])}

    def mean_by_category(self, question: str):
        """"this method responsible for returning the mean by category"""
        result = self.df[self.df['Question'] == question].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'],
                                                    errors='coerce')

        mean_values = result.groupby(['LocationDesc', 'StratificationCategory1',
                                      'Stratification1'])[
            'Data_Value'].mean().reset_index()
        mean_by_category_dict = {}

        for _, row in mean_values.iterrows():
            state = row['LocationDesc']
            category = row['StratificationCategory1']
            stratification = row['Stratification1']
            mean_value = row['Data_Value']
            key = f"('{state}', '{category}', '{stratification}')"
            mean_by_category_dict[key] = mean_value

        return mean_by_category_dict

    def state_mean_by_category(self, question: str, state: str):
        """""this method responsible for returning the state mean by category"""
        result = self.df[(self.df['Question'] == question) &
                         (self.df['LocationDesc'] == state)].copy()
        result.loc[:, 'Data_Value'] = pd.to_numeric(result['Data_Value'],
                                                    errors='coerce')
        # Group by category and stratification, then calculate the mean
        mean_values = result.groupby(['StratificationCategory1',
                                      'Stratification1'])['Data_Value'].mean().reset_index()
        state_dict = {}
        # Create a dictionary with the key as a tuple of category and stratification
        for _, row in mean_values.iterrows():
            category = row['StratificationCategory1']
            stratification = row['Stratification1']

            mean_value = row['Data_Value']
            key = f"('{category}', '{stratification}')"
            state_dict[key] = mean_value

        return {state: state_dict}

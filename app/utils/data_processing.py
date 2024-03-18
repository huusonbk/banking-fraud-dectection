import sys
import pandas as pd
from fastapi.encoders import jsonable_encoder
import joblib
import inflection
import pandas as pd

sys.path.append("..")
from schema import TransactionInfo


def format_input_data(data: TransactionInfo):
    """Format the input data to a prediction data structure

    Args:
        data (HouseInfo): Information about a house

    Returns:
        A Pandas DataFrame: Convert the input data into a Pandas DataFrame
    """
    return pd.DataFrame(jsonable_encoder(data), index=[0])


class Fraud:
    
    def __init__(self, min_max_scaler_path, one_hot_encoder_path):
        self.minmaxscaler = joblib.load(min_max_scaler_path)
        self.onehotencoder = joblib.load(one_hot_encoder_path)
        
    def data_cleaning(self, df1):
        cols_old = df1.columns.tolist()
        snakecase = lambda i: inflection.underscore(i)
        cols_new = list(map(snakecase, cols_old))
        df1.columns = cols_new
        return df1
    
    def feature_engineering(self, df2):
        # step
        df2['step_days'] = df2['step'].apply(lambda i: i/24)
        df2['step_weeks'] = df2['step'].apply(lambda i: i/(24*7))

        # difference between initial balance before the transaction and new balance after the transaction
        df2['diff_new_old_balance'] = df2['newbalance_orig'] - df2['oldbalance_org']

        # difference between initial balance recipient before the transaction and new balance recipient after the transaction.
        df2['diff_new_old_destiny'] = df2['newbalance_dest'] - df2['oldbalance_dest']

        # name orig and name dest
        df2['name_orig'] = df2['name_orig'].apply(lambda i: i[0])
        df2['name_dest'] = df2['name_dest'].apply(lambda i: i[0])
        return df2.drop(columns=['name_orig', 'name_dest', 'step_weeks', 'step_days'], axis=1)
    
    def data_preparation(self, df3):
        # Rescaling 
        num_columns = ['amount', 'oldbalance_org', 'newbalance_orig', 'oldbalance_dest', 
                       'newbalance_dest', 'diff_new_old_balance', 'diff_new_old_destiny']
        
        df3[num_columns] = self.minmaxscaler.transform(df3[num_columns])

        # OneHotEncoder
        df3 = self.onehotencoder.transform(df3)
        # selected columns
        final_columns_selected = ['step', 'oldbalance_org', 
                          'newbalance_orig', 'newbalance_dest', 
                          'diff_new_old_balance', 'diff_new_old_destiny', 
                          'type_CASH_IN', 'type_CASH_OUT', 'type_TRANSFER', 'type_PAYMENT']
        return df3[final_columns_selected]
    
    def get_prediction(self, model, original_data, test_data):
        pred = model.predict(test_data)
        original_data['prediction'] = pred
        return int(pred)
import numpy as np
import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.preprocessing import StandardScaler,OneHotEncoder,OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from dataclasses import dataclass
from sklearn.impute import SimpleImputer
from src.utils import save_object

@dataclass
class DataTranformationConfig:
    """
    This class only stores configuration values.

    Why we use @dataclass:
    - automatically creates __init__
    - keeps config clean
    - used heavily in production pipelines

    This path tells where the trained preprocessing
    object will be saved on disk.
    """
    preprocessor_obj_file_path: str=os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    """
    This class handles:

    1. Identifying column types automatically
    2. Building preprocessing pipelines
    3. Transforming train/test data
    4. Saving the fitted preprocessing object
    """
    def __init__(self):
        self.data_transformation_config=DataTranformationConfig()
    
    def get_data_transformation_object(self, df, target_columns):
        
        """
        Builds and returns a ColumnTransformer that:

        - Detects numerical & categorical columns automatically
        - Splits categorical columns into:
            * binary
            * ordinal
            * normal multi-category
        - Applies proper encoders to each group
        """
        try:
            # ==================================================
            # 1️⃣ Automatically detect column types
            # ==================================================

            logging.info("detecting column types")
            # Numeric columns = int or float
            numerical_columns=df.select_dtypes(include=["int64","float64"]).columns.tolist()

            # Categorical columns = object or category
            categorical_columns=df.select_dtypes(include=["object","category"]).columns.tolist()

            # Remove target columns from categorical columns
            categorical_columns=[col for col in categorical_columns if col not in target_columns]
            numerical_columns=[col for col in numerical_columns if col not in target_columns]

            logging.info(f"Detected numerical columns: {numerical_columns}")
            logging.info(f"Detected categorical columns: {categorical_columns}")

            # ==================================================
            # 2️⃣ Categorize categorical columns further
            # =================================================
            binary_cols=[]
            ordinal_cols=[]
            multi_cat_cols=[]

            #Simple heuristic:
            # If only 2 unique values -> binary
            # If <= 5 unique values -> ordinal-like
            # else -> general categorical

            for col in categorical_columns:
                unique_values=df[col].nunique()

                if unique_values==2:
                    binary_cols.append(col)
                
                elif unique_values<=5:
                    ordinal_cols.append(col)

                else:
                    multi_cat_cols.append(col)

            logging.info(f"Binary categorical columns: {binary_cols}")
            logging.info(f"Ordinal categorical columns: {ordinal_cols}")
            logging.info(f"Multi-category columns: {multi_cat_cols}")   

            # ==================================================
            # 3️⃣ NUMERICAL PIPELINE
            # ==================================================
            # For numbers:
            # - fill missing values with median
            # - scale to mean=0, std=1

            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )

              # ==================================================
            # 4️⃣ BINARY CATEGORICAL PIPELINE
            # ==================================================
            # gender, yes/no columns etc.
            # - fill missing with most frequent
            # - one-hot encode (drops one column if binary)

            binary_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder",OneHotEncoder(drop="if_binary"))
                ]
            )

            # ==================================================
            # 5️⃣ ORDINAL PIPELINE
            # ==================================================
            # Education levels etc.
            # Encoded as 0,1,2,...
            ordinal_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("ordinal",OrdinalEncoder())
                ]
            )

            # ==================================================
            # 6️⃣ MULTI-CATEGORY PIPELINE
            # ==================================================
            # Columns with many categories:
            # - impute
            # - one-hot encode
            # - ignore unseen categories at test time
            multi_cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot",OneHotEncoder(handle_unknown="ignore"))
                ]
            )

            # ==================================================
            # 7️⃣ ColumnTransformer
            # ==================================================
            # Applies different pipelines to different columns
            # and concatenates all outputs
            preprocessor=ColumnTransformer(
                transformers=[
                    ("num_pipeline",num_pipeline,numerical_columns),
                    ("binary_pipeline",binary_pipeline,binary_cols),
                    ("ordinal_pipeline",ordinal_pipeline,ordinal_cols),
                    ("multi_cat_pipeline",multi_cat_pipeline,multi_cat_cols)
               ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    
    # ------------------------------------------------------
    # Run transformation on train & test
    # ------------------------------------------------------
    def initiate_data_transformation(self,train_path,test_path):
        """
        Reads train/test CSV files, fits preprocessing
        pipeline on train data, transforms both sets,
        saves preprocessing object, and returns arrays.
        """
        try:
            # ==================================================
            # 1️⃣ Load CSV files
            # ==================================================
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Train and test data loaded successfully.")
            
            # ==================================================
            # ==================================================
            # 2️⃣ Define target columns (SINGLE-OUTPUT example)
            
            target_column=["math_score"]

            # ==================================================
            # 3️⃣ Create preprocessing object
            # ==================================================
            preprocessor=self.get_data_transformation_object(df=train_df,target_columns=target_column)
            logging.info("Preprocessing object created.")

            # ==================================================
            # 4️⃣ Separate input features and targets
            # ==================================================

            X_train_df=train_df.drop(columns=target_column)
            y_train_df=train_df[target_column]

            X_test_df=test_df.drop(columns=target_column)
            y_test_df=test_df[target_column]

            
            logging.info("Separated features and targets.")

            # ==================================================
            # 5️⃣ Fit on training data only
            # ==================================================

            X_train_processed=preprocessor.fit_transform(X_train_df)

            # Only transform test data (NO FIT!)
            X_test_processed=preprocessor.transform(X_test_df)

            '''preprocessing_obj is a ColumnTransformer.

                    Inside it are Pipelines that use:

                    • SimpleImputer
                    • StandardScaler
                    • OneHotEncoder

                    All of these are sklearn transformers.
                    ✅ sklearn transformers output:
                    By default, they return:
                    👉 NumPy arrays
                    or
                    👉 SciPy sparse matrices (if OneHotEncoder is used)
                    They do NOT return pandas DataFrames unless you explicitly enable it.'''

            # ==================================================
            # 6️⃣ Combine X_train_processed and X_test_processed  numpy arrays
            # ==================================================
            # np.c_ concatenates column-wise

            train_arr=np.c_[X_train_processed,np.array(y_train_df)]
            test_arr=np.c_[X_test_processed,np.array(y_test_df)]


            # ==================================================
            # 7️⃣ Save preprocessing object to disk
            # ==================================================

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor
            )
            logging.info("Preprocessing object saved successfully.")

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)
        
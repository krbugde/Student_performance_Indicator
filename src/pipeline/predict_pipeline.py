import sys
import os
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

class PredictPipeline:
    def __init__(self):
        pass  

    def predict(self,features):
        try:
            model_path=os.path.join("artifacts","model.pkl")
            preprocessor_path=os.path.join("artifacts","preprocessor.pkl")

            model=load_object(file_path=model_path)
            preprocessor=load_object(file_path=preprocessor_path)
            
            # Debug: Print the input dataframe to see what we're getting
            logging.info(f"Input features DataFrame:\n{features}")
            logging.info(f"Data types:\n{features.dtypes}")
            logging.info(f"Null values:\n{features.isnull().sum()}")

            data_scaled=preprocessor.transform(features)
            predicted_data=model.predict(data_scaled)

            return predicted_data
        
        except Exception as e:
            raise CustomException(e,sys)


class CustomData:
    def __init__(self,gender:str,race_ethnicity:str,parental_level_of_education:str,lunch:str,test_preparation_course:str,reading_score:int,writing_score:int):
        self.gender=gender  
        self.race_ethnicity=race_ethnicity
        self.parental_level_of_education=parental_level_of_education
        self.lunch=lunch
        self.test_preparation_course=test_preparation_course
        self.reading_score=int(reading_score) 
        self.writing_score=int(writing_score)

    ## below function returns data in form of data frame ,so to be used in prediction
    def get_data_as_dataFrame(self):

        try:
            # IMPORTANT: Column order must match training data (excluding target column)
            # Training columns (excluding math_score): gender, race_ethnicity, parental_level_of_education, 
            # lunch, test_preparation_course, reading_score, writing_score
            custom_data_input={
                "gender":[self.gender],
                "race_ethnicity":[self.race_ethnicity],
                "parental_level_of_education":[self.parental_level_of_education],
                "lunch":[self.lunch],
                "test_preparation_course":[self.test_preparation_course],
                "reading_score":[self.reading_score],
                "writing_score":[self.writing_score]
            }

            return pd.DataFrame(custom_data_input)
        
        except Exception as e:
            raise CustomException(e,sys)
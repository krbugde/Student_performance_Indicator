import pandas as pd
import numpy as np
import os
import sys
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
from src.exception import CustomException
from src.logger import logging
import dill

def save_object(file_path,obj):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)

        with open(file_path,"wb")as file_obj:
            dill.dump(obj,file_obj)
    
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    """
    Trains multiple models, performs hyperparameter tuning using GridSearchCV,
    evaluates them on test data, and returns a dictionary mapping:
    
    model_name -> {"score": test_R2_score, "model": trained_model_object}
    
    Parameters:
        X_train, y_train : np.array : Training data
        X_test, y_test   : np.array : Test data
        models           : dict : {model_name: model_object}
        param            : dict : {model_name: hyperparameter_grid}
    
    Returns:
        dict : {model_name: {"score": test_R2_score, "model": trained_model_object}}
    """

    try:
        report={}

        for model_name,model in models.items():
            logging.info(f"Training and tuning model: {model_name}")

            # Hyperparameter tuning using GridSearchCV
            grid=GridSearchCV(
                estimator=model,
                param_grid=param[model_name],
                cv=3,
                n_jobs=-1,
                verbose=0
            )

            grid.fit(X_train,y_train)

            # Best trained estimator from GridSearch along with its best selected hyperparameters
            best_model=grid.best_estimator_

            # Predict on test data
            y_test_pred=best_model.predict(X_test)

            # Compute R² score on test set
            test_score=r2_score(y_test,y_test_pred)

            # Save both score and trained model object

            report[model_name]={"score":test_score,"model":best_model}

            logging.info(f"{model_name} | Test R2 Score: {test_score}")
        
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(file_path):
        try:
            with open(file_path, 'rb') as file_obj:
                return dill.load(file_obj)
            
        except Exception as e:
            raise CustomException(e,sys)




            






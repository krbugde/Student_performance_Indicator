import os
import sys
from dataclasses import dataclass
from sklearn.metrics import r2_score

## Regressors
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor

# Project utilities
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models

@dataclass
class ModelTrainerConfig:
    """
    Configuration for ModelTrainer.
    Contains path to save trained model.
    """
    trained_model_file_path=os.path.join("artifacts","model.pkl")

class ModelTrainer:
    """
    Trains multiple regression models, selects the best based on R2 score,
    and saves the best hyperparameter-tuned model.
    """

    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        """
        Trains, tunes, evaluates, selects, and saves the best model.

        Parameters:
            train_array : np.array : Training data (features + target)
            test_array  : np.array : Test data (features + target)

        Returns:
            float : R2 score of the best model on test data
        """
        
        try:
            logging.info("Splitting training and test data into X and y")
            # Split arrays into features (X) and target (y)

            X_train,y_train=train_array[:,:-1],train_array[:,-1]
            X_test,y_test=test_array[:,:-1],test_array[:,-1]

            # Define models
            models={
                 "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "AdaBoost Regressor": AdaBoostRegressor()  
            }

            # Hyperparameter grids

            params = {
                "Decision Tree": {'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson']},
                "Random Forest": {'n_estimators': [8, 16, 32, 64, 128, 256]},
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {'learning_rate': [0.1, 0.01, 0.05, 0.001],
                                 'n_estimators': [8, 16, 32, 64, 128, 256]},
                "AdaBoost Regressor": {'learning_rate': [0.1, 0.01, 0.5, 0.001],
                                       'n_estimators': [8, 16, 32, 64, 128, 256]}
            }

            logging.info("Evaluating models to find the best one")

            # Evaluate models (returns dict with both score & trained model)

            model_report : dict=evaluate_models(X_train,y_train,X_test,y_test,models,params)

            # Select best model based on highest test R2 score
            best_model_name=max(model_report,key=lambda x:model_report[x]['score'])
            best_model_score=model_report[best_model_name]['score']
            best_model=model_report[best_model_name]['model']  # this is hyperparameter-tuned

            logging.info(f"Best model: {best_model_name} | R2 Score: {best_model_score}")

            # Check threshold for usability
            if best_model_score<0.6:
                 raise CustomException("No suitable model found")
            
            # Save the best model to file
            save_object(
                 file_path=self.model_trainer_config.trained_model_file_path,
                 obj=best_model
            )

            # Predict test data for final confirmation
            y_test_pred=best_model.predict(X_test)
            score=r2_score(y_test,y_test_pred) 
            logging.info(f"Best model R2 on test data: {score}")

            logging.info(f"Saved best model at: {self.model_trainer_config.trained_model_file_path}")

            return best_model_score
    
        except Exception as e:
            logging.error("Error occurred in ModelTrainer")
            raise CustomException(e, sys)



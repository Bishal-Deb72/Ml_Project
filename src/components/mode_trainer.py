import os
import sys
from dataclasses import dataclass
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingRegressor,
    RandomForestRegressor,
    AdaBoostRegressor
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object,evaluate_models



@dataclass
class ModelTrainerConfig:
    train_model_file_path = os.path.join("artifacts","model.pkl")

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()

    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("spliting training and test input data")
            X_train, y_train,X_test,y_test=(
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1],
            )

            models={
                "Random Forest":RandomForestRegressor(),
                "Gradient Boosting":GradientBoostingRegressor(),
                "Decision Tree":DecisionTreeRegressor(),
                "K-Neighbours Classifier":KNeighborsRegressor(),
                "XGBclassifier":XGBRegressor(),
                "CatBoosting classifier":CatBoostRegressor(verbose=False),
                "AdaBoost classifier":AdaBoostRegressor(),
            }

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models
            )

            ## to get the best model score
            best_model_score = max(model_report.values())

            ## to get best model score from dict
            best_model_name = [name for name, score in model_report.items() if score == best_model_score][0]

            best_model = models[best_model_name]

            if best_model_score<0.6:
                raise CustomException("No best model found")

            logging.info(f"Best found model on both training and testing dataset")

            save_object(
                file_path = self.model_trainer_config.train_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test,predicted)

            return r2_square
        except Exception as e:
            raise CustomException(e,sys)

        

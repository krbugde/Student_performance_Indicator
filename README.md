# Student Performance Prediction System

An end-to-end machine learning project that predicts student math scores based on demographic and academic factors using 6 ML algorithms with hyperparameter tuning and software engineering best practices.

## 🎯 Project Overview

This project implements a complete ML pipeline to predict student performance in mathematics using features like gender, ethnicity, parental education, lunch type, test preparation course, reading scores, and writing scores. The system demonstrates proficiency in data engineering, model development, and production deployment.

## 🏗️ Architecture

```
ML_PROJECT/
├── src/
│   ├── components/          # Data processing modules
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── pipeline/           # Prediction pipeline
│   ├── exception.py        # Custom exception handling
│   ├── logger.py          # Logging configuration
│   └── utils.py           # Utility functions
├── app.py                 # Flask web application
├── templates/             # HTML templates
├── artifacts/             # Trained models & processed data
├── notebook/              # Data exploration & experiments
└── requirements.txt       # Dependencies
```

## 🛠️ Technology Stack

- **Backend**: Flask (Web Framework)
- **Machine Learning**: Scikit-learn, XGBoost
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn
- **Serialization**: Pickle
- **Package Management**: setuptools, pip

## 📊 Dataset

The project uses student performance data with the following features:
- **Categorical**: gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course
- **Numerical**: reading_score, writing_score
- **Target**: math_score

## 🚀 Key Features

### Data Engineering
- Automated data ingestion with train/test split
- Robust data transformation pipeline
- Feature engineering for categorical variables
- Data validation and preprocessing

### Model Development
- **6 ML algorithms trained and compared:**
  - Linear Regression
  - Decision Tree Regressor
  - Random Forest Regressor
  - Gradient Boosting Regressor
  - XGBoost Regressor
  - AdaBoost Regressor
- GridSearchCV hyperparameter tuning for each model
- Auto-selection of best model based on R² score (threshold: 0.6)
- Persistent model storage using Pickle

### Production Deployment
- RESTful API using Flask
- Real-time prediction endpoint
- Web interface for user interaction
- Comprehensive error handling and logging

## 📈 ML Pipeline

1. **Data Ingestion**: Load and split dataset into train/test sets
2. **Data Transformation**: Encode categorical variables, scale features
3. **Model Training**: Train all 6 algorithms with hyperparameter tuning, auto-select best performer
4. **Model Persistence**: Save best trained model and preprocessing pipeline
5. **Prediction**: Load model and make real-time predictions via web API

## 🔧 Hyperparameter Tuning

Each model is tuned using GridSearchCV with the following grids:

| Model | Parameters Tuned |
|-------|-----------------|
| Decision Tree | criterion |
| Random Forest | n_estimators |
| Gradient Boosting | learning_rate, subsample, n_estimators |
| XGBoost | learning_rate, n_estimators |
| AdaBoost | learning_rate, n_estimators |
| Linear Regression | — (no tuning needed) |

## 🎯 Core Skills Demonstrated

- **Machine Learning**: Supervised learning, regression analysis, multi-model evaluation, hyperparameter optimization
- **Software Engineering**: Modular architecture, OOP design patterns, exception handling
- **Data Engineering**: ETL pipelines, data preprocessing, feature engineering
- **DevOps**: Package management, environment setup, logging systems
- **Web Development**: REST API design, Flask framework, frontend integration

## 🚀 Quick Start

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd ML_PROJECT
   pip install -r requirements.txt
   ```

2. **Train Models**
   ```bash
   python src/pipeline/training_pipeline.py
   ```

3. **Run Web Application**
   ```bash
   python app.py
   ```
   Access at: `http://localhost:8000`

## 📝 API Endpoints

- `GET /` - Home page
- `GET /predictdata` - Prediction form
- `POST /predictdata` - Submit data for prediction

## 🏆 Project Highlights

- **Production-Ready**: Complete ML pipeline from data to deployment
- **Multi-Model Comparison**: 6 algorithms evaluated with hyperparameter tuning
- **Auto Model Selection**: Best model chosen automatically based on R² threshold
- **Scalable Architecture**: Modular design for easy maintenance and extension
- **Best Practices**: Logging, exception handling, configuration management
- **User Interface**: Interactive web application for real-time predictions

## 📊 Model Performance

The system evaluates all 6 ML algorithms and selects the best performing model based on:
- R² Score (primary selection metric, minimum threshold: 0.6)
- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)

## 🔧 Technical Implementation

- **Custom Exception Handling**: Robust error management throughout the pipeline
- **Logging System**: Comprehensive logging for debugging and monitoring
- **Configuration Management**: Dataclass-based configuration for maintainability
- **Package Structure**: Professional Python package setup for distribution
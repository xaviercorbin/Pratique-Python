import numpy as np
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import threading
from sklearn.model_selection import cross_val_score


MAX_ITERATIONS = 100
TARGET_ACCURACY = 1
stop_training = False

def monitor_stop_command():
    global stop_training
    while True:
        command = input("Enter 'stop' to halt training: ").strip().lower()
        if command == 'stop':
            stop_training = True
            break

def train_until_target_accuracy(data: pd.DataFrame) -> RandomForestClassifier:
    iteration = 0
    best_accuracy = 0

    while iteration < MAX_ITERATIONS and best_accuracy < TARGET_ACCURACY and not stop_training:
        classifier = train_random_forest(data)
        features = ['5_Day_Mean_Volume', '5_Day_Mean_Close', '5_Day_STD_Close']
        X = data[features]
        y = data['Target']
        _, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=iteration)
        
        y_pred = classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy for Iteration {iteration}: {accuracy:.4f}")


        if accuracy > best_accuracy:
            best_accuracy = accuracy
            # Save the best model
            joblib.dump(classifier, 'best_model.pkl')

        iteration += 1
        print(f"Iteration: {iteration}, Best Accuracy: {best_accuracy:.4f}")

    return joblib.load('best_model.pkl')  # Return the best model

def fetch_data(ticker: str) -> pd.DataFrame:
    return yf.download(ticker, start='2000-01-01', end='2023-09-16')

def create_features(data: pd.DataFrame) -> pd.DataFrame:
    # Price Features
    data['1_Day_Price_Change'] = data['Close'].pct_change()
    data['5_Day_Mean_Close'] = data['Close'].rolling(window=5).mean()
    data['5_Day_STD_Close'] = data['Close'].rolling(window=5).std()
    
    # Volume Features
    data['5_Day_Mean_Volume'] = data['Volume'].rolling(window=5).mean()
    
    # Target Variable
    data['Target'] = data['1_Day_Price_Change'].shift(-1)
    data['Target'] = np.where(data['Target'] > 0, 1, 0)  # 1 if price increased, 0 otherwise
    
    # Drop NA values
    data.dropna(inplace=True)
    
    return data

def train_random_forest(data: pd.DataFrame) -> RandomForestClassifier:
    features = ['5_Day_Mean_Volume', '5_Day_Mean_Close', '5_Day_STD_Close']
    X = data[features]
    y = data['Target']
    
    # Initialize the model
    classifier = RandomForestClassifier(n_estimators=100, random_state=0)
    
    # Evaluate with cross-validation
    accuracies = cross_val_score(classifier, X, y, cv=5, scoring='accuracy')  # 5-fold CV
    avg_accuracy = np.mean(accuracies)
    std_accuracy = np.std(accuracies)

    print(f"Cross-Validation Accuracy: {avg_accuracy:.4f} ± {std_accuracy:.4f}")

    # Train the model on the entire dataset for future predictions
    classifier.fit(X, y)
    
    return classifier


def predict_price_movement(classifier: RandomForestClassifier, data: pd.DataFrame) -> np.ndarray:
    features = ['5_Day_Mean_Volume', '5_Day_Mean_Close', '5_Day_STD_Close']
    X = data[features]
    return classifier.predict(X)

if __name__ == "__main__":
    monitor_thread = threading.Thread(target=monitor_stop_command)
    monitor_thread.start()
    
    data = fetch_data('TSLA')
    data = create_features(data)
    classifier = train_until_target_accuracy(data)
    predictions = predict_price_movement(classifier, data)
    print("Predictions:", predictions)

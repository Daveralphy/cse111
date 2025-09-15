import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
import requests
import io

# --- Auxiliary Functions ---

def plot_confusion_matrix(y_true, y_predict, model_name):
    """This function plots the confusion matrix for a given model."""
    cm = confusion_matrix(y_true, y_predict)
    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, fmt='g')  # annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title(f'Confusion Matrix for {model_name}')
    ax.xaxis.set_ticklabels(['did not land', 'landed'])
    ax.yaxis.set_ticklabels(['did not land', 'landed'])
    # Save the plot instead of showing it directly
    plt.savefig(f'confusion_matrix_{model_name.replace(" ", "_").lower()}.png')
    plt.close() # Close the plot to free up memory

def load_data():
    """Loads the datasets from the URLs."""
    print("Fetching data...")
    try:
        # URL for the main dataset with the 'Class' column
        URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"
        resp1 = requests.get(URL1)
        resp1.raise_for_status() # Raise an exception for bad status codes
        data = pd.read_csv(io.BytesIO(resp1.content))

        # URL for the feature-engineered dataset
        URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'
        resp2 = requests.get(URL2)
        resp2.raise_for_status()
        X = pd.read_csv(io.BytesIO(resp2.content))
        
        print("Data loaded successfully.")
        return data, X
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None

def run_model_training(model, parameters, X_train, y_train):
    """
    Performs GridSearchCV to find the best model.

    Args:
        model: The scikit-learn model object.
        parameters (dict): The hyperparameter grid to search.
        X_train: Training features.
        y_train: Training labels.

    Returns:
        A trained GridSearchCV object.
    """
    grid_search = GridSearchCV(model, parameters, cv=10, n_jobs=-1) # Use all available CPU cores
    grid_search.fit(X_train, y_train)
    return grid_search


# --- Main Execution Block ---

def main():
    """Main function to run the machine learning pipeline."""
    data, X = load_data()
    if data is None or X is None:
        return # Exit if data loading failed

    # TASK 1: Create a NumPy array for the target variable Y
    Y = data['Class'].to_numpy()

    # TASK 2: Standardize the feature data in X
    transform = preprocessing.StandardScaler()
    X = transform.fit_transform(X)

    # TASK 3: Split data into training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)
    print(f"Data split into {len(X_train)} training samples and {len(X_test)} test samples.")

    # --- Model Definitions ---
    models = {
        "Logistic Regression": {
            "model": LogisticRegression(),
            "params": {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
        },
        "Support Vector Machine": {
            "model": SVC(),
            "params": {'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
                       'C': np.logspace(-3, 3, 5),
                       'gamma': np.logspace(-3, 3, 5)}
        },
        "Decision Tree": {
            "model": DecisionTreeClassifier(random_state=42),
            "params": {'criterion': ['gini', 'entropy'],
                       'max_depth': [2*n for n in range(1, 10)],
                       'min_samples_split': [2, 5, 10]}
        },
        "K-Nearest Neighbors": {
            "model": KNeighborsClassifier(),
            "params": {'n_neighbors': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
                       'p': [1, 2]}
        }
    }

    results = []

    # --- Training and Evaluation Loop ---
    for name, config in models.items():
        print(f"\n--- Training {name} ---")
        
        # TASKS 4, 6, 8, 10: Create and fit GridSearchCV object
        cv_model = run_model_training(config["model"], config["params"], X_train, Y_train)
        
        print(f"Best Parameters: {cv_model.best_params_}")
        print(f"Best Cross-Validation Score: {cv_model.best_score_:.4f}")

        # TASKS 5, 7, 9, 11: Calculate accuracy on the test data
        test_accuracy = cv_model.score(X_test, Y_test)
        print(f"Accuracy on Test Data: {test_accuracy:.4f}")

        # Plot and save confusion matrix
        yhat = cv_model.predict(X_test)
        plot_confusion_matrix(Y_test, yhat, name)
        print(f"Confusion matrix saved to 'confusion_matrix_{name.replace(' ', '_').lower()}.png'")

        results.append({
            "Model": name,
            "Best CV Score": cv_model.best_score_,
            "Test Accuracy": test_accuracy
        })

    # TASK 12: Find the method that performs best
    print("\n--- Model Comparison ---")
    results_df = pd.DataFrame(results).sort_values(by="Test Accuracy", ascending=False)
    results_df = results_df.set_index("Model")
    
    print(results_df)

    best_model = results_df.index[0]
    best_accuracy = results_df.iloc[0]["Test Accuracy"]
    
    print(f"\n🏆 The best performing model is '{best_model}' with a test accuracy of {best_accuracy:.4f}.")

if __name__ == "__main__":
    main()

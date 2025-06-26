import kagglehub
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
# from lazypredict.Supervised import LazyClassifier
import pickle

path = kagglehub.dataset_download("rakeshkapilavai/extrovert-vs-introvert-behavior-data")
print("Path to dataset files:", path)
# Display the first few rows of the dataset

df = pd.read_csv(path+ "/personality_dataset.csv")
#know the ratio of missing values
# print("Missing values in each column:\n", df.isnull().sum())
df = df.dropna()

# Extrovert to 0 introvert to 1
df['Personality'] = df['Personality'].map({'Extrovert': 0, 'Introvert': 1})
df['Stage_fear'] = df['Stage_fear'].map({'Yes': 1, 'No': 0})
df['Drained_after_socializing'] = df['Drained_after_socializing'].map({'Yes': 1, 'No': 0})
x = df.drop(columns=['Personality'])
y = df['Personality']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scalar = StandardScaler()
x_train = scalar.fit_transform(x_train)
x_test = scalar.transform(x_test)

# lazyClassifier is used to compare different models and find the best one
# clf = LazyClassifier(verbose=0,ignore_warnings=True, custom_metric=None)
# models, predictions = clf.fit(x_train, x_test, y_train, y_test)
# print(models) # Show that SVC is one of the best model based on accuracy, F1 score and time taken

# gridsearchcv is used to find the best hyperparameters for the model
# cv is used to split the data into k folds for cross validation
# verbose is used to print the progress of the model
# n_jobs is used to run the model in parallel (-1 means use all processors)
params = {
    "C": [0.1, 1, 10],
    "gamma": [0.01, 0.1, 1],
    "kernel": ["rbf"]  # Focus on one kernel type
}
model = RandomizedSearchCV(SVC(probability=True),
                          param_distributions=params,
                          n_iter=5, cv=3, verbose=1,
                          n_jobs=-1, random_state=42)
model.fit(x_train, y_train)
y_predict = model.predict(x_test)
print(model.best_params_)
print(model.best_score_)

predicted_prob = model.predict_proba(x_test)
print("Accuracy: ", accuracy_score(y_test, y_predict))
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_predict, average='binary')
print("Precision: ", precision)
print("Recall: ", recall)   
print("F1 Score: ", f1)

#pickle is used to save the model to a file
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

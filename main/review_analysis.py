import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "reviews_with_features.csv")
df = pd.read_csv(file_path)

# Convert all labels in 'category' column to lowercase and strip spaces for standardisation
df.loc[:, 'Review_Classification'] = df['Review_Classification'].str.lower().str.strip()

# selecting the label column, i.e. what is being predicted
label_col = 'Review_Classification'

# selecting which columns to drop, and which column that is the target variable
X = df.drop(columns=['business_name', 
                        'author_name', 
                        'text', 
                        'photo', 
                        'rating_category', 
                        label_col, 
                        'Review_Classification_reason'
                    ])
y = df[label_col]

# split the data into training and test sets
# 20% is for testing, 80% for training
# stratify=y ensures proportion of each class in train and test sets is similar to the full dataset
# random_state=42 ensures that the split is reproducible
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Random forest is an ensemble of decision trees that votes for the most likely class
model = RandomForestClassifier(
    n_estimators=200,        # more trees usually help with larger features
    random_state=42,
    class_weight='balanced', # handle label imbalance
    n_jobs=-1                # use all cores
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Precision: out of all predicted reviews of a certain category, how many were correct
# Recall: out of reviews that were actually in a category, how many were correctly predicted
# F1-score: balance precision and recall
print(classification_report(y_test, y_pred))
#This is a Bayes algorithm for AI Final Exam
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# READ
train_data_path = 'Ex2_train.csv'
test_data_path = 'Ex2_test.csv'

#train_data_path = '/Users/devonmcdermott/Downloads/Final_Exam_Data/Ex2_train.csv'
#test_data_path = '/Users/devonmcdermott/Downloads/Final_Exam_Data/Ex2_test.csv'


training_data = pd.read_csv(train_data_path, header=None)
testing_data = pd.read_csv(test_data_path, header=None)
features_train = training_data.iloc[:, :-1].to_numpy()  
labels_train = training_data.iloc[:, -1].to_numpy()   
features_test = testing_data.iloc[:, :-1].to_numpy()
labels_test = testing_data.iloc[:, -1].to_numpy()

# Min-Max Scaling 
def apply_min_max_scaling(data, feature_range=(0, 1)):
    # Calculate min max
    min_values = np.min(data, axis=0)
    max_values = np.max(data, axis=0)
    
    #Min-Max Scaling
    scaled_data = (data - min_values) / (max_values - min_values) * (feature_range[1] - feature_range[0]) + feature_range[0]
    return scaled_data

# Apply Min-Max Scaling 
features_train_normalized = apply_min_max_scaling(features_train)
features_test_normalized = apply_min_max_scaling(features_test)

# plot density probability distributions
def plot_density_distribution(feature_data, class_labels, feature_index):
    
    # Create a box plot to visualize 
    plt.figure()
    
    data_to_plot = [feature_data[class_labels == class_label] for class_label in np.unique(class_labels)]
    plt.boxplot(data_to_plot, labels=np.unique(class_labels), sym='k+')
    
    plt.title(f'Density Probability Distributions')
    plt.legend()
    plt.show()

# Iterate features and classes to plot
for feature_index in range(features_train_normalized.shape[1]):
    plot_density_distribution(features_train_normalized[:, feature_index], labels_train, feature_index)

# Naive Bayes Classifier
class_probabilities = {}

# Calculate statistics for each class
for class_label in np.unique(labels_train):
    class_data_normalized = features_train_normalized[labels_train == class_label]
    class_probabilities[class_label] = {
        'prior_probability': len(class_data_normalized) / len(features_train_normalized),
        'mean': np.mean(class_data_normalized, axis=0),
        'standard_deviation': np.std(class_data_normalized, axis=0),
    }

# predict
predictions = []

for sample_normalized in features_test_normalized:
    class_likelihoods = {}

    # Calculate likelihood 
    for class_label, class_info in class_probabilities.items():
        prior_probability = class_info['prior_probability']
        likelihood = np.prod(
            (1 / (np.sqrt(2 * np.pi) * class_info['standard_deviation'])) *
            np.exp(-(sample_normalized - class_info['mean'])**2 / (2 * class_info['standard_deviation']**2))
        )
        class_likelihoods[class_label] = prior_probability * likelihood

    # Predict the class with the highest 
    predicted_class = max(class_likelihoods, key=class_likelihoods.get)
    predictions.append(predicted_class)

# Calculate 
accuracy = np.sum(predictions == labels_test) / len(labels_test)


print(f'Accuracy%: {accuracy:.2%}')

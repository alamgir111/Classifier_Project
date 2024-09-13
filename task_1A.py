import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv('Synthetic_2_classifiers.csv')

# Create conditions for classification
both_correct = (df['label'] == df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label'])
only_one_correct = ((df['label'] == df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])) | \
                   ((df['label'] != df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label']))
none_correct = (df['label'] != df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])

# Assign colors for the scatter plot
df['color'] = 'white'
df.loc[both_correct, 'color'] = 'black'
df.loc[only_one_correct, 'color'] = 'gray'

# Scatter plot generation
plt.figure(figsize=(10, 6))
for label, color in [('dog', 'red'), ('cat', 'blue')]:
    subset = df[df['label'] == label]
    plt.scatter(subset['x'], subset['y'], edgecolor=color, c=subset['color'], label=label)

plt.title('Scatterplot of Dog and Cat Classifications')
plt.legend()
plt.show()

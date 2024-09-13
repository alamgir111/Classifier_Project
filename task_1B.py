import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load the dataset
df = pd.read_csv('Synthetic_2_classifiers.csv')

# Classifying images as correctly predicted by both, one, or none of the classifiers
both_correct = (df['label'] == df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label'])
one_correct = ((df['label'] == df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])) | \
              ((df['label'] != df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label']))
none_correct = (df['label'] != df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])

# Count the number of data points in each category (dogs and cats)
dog_both_correct = both_correct[df['label'] == 'dog'].sum()
dog_one_correct = one_correct[df['label'] == 'dog'].sum()
dog_none_correct = none_correct[df['label'] == 'dog'].sum()

cat_both_correct = both_correct[df['label'] == 'cat'].sum()
cat_one_correct = one_correct[df['label'] == 'cat'].sum()
cat_none_correct = none_correct[df['label'] == 'cat'].sum()

# Stacked bar chart data
labels = ['Classifier A - Correctly Predicted Dog', 'Classifier B - Correctly Predicted Dog',
          'Classifier A - Correctly Predicted Cat', 'Classifier B - Correctly Predicted Cat']

dog_correct = [dog_both_correct, dog_both_correct]
dog_partial = [dog_one_correct, dog_one_correct]

cat_correct = [cat_both_correct, cat_both_correct]
cat_partial = [cat_one_correct, cat_one_correct]

# Plotting the bar chart
fig, ax = plt.subplots(figsize=(10, 6))

# Adding borders
ax.add_patch(patches.Rectangle((-0.5, 0), 2.0, max(dog_correct) + max(dog_partial) + 800, 
                               linewidth=2, edgecolor='red', facecolor='red', alpha=0.2, zorder=0))
ax.add_patch(patches.Rectangle((2.5, 0), 2.0, max(cat_correct) + max(cat_partial) + 800, 
                               linewidth=2, edgecolor='blue', facecolor='blue', alpha=0.2, zorder=0))

# Plotting Dog bars
ax.bar([0, 1], dog_correct, color='black', width=0.4, label='Both Correct', zorder=2)
ax.bar([0, 1], dog_partial, bottom=dog_correct, color='gray', width=0.4, label='One Correct', zorder=2)

# Plotting Cat bars
ax.bar([3, 4], cat_correct, color='black', width=0.4, zorder=2)
ax.bar([3, 4], cat_partial, bottom=cat_correct, color='gray', width=0.4, zorder=2)

# Customizing the chart
ax.set_xticks([0, 1, 3, 4])
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.set_title("Assessing Classifiers' Performance for Each Class")
ax.set_ylabel('Count')
ax.legend()

# Adjust layout and display
plt.tight_layout()
plt.show()

import numpy as np
import pandas as pd
import plotly.express as px

# Generate sample data (you should replace this with your actual dataset)
num_classifiers = 20
classes = ['Dog', 'Cat']

# Simulate classifier accuracy between 0 and 1 for each classifier and class
data = {
    'Class': np.repeat(classes, num_classifiers),
    'Classifier': [f'Classifier {i+1}' for i in range(num_classifiers)] * len(classes),
    'Accuracy': np.random.rand(len(classes) * num_classifiers)  # Random accuracy values
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Use pivot_table to reshape the data correctly
df_pivot = df.pivot_table(index='Class', columns='Classifier', values='Accuracy')

# Create the heatmap
fig = px.imshow(df_pivot,
                color_continuous_scale='Blues',
                labels=dict(x="Classifiers", y="Classes", color="Accuracy"),
                title="Classifier Performance Heatmap")

# Display the heatmap
fig.show()

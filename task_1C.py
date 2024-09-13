from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.models.tools import BoxSelectTool, LassoSelectTool
import pandas as pd

# Load the data
df = pd.read_csv('Synthetic_2_classifiers.csv')

# Classify images as accurately predicted by both, one, or none of the classifiers
both_correct = (df['label'] == df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label'])
one_correct_a = (df['label'] == df['classifierA_predicted_label']) & (df['label'] != df['classifierB_predicted_label'])
one_correct_b = (df['label'] != df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label'])

# Define colors for points
df['color'] = ['black' if both else 'gray' if (a or b) else 'white' 
               for both, a, b in zip(both_correct, one_correct_a, one_correct_b)]
df['border_color'] = ['red' if label == 'dog' else 'blue' for label in df['label']]

# Prepare data for Bokeh
source = ColumnDataSource(data=df)

# Create scatterplot
p = figure(title="Scatterplot with Linked Interactivity", tools="lasso_select, box_select")
p.circle('x', 'y', fill_color='color', line_color='border_color', source=source, size=8)

# Create bar chart
bar_chart = figure(x_range=['Dog - A', 'Cat - A', 'Dog - B', 'Cat - B'], title="Classifier Performance")
bars = bar_chart.vbar(x=['Dog - A', 'Cat - A', 'Dog - B', 'Cat - B'], top=[0, 0, 0, 0], width=0.9)

# Callback to update bar chart based on selection
def update_bar_chart(attr, old, new):
    selected_indices = source.selected.indices
    selected_data = df.iloc[selected_indices]

    # Classifier A counts
    dog_a_count = selected_data[(selected_data['label'] == 'dog') & 
                                (selected_data['classifierA_predicted_label'] == selected_data['label'])].shape[0]
    cat_a_count = selected_data[(selected_data['label'] == 'cat') & 
                                (selected_data['classifierA_predicted_label'] == selected_data['label'])].shape[0]

    # Classifier B counts
    dog_b_count = selected_data[(selected_data['label'] == 'dog') & 
                                (selected_data['classifierB_predicted_label'] == selected_data['label'])].shape[0]
    cat_b_count = selected_data[(selected_data['label'] == 'cat') & 
                                (selected_data['classifierB_predicted_label'] == selected_data['label'])].shape[0]

    # Update the bar chart
    bars.data_source.data['top'] = [dog_a_count, cat_a_count, dog_b_count, cat_b_count]

# Add the callback to the selection event
source.selected.on_change('indices', update_bar_chart)

# Layout and show
layout = column(p, bar_chart)
curdoc().add_root(layout)
show(layout)

from bokeh.plotting import figure, show
import pandas as pd

# Loading data
df = pd.read_csv('Synthetic_2_classifiers.csv')

def plot():
    # Calculating key data
    df['both_correct'] = (df['label'] == df['classifierA_predicted_label']) & (df['label'] == df['classifierB_predicted_label'])
    Total_Red = (df['label'] == 'dog').sum()
    Total_Blue = (df['label'] == 'cat').sum()

    count_dog_A = ((df['classifierA_predicted_label'] == 'dog') & (df['label'] == 'dog')).sum()
    count_dog_B = ((df['classifierB_predicted_label'] == 'dog') & (df['label'] == 'dog')).sum()
    count_cat_A = ((df['classifierA_predicted_label'] == 'cat') & (df['label'] == 'cat')).sum()
    count_cat_B = ((df['classifierB_predicted_label'] == 'cat') & (df['label'] == 'cat')).sum()

    A = B = ((df['both_correct'] & (df['label'] == 'dog'))).sum()
    C = D = ((df['both_correct'] & (df['label'] == 'cat'))).sum()

    bar_x = [0.9, 1.1, 2.9, 3.1]
    bar_width = 0.15

    # Creating figure
    p = figure(title="Bar Chart Example", width=900, y_range=(0, max(Total_Red, Total_Blue)))

    # Plotting bars
    p.vbar(x=bar_x, top=[A, B, C, D], width=bar_width, fill_color="black", line_color=None)
    p.vbar(x=[1, 1], top=[Total_Red] * 2, width=0.5, fill_color="red", line_color=None, alpha=0.10)
    p.vbar(x=[3, 3], top=[Total_Blue] * 2, width=0.5, fill_color="blue", line_color=None, alpha=0.10)
    p.vbar(x=bar_x, top=[count_dog_A, count_dog_B, count_cat_A, count_cat_B], width=bar_width, fill_color="gray", line_color=None, alpha=0.7)

    # Customizing axes and labels
    p.xaxis.ticker = bar_x
    p.xaxis.major_label_overrides = {0.9: 'classifier A - Correctly Predicted Dog', 1.1: 'classifier B - Correctly Predicted Dog', 
                                     2.9: 'classifier A - Correctly Predicted Cat', 3.1: 'classifier B - Correctly Predicted Cat'}
    p.xaxis.major_label_orientation = 1.0
    p.xaxis.axis_label = "Categories"
    p.yaxis.axis_label = "Count"
    p.title.align = "center"
    p.title.text_font_size = "20px"


    # Display plot
    show(p)

plot()

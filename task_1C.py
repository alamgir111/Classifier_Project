import pandas as pd
from bokeh.plotting import figure, ColumnDataSource
from bokeh.layouts import column
from bokeh.models import BoxSelectTool, HoverTool, TapTool, CustomJS
from bokeh.io import curdoc

df = pd.read_csv('Synthetic_2_classifiers.csv')

df['fill_colors'] = df.apply(
    lambda row: 'black' if row['label'] == 'dog' and row['classifierA_predicted_label'] == 'dog' and row['classifierB_predicted_label'] == 'dog'
    else 'gray' if row['label'] == 'dog' and (row['classifierA_predicted_label'] == 'dog' or row['classifierB_predicted_label'] == 'dog')
    else 'black' if row['label'] == 'cat' and row['classifierA_predicted_label'] == 'cat' and row['classifierB_predicted_label'] == 'cat'
    else 'gray' if row['label'] == 'cat' and (row['classifierA_predicted_label'] == 'cat' or row['classifierB_predicted_label'] == 'cat')
    else 'white', axis=1
)

df['border_colors'] = df.apply(lambda row: 'red' if row['label'] == 'dog' else 'blue', axis=1)

source = ColumnDataSource(df)

scatter_plot = figure(width=800, height=600, title="Projected Data Space",
                      tools=[BoxSelectTool(), HoverTool(tooltips=[("Label", "@label"), ("Classifier A", "@classifierA_predicted_label"), ("Classifier B", "@classifierB_predicted_label")]), TapTool()])

scatter_plot.scatter(x="x", y="y", source=source, size=6, fill_color="fill_colors", line_color="border_colors", line_width=2, alpha=0.6)

# Updated colors for the bar chart
bar_source = ColumnDataSource(data={'categories': ['Both Correct (A)', 'Both Correct (B)', 'Only Classifier A Correct', 'Only Classifier B Correct', 'None Correct'],
                                    'counts': [0, 0, 0, 0, 0],
                                    'colors': ['violet', 'rosybrown', 'blue', 'red', 'aquamarine']})  # Updated colors

bar_plot = figure(x_range=['Both Correct (A)', 'Both Correct (B)', 'Only Classifier A Correct', 'Only Classifier B Correct', 'None Correct'], height=400, width=800, title="Classifier Performance", toolbar_location=None, tools="")
bar_plot.vbar(x='categories', top='counts', source=bar_source, width=0.4, fill_color='colors')

bar_plot.x_range.range_padding = 0.1
bar_plot.xgrid.grid_line_color = None

callback = CustomJS(args=dict(source=source, bar_source=bar_source), code="""
    function countSelected(source, indices) {
        let both_A = 0, both_B = 0, one_A = 0, one_B = 0, none = 0;
        for (let i = 0; i < indices.length; i++) {
            let index = indices[i];
            let label = source.data['label'][index];
            let classifierA_pred = source.data['classifierA_predicted_label'][index];
            let classifierB_pred = source.data['classifierB_predicted_label'][index];

            let classifierA_correct = classifierA_pred === label;
            let classifierB_correct = classifierB_pred === label;

            if (classifierA_correct && classifierB_correct) {
                both_A++;
                both_B++;
            } else if (classifierA_correct && !classifierB_correct) {
                one_A++;
            } else if (classifierB_correct && !classifierA_correct) {
                one_B++;
            } else {
                none++;
            }
        }
        return [both_A, both_B, one_A, one_B, none];
    }

    let counts = countSelected(source, source.selected.indices);
    
    bar_source.data = {
        'categories': ['Both Correct (A)', 'Both Correct (B)', 'Only Classifier A Correct', 'Only Classifier B Correct', 'None Correct'],
        'counts': [counts[0], counts[1], counts[2], counts[3], counts[4]],
        'colors': bar_source.data['colors']
    };
    bar_source.change.emit();
""")

source.selected.js_on_change('indices', callback)

layout = column(scatter_plot, bar_plot)
curdoc().add_root(layout)

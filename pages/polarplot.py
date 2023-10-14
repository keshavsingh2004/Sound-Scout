import numpy as np
import plotly.graph_objects as go

def feature_plot(features):

    labels = features.columns.tolist()
    stats = features.mean().tolist()

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # close the plot
    stats = np.concatenate((stats,[stats[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    # Create a Plotly figure
    fig = go.Figure()

    # Add a polar trace to the figure
    fig.add_trace(go.Scatter(
        theta=angles,
        r=stats,
        mode='lines+markers',
        line_width=2,
        name="Features",
        fill='toself',
        fill_color='gray',
        opacity=0.75
    ))

    # Set the layout of the figure
    fig.update_layout(
        polar=dict(
            angularaxis=dict(
                ticks='outside',
                labels=labels
            )
          ),
        radialaxis=dict(
            tickmode='array',
            tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1],
            ticktext=["0", "0.2", "0.4", "0.6", "0.8", "1.0"]
          ),
        legend=dict(x=0.1, y=0.1)
    )

    return fig
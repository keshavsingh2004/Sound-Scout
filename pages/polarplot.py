import numpy as np
import plotly.graph_objects as go
import streamlit as st

def feature_plot(features):
    labels = features.columns.tolist()
    stats = features.mean().tolist()

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    # Close the plot
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = go.Figure(data=go.Scatterpolar(
        r=stats,
        theta=angles,
        fill='toself',
        name='Features',
        line_color='gray',
        opacity=0.75
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                tickvals=[0.2, 0.4, 0.6, 0.8],
                ticktext=["0.2", '0.4', "0.6", "0.8"],
                color="grey",
                tickfont=dict(size=12),
            ),
        ),
        showlegend=True,
        legend=dict(x=0.1, y=0.1),
    )

    st.plotly_chart(fig, use_container_width=True)
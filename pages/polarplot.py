import numpy as np
import plotly.graph_objects as go
import streamlit as st

def feature_plot(features):
    labels = features.columns.tolist()
    stats = features.mean().tolist()

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    # Close the plot
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
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
                angle=0,  # Start angle at 0 degrees
                dtick=0.2,  # Distance between ticks
            ),
            angularaxis=dict(
                tickfont=dict(size=12),
                rotation=90,  # Rotate the angle labels
            )
        ),
        showlegend=True,
        legend=dict(x=0.1, y=0.1),
        width=600,
        height=600,
        margin=dict(l=50, r=50, t=50, b=50),
        template='plotly_white',  # Use a white background template
    )

    st.plotly_chart(fig, use_container_width=True)
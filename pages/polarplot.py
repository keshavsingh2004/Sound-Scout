import numpy as np
import plotly.graph_objects as go
import streamlit as st
import pandas as pd
# def feature_plot(features):

#     labels = features.columns.tolist()
#     stats = features.mean().tolist()

#     angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

#     # close the plot
#     stats = np.concatenate((stats,[stats[0]]))
#     angles = np.concatenate((angles,[angles[0]]))

#     # Size of the figure
#     fig = plt.figure(figsize=(18, 18))

#     ax = fig.add_subplot(221, polar=True)
#     ax.plot(angles, stats, 'o-', linewidth=2, label="Features", color='gray', alpha=0.75)
#     ax.fill(angles, stats, alpha=0.5, facecolor='gray')
#     ax.set_thetagrids(angles[0:7] * 180/np.pi, labels, fontsize=13)

#     ax.set_rlabel_position(250)
#     plt.yticks([0.2, 0.4, 0.6, 0.8], ["0.2", '0.4', "0.6", "0.8"], color="grey", size=12)
#     plt.ylim(0, 1)

#     plt.legend(loc='best', bbox_to_anchor=(0.1, 0.1))

#     st.pyplot(fig, bbox_inches='tight')

def feature_plot(features):
    # Create a polar trace
    trace = go.Scatterpolar(
        theta=np.linspace(0, 2 * np.pi, len(features)),
        r=features,
        fill='toself',
        line=dict(color='gray'),
        marker=dict(size=10, color='gray'),
        text=features.tolist(),
        hoverinfo='text'
    )

    # Create a layout
    layout = go.Layout(
        title='Feature Statistics',
        polar=dict(
            angularaxis=dict(
                tickmode='array',
                tickvals=np.linspace(0, 2 * np.pi, len(features)),
                ticktext=features.tolist()
            )
        )
    )

    # Create a figure
    fig = go.Figure(data=[trace], layout=layout)

    # Show the plot in Streamlit
    st.plotly_chart(fig)
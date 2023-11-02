import numpy as np
import matplotlib.pyplot as plt
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

    # Convert the Pandas DataFrame to a NumPy array
    features = features.to_numpy()

    # Calculate the mean of the features
    mean = features.mean(axis=0)

    # Calculate the angles for the polar plot
    angles = np.linspace(0, 2 * np.pi, len(mean), endpoint=False)

    # Close the plot
    mean = np.concatenate((mean, [mean[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    # Create the Plotly figure
    fig = px.polar_area(
        r=mean,
        theta=angles,
        color="Features",
        color_continuous_scale="gray",
        alpha=0.75,
        title="Feature Statistics",
    )

    # Set the axis labels
    fig.update_layout(
        xaxis_title="Feature",
        yaxis_title="Mean",
        polar_angularaxis_labels=features.columns.tolist(),
    )

    # Set the y-axis range
    fig.update_yaxes(range=(0, 1))

    # Show the plot in Streamlit
    st.plotly_chart(fig)
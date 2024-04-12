#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: devonmcdermott
"""

# Final Exam Part 1 - Kohonen Clustering

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
data_points = pd.read_csv("Ex1_data.csv").values

# Function to initialize random weights for neurons
def initialize_neuron_weights(num_neurons, num_features):
    return np.random.rand(num_neurons, num_features)

# Function to find the winner (neuron with the closest weight vector)
def find_winning_neuron(neuron_weights, data_sample):
    return np.argmin(np.linalg.norm(neuron_weights - data_sample, axis=1))

# Function to update weights of the winning neuron and its neighbors
def update_neuron_weights(neuron_weights, winning_neuron, data_sample, learning_rate):
    if winning_neuron < len(neuron_weights):
      neuron_weights[winning_neuron] += learning_rate * (data_sample - neuron_weights[winning_neuron])

# Function to plot normalized data points and neuron weights
def plot_clusters_normalized(data, neuron_weights, title):
    normalized_data = (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))
    normalized_neuron_weights = (neuron_weights - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))

    plt.figure(figsize=(8, 6))
    plt.scatter(normalized_data[:, 0], normalized_data[:, 1], c='yellow', marker='o', label='Data Points')
    plt.scatter(normalized_neuron_weights[:, 0], normalized_neuron_weights[:, 1], c='purple', marker='x', label='Neuron Weights')
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Kohonen's Clustering Algorithm
def kohonen_clustering(num_neurons, data, learning_rate=0.1, epochs=100, manual_weights=None):
    num_features = data.shape[1]
    neuron_weights = initialize_neuron_weights(num_neurons, num_features)

    for epoch in range(epochs):
        for data_sample in data:
            # Find the winning neuron
            winning_neuron = find_winning_neuron(neuron_weights, data_sample)
            
            # Update weights of the winning neuron and its neighbors
            update_neuron_weights(neuron_weights, winning_neuron, data_sample, learning_rate)
    print(f"\nFinal Weights for {num_neurons} Neurons:")
    print(neuron_weights)
    return neuron_weights

# Part 1: Two Neurons
print("Part 1: Two Neurons")
final_neuron_weights_2 = kohonen_clustering(2, data_points)
plot_clusters_normalized(data_points, final_neuron_weights_2, "Two Neurons  (Normalized)")

# Part 2: Three Neurons
print("Part 2: Three Neurons")
final_neuron_weights_3 = kohonen_clustering(3, data_points)
plot_clusters_normalized(data_points, final_neuron_weights_3, "Three Neurons (Normalized)")

# Part 3: Seven Neurons
print("Part 3: Seven Neurons")
final_neuron_weights_7 = kohonen_clustering(7, data_points)
plot_clusters_normalized(data_points, final_neuron_weights_7, "Seven Neurons (Normalized)")


# Part 1: Two Neurons with Manual Weights
print("Part 1: Two Neurons with Manual Weights")
manual_weights_2 = np.array([[0.2, 0.8], [0.7, 0.3]])  # Example manual weights
final_neuron_weights_2 = kohonen_clustering(2, data_points, manual_weights=manual_weights_2)
plot_clusters_normalized(data_points, final_neuron_weights_2, "Two Neurons (Normalized)")

# Part 2: Three Neurons with Manual Weights
print("Part 2: Three Neurons with Manual Weights")
manual_weights_3 = np.array([[0.3, 0.6], [0.5, 0.2], [0.8, 0.4]])  # Example manual weights
final_neuron_weights_3 = kohonen_clustering(3, data_points, manual_weights=manual_weights_3)
plot_clusters_normalized(data_points, final_neuron_weights_3, "Three Neurons (Normalized)")

# Part 3: Seven Neurons with Manual Weights
print("Part 3: Seven Neurons with Manual Weights")
manual_weights_7 = np.array([[0.2, 0.7], [0.5, 0.3], [0.4, 0.9], [0.8, 0.1], [0.6, 0.5], [0.3, 0.4], [0.7, 0.6]])  # Example manual weights
final_neuron_weights_7 = kohonen_clustering(7, data_points, manual_weights=manual_weights_7)
plot_clusters_normalized(data_points, final_neuron_weights_7, "Seven Neurons (Normalized)")

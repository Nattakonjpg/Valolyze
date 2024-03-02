import torch
import pandas as pd
import torch.nn.functional as F


def evaluate_model(loaded_model, test_loader, output_path):
    device = next(loaded_model.parameters()).device
    true_labels, predicted_labels = [], []
    with torch.no_grad():
        for data, _, target in test_loader:
            # Move data and target to the same device as the model
            data, target = data.to(device), target.to(device)

            output = F.log_softmax(loaded_model(data), dim=1)
            _, predicted = torch.max(output, dim=1)

            true_labels.extend(target.cpu().numpy())
            predicted_labels.extend(predicted.cpu().numpy())

    # Create DataFrame from true_labels and predicted_labels
    df_output = pd.DataFrame(
        {'true_label': true_labels, 'predicted_label': predicted_labels})

    # Save DataFrame as a CSV file
    df_output.to_csv(output_path, index=False)

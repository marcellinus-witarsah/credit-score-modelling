import pandas as pd

from credit_score_modelling.config import TRAIN_CONFIG
from credit_score_modelling.modeling.woe_logistic_regression import (
    WOELogisticRegression,
)


def main():
    # 1. Load data
    train_df = pd.read_csv(TRAIN_CONFIG.train_file)
    X_train, y_train = (
        train_df.drop(columns=[TRAIN_CONFIG.target]),
        train_df[TRAIN_CONFIG.target],
    )

    # 2. Initialize model
    model = WOELogisticRegression.from_parameters(
        woe_transformer_params=TRAIN_CONFIG.woe_transformer_params,
        logreg_params=TRAIN_CONFIG.logreg_params,
    )

    # 3. Train model
    model.fit(X_train, y_train)

    # 4. Save model
    model.save(file=TRAIN_CONFIG.model_file)


if __name__ == "__main__":
    main()

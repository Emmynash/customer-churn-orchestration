from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

def build_preprocessor(numerical_features, categorical_features):
    """
    Builds a preprocessor for numerical and categorical features.

    Parameters:
    numerical_features (list): List of names of numerical features.
    categorical_features (list): List of names of categorical features.

    Returns:
    ColumnTransformer: A preprocessor that can be used in a pipeline.
    """
    # Define transformers for numerical and categorical features
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Combine transformers into a ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor
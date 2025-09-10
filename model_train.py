# model_train.py (compatible con scikit-learn antiguo)
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
from joblib import dump

DATA_PATH = Path("data/bank.csv")
MODEL_DIR = Path("model")
MODEL_DIR.mkdir(exist_ok=True, parents=True)
MODEL_PATH = MODEL_DIR / "bank-marketing-rf-v1.joblib"

def main():
    # Lee CSV separado por coma
    df = pd.read_csv(DATA_PATH)

    # Target: 'deposit' con yes/no
    assert "deposit" in df.columns, "No se encontró la columna target 'deposit' (yes/no)."
    y = df["deposit"].map({"yes": 1, "no": 0})
    X = df.drop(columns=["deposit"])

    # Detecta columnas categóricas y numéricas
    cat_cols = [c for c in X.columns if X[c].dtype == "object"]
    num_cols = [c for c in X.columns if c not in cat_cols]

    # Preprocesamiento (sin verbose_feature_names_out)
    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", StandardScaler(), num_cols),
        ],
        remainder="drop"
    )

    clf = RandomForestClassifier(
        n_estimators=300,
        random_state=0,
        n_jobs=-1
    )

    pipe = Pipeline([("pre", pre), ("clf", clf)])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print("Entrenando...")
    pipe.fit(X_train, y_train)

    print("Evaluación en test:")
    y_pred = pipe.predict(X_test)
    print(classification_report(y_test, y_pred, digits=4))

    print(f"Guardando modelo en {MODEL_PATH} ...")
    dump(pipe, MODEL_PATH)
    print("OK.")

if __name__ == "__main__":
    main()

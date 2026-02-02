# 传统机器学习模型指南

## 模型概览

| 模型 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| Decision Tree | 可解释性强 | 易过拟合 | 基线/教学 |
| Random Forest | 稳定、不易过拟合 | 慢、内存大 | 通用 |
| XGBoost | 性能优、速度快 | 调参多 | 结构化数据首选 |
| LightGBM | 更快、内存效率高 | 对小数据不友好 | 大数据集 |
| CatBoost | 类别特征友好 | 慢 | 含类别特征 |
| SVM | 高维有效 | 大数据慢 | 小样本 |
| MLP | 非线性强 | 需调参 | 复杂模式 |

---

## XGBoost

### 安装与导入

```python
pip install xgboost

from xgboost import XGBClassifier, XGBRegressor
```

### 分类任务

```python
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score

# 基础模型
model = XGBClassifier(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    use_label_encoder=False,
    eval_metric='logloss',
)

# 训练
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
```

### 回归任务

```python
from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

### 超参数说明

| 参数 | 默认值 | 说明 | 调参建议 |
|------|--------|------|---------|
| n_estimators | 100 | 树的数量 | 100-1000 |
| max_depth | 6 | 树的最大深度 | 3-10 |
| learning_rate | 0.3 | 学习率 | 0.01-0.3 |
| subsample | 1 | 样本采样比例 | 0.6-1.0 |
| colsample_bytree | 1 | 特征采样比例 | 0.6-1.0 |
| min_child_weight | 1 | 最小叶子权重 | 1-10 |
| gamma | 0 | 分裂最小增益 | 0-5 |
| reg_alpha | 0 | L1 正则化 | 0-1 |
| reg_lambda | 1 | L2 正则化 | 0-10 |

### Optuna 超参数优化

```python
import optuna

def objective(trial):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 1),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 10),
    }

    model = XGBClassifier(**params, random_state=42, use_label_encoder=False)
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    return scores.mean()

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100, show_progress_bar=True)

print(f"Best AUC: {study.best_value:.4f}")
print(f"Best params: {study.best_params}")
```

---

## CatBoost

### 安装与导入

```python
pip install catboost

from catboost import CatBoostClassifier, CatBoostRegressor
```

### 分类任务（含类别特征）

```python
from catboost import CatBoostClassifier

# 指定类别特征列索引
cat_features = [0, 2, 5]  # 假设第0、2、5列是类别特征

model = CatBoostClassifier(
    iterations=500,
    depth=6,
    learning_rate=0.1,
    cat_features=cat_features,
    random_state=42,
    verbose=100,
)

model.fit(X_train, y_train, eval_set=(X_val, y_val), early_stopping_rounds=50)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]
```

### 超参数说明

| 参数 | 默认值 | 说明 |
|------|--------|------|
| iterations | 1000 | 树的数量 |
| depth | 6 | 树的深度 |
| learning_rate | 0.03 | 学习率 |
| l2_leaf_reg | 3 | L2 正则化 |
| border_count | 254 | 数值特征分桶数 |
| cat_features | None | 类别特征索引 |

---

## LightGBM

### 安装与导入

```python
pip install lightgbm

from lightgbm import LGBMClassifier, LGBMRegressor
```

### 基础使用

```python
from lightgbm import LGBMClassifier

model = LGBMClassifier(
    n_estimators=500,
    max_depth=6,
    learning_rate=0.05,
    num_leaves=31,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    eval_metric='auc',
    callbacks=[lightgbm.early_stopping(50)],
)
```

---

## SVM

```python
from sklearn.svm import SVC, SVR
from sklearn.preprocessing import StandardScaler

# SVM 需要特征缩放
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 分类
model = SVC(
    C=1.0,
    kernel='rbf',
    gamma='scale',
    probability=True,  # 需要概率输出时设置
    random_state=42,
)

model.fit(X_train_scaled, y_train)
y_prob = model.predict_proba(X_test_scaled)[:, 1]
```

---

## MLP (多层感知机)

```python
from sklearn.neural_network import MLPClassifier, MLPRegressor

model = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    learning_rate_init=0.001,
    max_iter=500,
    early_stopping=True,
    validation_fraction=0.1,
    random_state=42,
)

model.fit(X_train_scaled, y_train)
```

---

## 模型对比框架

```python
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_auc_score, accuracy_score
import time

def compare_models(models, X, y, cv=5, scoring='roc_auc'):
    """
    对比多个模型的性能
    """
    results = []

    for name, model in models.items():
        start_time = time.time()
        scores = cross_val_score(model, X, y, cv=cv, scoring=scoring)
        elapsed = time.time() - start_time

        results.append({
            'Model': name,
            'Mean Score': scores.mean(),
            'Std': scores.std(),
            'Time (s)': elapsed,
        })

        print(f"{name}: {scores.mean():.4f} (+/- {scores.std():.4f}) [{elapsed:.1f}s]")

    return pd.DataFrame(results).sort_values('Mean Score', ascending=False)

# 使用示例
models = {
    'XGBoost': XGBClassifier(random_state=42, use_label_encoder=False),
    'CatBoost': CatBoostClassifier(random_state=42, verbose=0),
    'LightGBM': LGBMClassifier(random_state=42, verbose=-1),
    'RandomForest': RandomForestClassifier(random_state=42),
    'SVM': SVC(probability=True, random_state=42),
}

results_df = compare_models(models, X_train_scaled, y_train)
print(results_df)
```

---

## 特征重要性分析

```python
import matplotlib.pyplot as plt

# XGBoost/LightGBM/CatBoost 内置
feature_importance = model.feature_importances_
feature_names = X_train.columns

# 可视化
plt.figure(figsize=(10, 6))
sorted_idx = np.argsort(feature_importance)[-20:]  # Top 20
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
plt.yticks(range(len(sorted_idx)), feature_names[sorted_idx])
plt.xlabel('Feature Importance')
plt.title('Top 20 Important Features')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150)
```

---

## SHAP 可解释性分析

```python
pip install shap

import shap

# 计算 SHAP 值
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)

# Summary plot
shap.summary_plot(shap_values, X_test, feature_names=feature_names)

# 单个样本解释
shap.waterfall_plot(shap.Explanation(
    values=shap_values[0],
    base_values=explainer.expected_value,
    data=X_test.iloc[0],
    feature_names=feature_names
))
```

---

## 模型保存与加载

```python
import joblib

# 保存
joblib.dump(model, 'best_model.pkl')
joblib.dump(scaler, 'scaler.pkl')

# 加载
model = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')

# CatBoost 专用
model.save_model('catboost_model.cbm')
model = CatBoostClassifier()
model.load_model('catboost_model.cbm')
```

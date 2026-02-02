---
name: medical-ml-predictor
description: "医疗数据混合机器学习预测系统。当用户提到'机器学习预测'、'混合模型'、'深度学习预测'、'医疗AI模型'、'影像预测'、'多模态预测'、'ML pipeline'、'XGBoost预测'、'神经网络预测'、'特征融合'、'模型训练'、'医学影像分类'、'临床预测模型'等时使用此skill。支持：数值参数+医学影像的多模态输入、传统ML与深度学习双路径、特征融合混合模型、完整的模型评估与优化流程。"
---

# Medical ML Predictor - 医疗数据混合机器学习预测系统

## 概述

这是一个**端到端的医疗数据机器学习预测系统**，支持：
- **多模态输入**：数值参数 + 医学影像
- **双路径建模**：传统ML + 深度学习并行
- **特征融合**：混合模型优化
- **完整评估**：回归与分类指标全覆盖

---

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              INPUT 输入层                                │
├─────────────────────────────────┬───────────────────────────────────────┤
│     数值参数 (Tabular Data)      │        医学影像 (Image Data)          │
│  • 人口统计学特征                │  • X光/CT/MRI                         │
│  • 临床检查指标                  │  • 眼科影像（眼底/OCT/角膜地形图）    │
│  • 实验室检验结果                │  • 皮肤镜图像                         │
│  • 生理参数                      │  • 病理切片                           │
│  • 问卷评分                      │  • 超声图像                           │
└─────────────────────────────────┴───────────────────────────────────────┘
                    ↓                                    ↓
┌─────────────────────────────────┐    ┌───────────────────────────────────┐
│      传统机器学习路径            │    │        深度学习路径                │
│  ┌─────────┐  ┌─────────┐       │    │  ┌─────────────────────────────┐  │
│  │   DTM   │  │   SVM   │       │    │  │     CNN Backbone            │  │
│  └─────────┘  └─────────┘       │    │  │  • ResNet / ResNeXt         │  │
│  ┌─────────┐  ┌─────────┐       │    │  │  • Inception-ResNet         │  │
│  │ XGBoost │  │   DNN   │       │    │  │  • EfficientNet             │  │
│  └─────────┘  └─────────┘       │    │  │  • Vision Transformer       │  │
│  ┌─────────┐                    │    │  └─────────────────────────────┘  │
│  │CatBoost │                    │    │                ↓                  │
│  └─────────┘                    │    │  ┌─────────────────────────────┐  │
│                                 │    │  │   Image Feature Extraction  │  │
│                                 │    │  └─────────────────────────────┘  │
└─────────────────────────────────┘    └───────────────────────────────────┘
                    ↓                                    ↓
                    └──────────────┬─────────────────────┘
                                   ↓
              ┌─────────────────────────────────────────────────┐
              │              Mixed Model 混合模型                │
              │  • 特征拼接 (Concatenation)                     │
              │  • 注意力融合 (Attention Fusion)                │
              │  • 集成学习 (Ensemble)                          │
              └─────────────────────────────────────────────────┘
                                   ↓
              ┌─────────────────────────────────────────────────┐
              │                   OUTPUT 输出                   │
              │  回归任务: 连续值预测                            │
              │  分类任务: 类别/概率预测                         │
              └─────────────────────────────────────────────────┘
                                   ↓
              ┌─────────────────────────────────────────────────┐
              │              Evaluation 评估指标                 │
              │  回归: MAE, MSE, RMSE, R², MAPE                 │
              │  分类: ACC, AUC, F1, Precision, Recall          │
              └─────────────────────────────────────────────────┘
```

---

## 工作流程

### 阶段一：项目初始化

#### 1.1 收集基本信息

向用户询问：

| 问题 | 选项/说明 |
|------|----------|
| 任务类型 | 回归 / 二分类 / 多分类 |
| 数据模态 | 仅数值 / 仅影像 / 数值+影像（混合） |
| 数据规模 | 样本量、特征数、图像数量 |
| 目标变量 | 预测什么？（如：疾病概率、严重程度评分、预后指标） |
| 硬件环境 | CPU / GPU型号 / 显存大小 |

#### 1.2 环境配置

根据用户环境生成依赖安装脚本：

```bash
# 基础依赖
pip install numpy pandas scikit-learn matplotlib seaborn

# 传统ML
pip install xgboost catboost lightgbm

# 深度学习（根据GPU选择）
pip install torch torchvision  # PyTorch
# 或
pip install tensorflow  # TensorFlow

# 医学影像处理
pip install opencv-python pillow albumentations

# 可选：高级工具
pip install optuna  # 超参数优化
pip install shap    # 模型解释
```

---

### 阶段二：数据准备

#### 2.1 数据结构定义

**数值数据格式**：
```
project/
├── data/
│   ├── tabular/
│   │   ├── train.csv      # 训练集
│   │   ├── val.csv        # 验证集（可选）
│   │   └── test.csv       # 测试集
```

CSV 格式要求：
| 列名 | 说明 |
|------|------|
| id | 样本唯一标识 |
| feature_1, feature_2, ... | 数值特征 |
| image_path | 对应影像路径（混合模式） |
| target | 目标变量 |

**影像数据格式**：
```
project/
├── data/
│   ├── images/
│   │   ├── train/
│   │   │   ├── class_0/    # 分类任务按类别组织
│   │   │   └── class_1/
│   │   └── test/
```

#### 2.2 数据预处理 Checklist

**数值数据**：
- [ ] 缺失值处理（删除/填充/插补）
- [ ] 异常值检测与处理
- [ ] 特征标准化/归一化
- [ ] 类别特征编码（One-Hot/Label/Target Encoding）
- [ ] 特征选择（可选）
- [ ] 数据集划分（Train/Val/Test）

**影像数据**：
- [ ] 尺寸统一（如 224×224, 299×299）
- [ ] 像素归一化（0-1 或 ImageNet 标准化）
- [ ] 数据增强策略
- [ ] 数据集划分

详见 [references/preprocessing_guide.md](file://./references/preprocessing_guide.md)

---

### 阶段三：传统机器学习路径

#### 3.1 模型选择

| 模型 | 特点 | 适用场景 |
|------|------|---------|
| **Decision Tree** | 可解释性强 | 基线模型 |
| **Random Forest** | 稳定，不易过拟合 | 中小数据集 |
| **SVM** | 高维有效 | 小样本，清晰边界 |
| **XGBoost** | 性能优秀，速度快 | 结构化数据首选 |
| **LightGBM** | 更快，内存效率高 | 大数据集 |
| **CatBoost** | 原生支持类别特征 | 含类别特征数据 |
| **DNN** | 非线性拟合强 | 复杂模式 |

#### 3.2 训练流程

```python
# 伪代码示意
from sklearn.model_selection import cross_val_score

models = {
    'XGBoost': XGBClassifier(**params),
    'CatBoost': CatBoostClassifier(**params),
    'LightGBM': LGBMClassifier(**params),
    'SVM': SVC(**params),
    'DNN': MLPClassifier(**params),
}

results = {}
for name, model in models.items():
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='roc_auc')
    results[name] = scores.mean()
```

#### 3.3 超参数优化

使用 Optuna 进行贝叶斯优化：

```python
import optuna

def objective(trial):
    params = {
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        # ...
    }
    model = XGBClassifier(**params)
    score = cross_val_score(model, X, y, cv=5).mean()
    return score

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)
```

详见 [references/ml_models_guide.md](file://./references/ml_models_guide.md)

---

### 阶段四：深度学习路径

#### 4.1 网络架构选择

| 架构 | 参数量 | 特点 | GPU显存需求 |
|------|--------|------|-------------|
| **ResNet-18** | 11M | 轻量，入门首选 | 2-4GB |
| **ResNet-50** | 25M | 平衡性能与效率 | 4-6GB |
| **EfficientNet-B0** | 5M | 高效，移动端友好 | 2-4GB |
| **EfficientNet-B4** | 19M | 性能优秀 | 6-8GB |
| **Inception-ResNet-v2** | 56M | 多尺度特征 | 8-12GB |
| **ViT-Base** | 86M | Transformer架构 | 8-12GB |

> **1660 Ti (6GB) 推荐**：ResNet-18/34, EfficientNet-B0/B1, batch_size=8-16

#### 4.2 训练配置

```python
# PyTorch 训练配置示例
config = {
    'backbone': 'resnet18',
    'pretrained': True,          # 使用预训练权重
    'input_size': (224, 224),
    'batch_size': 16,            # 根据显存调整
    'epochs': 50,
    'optimizer': 'AdamW',
    'lr': 1e-4,
    'weight_decay': 1e-4,
    'scheduler': 'CosineAnnealingLR',
    'early_stopping': 10,        # 早停轮数
}
```

#### 4.3 数据增强策略

```python
import albumentations as A

train_transform = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.8, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ColorJitter(brightness=0.2, contrast=0.2, p=0.3),
    A.GaussianBlur(blur_limit=3, p=0.1),
    A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ToTensorV2(),
])
```

详见 [references/deep_learning_guide.md](file://./references/deep_learning_guide.md)

---

### 阶段五：混合模型（特征融合）

#### 5.1 融合策略

| 策略 | 说明 | 实现复杂度 |
|------|------|-----------|
| **Early Fusion** | 原始特征直接拼接 | 低 |
| **Late Fusion** | 各模型预测结果融合 | 低 |
| **Feature Fusion** | 深度特征+数值特征拼接 | 中 |
| **Attention Fusion** | 注意力机制加权融合 | 高 |
| **Cross-Modal Attention** | 跨模态交互 | 高 |

#### 5.2 推荐实现：Feature Fusion

```python
class MultiModalModel(nn.Module):
    def __init__(self, num_tabular_features, num_classes):
        super().__init__()
        # 影像分支：提取深度特征
        self.image_backbone = models.resnet18(pretrained=True)
        self.image_backbone.fc = nn.Identity()  # 移除最后一层
        image_feature_dim = 512

        # 数值分支：MLP处理
        self.tabular_mlp = nn.Sequential(
            nn.Linear(num_tabular_features, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
        )
        tabular_feature_dim = 64

        # 融合层
        fusion_dim = image_feature_dim + tabular_feature_dim
        self.fusion_head = nn.Sequential(
            nn.Linear(fusion_dim, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, num_classes),
        )

    def forward(self, image, tabular):
        img_features = self.image_backbone(image)
        tab_features = self.tabular_mlp(tabular)
        fused = torch.cat([img_features, tab_features], dim=1)
        output = self.fusion_head(fused)
        return output
```

详见 [references/fusion_strategies.md](file://./references/fusion_strategies.md)

---

### 阶段六：模型评估

#### 6.1 评估指标

**回归任务**：

| 指标 | 公式 | 说明 |
|------|------|------|
| MAE | mean(\|y - ŷ\|) | 平均绝对误差 |
| MSE | mean((y - ŷ)²) | 均方误差 |
| RMSE | √MSE | 均方根误差 |
| R² | 1 - SS_res/SS_tot | 决定系数 |
| MAPE | mean(\|y - ŷ\|/y) × 100% | 平均百分比误差 |

**分类任务**：

| 指标 | 说明 |
|------|------|
| Accuracy | 整体准确率 |
| AUC-ROC | ROC曲线下面积 |
| F1-Score | 精确率与召回率调和平均 |
| Precision | 精确率 |
| Recall/Sensitivity | 召回率/敏感性 |
| Specificity | 特异性 |
| Confusion Matrix | 混淆矩阵 |

#### 6.2 评估代码

```python
from sklearn.metrics import (
    accuracy_score, roc_auc_score, f1_score,
    classification_report, confusion_matrix,
    mean_absolute_error, mean_squared_error, r2_score
)

# 分类评估
def evaluate_classification(y_true, y_pred, y_prob):
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'auc': roc_auc_score(y_true, y_prob),
        'f1': f1_score(y_true, y_pred),
        'report': classification_report(y_true, y_pred),
        'confusion_matrix': confusion_matrix(y_true, y_pred),
    }

# 回归评估
def evaluate_regression(y_true, y_pred):
    return {
        'mae': mean_absolute_error(y_true, y_pred),
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'r2': r2_score(y_true, y_pred),
    }
```

#### 6.3 模型对比

生成模型对比表：

| Model | ACC | AUC | F1 | MAE | R² | Train Time |
|-------|-----|-----|----|----|----|----|
| XGBoost | 0.85 | 0.91 | 0.84 | - | - | 2min |
| CatBoost | 0.86 | 0.92 | 0.85 | - | - | 3min |
| ResNet-18 | 0.88 | 0.93 | 0.87 | - | - | 30min |
| **Mixed Model** | **0.91** | **0.95** | **0.90** | - | - | 45min |

---

### 阶段七：模型优化

#### 7.1 优化策略

| 问题 | 解决方案 |
|------|---------|
| 过拟合 | Dropout, 数据增强, 正则化, 早停 |
| 欠拟合 | 增大模型, 更多特征, 减少正则化 |
| 类别不平衡 | 过采样/欠采样, 类别权重, Focal Loss |
| 训练不稳定 | 降低学习率, Gradient Clipping |
| 显存不足 | 减小batch_size, 混合精度训练, 梯度累积 |

#### 7.2 最优模型选择

```
选择标准：
1. 主要指标最优（如 AUC）
2. 验证集与测试集性能一致（无过拟合）
3. 推理速度满足需求
4. 模型可解释性（医疗场景重要）
```

---

### 阶段八：输出与部署

#### 8.1 必须输出

**1. 模型文件**
```
output/
├── models/
│   ├── best_xgboost.pkl
│   ├── best_catboost.cbm
│   └── best_deep_model.pth
├── scalers/
│   └── feature_scaler.pkl
└── configs/
    └── model_config.yaml
```

**2. 评估报告**
- 各模型性能对比表
- ROC曲线 / PR曲线
- 混淆矩阵可视化
- 特征重要性分析

**3. 代码文件**
```
src/
├── data_preprocessing.py
├── train_ml.py
├── train_deep.py
├── train_mixed.py
├── evaluate.py
└── predict.py
```

#### 8.2 可选输出

- 模型解释报告（SHAP值）
- API推理服务脚本
- Docker部署配置

---

## 快速开始模板

### 仅数值数据（传统ML）

```
用户: 我有一份眼科患者数据，想预测是否会发展为某疾病

Skill 响应:
1. 确认任务类型（二分类）
2. 了解数据规模（样本量、特征数）
3. 生成数据预处理代码
4. 训练多个ML模型（XGBoost, CatBoost, LightGBM等）
5. 交叉验证评估
6. 超参数优化
7. 输出最优模型和评估报告
```

### 数值 + 影像（混合模型）

```
用户: 我有患者的临床参数和角膜地形图，想预测术后效果

Skill 响应:
1. 确认任务类型（回归/分类）
2. 了解数据格式和规模
3. 数值数据预处理
4. 影像数据预处理和增强
5. 并行训练：传统ML处理数值 + CNN处理影像
6. 构建混合模型（特征融合）
7. 端到端训练和评估
8. 输出最优混合模型
```

---

## 质量保证 Checklist

### 数据质量
- [ ] 数据无泄漏（Train/Val/Test 严格分离）
- [ ] 目标变量分布合理
- [ ] 特征无严重缺失
- [ ] 类别平衡或已处理

### 模型训练
- [ ] 使用交叉验证
- [ ] 监控训练/验证曲线
- [ ] 早停防止过拟合
- [ ] 超参数已优化

### 评估完整性
- [ ] 测试集评估（非验证集）
- [ ] 多指标综合评估
- [ ] 置信区间或标准差
- [ ] 与基线模型对比

### 医疗场景特殊要求
- [ ] 敏感性/特异性满足临床需求
- [ ] 模型可解释性分析
- [ ] 外部验证（如有条件）

---

## Token 使用规范

### ⚠️ 严禁操作

| 禁止 | 原因 |
|------|------|
| ❌ 使用 Read 工具读取图像文件 | 每张图像消耗数千 token |
| ❌ 让 Claude 直接"看"医学影像 | 极度浪费 token |
| ❌ 在对话中传递图像内容 | 不必要的 token 消耗 |

### ✅ 正确做法

| 正确 | 说明 |
|------|------|
| ✅ 编写 Python 代码处理图像 | `cv2.imread()`, `PIL.Image.open()` |
| ✅ 使用 DataLoader 批量加载 | PyTorch/TensorFlow 数据加载器 |
| ✅ 只查看文本输出 | loss、accuracy、评估指标 |
| ✅ 读取生成的图表文件路径 | 告知用户图表位置，不读取图表本身 |

### 工作流程示意

```
Claude Code 职责              Python 代码职责
────────────────              ────────────────
编写数据加载代码      →       执行图像读取
编写训练代码          →       GPU 训练模型
运行 Bash 命令        →       处理所有图像数据
读取文本日志          ←       输出 loss/metrics
分析结果文本          ←       保存模型和图表

⚠️ 图像数据始终在 Python 进程中处理，不经过 Claude
```

---

## 交互风格

1. **语言**：中文交互
2. **分步执行**：每个阶段完成后确认再继续
3. **代码展示**：提供完整可运行代码
4. **进度反馈**：训练过程实时报告
5. **问题处理**：遇到错误主动诊断并提供解决方案

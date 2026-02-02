# 特征融合策略指南

## 融合方法概览

```
                    ┌─────────────────────────────────────────┐
                    │           融合策略选择                   │
                    └─────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
   ┌────▼────┐                  ┌─────▼─────┐                 ┌─────▼─────┐
   │Early    │                  │ Feature   │                 │ Late      │
   │Fusion   │                  │ Fusion    │                 │ Fusion    │
   │(简单)   │                  │ (推荐)    │                 │ (简单)    │
   └─────────┘                  └───────────┘                 └───────────┘
   原始特征拼接                  深度特征融合                   预测结果融合
```

| 策略 | 实现复杂度 | 性能 | 适用场景 |
|------|-----------|------|---------|
| Early Fusion | 低 | 中 | 快速实验 |
| Feature Fusion | 中 | 高 | **推荐** |
| Late Fusion | 低 | 中 | 模型已训练好 |
| Attention Fusion | 高 | 最高 | 追求极致性能 |

---

## Early Fusion (早期融合)

将影像特征（如全局统计量）与数值特征直接拼接，输入传统ML模型。

```python
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier

def extract_image_features(image_path):
    """
    从图像中提取手工特征
    """
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    features = []

    # 颜色统计
    for channel in cv2.split(img):
        features.extend([
            np.mean(channel),
            np.std(channel),
            np.median(channel),
            np.percentile(channel, 25),
            np.percentile(channel, 75),
        ])

    # 纹理特征 (灰度共生矩阵简化版)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features.extend([
        np.mean(gray),
        np.std(gray),
        cv2.Laplacian(gray, cv2.CV_64F).var(),  # 清晰度
    ])

    return np.array(features)

# 合并特征
def create_early_fusion_features(df, image_dir, tabular_columns):
    all_features = []

    for idx, row in df.iterrows():
        # 数值特征
        tabular_feat = row[tabular_columns].values

        # 图像特征
        img_path = os.path.join(image_dir, row['image_path'])
        image_feat = extract_image_features(img_path)

        # 拼接
        combined = np.concatenate([tabular_feat, image_feat])
        all_features.append(combined)

    return np.array(all_features)

# 训练
X_combined = create_early_fusion_features(train_df, image_dir, tabular_cols)
model = XGBClassifier()
model.fit(X_combined, y_train)
```

---

## Feature Fusion (特征融合) - 推荐

将CNN提取的深度特征与数值特征拼接，端到端训练。

### 完整实现

```python
import torch
import torch.nn as nn
from torchvision import models

class MultiModalFusionModel(nn.Module):
    """
    多模态特征融合模型
    - 图像分支：预训练 CNN 提取特征
    - 数值分支：MLP 处理表格数据
    - 融合层：拼接后通过 MLP
    """

    def __init__(
        self,
        num_tabular_features,
        num_classes,
        image_backbone='resnet18',
        pretrained=True,
        dropout=0.3,
    ):
        super().__init__()

        # ============ 图像分支 ============
        if image_backbone == 'resnet18':
            self.image_encoder = models.resnet18(pretrained=pretrained)
            image_feature_dim = self.image_encoder.fc.in_features
            self.image_encoder.fc = nn.Identity()
        elif image_backbone == 'resnet50':
            self.image_encoder = models.resnet50(pretrained=pretrained)
            image_feature_dim = self.image_encoder.fc.in_features
            self.image_encoder.fc = nn.Identity()
        elif image_backbone == 'efficientnet_b0':
            self.image_encoder = models.efficientnet_b0(pretrained=pretrained)
            image_feature_dim = self.image_encoder.classifier[1].in_features
            self.image_encoder.classifier = nn.Identity()
        else:
            raise ValueError(f"Unknown backbone: {image_backbone}")

        # ============ 数值分支 ============
        self.tabular_encoder = nn.Sequential(
            nn.Linear(num_tabular_features, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout),
        )
        tabular_feature_dim = 64

        # ============ 融合层 ============
        fusion_dim = image_feature_dim + tabular_feature_dim

        self.fusion_head = nn.Sequential(
            nn.Linear(fusion_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(256, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes),
        )

        # 保存维度信息
        self.image_feature_dim = image_feature_dim
        self.tabular_feature_dim = tabular_feature_dim

    def forward(self, image, tabular):
        # 图像特征
        img_features = self.image_encoder(image)

        # 数值特征
        tab_features = self.tabular_encoder(tabular)

        # 特征拼接
        fused = torch.cat([img_features, tab_features], dim=1)

        # 分类/回归输出
        output = self.fusion_head(fused)

        return output

    def get_features(self, image, tabular):
        """
        获取融合前的特征，用于可视化或分析
        """
        with torch.no_grad():
            img_features = self.image_encoder(image)
            tab_features = self.tabular_encoder(tabular)
        return img_features, tab_features
```

### Dataset 实现

```python
class MultiModalDataset(torch.utils.data.Dataset):
    def __init__(self, df, image_dir, tabular_columns, target_column, transform=None):
        self.df = df.reset_index(drop=True)
        self.image_dir = image_dir
        self.tabular_columns = tabular_columns
        self.target_column = target_column
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        # 加载图像
        img_path = os.path.join(self.image_dir, row['image_path'])
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']

        # 数值特征
        tabular = torch.tensor(
            row[self.tabular_columns].values.astype(np.float32),
            dtype=torch.float32
        )

        # 标签
        label = torch.tensor(row[self.target_column], dtype=torch.long)

        return image, tabular, label
```

### 训练循环

```python
def train_multimodal(model, train_loader, val_loader, config):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config['lr'])
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=config['epochs']
    )

    best_auc = 0

    for epoch in range(config['epochs']):
        # 训练
        model.train()
        train_loss = 0

        for images, tabular, labels in tqdm(train_loader):
            images = images.to(device)
            tabular = tabular.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(images, tabular)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            train_loss += loss.item()

        # 验证
        model.eval()
        all_probs = []
        all_labels = []

        with torch.no_grad():
            for images, tabular, labels in val_loader:
                images = images.to(device)
                tabular = tabular.to(device)

                outputs = model(images, tabular)
                probs = torch.softmax(outputs, dim=1)[:, 1]

                all_probs.extend(probs.cpu().numpy())
                all_labels.extend(labels.numpy())

        val_auc = roc_auc_score(all_labels, all_probs)

        print(f"Epoch {epoch+1}: Train Loss={train_loss/len(train_loader):.4f}, Val AUC={val_auc:.4f}")

        if val_auc > best_auc:
            best_auc = val_auc
            torch.save(model.state_dict(), 'best_multimodal.pth')

        scheduler.step()

    return model
```

---

## Late Fusion (后期融合)

分别训练图像模型和数值模型，最后融合预测结果。

```python
def late_fusion_predict(image_model, tabular_model, image, tabular_features):
    """
    后期融合：加权平均预测概率
    """
    # 图像模型预测
    img_prob = image_model.predict_proba(image)[:, 1]

    # 数值模型预测
    tab_prob = tabular_model.predict_proba(tabular_features)[:, 1]

    # 加权融合
    alpha = 0.6  # 图像权重
    fused_prob = alpha * img_prob + (1 - alpha) * tab_prob

    return fused_prob

# 也可以用 Stacking
from sklearn.ensemble import StackingClassifier

stacking_model = StackingClassifier(
    estimators=[
        ('image', image_model),
        ('tabular', tabular_model),
    ],
    final_estimator=LogisticRegression(),
    cv=5,
)
```

---

## Attention Fusion (注意力融合)

使用注意力机制动态加权不同模态的特征。

```python
class AttentionFusionModel(nn.Module):
    def __init__(self, num_tabular_features, num_classes):
        super().__init__()

        # 图像编码器
        self.image_encoder = models.resnet18(pretrained=True)
        img_dim = self.image_encoder.fc.in_features
        self.image_encoder.fc = nn.Identity()

        # 数值编码器
        self.tabular_encoder = nn.Sequential(
            nn.Linear(num_tabular_features, 256),
            nn.ReLU(),
            nn.Linear(256, img_dim),  # 投影到相同维度
        )

        # 注意力层
        self.attention = nn.Sequential(
            nn.Linear(img_dim * 2, 128),
            nn.Tanh(),
            nn.Linear(128, 2),
            nn.Softmax(dim=1),
        )

        # 分类器
        self.classifier = nn.Linear(img_dim, num_classes)

    def forward(self, image, tabular):
        # 提取特征
        img_feat = self.image_encoder(image)  # [B, D]
        tab_feat = self.tabular_encoder(tabular)  # [B, D]

        # 计算注意力权重
        concat_feat = torch.cat([img_feat, tab_feat], dim=1)  # [B, 2D]
        attention_weights = self.attention(concat_feat)  # [B, 2]

        # 加权融合
        img_weight = attention_weights[:, 0:1]  # [B, 1]
        tab_weight = attention_weights[:, 1:2]  # [B, 1]

        fused = img_weight * img_feat + tab_weight * tab_feat  # [B, D]

        # 分类
        output = self.classifier(fused)

        return output
```

---

## Cross-Modal Transformer (跨模态Transformer)

更高级的融合方式，使用 Transformer 实现跨模态交互。

```python
class CrossModalTransformer(nn.Module):
    def __init__(self, num_tabular_features, num_classes, d_model=256, nhead=8):
        super().__init__()

        # 图像编码器
        self.image_encoder = models.resnet18(pretrained=True)
        img_dim = self.image_encoder.fc.in_features
        self.image_encoder.fc = nn.Identity()

        # 投影层
        self.img_proj = nn.Linear(img_dim, d_model)
        self.tab_proj = nn.Linear(num_tabular_features, d_model)

        # 跨模态 Transformer
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=512,
            dropout=0.1,
            batch_first=True,
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=2)

        # 分类器
        self.classifier = nn.Sequential(
            nn.Linear(d_model * 2, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes),
        )

    def forward(self, image, tabular):
        # 特征提取
        img_feat = self.img_proj(self.image_encoder(image))  # [B, D]
        tab_feat = self.tab_proj(tabular)  # [B, D]

        # 构建序列 [img, tab]
        seq = torch.stack([img_feat, tab_feat], dim=1)  # [B, 2, D]

        # Transformer 编码
        encoded = self.transformer(seq)  # [B, 2, D]

        # 拼接两个 token
        fused = encoded.view(encoded.size(0), -1)  # [B, 2*D]

        output = self.classifier(fused)
        return output
```

---

## 融合策略对比实验模板

```python
def compare_fusion_strategies(train_df, val_df, image_dir, tabular_cols):
    results = {}

    # 1. 仅数值
    print("Training tabular-only model...")
    tab_model = XGBClassifier()
    tab_model.fit(train_df[tabular_cols], train_df['target'])
    tab_auc = evaluate(tab_model, val_df[tabular_cols], val_df['target'])
    results['Tabular Only'] = tab_auc

    # 2. 仅图像
    print("Training image-only model...")
    img_model = train_image_model(train_df, val_df, image_dir)
    img_auc = evaluate_image_model(img_model, val_df, image_dir)
    results['Image Only'] = img_auc

    # 3. Early Fusion
    print("Training early fusion model...")
    early_features = create_early_fusion_features(train_df, image_dir, tabular_cols)
    early_model = XGBClassifier()
    early_model.fit(early_features, train_df['target'])
    early_auc = evaluate_early_fusion(early_model, val_df, image_dir, tabular_cols)
    results['Early Fusion'] = early_auc

    # 4. Feature Fusion
    print("Training feature fusion model...")
    fusion_model = MultiModalFusionModel(len(tabular_cols), 2)
    train_multimodal(fusion_model, train_loader, val_loader, config)
    fusion_auc = evaluate_multimodal(fusion_model, val_loader)
    results['Feature Fusion'] = fusion_auc

    # 5. Late Fusion
    print("Training late fusion model...")
    late_auc = evaluate_late_fusion(img_model, tab_model, val_df)
    results['Late Fusion'] = late_auc

    # 打印对比结果
    print("\n" + "="*50)
    print("Fusion Strategy Comparison")
    print("="*50)
    for strategy, auc in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"{strategy:20s}: AUC = {auc:.4f}")

    return results
```

---

## 选择建议

| 场景 | 推荐策略 |
|------|---------|
| 快速实验 / 基线 | Late Fusion |
| 中小数据集 | Feature Fusion |
| 大数据集 + 追求性能 | Attention Fusion |
| 研究 / 论文 | Cross-Modal Transformer |
| 1660Ti (6GB显存) | **Feature Fusion (ResNet-18)** |

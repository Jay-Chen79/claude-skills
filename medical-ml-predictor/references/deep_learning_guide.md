# 深度学习指南

## 硬件配置建议

| GPU | 显存 | 推荐配置 |
|-----|------|---------|
| GTX 1660 Ti | 6GB | ResNet-18/34, EfficientNet-B0/B1, batch=8-16 |
| RTX 3060 | 12GB | ResNet-50, EfficientNet-B2/B3, batch=16-32 |
| RTX 3080 | 10GB | EfficientNet-B4, ViT-Small, batch=16-32 |
| RTX 4090 | 24GB | 大模型随意 |

---

## PyTorch 环境配置

```bash
# CUDA 11.8 + PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 验证 GPU
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 网络架构

### ResNet (推荐入门)

```python
import torch
import torch.nn as nn
from torchvision import models

class ResNetClassifier(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        super().__init__()
        # 加载预训练 ResNet-18
        self.backbone = models.resnet18(pretrained=pretrained)

        # 替换最后一层
        in_features = self.backbone.fc.in_features
        self.backbone.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)

# 使用
model = ResNetClassifier(num_classes=2, pretrained=True)
```

### EfficientNet (高效)

```python
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

class EfficientNetClassifier(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        super().__init__()
        weights = EfficientNet_B0_Weights.DEFAULT if pretrained else None
        self.backbone = efficientnet_b0(weights=weights)

        in_features = self.backbone.classifier[1].in_features
        self.backbone.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(in_features, num_classes)
        )

    def forward(self, x):
        return self.backbone(x)
```

### Inception-ResNet-v2 (如流程图所示)

```python
# 需要安装 timm 库
pip install timm

import timm

class InceptionResNetClassifier(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        super().__init__()
        self.backbone = timm.create_model(
            'inception_resnet_v2',
            pretrained=pretrained,
            num_classes=num_classes
        )

    def forward(self, x):
        return self.backbone(x)

# 注意：Inception-ResNet 需要 299x299 输入
# 显存需求较大，6GB 显卡需要 batch_size=4-8
```

### Vision Transformer (ViT)

```python
import timm

class ViTClassifier(nn.Module):
    def __init__(self, num_classes, pretrained=True):
        super().__init__()
        self.backbone = timm.create_model(
            'vit_small_patch16_224',  # 较小的 ViT
            pretrained=pretrained,
            num_classes=num_classes
        )

    def forward(self, x):
        return self.backbone(x)
```

---

## 训练循环

### 完整训练脚本

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from tqdm import tqdm

class Trainer:
    def __init__(self, model, train_loader, val_loader, config):
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.config = config

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

        # 损失函数
        self.criterion = nn.CrossEntropyLoss()

        # 优化器
        self.optimizer = optim.AdamW(
            model.parameters(),
            lr=config['lr'],
            weight_decay=config['weight_decay']
        )

        # 学习率调度
        self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer,
            T_max=config['epochs']
        )

        # 早停
        self.best_val_loss = float('inf')
        self.patience_counter = 0

    def train_epoch(self):
        self.model.train()
        total_loss = 0
        correct = 0
        total = 0

        pbar = tqdm(self.train_loader, desc='Training')
        for images, labels in pbar:
            images = images.to(self.device)
            labels = labels.to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(images)
            loss = self.criterion(outputs, labels)
            loss.backward()
            self.optimizer.step()

            total_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })

        return total_loss / len(self.train_loader), correct / total

    def validate(self):
        self.model.eval()
        total_loss = 0
        correct = 0
        total = 0
        all_probs = []
        all_labels = []

        with torch.no_grad():
            for images, labels in tqdm(self.val_loader, desc='Validating'):
                images = images.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(images)
                loss = self.criterion(outputs, labels)

                total_loss += loss.item()
                probs = torch.softmax(outputs, dim=1)
                _, predicted = outputs.max(1)

                total += labels.size(0)
                correct += predicted.eq(labels).sum().item()

                all_probs.extend(probs[:, 1].cpu().numpy())
                all_labels.extend(labels.cpu().numpy())

        from sklearn.metrics import roc_auc_score
        auc = roc_auc_score(all_labels, all_probs)

        return total_loss / len(self.val_loader), correct / total, auc

    def train(self):
        for epoch in range(self.config['epochs']):
            print(f"\nEpoch {epoch+1}/{self.config['epochs']}")

            train_loss, train_acc = self.train_epoch()
            val_loss, val_acc, val_auc = self.validate()
            self.scheduler.step()

            print(f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")
            print(f"Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}, Val AUC: {val_auc:.4f}")

            # 保存最优模型
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.patience_counter = 0
                torch.save(self.model.state_dict(), 'best_model.pth')
                print("Saved best model!")
            else:
                self.patience_counter += 1

            # 早停
            if self.patience_counter >= self.config['patience']:
                print(f"Early stopping at epoch {epoch+1}")
                break

        return self.model

# 使用示例
config = {
    'epochs': 50,
    'lr': 1e-4,
    'weight_decay': 1e-4,
    'patience': 10,
}

trainer = Trainer(model, train_loader, val_loader, config)
trained_model = trainer.train()
```

---

## 显存优化技巧

### 1. 减小 Batch Size

```python
# 6GB 显卡推荐
train_loader = DataLoader(dataset, batch_size=8, shuffle=True)
```

### 2. 梯度累积

```python
accumulation_steps = 4  # 等效 batch_size = 8 * 4 = 32

for i, (images, labels) in enumerate(train_loader):
    outputs = model(images)
    loss = criterion(outputs, labels)
    loss = loss / accumulation_steps
    loss.backward()

    if (i + 1) % accumulation_steps == 0:
        optimizer.step()
        optimizer.zero_grad()
```

### 3. 混合精度训练 (FP16)

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for images, labels in train_loader:
    optimizer.zero_grad()

    with autocast():
        outputs = model(images)
        loss = criterion(outputs, labels)

    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```

### 4. 梯度检查点 (省显存换时间)

```python
from torch.utils.checkpoint import checkpoint

class MemoryEfficientModel(nn.Module):
    def forward(self, x):
        # 使用 checkpoint 包装计算密集的层
        x = checkpoint(self.layer1, x)
        x = checkpoint(self.layer2, x)
        return x
```

---

## 回归任务修改

```python
# 修改输出层
self.backbone.fc = nn.Linear(in_features, 1)  # 单值回归

# 修改损失函数
criterion = nn.MSELoss()  # 或 nn.L1Loss()

# 修改标签类型
labels = labels.float()
```

---

## 迁移学习策略

### 策略1：仅训练最后一层

```python
# 冻结所有层
for param in model.parameters():
    param.requires_grad = False

# 解冻最后一层
for param in model.backbone.fc.parameters():
    param.requires_grad = True
```

### 策略2：分层学习率

```python
# 底层小学习率，顶层大学习率
param_groups = [
    {'params': model.backbone.layer1.parameters(), 'lr': 1e-5},
    {'params': model.backbone.layer2.parameters(), 'lr': 5e-5},
    {'params': model.backbone.layer3.parameters(), 'lr': 1e-4},
    {'params': model.backbone.layer4.parameters(), 'lr': 5e-4},
    {'params': model.backbone.fc.parameters(), 'lr': 1e-3},
]

optimizer = optim.AdamW(param_groups)
```

### 策略3：渐进解冻

```python
# 第1阶段：只训练 fc
# 第2阶段：解冻 layer4
# 第3阶段：解冻 layer3
# ...
```

---

## 模型保存与加载

```python
# 保存完整模型
torch.save(model.state_dict(), 'model.pth')

# 加载
model = ResNetClassifier(num_classes=2)
model.load_state_dict(torch.load('model.pth'))
model.eval()

# 保存训练状态（用于恢复训练）
torch.save({
    'epoch': epoch,
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
    'loss': loss,
}, 'checkpoint.pth')
```

---

## 推理代码

```python
def predict(model, image_path, transform):
    model.eval()
    device = next(model.parameters()).device

    # 加载并预处理图像
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    augmented = transform(image=image)
    image_tensor = augmented['image'].unsqueeze(0).to(device)

    # 推理
    with torch.no_grad():
        output = model(image_tensor)
        prob = torch.softmax(output, dim=1)
        pred_class = prob.argmax(dim=1).item()
        confidence = prob.max().item()

    return pred_class, confidence
```

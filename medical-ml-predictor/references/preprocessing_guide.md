# 数据预处理指南

## 数值数据预处理

### 1. 缺失值处理

```python
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer, KNNImputer

# 检查缺失值
def check_missing(df):
    missing = df.isnull().sum()
    missing_pct = missing / len(df) * 100
    return pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct})

# 删除策略（缺失>50%的列）
def drop_high_missing(df, threshold=0.5):
    cols_to_drop = df.columns[df.isnull().mean() > threshold]
    return df.drop(columns=cols_to_drop)

# 填充策略
def impute_missing(df, strategy='median'):
    """
    strategy: 'mean', 'median', 'most_frequent', 'knn'
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    if strategy == 'knn':
        imputer = KNNImputer(n_neighbors=5)
    else:
        imputer = SimpleImputer(strategy=strategy)

    df[numeric_cols] = imputer.fit_transform(df[numeric_cols])
    return df
```

### 2. 异常值处理

```python
from scipy import stats

# IQR 方法
def detect_outliers_iqr(df, columns, threshold=1.5):
    outlier_indices = []
    for col in columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_mask = (df[col] < Q1 - threshold * IQR) | (df[col] > Q3 + threshold * IQR)
        outlier_indices.extend(df[outlier_mask].index.tolist())
    return list(set(outlier_indices))

# Z-score 方法
def detect_outliers_zscore(df, columns, threshold=3):
    outlier_indices = []
    for col in columns:
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        outlier_mask = z_scores > threshold
        outlier_indices.extend(df[col].dropna()[outlier_mask].index.tolist())
    return list(set(outlier_indices))

# 处理方式：截断到边界
def clip_outliers(df, columns, lower_pct=1, upper_pct=99):
    for col in columns:
        lower = df[col].quantile(lower_pct / 100)
        upper = df[col].quantile(upper_pct / 100)
        df[col] = df[col].clip(lower, upper)
    return df
```

### 3. 特征缩放

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# 标准化（推荐）
scaler = StandardScaler()  # mean=0, std=1

# 归一化
scaler = MinMaxScaler()  # [0, 1]

# 鲁棒缩放（对异常值不敏感）
scaler = RobustScaler()  # 使用中位数和四分位数

# 使用示例
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # 注意：只 transform，不 fit

# 保存 scaler
import joblib
joblib.dump(scaler, 'scaler.pkl')
```

### 4. 类别特征编码

```python
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import category_encoders as ce

# Label Encoding（有序类别）
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# One-Hot Encoding（无序类别，类别数少）
df_encoded = pd.get_dummies(df, columns=['category'], drop_first=True)

# Target Encoding（类别数多，如科室、诊断码）
encoder = ce.TargetEncoder(cols=['category'])
df['category_encoded'] = encoder.fit_transform(df['category'], df['target'])
```

### 5. 数据集划分

```python
from sklearn.model_selection import train_test_split, StratifiedKFold

# 简单划分
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # 分类任务保持类别比例
)

# 进一步划分验证集
X_train, X_val, y_train, y_val = train_test_split(
    X_train, y_train,
    test_size=0.125,  # 0.8 * 0.125 = 0.1
    random_state=42,
    stratify=y_train
)

# 交叉验证
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(X, y):
    X_train_fold, X_val_fold = X[train_idx], X[val_idx]
    y_train_fold, y_val_fold = y[train_idx], y[val_idx]
```

---

## 影像数据预处理

### 1. 基础预处理

```python
import cv2
from PIL import Image
import numpy as np

def preprocess_image(image_path, target_size=(224, 224)):
    """
    基础影像预处理
    """
    # 读取图像
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 调整尺寸
    img = cv2.resize(img, target_size)

    # 归一化到 [0, 1]
    img = img / 255.0

    return img

# ImageNet 标准化
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

def normalize_imagenet(img):
    img = (img - IMAGENET_MEAN) / IMAGENET_STD
    return img
```

### 2. 数据增强（Albumentations）

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

# 训练集增强
train_transform = A.Compose([
    A.RandomResizedCrop(224, 224, scale=(0.8, 1.0)),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.1, rotate_limit=15, p=0.5),
    A.OneOf([
        A.GaussNoise(var_limit=(10, 50)),
        A.GaussianBlur(blur_limit=3),
        A.MotionBlur(blur_limit=3),
    ], p=0.2),
    A.OneOf([
        A.OpticalDistortion(distort_limit=0.05),
        A.GridDistortion(distort_limit=0.05),
    ], p=0.2),
    A.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1, p=0.3),
    A.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ToTensorV2(),
])

# 验证/测试集（不增强）
val_transform = A.Compose([
    A.Resize(224, 224),
    A.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ToTensorV2(),
])
```

### 3. PyTorch Dataset

```python
from torch.utils.data import Dataset, DataLoader

class MedicalImageDataset(Dataset):
    def __init__(self, df, image_dir, transform=None):
        self.df = df
        self.image_dir = image_dir
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        # 加载图像
        img_path = os.path.join(self.image_dir, row['image_path'])
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 应用变换
        if self.transform:
            augmented = self.transform(image=image)
            image = augmented['image']

        # 获取标签
        label = row['target']

        return image, label

# 创建 DataLoader
train_dataset = MedicalImageDataset(train_df, image_dir, train_transform)
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True, num_workers=4)
```

### 4. 多模态 Dataset

```python
class MultiModalDataset(Dataset):
    def __init__(self, df, image_dir, tabular_columns, transform=None):
        self.df = df
        self.image_dir = image_dir
        self.tabular_columns = tabular_columns
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]

        # 图像数据
        img_path = os.path.join(self.image_dir, row['image_path'])
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.transform:
            image = self.transform(image=image)['image']

        # 数值数据
        tabular = torch.tensor(row[self.tabular_columns].values, dtype=torch.float32)

        # 标签
        label = torch.tensor(row['target'], dtype=torch.long)  # 分类
        # label = torch.tensor(row['target'], dtype=torch.float32)  # 回归

        return image, tabular, label
```

---

## 医学影像特殊处理

### 眼科影像

```python
# 眼底图像预处理
def preprocess_fundus(image):
    # 绿色通道增强（血管更清晰）
    green_channel = image[:, :, 1]

    # CLAHE 增强对比度
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(green_channel)

    return enhanced

# 角膜地形图处理
def preprocess_topography(image):
    # 通常已经是热力图，直接 resize 即可
    image = cv2.resize(image, (224, 224))
    return image
```

### CT/MRI 影像

```python
# 窗宽窗位调整（CT）
def apply_window(image, window_center, window_width):
    min_value = window_center - window_width // 2
    max_value = window_center + window_width // 2
    image = np.clip(image, min_value, max_value)
    image = (image - min_value) / (max_value - min_value)
    return image

# 常用窗位
WINDOWS = {
    'lung': (center=-600, width=1500),
    'mediastinum': (center=40, width=400),
    'bone': (center=400, width=1800),
    'brain': (center=40, width=80),
}
```

---

## 类别不平衡处理

```python
from imblearn.over_sampling import SMOTE, RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler

# SMOTE 过采样
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

# 类别权重（用于损失函数）
from sklearn.utils.class_weight import compute_class_weight

class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weights = torch.tensor(class_weights, dtype=torch.float32)

# PyTorch 中使用
criterion = nn.CrossEntropyLoss(weight=class_weights)
```

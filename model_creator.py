import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle
import time
import os

class ModelCreator:
    def __init__(self, config, patient_ID=None, mode='train'):
        self.config = config  # Lưu config để truy cập các đường dẫn
        self.mode = mode

        # Khởi tạo mô hình và bộ tiền xử lý trước
        if self.mode == 'test':
            self.model = xgb.XGBClassifier()
            self.model.load_model(self.config.model_checkpoint_path)
            # Tải scaler và label_encoders từ file pickle
            with open(self.config.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            if os.path.exists(self.config.encoders_path):
                with open(self.config.encoders_path, 'rb') as f:
                    self.label_encoders = pickle.load(f)
                if not isinstance(self.label_encoders, dict) or not self.label_encoders:
                    raise ValueError("Invalid or empty label_encoders loaded from encoders.pkl")
            else:
                raise FileNotFoundError(f"{self.config.encoders_path} not found. Please ensure it is created during training.")
        elif self.mode == 'train':
            self.model = xgb.XGBClassifier(random_state=2, max_depth=10, learning_rate=0.1)
            self.scaler = StandardScaler()
            self.label_encoders = {}
        else:
            raise ValueError("mode must be 'train' or 'test'.")

        # Đọc dữ liệu
        try:
            if self.mode == 'train':
                self.data = pd.read_excel(self.config.submited_data_path, sheet_name='Sheet_name_1')
            elif self.mode == 'test':
                self.data = pd.read_excel(self.config.unsubmited_data_path, sheet_name='Sheet_name_1')
                if not patient_ID:
                    raise ValueError('The patient ID is None')
                else:
                    self.data = self.data[self.data['ID'] == patient_ID]
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")

        # Gọi preprocess_data nếu dữ liệu không rỗng
        if not self.data.empty:
            self.preprocess_data()

    def preprocess_data(self):
        # Ánh xạ tên cột từ ứng dụng sang dữ liệu huấn luyện
        column_mapping = {
            'NAMSINH': 'Nam_Sinh',
            'SOLANMAN': 'So_Lan_Mang_Thai',
            'SOCONSINH': 'So_Lan_Sinh_Con',
            'TRANHTHA': 'Tien_Su_Tranh_Thai',
            'GDINHRAM': 'Tien_Su_Gia_Dinh',
            'RAMMAMAN': 'Tien_Su_MangThai',
            'NGHENGHI': 'Nghe_Nghiep',
            'HOCVAN': 'Trinh_Do_Hoc_Van',
            'HONNHAN': 'Tinh_Trang_hon_nhan'
        }
        self.data = self.data.rename(columns=column_mapping)

        # Tính tuổi
        self.data['Tuoi'] = time.localtime().tm_year - self.data['Nam_Sinh']

        # Định nghĩa đặc trưng
        self.selected_columns = [
            'Tuoi', 'So_Lan_Mang_Thai', 'So_Lan_Sinh_Con',
            'Tien_Su_Tranh_Thai', 'Tien_Su_Gia_Dinh', 'Tien_Su_MangThai',
            'Nghe_Nghiep', 'Trinh_Do_Hoc_Van', 'Tinh_Trang_hon_nhan'
        ]

        # Mã hóa biến categorical
        categorical_cols = ['Nghe_Nghiep', 'Trinh_Do_Hoc_Van', 'Tinh_Trang_hon_nhan', 'Tien_Su_Tranh_Thai']
        if self.mode == 'train':
            for col in categorical_cols:
                le = LabelEncoder()
                self.data[col] = le.fit_transform(self.data[col])
                self.label_encoders[col] = le
        elif self.mode == 'test':
            for col in categorical_cols:
                if col not in self.label_encoders:
                    raise ValueError(f"LabelEncoder for column '{col}' not found in loaded encoders")
                le = self.label_encoders[col]
                # Xử lý giá trị chưa thấy bằng cách ánh xạ về lớp đầu tiên
                self.data[col] = self.data[col].apply(lambda x: x if pd.notna(x) and x in le.classes_ else le.classes_[0] if le.classes_.size > 0 else x)
                self.data[col] = le.transform(self.data[col])
        # Chuẩn hóa biến numerical
        numerical_cols = ['Tuoi', 'So_Lan_Mang_Thai', 'So_Lan_Sinh_Con']
        if self.mode == 'train':
            self.data[numerical_cols] = self.scaler.fit_transform(self.data[numerical_cols])
        elif self.mode == 'test':
            self.data[numerical_cols] = self.scaler.transform(self.data[numerical_cols])

        # Định nghĩa nhãn (chỉ cho huấn luyện)
        if self.mode == 'train':
            self.data['Label'] = self.data['RAMMA'].apply(lambda x: 0 if x == 'khong' else 1 if pd.notna(x) else np.nan)

    def train(self):
        train, valid = train_test_split(self.data, test_size=0.1, random_state=7, stratify=self.data['Label'])
        valid, test = train_test_split(valid, test_size=0.3, random_state=7, stratify=valid['Label'])
        self.model.fit(train[self.selected_columns], train['Label'])
        self.model.save_model(self.config.model_checkpoint_path)
        with open(self.config.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        with open(self.config.encoders_path, 'wb') as f:
            pickle.dump(self.label_encoders, f)

    def predict(self):
        return self.model.predict_proba(self.data[self.selected_columns])
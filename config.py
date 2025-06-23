import time

class Config():
    def __init__(self):
        self.unsubmited_data_path   = r"C:\\Users\\XUAN TUYEN\\Desktop\\HospitalAI\\HospitalAI\\storages\\database\\unsubmited_data.xlsx"
        self.submited_data_path     = r"C:\\Users\\XUAN TUYEN\\Desktop\\HospitalAI\\HospitalAI\\storages\\database_V1\\submited_data.xlsx"
        self.knowledgeTest_path     = r"C:\\Users\\XUAN TUYEN\\Desktop\\HospitalAI\\HospitalAI\\storages\\database\\knowledgeTest_data.xlsx"
        self.model_checkpoint_path  = r'C:\\Users\\XUAN TUYEN\\Desktop\\HospitalAI\\HospitalAI\\my_trained_model.model'
        self.scaler_path            = r'C:\\Users\\XUAN TUYEN\\Desktop\\HospitalAI\\HospitalAI\\scaler.pkl'    # Thêm đường dẫn tuyệt đối
        self.encoders_path          = r'C:\\Users\\XUAN TUYEN\\Desktop\\HospitalAI\\HospitalAI\\encoders.pkl'  # Thêm đường dẫn tuyệt đối
        self.training_features      = ['Age', 'Education_level', 'Job_1', 'Job_2', 'Job_3', 'Job_4', 'Job_5',
                                       'Economy_level', 'Num_of_pregnant', 'Num_of_child', 'Family_history',
                                       'status_when_pregnant', 'Unamed_1',
                                       'Health_history_1', 'Health_history_2', 'Health_history_3', 'Health_history_4',
                                       'Time_in_the_sun', 'Morning_in_the_sun', 'Noon_in_the_sun',
                                       'Afternoon_in_the_sun', 'Use_cosmetics', 'Source', 'From_1', 'From_2',
                                       'From_3', 'From_4', 'From_5', 'From_6', 'From_7', 'From_8', 'Price',
                                       'Purpose_1', 'Purpose_2', 'Purpose_3', 'Purpose_4', 'Start_cosmetics']
        self.current_year           = time.localtime().tm_year
import os
import pandas as pd
import time
import numpy as np
from config import Config
from xgboost import XGBClassifier
from flask import Flask, render_template, redirect, request, url_for
from model_creator import ModelCreator

app = Flask(__name__)
config = Config()


@app.route('/')
def welcome():
    return redirect('/home')

@app.route('/home', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return redirect('/survey')
    return render_template('index.html')

@app.route('/exception_case', methods=['GET', 'POST'])
def exception_case():
    return render_template('exception_case.html')

@app.route('/survey', methods=['GET', 'POST'])
def survey():
    if 'area' not in request.form:
#        print(request.form)
        gender = request.form['gender']
        name = request.form['name']
        bd_year = request.form['bd_year']
        bd_month = request.form['bd_month']
        current_age = config.current_year-int(bd_year)
        if gender=='0' or current_age<18 or current_age>55:
            return redirect("/exception_case")
        else:
            return render_template('patient_01_SurveyCollection.html', name = name, bd_year = bd_year, bd_month = bd_month)
    else:
        name = request.form['name']          
#        print(name)
        bd_year = request.form['bd_year']   
        bd_month = request.form['bd_month']
        area = request.form['area']           
        phone = request.form['phone']                                                   
        nation = request.form['nation']                                                                 #2
        job = request.form['job']                                                                       #3
        education = request.form['education']                                                           #4
        married = request.form['married']                                                               #5
        number_of_pregnancies = request.form['number_of_pregnancies']                                   #6
        number_of_children_born = request.form['number_of_children_born']                               #7
        prehistoric_frame_has_pregnant = request.form['prehistoric_frame_has_pregnant']                 #8
        contraception = request.form['contraception']                                                   #9
        prehistoric_famaly_frame_has = request.form['prehistoric_famaly_frame_has']                     #10
        prehistoric_frame_has_pregnant_month = request.form['prehistoric_frame_has_pregnant_month']
        pathological = request.form['pathological']                                                     #11 
        # pathological_name = request.form['pathological_name']                                           #11 

        try:                                         #12
            Health_history_1 = int(request.form['pathological_name1'])
        except:
            Health_history_1 = 0
        try:                                         #12
            Health_history_2 = int(request.form['pathological_name2'])
        except:
            Health_history_2 = 0
        try:                                         #12
            Health_history_3 = int(request.form['pathological_name2'])
        except:
            Health_history_3 = 0
        try:                                         #12
            Health_history_4 = int(request.form['pathological_name2'])
        except:
            Health_history_4 = 0


        
        time_contact_light = request.form['time_contact_light']
        try:                                         #12
            morning = int(request.form['contact_light_session1'])
        except:
            morning = 2
        try:                                         #12
            noon = int(request.form['contact_light_session2'])
        except:
            noon = 2
        try:                                         #12
            afternoon = int(request.form['contact_light_session2'])
        except:
            afternoon = 2
        

        TSUHOACH = request.form['TSUHOACH']                                                             #16
        TENHOACH = request.form['TENHOACH']                                                             #17
        if('0' in TENHOACH):
            TENHOACH = None
        
        
        age_cosmetic = request.form['age_cosmetic']                                                     #19
        name_cosmectic = request.form['name_cosmectic']                                                 #20
        country_of_manufacture = request.form['country_of_manufacture']                                 #21

        
        bought_place = request.form['bought_place']                                                     #22
        if('0' in bought_place):
           bought_place = None

        price = request.form['price']                                                                   #23

        White_skin = 1                                                                                  #24
        melasma_cure = 1                                                                                #25
        wrinkled_skin = 1                                                                               #26
        another_purpose = 1                                                                             #27
        try:                                         #12
            White_skin = int(request.form['cosmectic_purpose1'])
        except:
            White_skin = 2
        try:                                         #12
            melasma_cure = int(request.form['cosmectic_purpose2'])
        except:
            melasma_cure = 2
        try:                                         #12
            wrinkled_skin = int(request.form['cosmectic_purpose3'])
        except:
            wrinkled_skin = 2
        try:                                         #12
            another_purpose = int(request.form['cosmectic_purpose4'])
        except:
            another_purpose = 2
        
        # if not using cosmtic auto default None
        use_cosmetic = request.form['use_cosmetic']                                     #18
        if('2' in use_cosmetic):
            age_cosmetic = None
            name_cosmectic = None
            country_of_manufacture = None
            bought_place = None
            price = None
            White_skin = None
            melasma_cure = None
            wrinkled_skin = None
            another_purpose = None
            
        

        # Defaul None
        THANGTHA= None                                                                  #28
        economy = None                                                                  #29
        group_age_1 = None                                                              #30


        TAPHOA = SIEUTHI = CHO = XACHTAY = BANBE = DAILY = NHATHUOC = MUAKHAC = 'khong'
        if bought_place==1:
            TAPHOA = 'co'
        elif bought_place==2:
            SIEUTHI = 'co'
        elif bought_place==3:
            CHO = 'co'
        elif bought_place==4:
            XACHTAY = 'co'
        elif bought_place==5:
            BANBE = 'co'
        elif bought_place==6:
            DAILY = 'co'
        elif bought_place==7:
            NHATHUOC = 'co'
        elif bought_place==8:
            MUAKHAC = 'co'
        patient_ID = "".join([i[0] for i in name.split(" ")])+"%s%s"%(str(time.time())[-3:],np.random.randint(low = 100, high = 999, size=1)[0])
        data = {'ID':[patient_ID],
                'NAME':[name],
                'AGE':[config.current_year - int(bd_year)],
                'KHUVUC':[area],
                'SDT':[phone],
                'NAMSINH':[bd_year],
                'NGHENGHI':[job],
                'DANTOC':[nation],
                'HOCVAN':[education],
                'KINHTE':None,
                'HONNHAN':[married],
                'SOLANMAN':[number_of_pregnancies],
                'SOCONSINH':[number_of_children_born],
                'TRANHTHA':[contraception],
                'GDINHRAM':[prehistoric_famaly_frame_has],
                'RAMMAMAN':[prehistoric_frame_has_pregnant], 
                'THANGTHA':[prehistoric_frame_has_pregnant_month],
                # 'BENHLY':[pathological_name],
                'BENHLY1':[Health_history_1],
                'BENHLY2':[Health_history_2],
                'BENHLY3':[Health_history_3],
                'BENHLY4':[Health_history_4],
                'SOGIOTIE':[time_contact_light],
                'BUOISANG':[morning],
                'BUOITRUA':[noon],
                'BUOICHIE':[afternoon],                
                'TSUHOACH':[TSUHOACH],
                'TENHOACH':[TENHOACH],
                'SDMYPHAM':[use_cosmetic],
                'TUOIMYPH':[age_cosmetic],
                'TENMPHAM':[name_cosmectic],
                'NUOCSX':[country_of_manufacture],
                'GIATIEN':[price],       
                'TRANGDA':[White_skin],
                'CHUANAM':[melasma_cure],
                'NHANDA':[wrinkled_skin],
                'MDICHKHA':[another_purpose],
                'TAPHOA':[TAPHOA],
                'SIEUTHI':[SIEUTHI],
                'CHO':[CHO],
                'XACHTAY':[XACHTAY],
                'BANBE':[BANBE],
                'DAILY':[DAILY],
                'NHATHUOC':[NHATHUOC],
                'MUAKHAC':[MUAKHAC],
                'RAMMA':None,
                'DETAIL':None,
                'prediction':None
        }
        if os.path.exists(config.unsubmited_data_path):
            database = pd.read_excel(config.unsubmited_data_path)
            df = pd.DataFrame(data)
            database = pd.concat([database, df])
        else:
            database = pd.DataFrame.from_dict(data)
        database.to_excel(config.unsubmited_data_path,sheet_name='Sheet_name_1')

        return redirect(url_for('knowledgeTest',patient_ID=patient_ID))


@app.route('/knowledgeTest', methods=['GET', 'POST'])
def knowledgeTest():
    if request.method == 'POST':
        QA01 = int(request.form['QA01'])==1
        QA02 = int(request.form['QA02'])==1
        QA03 = int(request.form['QA03'])==1
        QA04 = int(request.form['QA04'])==1
        QA05 = int(request.form['QA05'])==1
        QA06 = int(request.form['QA06'])==1
        QA07 = int(request.form['QA07'])==1
        QA08 = int(request.form['QA08'])==0
        QA09 = int(request.form['QA09'])==1

        QB01 = int(request.form['QB01'])==1
        QB02 = int(request.form['QB02'])==1
        QB03 = int(request.form['QB03'])==1
        QB04 = int(request.form['QB04'])==0
        QB05 = int(request.form['QB05'])==1
        QB06 = int(request.form['QB06'])==1
        QB07 = int(request.form['QB07'])==1
        QB08 = int(request.form['QB08'])==1
        QB09 = int(request.form['QB09'])==1

        pantient_theory_answer   = [QA01,QA02,QA03,QA04,QA05,QA06,QA07,QA08,QA09]
        pantient_practice_answer = [QB01,QB02,QB03,QB04,QB05,QB06,QB07,QB08,QB09]
        patient_ID =  request.form['patient_ID']
        if os.path.exists(config.knowledgeTest_path):
            database = pd.read_excel(config.knowledgeTest_path,sheet_name='Sheet_name_1',)
        else:
            database = pd.DataFrame()
        data =  {'ID':[patient_ID],
                 'QA01':[QA01],'QA02':[QA02],'QA03':[QA03],'QA04':[QA04],'QA05':[QA05],'QA06':[QA06],'QA07':[QA07],'QA08':[QA08],'QA09':[QA09],
                 'QB01':[QB01],'QB02':[QB02],'QB03':[QB03],'QB04':[QB04],'QB05':[QB05],'QB06':[QB06],'QB07':[QB07],'QB08':[QB08],'QB09':[QB09]}    
        data = pd.DataFrame.from_dict(data)            
        database = pd.concat([database, data])
        database.to_excel(config.knowledgeTest_path,sheet_name='Sheet_name_1',)
        
        return redirect(url_for('loadModel',patient_ID=patient_ID, theory_results = pantient_theory_answer.count(True), practice_results = pantient_practice_answer.count(True)))
    patient_ID = request.args.get('patient_ID',type = str)
    return render_template('patient_02_KnowlegdeTest.html',patient_ID=patient_ID)



@app.route('/loadModel', methods = ['GET'])
def loadModel():
    database = pd.read_excel(config.unsubmited_data_path, sheet_name='Sheet_name_1')
    patient_ID = request.args.get('patient_ID',type = str)
    patient_data = database[database['ID']==patient_ID]
    name = patient_data['NAME'].values[0]
    theory_results = request.args.get('theory_results',type = int)
    practice_results = request.args.get('practice_results',type = int)
    print(theory_results)
    print(practice_results)
    model = ModelCreator(config, patient_ID=patient_ID, mode='test')
    output = model.predict()
    output = ((output[0][1]*10000)//1)/100
    database.loc[database['ID']==patient_ID,'prediction']=output
    database.to_excel(config.unsubmited_data_path,sheet_name = 'Sheet_name_1')
    if theory_results+practice_results==18:
        message = "Bạn đã đạt trả lời đúng 18/18 câu hỏi trong khi khảo sát."
    else:
        message = "Bạn đã đạt trả lời đúng %s/9 câu hỏi về kiến thức cơ bản và %s/9 câu hỏi về thực hành."%(theory_results,practice_results)
    return render_template('patient_03_PredictionResults.html',data=output, message = message, patient_ID = patient_ID, name = name)

@app.route('/getInfo',methods = ['GET','POST'])
def get_sample():
    if request.method == 'POST':
        try:
            patient_ID = request.form['patient_ID']
            return redirect(url_for('info_display',patient_ID = patient_ID))
        except:
            return render_template('doctor_01_GetPatientInfo.html')
    else:
        return render_template('doctor_01_GetPatientInfo.html')

@app.route('/wrongID',methods = ['GET','POST'])
def wrongID_display():
    if request.method == 'POST':
        return redirect('/getInfo')
    return render_template('doctor_03_WrongID.html')


@app.route('/infoDisplay',methods = ['GET','POST'])
def info_display():

    if request.method == 'POST':
        database = pd.read_excel(config.unsubmited_data_path, sheet_name='Sheet_name_1')      
        patient_ID = request.args.get('patient_ID',type = str)
        
        print("="*100)
        print(patient_ID)
        print("="*100)
        patient_data = database[database['ID']==patient_ID]
        print(patient_data)  
        results = request.form['results']
        detail = request.form['detail']
        patient_data.loc[0,'RAMMA'] = results
        patient_data.loc[0,'DETAIL'] = detail
        print(patient_data)
        if os.path.exists(config.submited_data_path):
            submit_database = pd.read_excel(config.submited_data_path, sheet_name='Sheet_name_1')
            submit_database.append(patient_data)
        else:
            submit_database = patient_data
        submit_database.to_excel(config.submited_data_path,sheet_name='Sheet_name_1')
        return redirect('/getInfo')
    else:
        database = pd.read_excel(config.unsubmited_data_path, sheet_name='Sheet_name_1')
        
        patient_ID = request.args.get('patient_ID',type = str)
        patient_data = database[database['ID']==patient_ID]
        if patient_data.empty:
            return redirect('/wrongID')
        data_sun_light = ['BUOISANG','BUOITRUA','BUOICHIE']
        sun_light = ['Buổi sáng','Buổi trưa','Buổi chiều']
        data_cosmetic_purpose = ['TRANGDA','CHUANAM','NHANDA','MDICHKHA']
        cosmetic_purpose = ['Trắng da, mịn da, làm đẹp da','Chữa nám má, tàn nhang','Chống nhăn da','Mục đích khác']
        data_bought_place = ['TAPHOA','SIEUTHI','CHO','XACHTAY','BANBE','DAILY','NHATHUOC','MUAKHAC']
        bought_place = ['Cửa hàng tạp hóa','Siêu thị','Chợ','Hàng xách tay','Bạn bè người quen mua giúp/tặng','Mua ở đại lý, nhà phân phối chính thức','Mua ở nhà thuốc, cửa hàng thuốc','Các địa điểm khác']
        job = ['Nông dân','Buôn bán','Cán bộ, Sinh viên','Công nhân','Chăn nuôi','Nội trợ','Khác']
        education_level = ['Mù chữ, tiểu học','THCS (cấp 2)','THPT (Cấp 3)','Trung cấp, cao đẳng','Đại học trở lên']
        relationship_status = ['Chưa kết hôn','Đã kết hôn']
        data_health_history = ['BENHLY1','BENHLY2','BENHLY3','BENHLY4']
        health_history_status = ['Bệnh tuyến giáp', 'Bệnh cổ tử cung','Bệnh động kinh','Bệnh khác']


        def change_text(data_list, compare_list): 
            print(patient_data[data_list])
            results = patient_data[data_list].values[0]
            a =  [j for i,j in zip(results,compare_list) if i in [1,'co']]
            if a:
                return a
            else:
                return ["Không có thông tin"]
        
        def pregnant_change(x):
            if x==0:
                return 'Chưa mang thai'
            else:
                return 'Đã mang thai %s lần'%x
                
        def has_child_change(x):
            if x==0:
                return 'Chưa có con'
            else:
                return 'Hiện có %s con.'%x

        def TTT_status(x):
            if x==0:
                return 'Không sử dụng'
            else:
                return 'Có sử dụng'

        def family_history(x):
            if x==0:
                return 'Không có người bị nám má trước đây'
            else:
                return 'Đã có người bị nám má trước đây'

        def pregnant_history(x):
            if x==0:
                return 'Không bị nám má khi mang thai'
            else:
                return 'Bị nám má khi mang thai từ tháng thứ %s'%s

        def display_preprocess(x):
            if x and str(x)!='nan':
                return x
            else:
                return "Không có thông tin."


        survey_data = [ {'Feature':'Họ và tên'                                         ,'Value':patient_data['NAME'].values[0]},
                        {'Feature':'Địa chỉ'                                           ,'Value':patient_data['KHUVUC'].values[0]},
                        {'Feature':'Năm sinh'                                          ,'Value':patient_data['NAMSINH'].values[0]},
                        {'Feature':'Nghề nghiệp hiện tại'                              ,'Value':job[patient_data['NGHENGHI'].values[0]]},
                        {'Feature':'Trình độ học vấn'                                  ,'Value':education_level[patient_data['HOCVAN'].values[0]]},
                        {'Feature':'Tình trạng hôn nhân'                               ,'Value':relationship_status[patient_data['HONNHAN'].values[0]]},
                        {'Feature':'Số lần mang thai'                                  ,'Value':pregnant_change(patient_data['SOLANMAN'].values[0])},
                        {'Feature':'Số con hiện có'                                    ,'Value':has_child_change(patient_data['SOCONSINH'].values[0])},
                        {'Feature':'Tình trạng sử dụng thuốc tránh thai'               ,'Value':TTT_status(patient_data['TRANHTHA'].values[0])},
                        {'Feature':'Tiền sử rám má của gia đình'                       ,'Value':family_history(patient_data['GDINHRAM'].values[0])},
                        {'Feature':'Tình trạng xuất hiện rám má khi mang thai'         ,'Value':pregnant_history(patient_data['THANGTHA'].values[0])}, 
                        {'Feature':'Tiền sử bệnh nội khoa'                             ,'Value':",".join(change_text(data_health_history,health_history_status))+'.'},
                        {'Feature':'Thời gian tiếp xúc với ánh nắng mặt trời'          ,'Value':",".join(change_text(data_sun_light,sun_light))+'.'},
                        {'Feature':'Tình hình tiếp xúc với các loại hóa chất'          ,'Value':display_preprocess(patient_data['TSUHOACH'].values[0])},
                        {'Feature':'Thông tin về việc sử dụng mỹ phẩm'                 ,'Value':display_preprocess(patient_data['SDMYPHAM'].values[0])},
                        {'Feature':'Tuổi bắt đầu sử dụng mỹ phẩm'                      ,'Value':display_preprocess(patient_data['TUOIMYPH'].values[0])},
                        {'Feature':'Tên loại mỹ phẩm thường xuyên sử dụng'             ,'Value':display_preprocess(patient_data['TENMPHAM'].values[0])},
                        {'Feature':'Nơi sản xuất loại mỹ phẩm thường xuyên sử dụng'    ,'Value':display_preprocess(patient_data['NUOCSX'].values[0])},
                        {'Feature':'Giá tiền loại mỹ phẩm thường xuyên sử dụng'        ,'Value':display_preprocess(patient_data['GIATIEN'].values[0])}, 
                        {'Feature':'Mục đích của loại mỹ phẩm thường xuyên sử dụng'    ,'Value':",".join(change_text(data_cosmetic_purpose,cosmetic_purpose))+'.'},
                        {'Feature':"Nơi mua mỹ phẩm"                                   ,'Value':",".join(change_text(data_bought_place,bought_place))+'.'},
                        {'Feature':"Kết quả dự đoán của mô hình"                       ,'Value':str(patient_data['prediction'].values[0])+"%."}
            ]
        knowledge_database = pd.read_excel(config.knowledgeTest_path, sheet_name='Sheet_name_1', index = False)
        test_results = knowledge_database[knowledge_database['ID']==patient_ID]

        def change_display(x):
            if x:
                return "Đúng"
            else:
                return "Sai"

        knowledgeTest_results = [
                                    {"Question":"Rám má có phải là do di truyền không?",
                                    "Result":change_display(test_results['QA01'].values[0])},

                                    {"Question":"Rám má có phải là do nội tiết không?",
                                    "Result":change_display(test_results['QA02'].values[0])},

                                    {"Question":"Có phải rám má là do mang thai, sinh đẻ không?",
                                    "Result":change_display(test_results['QA03'].values[0])},

                                    {"Question":"Có phải rám má là do tiếp xúc với ánh nắng mặt trời hay không?",
                                    "Result":change_display(test_results['QA04'].values[0])},

                                    {"Question":"Có phải rám má là do dùng mỹ phẩm không đúng cách không?",
                                    "Result":change_display(test_results['QA05'].values[0])},

                                    {"Question":"Có phải rám má là do lão hóa da không?",
                                    "Result":change_display(test_results['QA06'].values[0])},

                                    {"Question":"Có phải rám má là do ảnh hưởng một số bệnh nội khoa không?",
                                    "Result":change_display(test_results['QA07'].values[0])},

                                    {"Question":"Có phải rám má có thể tự khỏi mà không cần điều trị không?",
                                    "Result":change_display(test_results['QA08'].values[0])},

                                    {"Question":"Có phải sử dụng kem chống nắng thường xuyên có thể phòng tránh rám má không?",
                                    "Result":change_display(test_results['QA09'].values[0])},                                    

                                    ##########################################################################
                                    {"Question":"Bạn có Mang khẩu trang hàng ngày trước khi đi ra nắng không?",
                                    "Result":change_display(test_results['QB01'].values[0])},

                                    {"Question":"Khẩu trang bạn sử dụng hàng ngày có trùm kín mặt, vải dày, sẫm màu không?",
                                    "Result":change_display(test_results['QB02'].values[0])},

                                    {"Question":"Bạn có bôi kem chống nắng hàng ngày trước khi đi ra nắng 20-30 phút không?",
                                    "Result":change_display(test_results['QB03'].values[0])},

                                    {"Question":"Bạn có sử dụng kem dưỡng trắng da ban đêm không?",
                                    "Result":change_display(test_results['QB04'].values[0])},

                                    {"Question":"Bạn có được soi da, tư vấn sử dụng mỹ phẩm không?",
                                    "Result":change_display(test_results['QB05'].values[0])},

                                    {"Question":"Mỹ phẩm bạn sử dụng có nhãn mác, nguồn gốc xuất xứ rõ ràng không?",
                                    "Result":change_display(test_results['QB06'].values[0])},

                                    {"Question":"Mỹ phẩm bạn sử dụng có hạn sử dụng không?",
                                    "Result":change_display(test_results['QB07'].values[0])},

                                    {"Question":"Bạn đã từng khám, tư vấn chăm sóc da ở cơ sở Y tế chưa?",
                                    "Result":change_display(test_results['QB08'].values[0])},

                                    {"Question":"Bạn đã từng điều trị rám má ở cơ sở y tế chuyên khoa da liễu chưa?",
                                    "Result":change_display(test_results['QB09'].values[0])},


                                ]
        return render_template('doctor_02_DisplayPatientInfor.html',survey_data = survey_data, knowledge_data = knowledgeTest_results, patient_ID = patient_ID)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)


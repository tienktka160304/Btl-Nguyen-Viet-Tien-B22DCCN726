import pickle
import csv
import statistics
from common import header,row,row2,header2,rowsquad
import pandas as pd
import os


list_squad=[]
with open("squads.pkl", "rb") as file:
    list_squad = pickle.load(file)

squads=['Arsenal','Aston Villa','Bournemouth','Brentford','Brighton',
                'Burnley','Chelsea','Crystal Palace','Everton','Fulham','Liverpool','Luton Town',
                'Manchester City','Manchester Utd','Newcastle Utd',"Nott'ham Forest",'Sheffield Utd','Tottenham','West Ham','Wolves']


df = pd.read_csv('result.csv')
df.replace("N/a", 0, inplace=True)
ATTR_NUMBER=172
for i in range(5, ATTR_NUMBER):
    df[df.columns[i]] = pd.to_numeric(df[df.columns[i]], errors='coerce').fillna(0)
top_3_rows = df.nlargest(3, df.columns[5])




#top3
if 1==1:
    for i in range(5,ATTR_NUMBER):
        top_3_rows = df.nlargest(3, df.columns[i])
        print("Top3 cao nhất thuộc tính",header[i])
        print(top_3_rows.iloc[:,0].values)
        print("Top 3 thấp nhất thuộc tính",header[i])
        bot_3_rows = df.nsmallest(3, df.columns[i])
        print(bot_3_rows.iloc[:,0].values)



#tinh trung binh
if 1==1:
    with open('result2.csv', mode='w', newline='', encoding='utf-8') as file:
 
        all_attr=[]
        for i in range(5,ATTR_NUMBER):
            arr=df.iloc[:, i]
            all_attr.append(arr)
        mean_value_list=[0]*(ATTR_NUMBER-5)
        median_value_list=[0]*(ATTR_NUMBER-5)
        std_dev_list=[0]*(ATTR_NUMBER-5)

        for index,arr in enumerate(all_attr):
            mean_value_list[index]=statistics.mean(arr)
            median_value_list[index]=statistics.median(arr)
            std_dev_list[index]=statistics.stdev(arr)

        writer = csv.writer(file)
        writer.writerow(header2)

        r=row2(0,"All",median_value_list,mean_value_list,std_dev_list)
        writer.writerow(r)


    
        for stt,squad in enumerate(squads):
            all_attr1=[]
            filtered_df  = df[df.iloc[:, 2] == squad]  
            mean_value_list1=[0]*(ATTR_NUMBER-5)
            median_value_list1=[0]*(ATTR_NUMBER-5)
            std_dev_list1=[0]*(ATTR_NUMBER-5)

            for i in range(5,ATTR_NUMBER):
                arr=filtered_df.iloc[:, i].values
                all_attr1.append(arr)

            for index,arr in enumerate(all_attr1):
                mean_value_list1[index]=statistics.mean(arr)
                median_value_list1[index]=statistics.median(arr)
                if len(arr)<2:
                    std_dev_list1[index]="N/a"
                else: std_dev_list1[index]=statistics.stdev(arr)
            
            writer = csv.writer(file)
            r=row2(stt+1,squad,median_value_list1,mean_value_list1,std_dev_list1)
            writer.writerow(r)

    import subprocess
    subprocess.Popen(["start", r"result2.csv"], shell=True)



#ve bieu do
if 1==1:
    import matplotlib.pyplot as plt
    output_directory = 'histograms'
    os.makedirs(output_directory, exist_ok=True)  # Tạo thư mục nếu chưa tồn tại
    all_attr=[]
    for i in range(5,ATTR_NUMBER):
        arr=df.iloc[:, i]
        all_attr.append(arr)
    for index,arr in enumerate(all_attr):
        plt.figure(figsize=(8, 6))
        plt.hist(arr, bins=30, color='blue', alpha=0.7, edgecolor='black')
        plt.title(f'Histogram of Data {header[5+index]}')
        plt.xlabel('Value')
        plt.ylabel('Frequency')
        image_path = os.path.join(output_directory, f'histogram_{index}.png')  # Đặt tên file
        plt.savefig(image_path)  # Lưu hình ảnh
        plt.close()  # Đóng biểu đồ để giải phóng bộ nhớ

    #doi tuyen
    for squad in squads:
        output_squad_directory = f'histogramsof{squad}'
        os.makedirs(output_squad_directory, exist_ok=True)

        all_attr1=[]
        filtered_df  = df[df.iloc[:, 2] == squad]  
        for i in range(5,ATTR_NUMBER):
            arr=filtered_df.iloc[:, i].values
            all_attr1.append(arr)
        
        for index,arr in enumerate(all_attr1):
            plt.figure(figsize=(8, 6))
            plt.hist(arr, bins=30, color='blue', alpha=0.7, edgecolor='black')
            plt.title(f'Histogram of Data {header[5+index]}')
            plt.xlabel('Value')
            plt.ylabel('Frequency')
            image_path1 = os.path.join(output_squad_directory, f'histogram_{index}.png')  # Đặt tên file
            plt.savefig(image_path1)  # Lưu hình ảnh
            plt.close()  # Đóng biểu đồ
        print(f"Các biểu đồ đã được lưu ")



#tim doi chi so cao nhat
if 1==1:
    biggest_attr_value=[-1e9]*167
    best_team_in_one_attr=[""]*167
    for i in list_squad:
        arr=rowsquad(i)[5:]
        for index,value in enumerate(arr):
            if value!="N/a" and value>biggest_attr_value[index]:
                biggest_attr_value[index]=value
                best_team_in_one_attr[index]=i.name
                
            elif value=="N/a" and biggest_attr_value[index]==-1e9 and best_team_in_one_attr[index]=="":
                biggest_attr_value[index]=0
                best_team_in_one_attr[index]=i.name
    for index,i in enumerate(best_team_in_one_attr):
        print(header[5+index]+": ",i)

    #đội nào có phong độ tốt nhất giải ngoại Hạng Anh mùa 2023-2024
    from collections import Counter
    rank=Counter(best_team_in_one_attr)
    print("Đội ấn tượng nhất: ",(rank.most_common(1)[0][0]))

        

        




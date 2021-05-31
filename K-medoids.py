from sklearn.metrics.pairwise import pairwise_distances
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import csv
import shapefile as shp
import codecs
# import conda

# conda_file_dir = conda.__file__
# conda_dir = conda_file_dir.split('lib')[0]
# proj_lib = os.path.join(os.path.join(conda_dir, 'share'), 'proj')
# os.environ["PROJ_LIB"] = proj_lib

# from mpl_toolkits.basemap import Basemap

###############################################################################

data0 = pd.read_csv("Input\chuanhoa.csv")
data00 = pd.read_csv("Input\O.csv")
data = pd.DataFrame(data0)
data = data.values.tolist()
data11 = pd.DataFrame(data00)
data11 = data11.values.tolist()
#print("Dữ liệu đầu vào: \n", data0)
#print("Số mẫu là: ", len(data))

k = int(input("Nhập số cụm cần chia: "))
listdata = pairwise_distances(data, metric = 'euclidean')
# print(listdata)

#Ma trận 2 chiều m x n
m,n = listdata.shape

ArrayMedoidLeft = set(range(n))
ArrayMedoidOut = set([])

row, col = np.where(listdata == 0)

ArrayRandomShuffle = list(range(len(row)))
np.random.shuffle(ArrayRandomShuffle)

row = row[ArrayRandomShuffle]
col = col[ArrayRandomShuffle]

#Nhưng dòng qua thì loại bỏ cột tương ứng
for i,j in zip(row, col):
    if ((i < j) and (i not in ArrayMedoidOut)):
        ArrayMedoidOut.add(i)
ArrayMedoidLeft = list(ArrayMedoidLeft - ArrayMedoidOut)

# #Khởi tạo k tâm ngẫu nhiên
# M = np.array(ArrayMedoidLeft)
# np.random.shuffle(M)
# M = np.sort(M[:k])

#Khởi tạo k tâm chỉ định
M = []
for i in range(0, k):
    flag = True
    while (flag == True):
        print("Nhập chỉ số tâm chỉ định cụm", i, "\b: ", end='')
        t = int(input())
        if((t < 0) | (t > max(row))):
            print("Lỗi! Bạn chỉ được phép nhập chỉ số của tâm trong khoảng từ 0 đến", max(row))
        else:
            M.append(t)
            flag = False
M = np.sort(M)
print(M)

dem = 1
for i in M:
    print("-> Khởi tạo tâm ", dem, ": ", i, "ứng với giá trị: \n", data[i])
    dem = dem + 1

#Tạo mảng mới và mảng đại diện cho nó
Mnew = np.copy(M)
C = {}
for i in range(1000):
    #Xác định cụm và chỉ số trong mảng với mảng bé nhất từ 1->
    J = np.argmin(listdata[:,M], axis=1)
    for j in range(k):
        C[j] = np.where(J==j)[0]
    #update cụm medoid
    for j in range(k):
        #tính mean của 
        J = np.mean(listdata[np.ix_(C[j],C[j])],axis=1)
        l = np.argmin(J)
        Mnew[j] = C[j][l]   #Lưu toạ độ tâm
    np.sort(Mnew)
    #check hội tụ
    if np.array_equal(M, Mnew):
        break
    M = np.copy(Mnew)
else:
    # kết thúc update phân cụm
    J = np.argmin(listdata[:,M], axis=1)
    for j in range(k):
        C[j] = np.where(J==j)[0]

a=[]
print('medoids:')

#Chọn cột biểu diễn toạ độ xy
ii=0
jj=1
sum=0

a=[]
for point_idx in M:
    a.append(data[point_idx])
    
#Gán màu vào mỗi label
region_set = list(range(len(C)))
colour_set = ['red','orange','yellow','green','blue','navy','purple','#2E4053','#F1c40F','#A9DFBF','#F0B27A']
region_colour_dict = dict(zip(region_set, colour_set))
#end gán màu

for label in C:
    for i in C[label]:
        print('cụm {0}:　{1}'.format(label, data[i]))
        plt.scatter(float(data[i][ii]),float(data[i][jj]),color = region_colour_dict[label])
        for j in M:
            if(j==i):
                # In tâm
                plt.scatter(float(data[i][ii]),float(data[i][jj]),color = region_colour_dict[label],s=20**2)
        
        sum+= (abs(float(a[label][0])-float(data[i][0])) + abs(float(a[label][1])-float(data[i][1])) + abs(float(a[label][2])-float(data[i][2])) + abs(float(a[label][3])-float(data[i][3]))
                + abs(float(a[label][4])-float(data[i][4])) + abs(float(a[label][5])-float(data[i][5])) + abs(float(a[label][6])-float(data[i][6]))
                + abs(float(a[label][7])-float(data[i][7]) + abs(float(a[label][8])-float(data[i][8]))) + abs(float(a[label][9])-float(data[i][9])) + abs(float(a[label][10])-float(data[i][10])) + abs(float(a[label][11])-float(data[i][11])))

print('Tong la :',sum)
print('vị trí tâm trong mảng : ',M)
print('Toạ độ tâm :')
for i in M:
#    plt.scatter(data[i][0],data[i][1],color = 'orange',s=20**2)
#    plt.scatter(data[i][0],data[i][1],color = 'yellow',s=20**2)
    print(data[i])

plt.title('Biểu đồ mediod')
plt.show()

##########################################################

# Chuẩn hóa tạo độ đối tượng về tọa độ ứng với map trên Qgis
for x in data11:
    x[0] = 27750 * (((x[0] - 1) - 4) / 4) - 763267
for y in data11:
    y[1] = 10000 * ((4 - (y[1] - 1)) / 4) + 5145034

# Chuyển list sang csv
dem = 0
for label in C:
    O = []
    name = "Output\\CSV\\" + str(dem) + ".csv"
    name1 = "Output\\SHP\\" + str(dem) + ".shp"
    if (dem == label):
        for i in C[label]:
            O.append(data11[i])
        # chuyển đổi list sang csv
        with open(name, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['X', 'Y', 'month', 'FFMC', 'DMC', 'DC', 'ISI', 'temp', 'RH', 'wind', 'rain', 'area'])
            for lines in O:
                wr = csv.writer(file, quoting=csv.QUOTE_ALL)
                wr.writerow(lines)
        
# chuyển đổi csv sang shp
        w = shp.Writer(name1)
        w.autoBalance = 1
        
        w.field('X', 'F')
        w.field('Y', 'F')
        w.field('month', 'F')
        w.field('FFMC', 'F')
        w.field('DMC', 'F')
        w.field('DC', 'F')
        w.field('ISI', 'F')
        w.field('temp', 'F')
        w.field('RH', 'F')
        w.field('wind', 'F')
        w.field('rain', 'F')
        w.field('area', 'F')
        
        with open(name, 'rb') as csvfile:
            reader = csv.reader(codecs.iterdecode(csvfile, 'utf-8'))
            # bỏ qua tiêu đề
            next(reader)
            for row in reader:
                X = row[0]
                Y = row[1]
                month = row[2]
                FFMC = row[3]
                DMC = row[4]
                DC = row[5]
                ISI = row[6]
                temp = row[7]
                RH = row[8]
                wind = row[9]
                rain = row[10]
                area = row[11]
                
                a = w.point(float(X),float(Y))
                w.record(X, Y, month, FFMC, DMC, DC, ISI, temp, RH, wind, rain, area)
        w.close()
        dem = dem + 1
        file.close()

##########################################################
# #setting map
# fig, ax = plt.subplots(figsize=(10,10))
# m = Basemap(llcrnrlon=-7.208542,llcrnrlat=41.729305,
#             urcrnrlon=-6.513643,urcrnrlat=41.978686,
#             resolution='i',
#             projection='tmerc',
#             lon_0=-6.856543,lat_0=41.893475,
#             epsg=3763)

# m.drawmapboundary(fill_color='#e2e2d7')
# m.fillcontinents(color='#007fff',lake_color='#ffffff') #zorder=0
# m.drawcoastlines()
# m.drawrivers(color = '#ffffff', linewidth=2)
# m.drawcountries(linewidth=2)
# #end setting map

# for label in C:
#     for i in C[label]:
#         m.plot(float(data[i][0]), float(data[i][1]), marker = 'o', c=region_colour_dict[label], markersize=3, alpha=0.8, latlon=True)
#         for j in M:
#             if(j==i):
#                 m.plot(float(data[i][0]), float(data[i][1]), marker = 'o', c=region_colour_dict[label], markersize=20, alpha=0.8, latlon=True)
#                 m.plot(float(data[i][0]), float(data[i][1]), marker = '+', c=region_colour_dict[label], markersize=20, alpha=0.8, latlon=True)
        
# plt.show()

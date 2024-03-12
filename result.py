

def detect_result_del(result):
        '''处理检测结果,得到name,label,xxyy'''
        class_label = ['CA001', 'CA002', 'CA003', 'CA004', 'CB001', 'CB002', 'CB003', 'CB004', 'CC001', 'CC002', 'CC003', 'CC004', 'CD001', 'CD002', 'CD003', 'CD004', '2D']
        class_name = ['spoon','chopsticks','bowl','hanger','shaqima','canned preserves','Ham sausage','chip','canned beverages','bottled beverages','carton milk','bottled water','apple','orange','banana','mango','Picture']
        zero = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        object_class_name = []
        object_class_label = []
        object_xxyy = []
        
        for obj in result:
            item = obj.boxes.cls
            
            object_class_name.append(class_name[int(item)])
            object_class_label.append(class_label[int(item)])

            item = obj.boxes.xyxy
            # print(item)
        
            object_xxyy.append([[int(item[0][0].item()), int(item[0][1].item())], [int(item[0][2].item()), int(item[0][3].item())]])
        
        object_class = object_class_label
        object_class.sort() #按字母排序
        object_num = dict(zip(class_label,zero))
        for key in object_class:
             object_num[key]=object_num.get(key,0)+1 #统计结果中每一个类别出现的次数
        # print(object_num)
        return object_class_name, object_num, object_xxyy

def num_1(object_num):
    class_label = ['CA001', 'CA002', 'CA003', 'CA004', 'CB001', 'CB002', 'CB003', 'CB004', 'CC001', 'CC002', 'CC003', 'CC004', 'CD001', 'CD002', 'CD003', 'CD004', '2D']
    list1 = list(object_num[0].values())
    list2 =  list(object_num[1].values())
    lis = []
    for i in range(17):
        lis.append(max(list1[i],list2[i]))
    return dict(zip(class_label,lis))
        
def num_2(object_num):
    class_label = ['CA001', 'CA002', 'CA003', 'CA004', 'CB001', 'CB002', 'CB003', 'CB004', 'CC001', 'CC002', 'CC003', 'CC004', 'CD001', 'CD002', 'CD003', 'CD004', 'Picture','W001','W002','W003','W004']
    list1 = list(object_num[0].values())
    list2 =  list(object_num[1].values())
    list3 = list(object_num[2].values())
    lis = []
    for i in range(21):
        lis.append(list1[i]+list2[i]+list3[i])
    return dict(zip(class_label,lis))
def result_txt_generate(object_num):
        result_txt = 'START' + '\r' #结果文本头部
        #START\rGoal_ID=CA002;Num=2\rEND
        for i,j in object_num.items():
            #遍历每一个结果,生成结果文本
            if i == '2D':
                continue
            if j ==0:
                 continue
            result_txt = result_txt + 'Goal_ID=' + i + ';Num=' + str(j) + '\r'
        result_txt += 'END' #结果文本尾部

        result_txt1 = ''
        #START\rGoal_ID=CA002;Num=2\rEND
        for i,j in object_num.items():
            #遍历每一个结果,生成结果文本
            if i == '2D':
                continue
            if j ==0:
                 continue
            result_txt1 = result_txt1 + '目标ID=' + i + ';数目=' + str(j) + '\n'


        return result_txt,result_txt1




# _, detect_object_class_label, detect_object_xxyy = detect_result_del(detect_result)
# result_txt = result_txt_generate(detect_object_class_label)
# path_txt = 'result_r/CSU-CSUPER-VISION-R1.txt'
# f = open(path_txt, 'w')
# f.write(result_txt)
# f.close()
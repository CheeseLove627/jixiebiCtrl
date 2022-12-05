import cv2
import easyocr
reader = easyocr.Reader(['en'])

class num():
    def __init__(self, img):
        self.img = img

    '''
    1+1=3 ？
    '''
    def Correcting_Machines_2(self):
        result = reader.readtext(img)
        m = []
        for res in result:
            m.append(res[1])
        #print(m)  # m:['11+11', '=20']
        #print('\n')
        # print(m[0]) #m[0]:11+11   m[1]:=20
        # print('\n')
        arry = []
        for i in m:

            for q in i:
                arry.append(q)
        # print(arry) #arry:  ['1', '1', '+', '1', '1', '=', '2', '0']
        num_1 = []
        num_2 = []
        num_3 = []
        flag = 0
        for i in arry:
            if i.isdigit() and (flag == 0):
                num_1.append(int(i))  # [1, 1]
            elif i.isdigit() and (flag == 1):
                num_2.append(int(i))  # [1, 1]
            elif i.isdigit() and (flag == 2):
                num_3.append(int(i))  # [2, 0]
            elif i != ' ':
                flag = flag + 1
        add_1 = ""
        add_2 = ""
        sum = ""
        for a in num_1:
            add_1 += str(a)
        for a in num_2:
            add_2 += str(a)
        for a in num_3:
            sum += str(a)
        add_1 = int(add_1)  # add_1:11
        add_2 = int(add_2)  # add_2:11
        sum = int(sum)  # sum:20

        if (add_1 + add_2) == sum:
            print("Correct!")
            return True
        else:
            print("Wrong!")
            return False

    def predict(x, y, z):
        if x * y == z:
            print("*")
            return 0
        elif x + y == z:
            print("+")
            return 1
        elif x - y == z:
            print("-")
            return 2
        elif x // y == z:
            print("/")
            return 3

    '''
    1？1 =2
    '''
    def Predict_Machines(self):
        result = reader.readtext(img)
        m = []
        for res in result:
            m.append(res[1])
        arry = []
        for i in m:
            for q in i:
                arry.append(q)
        num_1 = []
        num_2 = []
        num_3 = []
        flag = 0
        for i in arry:
            if i.isdigit() and (flag == 0):
                num_1.append(int(i))  # [3]
            elif i.isdigit() and (flag == 1):
                num_2.append(int(i))  # [1, 1]
            # elif i.isdigit() and (flag == 2):
            #   num_3.append(int(i)) #[2, 0]
            elif i != ' ':
                flag = flag + 1
        insert_pos = len(num_1) // 2
        num_1.insert(insert_pos, 'x')
        num_1_1 = []
        num_2_2 = []
        funk = 0
        for i in num_1:
            if type(i) == int and (funk == 0):
                num_1_1.append(int(i))
            elif type(i) == int and (funk == 1):
                num_2_2.append(int(i))
            elif i != ' ':
                funk = funk + 1
        add_1 = ""
        add_2 = ""
        sum = ""
        for a in num_1_1:
            add_1 += str(a)
        for a in num_2_2:
            add_2 += str(a)
        for a in num_2:
            sum += str(a)
        add_1 = int(add_1)  # add_1:14
        add_2 = int(add_2)  # add_2:21
        sum = int(sum)  # sum:294
        num.predict(add_1, add_2, sum)

    '''
    1+1=?
    '''
    def Compute_machine(self):
        m = []
        result = reader.readtext(img)
        for res in result:
            m.append(res[1])
        print('\n')
        arry = []
        for i in m:
            for q in i:
                arry.append(q)
        num_1 = []
        num_2 = []
        num_3 = []
        flag = 0
        for i in arry:
            if i.isdigit() and (flag == 0):
                num_1.append(int(i))  # [3]
            elif i.isdigit() and (flag == 1):
                num_2.append(int(i))  # [1, 1]
            elif i != ' ':
                num_3.append(i)
                flag = flag + 1
        num_4 = str(num_3[0])  # 符号 +
        add_1 = ""
        add_2 = ""
        for a in num_1:
            add_1 += str(a)
        for a in num_2:
            add_2 += str(a)
        add_1 = int(add_1)  # add_1:12
        add_2 = int(add_2)  # add_2:18
        if num_4 == '+':
            final = add_1 + add_2
        elif num_4 == '-':
            final = add_1 - add_2
        elif num_4 == 'X':
            final = add_1 * add_2
        elif num_4 == '/':
            final = add_1 // add_2
        print(final)
        return final


if __name__ == '__main__':
    #img = cv2.imread('F:/class/vision/pic/22.png')
    #video = cv2.VideoCapture(0)
    #num.Predict_Machines(img)
    #num.Correcting_Machines_2(img)
    # num.Compute_machine(img)

    # cap  = cv2.VideoCapture(0) # 打开摄像头
    cap_usb = cv2.VideoCapture(0)


    while (1):
        # get a frame
        ret, frame = cap_usb.read()
        # show a frame
        cv2.imshow("capture", frame)  # 生成摄像头窗口

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果按下q 就截图保存并退出
            cv2.imwrite('./data/frame.jpg', frame)  # 保存路径
            break

    cap_usb.release()
    cv2.destroyAllWindows()
    img = cv2.imread('./data/frame.jpg')
    num.Correcting_Machines_2(img)
    # num.Compute_machine(img)
    # num.Predict_Machines(img)
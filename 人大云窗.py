from selenium.webdriver import EdgeOptions

option=EdgeOptions()
option.add_experimental_option('excludeSwitches',['enable-automation'])


from selenium import webdriver
from lxml import etree
import time,requests

def login():
    bro = webdriver.Edge(options=option)
    bro.get('http://student.rdyc.cn/')
    name_input = bro.find_element('id', 'UserName')
    name_input.send_keys('18359651255')
    password_input = bro.find_element('id', 'Password')
    password_input.send_keys('awslandfly666')
    login_bt = bro.find_element('xpath', '//*[@id="login-form"]/footer/button')
    login_bt.click()
    course_bt = bro.find_element('xpath', '//*[@id="70801366"]/div/div/div/div[2]/div/div/div[2]/a[1]')
    course_bt.click()
    homework_bt = bro.find_element('xpath', '//*[@id="left-panel"]/nav/ul/li[4]/a')
    homework_bt.click()
    print("登录成功")
    unit_list=[]
    print("请输入要刷的单元号")
    while (1):
        input_temp = input()
        if input_temp != '0':
            unit_list.append(int(input_temp))
        else:
            break
    unit_list.reverse()
    print('要刷的单元为',unit_list)
    while(len(unit_list)!=0):
        unit=unit_list.pop()
        print(f'第{unit}单元开刷...')
        mark_table = bro.find_element('xpath', f'//*[@id="content"]/div/div/div/div[2]/fieldset/div/table/tbody/tr[{unit}]/td[5]/span')
        mark=int(mark_table.text)
        origin_mark=mark
        print("当前分数:",mark)
        pb_questions=[]
        count=1
        count_text=int(count)
        #key=int(input('选择题号录入方式:1、手动录入 2、自动录入（全局暴力）'))
        key=2
        if key==1:
            print("请输入错误题号")
            while(1):
                input_temp=input()
                if input_temp!='0':
                    pb_questions.append(int(input_temp))
                else:
                    break
        elif key==2:
            number_range = range(1, 26)
            pb_questions = list(number_range)
        else:
            exit('请输入1或2')
        pb_questions.reverse()
        print('错误题号为',pb_questions)
        print('开始刷分...')
        while(len(pb_questions)!=0):
            num=pb_questions[-1]
            print(f'第{num}题开始第{count}次测试')
            back_bt = bro.find_element('xpath',f'//*[@id="content"]/div/div/div/div[2]/fieldset/div/table/tbody/tr[{unit}]/td[6]/a[2]')
            back_bt.click()
            time.sleep(2)
            web_handles = bro.window_handles
            bro.switch_to.window(web_handles[1])
            bro.find_element('xpath', '//*[@id="Button1"]').click()  # 点击撤回大按钮
            bro.switch_to.alert.accept()
            time.sleep(2)
            bro.switch_to.alert.accept()
            bro.close()
            web_handles = bro.window_handles
            bro.switch_to.window(web_handles[0])
            bro.refresh()
            bro.find_element('xpath',f'//*[@id="content"]/div/div/div/div[2]/fieldset/div/table/tbody/tr[{unit}]/td[6]/a[1]').click()  # 点做题
            web_handles = bro.window_handles
            bro.switch_to.window(web_handles[1])
            bro.close()
            web_handles = bro.window_handles
            bro.switch_to.window(web_handles[0])
            bro.find_element('xpath', f'//*[@id="form0"]/ul/li[{num}]').click()  # 点击做题页面下的题号
            time.sleep(1)
            bro.find_element('xpath',f'//*[@id="a_{count_text}"]').click()#点击选项
            bro.find_element('xpath','//*[@id="submitStudentAnswer"]').click()#点击提交按钮
            alert=bro.switch_to.alert
            alert.accept()
            time.sleep(3)
            bro.switch_to.alert.accept()
            mark_current=int(bro.find_element('xpath', f'//*[@id="content"]/div/div/div/div[2]/fieldset/div/table/tbody/tr[{unit}]/td[5]/span').text)
            if mark_current>mark:
                mark=mark_current
                pb_questions.pop()
                count=1
                count_text = int(count)
                print(f"第{num}题测试成功,当前分数为{mark}，剩余题目列表",pb_questions)
            else:
                count=count+1
                count_text=int(count)
                continue
        print(f'第{unit}单元刷分完毕！最终分数为{mark},已为您提分{int(mark)-int(origin_mark)}分')

login()

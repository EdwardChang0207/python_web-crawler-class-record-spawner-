import imp
import time
from re import I
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

###############################init#############################
PATH = 'C:/Users/User/Desktop/Coding/Projects/python爬蟲/chromedriver.exe' #path of webdriver.exe
url = 'https://corp.orangeapple.co/courses/dt/1782#lesson-reports' #targe link

user_mail = '' #user_mail
user_pw = '' #user_password

#get webdriver and connect to targe link
driver = webdriver.Chrome(PATH)
driver.get(url)

###############################login###########################
mail = driver.find_element_by_name('employee[email]')
mail.send_keys(user_mail)
pw = driver.find_element_by_name('employee[password]')
pw.send_keys(user_pw)

pw.send_keys(Keys.RETURN)
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.ID, 'students-table'))
)

#########################select record page########################
tab = driver.find_elements(By.TAG_NAME, 'li')
for i in tab:
    if i.text == "課堂記錄":
        i.click()
# WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-primary'))
# )
time.sleep(5)
 
#########################find record btns########################
recBtns = []
r = driver.find_elements_by_class_name('btn-success')
print(r)
time.sleep(3)
for i in r:
    if i.text == '記錄':
        recBtns.append(i)

print(len(recBtns))

########################open record of each student######################
for i in range(len(recBtns)):
    print(recBtns[i].text)
    recBtns[i].click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.ID, 'lesson_report_attendance_status'))
    )

    #student attendance
    # student_attendance = Select(driver.find_element_by_id('lesson_report_attendance_status'))
    # student_attendance = student_attendance.first_selected_option.text.split()[1]
    # print(student_attendance)

    #get student name
    student_name = driver.find_element_by_id('myModalLabel').text
    student_name = student_name.split()[0]
    student_name = student_name[-2] + student_name[-1]
    print(student_name)

    #get student level
    student_level = driver.find_element_by_id('lesson_report_feedback').text
    print(student_level)

    #get student process
    student_process_select = Select(driver.find_element_by_id('dt_admission_lesson_report_learning_stage'))
    student_process = student_process_select.first_selected_option.text.split()[1]
    print(student_process)

    #get student process section
    student_process_section_select = Select(driver.find_element_by_id('dt_admission_lesson_report_completion_status'))
    student_process_section = student_process_section_select.first_selected_option.text
    if student_process_section != '完整完成':
        student_process_section = Select(driver.find_element_by_id('dt_admission_lesson_report_end_to')).first_selected_option.text
        student_process_section = '已完成至:' + student_process_section
        student_contect = student_name + '今日上課認真，專心製作專案，今天的專案還未完成，可以利用在家的空閒時間或是下周早一點到教室完成喔!加油!'
    else:
        student_process_section = '已完整完成'
        student_contect = student_name + '今日上課認真，專心製作專案，今日專案已完整完成，下周也要繼續保持喔'
    print(student_process_section)

    #get lesson from koding school
    koding_school = { #list of lesson links
        'sb': 'https://koding.school/courses/scratch/dt-sb3',
        'sa': 'https://koding.school/courses/scratch/dt-sa3',
        'py': 'https://koding.school/courses/python/dt-python',
        'js': 'https://koding.school/courses/javascript/dt-js',
        'html': 'https://koding.school/courses/javascript/dt-web',
        'al': '',
        'ai': '',
        'mc': 'https://koding.school/courses/programming/dt-meeb',
        'mcadv': 'https://koding.school/courses/programming/dt-mca',
        'meec': 'https://koding.school/courses/programming/dt-meec'
    }

    #bug: 抓到錯誤的章節(fixed)
    koding = webdriver.Chrome(PATH)
    koding.get(koding_school[student_level])
    lessons = koding.find_elements_by_tag_name('h4')
    student_lesson = lessons[int(student_process)-1].text
    print(student_lesson)
    koding.quit()


    #stars
    # stars = driver.find_elements_by_class_name('full')
    # print(len(stars))
    # stars[9].click()

    #perfromance
    student_perfromance = '同學今日表現優良，上課認真製作專案，今日專案:' + student_lesson + student_process_section + '表現的很棒要繼續加油喔'

    #insert messages
    learning_process = driver.find_element_by_id('lesson_report_feedback')
    for i in range(len(student_level)):
        learning_process.send_keys(Keys.BACK_SPACE)
    learning_process.send_keys(student_perfromance)
    contect = driver.find_element_by_id('dt_admission_lesson_report_contact')
    contect.send_keys(student_contect)

    company_message = driver.find_element_by_id('dt_admission_lesson_report_learning_status')
    select_object = Select(company_message)
    select_object.select_by_index(1)
    
    #log
    # f = open("log.txt", "w")
    # f.write(student_name)
    # f.close()

    #save & quit
    saveBtns = driver.find_elements_by_class_name('btn-primary')
    for i in saveBtns:
        print(i.text)
        if i.text == '更新課堂紀錄':
            i.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-report-btn'))
            )
    time.sleep(3)

        # else:
        #     closeBtn = driver.find_element_by_class_name('close')
        #     closeBtn.click()
        #     WebDriverWait(driver, 10).until(
        #         EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-report-btn'))
        #     )
driver.quit()
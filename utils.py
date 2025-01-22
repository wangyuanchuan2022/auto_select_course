#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# auto course select for rdfz.jyyun.com
# Created: 2024-08-31
# Last modified: 2024-11-10
# Author: Yuanchuan Wang, Haochen Li
import hashlib
import json
import os
import platform
import sys
import threading
import time
import uuid

import requests

with open("./cfg.json", encoding="utf-8") as f:
    cfg = json.load(f)
    COOKIE = cfg["cookie"]

is_windows = True if platform.system() == "Windows" else False


def clear():
    if is_windows:
        os.system("cls")
    else:
        os.system("clear")


def pause():
    if is_windows:
        print(blue("按任意键继续。。。"))
        os.system(f"pause >nul")
    else:
        input("按Enter继续。。。")


def leave():
    try:
        sys.exit()
    except:
        exit()


def error(err):
    print(red(f"[!] Error : {err}"), end="")
    pause()
    clear()
    leave()


def red(text, _input=False):
    faded = ""
    for line in text.splitlines():
        green = 170
        for character in line:
            green -= 10
            if green < 0:
                green = 0
            faded += f"\033[38;2;255;{green};0m{character}\033[0m"
        if _input:
            faded += f"\033[38;2;255;{green};0m"
    return faded


def blue(text, _input=False):
    faded = ""
    for line in text.splitlines():
        red = 44
        green = 180
        for character in line:
            green += 2
            red += 5
            if green > 255:
                green = 255
            if red > 173:
                red = 173
            faded += f"\033[38;2;{red};{green};255m{character}\033[0m"
        if _input:
            faded += f"\033[38;2;{red};{green};255m"
    return faded


def green(text):
    os.system("")
    faded = ""
    for line in text.splitlines():
        red = 2
        green = 180
        for character in line:
            green += 2
            red += 2
            if green > 255:
                green = 255
            if red > 44:
                red = 44
            faded += f"\033[38;2;{red};{green};0m{character}\033[0m"
        faded += "\n"
    faded = faded.strip()
    return faded

def water(text):
    os.system("")
    faded = ""
    for line in text.splitlines():
        red = 44
        green = 150
        for character in line:
            green += 1
            red += 2
            if green > 255:
                green = 255
            if red > 173:
                red = 173
            faded += f"\033[38;2;{red};{green};255m{character}\033[0m"
        faded += "\n"
    return faded


def purple(text):
    os.system("")
    faded = ""
    down = False

    for line in text.splitlines():
        red = 40
        for character in line:
            if down:
                red -= 3
            else:
                red += 3
            if red > 254:
                red = 255
                down = True
            elif red < 1:
                red = 30
                down = False
            faded += f"\033[38;2;{red};0;220m{character}\033[0m"
    return faded


def get_mac_address():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return mac


def get_course(termid=""):
    html_url = (
        "https://rdfz.lezhiyun.com/xsxk/studentElective/redisEnterStudentSelect.do"
    )
    headers = {
        "cookie": COOKIE,
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    data = {"termid": termid}
    response = requests.get(url=html_url, headers=headers, data=data)
    return response.json()


def choose_course(termId, c_name, courseId, versionNum, course_name_list):
    html_url = (
        "https://rdfz.lezhiyun.com/xsxk/studentElective/redisStudentSelectCourse.do"
    )
    headers = {
        "cookie": COOKIE,
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    }
    data = {"termId": termId, "courseId": courseId, "versionNum": versionNum}
    response = requests.post(url=html_url, headers=headers, data=data)
    data = response.json()
    success = data['success']
    if success:
        print(green(f"{c_name}选择成功 {data['message']}"))
        course_name_list.remove(c_name)  # 从course_name_list中移除已选择的课程
    else:
        print(red(f"{c_name}选择失败 {data['message']}"))
    return success


def check(_computer_str, _tm, aes):
    tm = input(blue("token: ", True))
    while tm != _tm:
        tm = input(red("token 不正确: ", True))

    with open("./core/data.txt", "w") as f:
        string = json.dumps(
            {
                hashlib.md5("computer_str".encode()).hexdigest(): _computer_str,
                hashlib.md5("start_time".encode()).hexdigest(): time.strftime(
                    "%Y-%m-%d"
                ),
                hashlib.md5("tm".encode()).hexdigest(): _tm,
            }
        )
        string = aes.encrypt(string)
        f.write(string)
    return _computer_str


def main():
    clear()
    if is_windows:
        os.system("title 自动选课 by wyc")

    BOARD = """ 
       **                .@@                               .@*                                      
      *@@              .@@.                                .@@                  @@                  
     **.              ...@@.*.                        ..    @@.                 .@@          .@*.   
                        .@@*.                         @@ ..@@@@                          **@@@..*@. 
       @@@..        ..***@.         ..        ..     *@@@@@@@@.                  @@.  *. ...@*  *@@ 
          @*   ..***.....@*..*@@  .**@@       *@@   *@@@@@@@@*.*@.         .@@@@@...  *@. .@@*@@@*  
           @         *..*@*. .@. ..  @.       .@*   @@@*..*@@@@@*      .*@@@.  ...     *@* .@*@*    
  ...  .*  .        @. .*@..*@      @@..      .      ...*@@**@@.    .*         @@.      *@**@*      
 .@@.  @.  .       .@...*@*..  ....@@..*@*    *.    *@@@*  .@@@   .@*.                     .@@.**   
 @@@. .*   @.      .@*...@..   ** .@   .@*    *@   ***   .@@*@@@  @*          @@@.       @@@@@      
 @* @  *.  @        .. .*@**.  *..@    @@     .@       .@@@   @@@@*              ...        @@      
    .. *@**.         .*.*@*.   .@*   .@@       **     .**.    .@@.          .  ..*@@  .@.   @@  .*. 
     *@@**.             *@.    *@*. *@*    @@@@@@@*.                        *@*@.*@.  *@.   @@   .@@
   .@*.               .@@.   .*  *@@@.     ..****@@@@@@@******..**@*          @*.        .*@@     ..
  .*.                .**   .                        ..**@@@@@@@@@@@.                      ..        

    """
    print(water(BOARD))
    print(red("                  [Warning] 本项目仅供学习、交流使用，严禁用于商业或任何非法用途！"))
    print()

    if len(COOKIE) < 50:
        print(red("请写入参照 操作示例.mp4 写入cookie。"))
        pause()
        leave()

    TIME = input(blue("输入选课时间（例：2024-09-21 08:00:00）：", True))
    while True:
        try:
            start_time = time.mktime(time.strptime(TIME, "%Y-%m-%d %H:%M:%S"))
            break
        except:
            TIME = input(red("时间格式不正确（例：2024-09-21 08:00:00）：", True))

    try:
        courses = get_course()["data"]
    except KeyError:
        print(red("没有可选课程"))
        pause()
        leave()
    except requests.exceptions.JSONDecodeError:
        print(red("请写入参照 操作示例.mp4 写入cookie。"))
        pause()
        leave()

    versionNum = courses["versionNum"]
    activityList = courses["activityList"]

    for i, _list in enumerate(activityList):
        print(blue(f"{i}: {_list[list(_list.keys())[-1]]}"))

    if len(activityList) == 1:
        termId = activityList[0]["activityId"]
    else:
        i = input(blue("您要选择的时段：", True))
        while True:
            try:
                i = int(i) - 1
                break
            except ValueError:
                i = input(red("请输入数字：", True))
        termId = activityList[i]["activityId"]

    courses = get_course(termId)["data"]["allCourseInfo"]

    course_dict = {}
    course_info = {}
    for i, k_ in enumerate(courses.keys()):
        course = courses[k_]
        course_name = course["courseName"].replace(' ', '_')
        courseId = course["courseId"]
        print(blue(f"{i}: {course_name}"))
        course_dict[course_name] = courseId
        info_dict = []
        for key in ["teacherIntroducation", "courseRemark", "courseIntroducation"]:
            try:
                info_dict.append(course[key])
            except KeyError:
                info_dict.append("暂无")
        info_dict = (f"授课老师：{info_dict[0]}\n"
                     f"{info_dict[1]}"
                     f"课程简介：{info_dict[2]}")

        course_info[course_name] = info_dict

    course_name = input(blue("请输入所选课程名称：（以空格分隔 -q classname查看简介）", True)).split(" ")
    while True:
        if course_name[0].startswith('-q'):
            course_name = course_name[1:]
            if all([x in course_dict.keys() for x in course_name]):
                for k in course_name:
                    print(water(f"{k}:\n"
                          f"{course_info[k]}"))
                course_name = input(blue("请输入所选课程名称：（以空格分隔 -q classname查看简介）", True)).split(" ")
                continue
            else:
                course_name = input(red("所选课程名称不正确：（以空格分隔 -q classname查看简介）", True)).split(" ")
                continue

        elif not all([x in course_dict.keys() for x in course_name]):
            course_name = input(red("所选课程名称不正确：（以空格分隔 -q classname查看简介）", True)).split(" ")
            continue

        break

    course_str = "、".join(course_name)
    while True:
        if time.time() > start_time + 30:
            for c_name in course_name[:]:  # 使用course_name[:]来避免在迭代过程中修改列表
                t = threading.Thread(
                    target=choose_course,
                    args=(termId, c_name, course_dict[c_name], versionNum, course_name),
                )
                t.start()
            time.sleep(0.5)

        elif time.time() > start_time - 0.1:
            for c_name in course_name[:]:  # 使用course_name[:]来避免在迭代过程中修改列表
                t = threading.Thread(
                    target=choose_course,
                    args=(termId, c_name, course_dict[c_name], versionNum, course_name),
                )
                t.start()
            time.sleep(0.02)  # 保护学校系统

        else:
            print(
                f"\r\033[K{blue(f'chosen {course_str} waiting {- time.time() + start_time:.2f} seconds')}",
                flush=True,
                end="",
            )
            time.sleep(0.05)

        if len(course_name) == 0:
            print(green("选课完成"))
            pause()
            leave()

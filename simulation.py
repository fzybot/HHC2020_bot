# -*- coding: utf-8 -*-
"""
Created on 10/12/2020 12:27 PM

@author: Ruslan V. Akhpashev
"""
#TODO the documentation should be added
#TODO the code should be optimized



TOKEN = 'find your token in source code, try to find by "sign" phrase'

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time

import numpy as np
import random
import json
import pickle

mode = 0 # play 5G
category = 0 # play first category
sub_path_5G =['5G\IRF\\', '5G\RTT\\', '5G\RRM\\']
play_button_path = ['/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[1]/div/div/div[2]/div',
                    '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[2]/div/div/div[2]/div',
                    '/html/body/app/div[1]/nomination/div/div/div[2]/div[3]/div[3]/div/div/div[2]/div']
browser = webdriver.Firefox(executable_path='geckodriver.exe')

questions = []


def score():
    return browser.find_element_by_class_name('game__user-value').text

def open_browser():
    browser.get(TOKEN)
    print('Open browser')
    time.sleep(3)

def enter_quiz():
    battle_button = browser.find_element_by_class_name('about__buttons')
    battle_button.click()
    print("Enter to the quiz")
    time.sleep(3)

def choose_category(mode, category):
    print("category: ", category)
    slider = browser.find_elements_by_class_name('slider__item')
    slider[mode].click()
    print("Enter 5G")
    menu = browser.find_elements_by_class_name('profile__theme')
    menu[category].click()
    print('Enter theme')
    time.sleep(2)

def play():
    categories_play_button = browser.find_element_by_xpath(play_button_path[category])#('button-group-2x')
    categories_play_button.click()
    print('Play a game click')
    time.sleep(20)

def re_play():
    replay_button = browser.find_element_by_xpath('/html/body/app/div[1]/result/div/div/div[9]/div[1]')
    replay_button.click()
    time.sleep(20)

def rounds():

    json_data = {}
    for game in range(5):
        with open(sub_path_5G[category] + 'questions.json', 'r') as file:
            questions = json.load(file)
        counter = 0
        for i in questions:
            if (i["answers"]["right"]) != "":
                counter += 1
        print("Right answers:",counter,"  ","All questions: ", len(questions))
        print('Раунд {}'.format(game + 1))

        round_url = ""
        round_question = browser.find_element_by_class_name('game__question-text')
        print("current question is: ",round_question.text)
        round_answers = browser.find_elements_by_class_name('game__answer')
        # if browser.find_element_by_class_name('game__question-image'):
        #     round_url = browser.find_element_by_class_name('game__question-image').text

        question_flag = False
        question_index = 0
        game_score = score()
        right_answer = ''
        wrong_answer = ''
        for i in range(len(questions)):
            if round_question.text == questions[i]["question"]:
                question_flag = True
                question_index = i
                print("We found a question in data base")
                print("Right answer : ", questions[question_index]["answers"]["right"])
        if question_flag:
            if questions[question_index]["answers"]["right"] != "":
                #right_index = int(questions[question_index]["answers"]["right"])
                print("We already have the right answer")
                for k in range(len(round_answers)):
                    if round_answers[k].text == questions[question_index]["answers"]["right"]:
                        round_answers[k].click()
                        #time.sleep(2)
                        print("Right answer is cliked")
                        break
                #time.sleep(4)
                curr_score = score()
                if game_score == curr_score:
                    print("ALARM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    #questions[question_index]["answers"]["right"] = ""
                else:
                    print("Uraaaaaaaaaaaaaaaaaa")
            else:
                rand_index = np.random.randint(0, 4)
                # print("Random click: ", rand_index)
                # round_answers[rand_index].click()
                for n in range(len(round_answers)):
                    count_2 = 0
                    for m in range(len(questions[question_index]["answers"]["wrong"])):
                        if round_answers[n].text == questions[question_index]["answers"]["wrong"][m]:
                            count_2 += 1
                            print("Wrong copy checked")
                            break
                    if count_2 == 0:
                        round_answers[n].click()
                        rand_index = n
                        print("Wrong copy checked is not found")
                        break
                #time.sleep(4)
                curr_score = score()
                if curr_score != game_score:
                    right_answer = round_answers[rand_index].text
                    print("Right answer is found")
                    questions[question_index]["answers"]["right"] = right_answer
                else:
                    wrong_answer = round_answers[rand_index].text
                    if len(questions[question_index]["answers"]["wrong"]) > 0:
                        count = 0
                        for wr in questions[question_index]["answers"]["wrong"]:
                            if wrong_answer == wr:
                                count += 1
                                print("Wrong copy found")
                        if count == 0:
                            print("append wrong answer")
                            questions[question_index]["answers"]["wrong"].append(wrong_answer)
                    else:
                        print("append wrong answer")
                        questions[question_index]["answers"]["wrong"].append(wrong_answer)

        else:
            print("The question is not found in data base")
            rand_index = np.random.randint(0, 4)
            print("Random click: ", rand_index)
            round_answers[rand_index].click()
            #time.sleep(4)
            curr_score = score()
            if curr_score != game_score:
                right_answer = round_answers[rand_index].text
            else:
                wrong_answer = round_answers[rand_index].text
            json_data = {
                "question": str(round_question.text),
                "answers":
                    {
                        "0": round_answers[0].text,
                        "1": round_answers[1].text,
                        "2": round_answers[2].text,
                        "3": round_answers[3].text,
                        "right": right_answer,
                        "wrong": [wrong_answer]
                    }
            }
            print("New question is added")
            questions.append(json_data)
        if game == 4:
            time.sleep(5)
        else:
            time.sleep(40)
        with open(sub_path_5G[category] + 'questions.json', 'w') as write_file:
            json.dump(questions, write_file, indent=2)
    # with open(sub_path_5G[category] + 'questions.txt', 'r') as write_file:
    #     json.dump(questions, write_file, indent=2)
    time.sleep(5)








if __name__ == '__main__':
    while True:
        try:
            category = np.random.randint(0, 3)
            open_browser()
            enter_quiz()
            choose_category(mode, category)
            play()
            for i in range(10):
                rounds()
                re_play()
        except Exception as e:
            print(e)
            print("something wrong")
            browser.quit()
            time.sleep(2)
            browser = webdriver.Firefox(executable_path='geckodriver.exe')
            time.sleep(3)
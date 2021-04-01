import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
import design  # Это наш конвертированный файл дизайна
from design import Ui_MainWindow
from yandex_connect import YandexConnectDirectory
import transliterate
from pyad import pyad

import shutil, os, sys, subprocess, time

api = YandexConnectDirectory('API от яндекса', org_id=None)  # ключ почтаря
pyad.set_defaults(ldap_server="domenname.corp", username="admin", password="PASSWORD")  # от какого имени использовать АД
# dict_depmini = ["АВА Инвест", "АВА СИТИ", "АВА Сочи", "Агентство по продажам недвижимости",
#                 "Административный департамент", "Администрация", "АСК",
#                 "АХО", "ГрантСтрой", "Департамант развития УК", "Департамент HR", "Департамент бухгалтерии",
#                 "Департамент бюджетного управления", "Департамент бюджетного управления",
#                 "Департамент маркетинга и анализа", "Департамент по взаимодействию со СМИ",
#                 "Департамент рекламы", "Единый контактный центр", "Инженерные сети", "ИП Арутюнян ЛС", "ИТ",
#                 "Контрольно-ревизионный департамент", "Лидер Авто Строй", "ОП АВА СИТИ", "ОП АСК", "ОП СЗ АВА Сочи",
#                 "ОП СЗ АВА Сочи",
#                 "СБ", "Служба охраны труда", "Служба охраны труда", "Строительный департамент", "Строй Центр Проект",
#                 "Финансы", "Юристы"
#
#                 ]
dict_dep = {
    "АВА Инвест": {"Градстрой": "ou=АВА Инвест, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   "Инвест проект Сочи": "ou=АВА Инвест, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   "Коммерческий блок": "ou=АВА Инвест, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   "Руководители": "ou=АВА Инвест, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   "Служба тех заказчика": "ou=АВА Инвест, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "АВА СИТИ": {"АВА СИТИ": "ou=АВА СИТИ, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "АВА Сочи": {"Администрация": "OU=Администрация,OU=Sochi,DC=AVA,DC=corp",
                 "Бухгалтерия": "ou=Бухгалтерия, OU=Sochi,DC=AVA,DC=corp",
                 "деп упр проектами": "ou=деп упр проектами,OU=Sochi,DC=AVA,DC=corp",
                 "Инвест": "ou=Инвест,OU=Sochi,DC=AVA,DC=corp",
                 "Ипотека": "ou=Ипотека,OU=Sochi,DC=AVA,DC=corp",
                 "ИТ": "ou=ИТ,OU=Sochi,DC=AVA,DC=corp",
                 "отдел кадров": "ou=Кадр,OU=Sochi,DC=AVA,DC=corp",
                 "Клиентский СКС": "ou=Клиентский СКС,OU=Sochi,DC=AVA,DC=corp",
                 "ОП": "OU=ОКС,OU=Sochi,DC=AVA,DC=corp",
                 "ОКС": "OU=ОКС,OU=Sochi,DC=AVA,DC=corp",
                 "ПТО": "ou=ПТО,OU=Sochi,DC=AVA,DC=corp",
                 "Ресепшн": "ou=Ресепшн,OU=Sochi,DC=AVA,DC=corp",
                 "УК МО": "ou=УК МО,OU=Sochi,DC=AVA,DC=corp",
                 "Юристы": "ou=Юристы,OU=Sochi,DC=AVA,DC=corp",
                 },
    "Агентство по продажам недвижимости": {
        "Агентство по продажам недвижимости": "ou=Агентство по продажам недвижимости, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Административный департамент": {
        "Административный департамент": "ou=Административный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Администрация": {"Администрация": "ou=Администрация, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "АСК": {"Администрация": "ou=Администрация,ou=АСК, ou=!NEW, ou=KSC, dc=ava, dc=corp",
            "Служба технической экспертизы недвижимости": "ou=Служба технической экспертизы недвижимости,ou=АСК, ou=!NEW, ou=KSC, dc=ava, dc=corp",
            "Юридический отдел": "ou=Юридический отдел,ou=АСК, ou=!NEW, ou=KSC, dc=ava, dc=corp",
            },
    "АХО": {"АХО": "ou=АХО, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    # "ГК АВА по г Сочи": {"ou=ГК АВА по г Сочи, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "ГрантСтрой": {"Администрация": "ou=Администрация, ou=ГрантСтрой, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   "ПТО": "ou=ПТО, ou=ГрантСтрой, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   "СДО": "ou=СДО, ou=ГрантСтрой, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                   },
    "Департамант развития УК": {"Европейский дом": "ou=Департамант развития УК, ou=!NEW, ou=KSC, dc=ava, dc=cor",
                                "Министерские озера": "ou=Департамант развития УК, ou=!NEW, ou=KSC, dc=ava, dc=cor",
                                "Уютный дом": "ou=Департамант развития УК, ou=!NEW, ou=KSC, dc=ava, dc=cor",
                                },
    "Департамент HR": {"Отдел персонала": "ou=Отдел персонала, ou=Департамент HR, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                       "Служба кадрового администрирования": "ou=Служба кадрового администрирования, ou=Департамент HR, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                       "Учебный центр": "ou=Учебный центр, ou=Департамент HR, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                       },
    "Департамент бухгалтерии": {"214 ФЗ": "ou=214 ФЗ, ou=Департамент бухгалтерии, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                                "АСК": "ou=АСК, ou=Департамент бухгалтерии, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                                "Бородинская": "ou=Бородинская, ou=Департамент бухгалтерии, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                                "Генеральный подрядчик": "ou=Генеральный подрядчик, ou=Департамент бухгалтерии, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                                "УК": "ou=УК, ou=Департамент бухгалтерии, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                                },
    "Департамент бюджетного управления": {
        "Департамент бюджетного управления": "ou=Департамент бюджетного управления, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Департамент маркетинга и анализа": {
        "Департамент маркетинга и анализа": "ou=Департамент маркетинга и анализа, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Департамент по взаимодействию со СМИ": {"Департамент по взаимодействию со СМИ":
                                                 "ou=Департамент по взаимодействию со СМИ, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Департамент рекламы": {"Департамент рекламы": "ou=Департамент рекламы, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Единый контактный центр": {
        "Единый контактный центр": "ou=Единый контактный центр, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Инженерные сети": {"Инженерные сети": "ou=Инженерные сети, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "ИП Арутюнян ЛС": {"ИП Арутюнян ЛС": "ou=ИП Арутюнян ЛС, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "ИТ": {"ИТ": "ou=ИТ, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Контрольно-ревизионный департамент": {
        "Контрольно-ревизионный департамент": "ou=Контрольно-ревизионный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Лидер Авто Строй": {"Лидер Авто Строй": "ou=Лидер Авто Строй, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "ОП АВА СИТИ": {"ОП АВА СИТИ": "ou=ОП АВА СИТИ, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "ОП АСК": {"Администрация": "ou=Администрация, ou=ОП АСК, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               "Ипотека": "ou=Ипотека, ou=ОП АСК, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               "Менеджеры ОРИП": "ou=Менеджеры ОРИП, ou=ОП АСК, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               },
    "ОП СЗ АВА Сочи": {"ОП СЗ АВА Сочи": "ou=ОП СЗ АВА Сочи, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "СБ": {"КРУ": "ou=КРУ, ou=СБ, ou=!NEW, ou=KSC, dc=ava, dc=corp",
           "Отдел внутреннего контроля": "ou=Отдел внутреннего контроля, ou=СБ, ou=!NEW, ou=KSC, dc=ava, dc=corp",
           "Отдел контроля закупок": "ou=Отдел контроля закупок, ou=СБ, ou=!NEW, ou=KSC, dc=ava, dc=corp",
           "ЧОО АВА": "ou=ЧОО АВА, ou=СБ, ou=!NEW, ou=KSC, dc=ava, dc=corp", },
    "Служба охраны труда": {"Служба охраны труда": "ou=Служба охраны труда, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "Строительный департамент": {
        "Инженерная служба": "ou=Инженерная служба, ou=Строительный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp",
        "ОКС": "ou=ОКС, ou=Строительный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp",
        "ПТО": "ou=ПТО, ou=Строительный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp",
        "Рабочие группы по проектам": "ou=Рабочие группы по проектам, ou=Строительный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp",
        "СДО": "ou=СДО, ou=Строительный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp",
        "Служба технического надзора": "ou=Служба технического надзора, ou=Строительный департамент, ou=!NEW, ou=KSC, dc=ava, dc=corp",
    },
    "Строй Центр Проект": "ou=Строй Центр Проект, ou=!NEW, ou=KSC, dc=ava, dc=corp",
    "Финансы": {"Департамент казначейства": "ou=Департамент казначейства, ou=Финансы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                "Департамент корпоративных финансов": "ou=Департамент корпоративных финансов, ou=Финансы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                "ПИФ": "ou=ПИФ, ou=Финансы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
                },
    "Юристы": {"Администрация": "ou=Администрация, ou=Юристы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               "Департамент земельно-имущественных отношений": "ou=Департамент земельно-имущественных отношений, ou=Юристы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               "Корпоративно-договорной отдел ГК АВА": "ou=Корпоративно-договорной отдел ГК АВА, ou=Юристы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               "Отдел судебного сопровождения": "ou=Отдел судебного сопровождения, ou=Юристы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               "Отдел юридического сопровождения сделок": "ou=Отдел юридического сопровождения сделок, ou=Юристы, ou=!NEW, ou=KSC, dc=ava, dc=corp",
               }
}
# print(dict_dep["СБ"]["КРУ"])

dict_hranilka = {
    "АВА Инвест": {"Градстрой": "\\\\hranilka\\AVAGroup\\AVA\\АВА инвест\\!Градстрой",
                   "Инвест проект Сочи": "\\\\hranilka\\AVAGroup\\AVA\\АВА инвест\\!Инвест проект Сочи",
                   "Коммерческий блок": "\\\\hranilka\\AVAGroup\\AVA\\АВА инвест\\!Коммерческий блок",
                   "Руководители": "\\\\hranilka\\AVAGroup\\AVA\\АВА инвест\\!Руководители",
                   "Служба тех заказчика": "\\\\hranilka\\AVAGroup\\AVA\\АВА инвест\\!Служба тех заказчика"},
    "АВА СИТИ": {"АВА СИТИ": "\\\\hranilka\\AVAGroup\\AVA\\АВА СИТИ\\Документы отдела"},
    "АВА Сочи": {"Администрация": "\\\\192.168.170.4\\ForAll AS\\Администрация",
                 "Бухгалтерия": "\\\\192.168.170.4\\ForAll AS\\Бухгалтерия",
                 "деп упр проектами": "\\\\192.168.170.4\\ForAll AS\\Управление проектами",
                 "Инвест": "\\\\192.168.170.4\\ForAll AS\\взаимодействие с гос. структурами",
                 "Ипотека": "\\\\192.168.170.4\\ForAll AS\Ипотека",
                 "ИТ": "\\\\192.168.170.4\\ForAll AS\\ИТ",
                 "отдел кадров": "\\\\192.168.170.4\\ForAll AS\\HR",
                 "Клиентский СКС": "\\\\192.168.170.4\\ForAll AS\\СКС",
                 "ОП": "\\\\192.168.170.4\\ForAll AS\\ОП",
                 "ПТО": "\\\\192.168.170.4\\ForAll AS\\ПТО СДО",
                 "ОКС": "\\\\192.168.170.4\\ForAll AS\\ПТО СДО",
                 "Ресепшн": "\\\\192.168.170.4\\ForAll AS\\Ресепшн",
                 "УК МО": "\\\\192.168.170.4\\ForAll AS\\УК МО",
                 "Юристы": "\\\\192.168.170.4\\ForAll AS\\Юристы",
                 },
    "Агентство по продажам недвижимости": {
        "Агентство по продажам недвижимости": "\\\\hranilka\\AVAGroup\\AVA\\Агентство по продажам недвижимости"},

    "Административный департамент": {
        "Административный департамент": "\\\\hranilka\\AVAGroup\\AVA\\Административный департамент\\!Документы отдела"},
    "Администрация": {"Администрация": "\\\\hranilka\\AVAGroup\\AVA\\Администрация"},
    "АСК": {"Администрация": "\\\\hranilka\\AVAGroup\\AVA\\АСК\\!Администрация",
            "Служба технической экспертизы недвижимости": "\\\\hranilka\\AVAGroup\\AVA\\АСК\\!Служба технической экспертизы недвижимости",
            "Юридический отдел": "\\\\hranilka\\AVAGroup\\AVA\\АСК\\!Юридический отдел",
            },
    "АХО": {"АХО": "\\\\hranilka\\AVAGroup\\AVA\\АХО"},
    "ГК АВА по г Сочи": {"ГК АВА по г Сочи": "\\\\hranilka\\AVAGroup\\AVA\\ГК АВА по г Сочи\\Документы отдела"},
    "ГрантСтрой": {"Администрация": "\\\\hranilka\\AVAGroup\\AVA\\ГрантСтрой\\!Документы Администрация",
                   "ПТО": "\\\\hranilka\\AVAGroup\\AVA\\ГрантСтрой\\!Документы ПТО",
                   "СДО": "\\\\hranilka\\AVAGroup\\AVA\\ГрантСтрой\\!Документы СДО",
                   },
    "Департамант развития УК": {
        "Европейский дом": "\\\\hranilka\\AVAGroup\\AVA\\Департамант развития УК\\Документы Европейский дом",
        "Министерские озера": "\\\\hranilka\\AVAGroup\\AVA\\Департамант развития УК\\Документы Министерские озера",
        "Уютный дом": "\\\\hranilka\\AVAGroup\\AVA\\Департамант развития УК\\Документы Уютный дом",
    },
    "Департамент HR": {
        "Отдел персонала": "\\\\hranilka\\AVAGroup\\AVA\\Департамент HR\\!Отдел подбора, обучения и развития персонала",
        "Служба кадрового администрирования": "\\\\hranilka\\AVAGroup\\AVA\\Департамент HR\\!Служба кадрового администрирования",
        "Учебный центр": "\\\\hranilka\\AVAGroup\\AVA\\Департамент HR\\!Учебный центр",
        "!Служба мотивации": "\\\\hranilka\\AVAGroup\\AVA\\Департамент HR\\!Служба мотивации",
    },
    "Департамент бухгалтерии": {"214 ФЗ": "\\\\hranilka\\AVAGroup\\AVA\\Департамент бухгалтерии\\!Документы 214 ФЗ",
                                "АСК": "\\\\hranilka\\AVAGroup\\AVA\\Департамент бухгалтерии\\!Документы АСК",
                                "Бородинская": "\\\\hranilka\\AVAGroup\\AVA\\Департамент бухгалтерии\\!Документы Бородинская",
                                "Генеральный подрядчик": "\\\\hranilka\\AVAGroup\\AVA\\Департамент бухгалтерии\\!Документы Генеральный подрядчик",
                                "УК": "\\\\hranilka\\AVAGroup\\AVA\\Департамент бухгалтерии\\!Документы Управляющие компании",
                                },
    "Департамент бюджетного управления": {
        "Департамент бюджетного управления": "\\\\hranilka\\AVAGroup\\AVA\\Департамент бюджетного управления"},
    "Департамент маркетинга и анализа": {
        "Департамент маркетинга и анализа": "\\\\hranilka\\AVAGroup\\AVA\\Департамент маркетинга и анализа"},
    "Департамент по взаимодействию со СМИ": {
        "Департамент по взаимодействию со СМИ": "\\\\hranilka\\AVAGroup\\AVA\\Департамент по взаимодействию со СМИ"},
    "Департамент рекламы": {"Департамент рекламы": "\\\\hranilka\\AVAGroup\\AVA\\Департамент рекламы"},
    "Единый контактный центр": {"Единый контактный центр": "\\\\hranilka\\AVAGroup\\AVA\\Единый контактный центр"},
    "Инженерные сети": {"Инженерные сети": "\\\\hranilka\\AVAGroup\\AVA\\Инженерные сети\\!Документы отдела"},
    "ИП Арутюнян ЛС": {"ИП Арутюнян ЛС": "\\\\hranilka\\AVAGroup\\AVA\\ИП Арутюнян ЛС"},
    "ИТ": {"ИТ": "\\\\hranilka\\AVAGroup\\AVA\\ИТ"},
    "Контрольно-ревизионный департамент": {
        "Контрольно-ревизионный департамент": "\\\\hranilka\\AVAGroup\\AVA\\Контрольно-ревизионный департамент"},
    "Лидер Авто Строй": {"Лидер Авто Строй": "\\\\hranilka\\AVAGroup\\AVA\\Лидер Авто Строй"},
    "ОП АВА СИТИ": {"ОП АВА СИТИ": "\\\\hranilka\AVAGroup\\AVA\\ОП АВА СИТИ\\Документы отдела"},
    "ОП АСК": {"Администрация": "\\\\hranilka\\AVAGroup\\AVA\\ОП АСК\\ОТДЕЛ ПРОДАЖ\\008-Сотрудники",
               "Ипотека": "\\\\hranilka\\AVAGroup\\AVA\\ОП АСК\\ОТДЕЛ ПРОДАЖ\\008-Сотрудники",
               "Менеджеры ОРИП": "\\\\hranilka\\AVAGroup\\AVA\\ОП АСК\\ОТДЕЛ ПРОДАЖ\\008-Сотрудники",
               },
    "ОП СЗ АВА Сочи": {"ОП СЗ АВА Сочи": "\\\\hranilka\\AVAGroup\\AVA\\ОП СЗ АВА Сочи\\Документы отдела"},
    "СБ": {"КРУ": "\\\\hranilka\\AVAGroup\\AVA\\СБ\\!Документы отдела",
           "Отдел внутреннего контроля": "\\\\hranilka\\AVAGroup\\AVA\\СБ\\!Документы отдела",
           "Отдел контроля закупок": "\\\\hranilka\\AVAGroup\\AVA\\СБ\\!Документы отдела",
           "ЧОО АВА": "\\\\hranilka\\AVAGroup\\AVA\\СБ\\!Документы отдела", },
    "Служба охраны труда": {"Служба охраны труда": "\\\\hranilka\\AVAGroup\\AVA\\Служба охраны труда"},
    "Строительный департамент": {
        "Инженерная служба": "\\\\hranilka\\AVAGroup\\AVA\\Строительный департамент\\Документы Инженерная служба",
        "ОКС": "\\\\hranilka\\AVAGroup\\AVA\\Строительный департамент\\Документы ОКС",
        "ПТО": "\\\\hranilka\\AVAGroup\\AVA\\Строительный департамент\\Документы ОКС",
        "Рабочие группы по проектам": "\\\\hranilka\\AVAGroup\\AVA\\Строительный департамент\\Документы Рабочие группы",
        "СДО": "\\\\hranilka\\AVAGroup\\AVA\\Строительный департамент\\Документы ОКС",
        "Служба технического надзора": "\\\\hranilka\\AVAGroup\\AVA\\Строительный департамент\\Документы ОКС",
    },
    "Строй Центр Проект": {"Строй Центр Проект": "\\\\hranilka\\AVAGroup\\AVA\\Строй Центр Проект\\!Документы отдела"},
    "Финансы": {"Департамент казначейства": "\\\\hranilka\\AVAGroup\\AVA\\Финансы\\!Департамент казначейства",
                "Департамент корпоративных финансов": "\\\\hranilka\\AVAGroup\\AVA\\Финансы\\!ДКФ",
                "ПИФ": "\\\\hranilka\\AVAGroup\\AVA\\Финансы\\!ПИФ",
                },
    "Юристы": {"Администрация": "\\\\hranilka\\AVAGroup\\AVA\\Юристы\\Администрация",
               "Департамент земельно-имущественных отношений": "\\\\hranilka\\AVAGroup\\AVA\\Юристы\\!Департамент земельно-имущественных отношений",
               "Корпоративно-договорной отдел ГК АВА": "\\\\hranilka\\AVAGroup\\AVA\\Юристы\\!Корпоративно-договорной отдел ГК АВА",
               "Отдел судебного сопровождения": "\\\\hranilka\\AVAGroup\\AVA\\Юристы\\!Отдел судебного сопровождения",
               "Отдел юридического сопровождения сделок": "\\\\hranilka\\AVAGroup\\AVA\\Юристы\\!Отдел ЮСС",
               }
}

dict_OUGroup = {
    "АВА Инвест": {"Градстрой": "Инв_Деп_Градостроительства_G_B14",
                   "Инвест проект Сочи": "Инв_инвест проект Сочи_G_B14",
                   "Коммерческий блок": "Инв_Коммерческий блок_G_B14",
                   "Руководители": "Инв_Руководство_G_B14",
                   "Служба тех заказчика": "Инвест_Служба тех заказчика_G_B14"},
    "АВА СИТИ": {"АВА СИТИ": "MSK_AVA_G"},
    "АВА Сочи": {"Администрация": "АВА Сочи_G_B14",
                 "Бухгалтерия": "Бухгалтерия_G_Sochi",
                 "деп упр проектами": "управление проектами_G_Sochi",
                 "Инвест": "взаимодействие с гос. структурами_G_AS",
                 "Ипотека": "Ипотека_G_Sochi",
                 "ИТ": "IT_G_Sochi",
                 "отдел кадров": "HR_Кадры_G_AS",
                 "Клиентский СКС": "СКС_G_Sochi",
                 "ОП": "ОП_G_Sochi",
                 "ПТО": "ПТО_АВА Сочи_G",
                 "ОКС": "ОКС_G_Sochi",
                 "Ресепшн": "ресепшн Сочи_G",
                 "УК МО": "УК_МО_G_AS",
                 "Юристы": "Юристы_G_Sochi",
                 },
    "Агентство по продажам недвижимости": {
        "Агентство по продажам недвижимости": "Агенство по продажам_G_B14"},
    "Административный департамент": {
        "Административный департамент": "Админ деп_G_B14"},
    "Администрация": {"Администрация": "Администрация_G_B14"},
    "АСК": {"Администрация": "Администрация_G_ACK",
            "Служба технической экспертизы недвижимости": "АСК_техэкспертиза_G_B14",
            "Юридический отдел": "АСК_Юристы_G",
            },
    "АХО": {"АХО": "АХО_G_B14"},
    # "ГК АВА по г Сочи": {"ou=ГК АВА по г Сочи, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "ГрантСтрой": {"Администрация": "ГрантСтрой_Администрация_G_B14",
                   "ПТО": "ГрантСтрой_ПТО_G_B14",
                   "СДО": "ГрантСтрой_СДО_G_B14",
                   },
    "Департамант развития УК": {"Европейский дом": "УК все_G",
                                "Министерские озера": "УК все_G",
                                "Уютный дом": "УК все_G",
                                },
    "Департамент HR": {"Отдел персонала": "HR_Персонал_G_B14",
                       "Служба кадрового администрирования": "HR_Кадры_G_B14",
                       "Учебный центр": "HR_Учебный центр_G_B14",
                       },
    "Департамент бухгалтерии": {"214 ФЗ": "Бух_213 ФЗ_G_АСК",
                                "АСК": "Бух_АСК_G_АСК",
                                "Бородинская": "Бух_Бородинская_G_B14",
                                "Генеральный подрядчик": "Бух_Генеральный подрядчик_G_B14",
                                "УК": "Бух_УК",
                                },
    "Департамент бюджетного управления": {
        "Департамент бюджетного управления": "деп бюджетного управления_G_B14"},
    "Департамент маркетинга и анализа": {
        "Департамент маркетинга и анализа": "Маркетинг_G_ACK"},
    "Департамент по взаимодействию со СМИ": {"Департамент по взаимодействию со СМИ": "СМИ"},
    "Департамент рекламы": {"Департамент рекламы": "Департамент рекламы_G_ACK"},
    "Единый контактный центр": {
        "Единый контактный центр": "CallCenter_G_ACK"},
    "Инженерные сети": {"Инженерные сети": "Инженерные сети_G_B14"},
    "ИП Арутюнян ЛС": {"ИП Арутюнян ЛС": "ИП_АрутюнянЛС_G_B10"},
    "ИТ": {"ИТ": "IT_G_B14"},
    "Контрольно-ревизионный департамент": {
        "Контрольно-ревизионный департамент": "КРД_G_B14"},
    "Лидер Авто Строй": {"Лидер Авто Строй": "Лидер Авто Строй_G"},
    "ОП АВА СИТИ": {"ОП АВА СИТИ": "Москва_G"},
    "ОП АСК": {"Администрация": "ОП_Админ_G_ACK",
               "Ипотека": "ОП_ипотека_G_ACK",
               "Менеджеры ОРИП": "ОРИП_Дом_G_U75",
               },
    # "ОП СЗ АВА Сочи": {"ОП СЗ АВА Сочи": "ou=ОП СЗ АВА Сочи, ou=!NEW, ou=KSC, dc=ava, dc=corp"},
    "СБ": {"КРУ": "СБ_КРУ_G_b14",
           "Отдел внутреннего контроля": "СБ_ОВК_G_b14",
           "Отдел контроля закупок": "СБ_ОКЗ_G_b14",
           "ЧОО АВА": "СБ_ЧОО АВА_G_B14", },
    "Служба охраны труда": {"Служба охраны труда": "Охрана труда_G_B14"},
    "Строительный департамент": {
        "Инженерная служба": "Строительный деп АСК_Инженерная служба_G_B14",
        "ОКС": "Строительный деп АСК_ОКС_G_B14",
        "ПТО": "ПТО_G_ACK",
        "Рабочие группы по проектам": "Строительный деп АСК_Раб группы_G_B14",
        "СДО": "Строительный деп АСК_СДО_G_B14",
        "Служба технического надзора": "Строительный деп АСК_технадзор_G_B14",
    },
    "Строй Центр Проект": {"Строй Центр Проект": "AllUsers_G_SCP"},
    "Финансы": {"Департамент казначейства": "Финансы_Казначейство_G_B14",
                "Департамент корпоративных финансов": "Финансы_корп финансы_G_B14",
                "ПИФ": "Финансы_ПИФ_G_B14",
                },
    "Юристы": {"Администрация": "Юристы_G_B14",
               "Департамент земельно-имущественных отношений": "деп земели_G_B14",
               "Корпоративно-договорной отдел ГК АВА": "Юристы_Копроративно-договорной ГК АВА_G_B14",
               "Отдел судебного сопровождения": "Юристы_Судебное сопровождение_G_B14",
               "Отдел юридического сопровождения сделок": "Юристы_юр сопровождение_G_B14",
               }
}


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.init_UI()  # имя в Титуле

    def init_UI(self):  # имя в Титуле
        self.setWindowTitle("Новый человечек")

        self.ui.lineEdit.setPlaceholderText("Фамилия Имя Отчество")
        self.ui.lineEdit_3.setPlaceholderText("номер телефона")
        self.ui.lineEdit_2.setPlaceholderText("Дожность")
        self.ui.plainTextEdit.setPlaceholderText("Лобов еврей")

        for _ in dict_dep:
            self.ui.comboBox.addItem(_)

        self.ui.pushButton.clicked.connect(self.act)  # заставляет работать
        self.ui.pushButton_2.clicked.connect(self.accept_dep)  # заставляет работать
        self.ui.pushButton_3.clicked.connect(self.accept_otdel)  # заставляет работать
        self.ui.pushButton_4.clicked.connect(self.nameFIO)  # проверка имени

    def accept_dep(self):
        global department
        department = self.ui.comboBox.currentText()
        for _ in dict_dep[department]:
            self.ui.comboBox_2.addItem(_)

    def accept_otdel(self):
        global OUdep, otdel
        otdel = self.ui.comboBox_2.currentText()
        OUdep = dict_dep[department][otdel]

    def act(self):
        global doljnost, mobile
        self.nameFIO()

        doljnost = self.ui.lineEdit_2.text()
        mobile = self.ui.lineEdit_3.text()
        self.nametranslite()
        self.create_user()

        self.create_folder()
        self.mail()
        self.give_folder_rights()
        self.ui.plainTextEdit.clear()
        self.ui.plainTextEdit.appendPlainText(
            "для {} Была создана учётка {} с паролем PASSWORD, почтой {}@domen.ru,и паролем почты PASSWORD  ".format(
                name, nameEngTrans, nameEngTrans))

    def nameFIO(self):

        global name
        name = self.ui.lineEdit.text()

        if [s for s in name if s in '1234567890QWERTYUIOPASDFGHJLZXCVBNMqwertyuiopasdfghjklzxcvbnm+-,.!:']:
            self.ui.plainTextEdit.appendPlainText('В имени могут быть только РУССКИЕ буквы')
        else:
            self.ui.plainTextEdit.appendPlainText(name)

    def nametranslite(self):
        global name1, name2, name3, nameEngTrans, nameRus
        nameEng = transliterate.translit(name, reversed=True)  # инициалы на английском
        # nameEng = nameEng.replace("ts'", "c")
        a = nameEng.split()
        nameEngTrans = (f'{a[0]}{a[1][0]}{a[2][0]}')
        nameEngTrans = nameEngTrans.replace("'", "")


        b = name.split()  # инициалы на русском
        nameRus = (f'{b[0]}{b[1][0]}{b[2][0]}')

        name1 = (f'{b[0]} ')  # фамилия
        name2 = (f'{b[1]} ')  # имя
        name3 = (f'{b[2]} ')  # отчество

    def create_user(self):  # создать почту
        global new_user
        ou = pyad.adcontainer.ADContainer.from_dn(OUdep)  # где создавать ?

        new_user = pyad.aduser.ADUser.create(nameEngTrans, ou, password="PASSWORD")

        new_user.update_attribute("displayName", name)  # выводимое имя
        new_user.update_attribute("sn", name1)  # Фамилия
        # new_user.update_attribute("cn", nameRus)  # Фамилия
        new_user.update_attribute("givenName", name2)  # Имя
        new_user.update_attribute("displayNamePrintable", nameRus)  # Имя

        new_user.update_attribute("mail", nameEngTrans + "@avagroup.ru")  # почта
        new_user.update_attribute("telephonenumber", mobile)  # телефон
        new_user.update_attribute("mobile", mobile)  # сотовый
        new_user.update_attribute("ipPhone", "3333")  # Рабочий
        new_user.update_attribute("sAMAccountName", nameEngTrans)
        new_user.update_attribute("userPrincipalName", nameEngTrans)

        new_user.update_attribute("title", doljnost)  # Должность
        new_user.update_attribute("department", department)  # Департамент
        # добавление в пользака в группу
        time.sleep(1)
        pscommand = 'Add-AdGroupMember -Identity "{}" -Members {}'.format(dict_OUGroup[department][otdel], nameEngTrans)
        subprocess.Popen(['powershell.exe', pscommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(2)
        pscommand = 'Add-AdGroupMember -Identity "AllAllUsers_G_AVA" -Members {}'.format(nameEngTrans)
        subprocess.Popen(['powershell.exe', pscommand], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            new_user.rename(name)
        except Exception:
            pass

    def create_folder(self):
        global adres_papki
        adres_papki = dict_hranilka[department][otdel] + "\\" + nameRus
        os.mkdir(adres_papki)

    def give_folder_rights(self):
        time.sleep(5)
        subprocess.check_output(
            r'C:\Windows\System32\icacls.exe "{}" /grant "{}":(OI)(CI)(F) /T /C /inheritance:e'.format(adres_papki,
                                                                                                       nameEngTrans),
            stderr=subprocess.STDOUT)

    def mail(self):
        api.user_add(nickname=nameEngTrans, password="PASSWORD", name=name2, secname=name1)  # добавление сотрудника


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложен ие


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

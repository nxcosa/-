import sqlite3


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def select_goods(name, size, place):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    sql = 'select * from goods where name like \'%' + name + '%\' and size like \'%' + size + '%\' and place like\'%' + place + '%\';'
    cursor.execute(sql)
    goods = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return goods


def select_records():
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute(
        'select time,name,size,place,kind,change,operating_personnel from records left join goods on records.id=goods.id order by time desc ;')
    records = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return records


def insert_goods(name, size, factory, place, price):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute('insert into goods values(null,?,?,?,?,?,0);', (name, size, factory, place, price,))
    cursor.close()
    conn.commit()
    conn.close()


def del_goods(id):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute('delete from goods where id=?;', (id,))
    cursor.close()
    conn.commit()
    conn.close()


def insert_records(id, kind, change, operating_personnel):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    if kind == 1:
        cursor.execute('insert into records values(?,datetime(\'now\',\'localtime\'),?,?,?);',
                       (id, '入库', change, operating_personnel,))
        cursor.execute('update goods set number=number+? where id=?;', (change, id,))
    else:
        cursor.execute('insert into records values(?,datetime(\'now\',\'localtime\'),?,?,?);',
                       (id, '出库', change, operating_personnel,))
        cursor.execute('update goods set number=number-? where id=?;', (change, id,))
    cursor.close()
    conn.commit()
    conn.close()


def update_goods(id, name, size, place, factory, price):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute('update goods set name=? ,size=?,place=?,factory=?,price=? where id=?;',
                   (name, size, place, factory, price, id,))
    cursor.close()
    conn.commit()
    conn.close()


def count_goods(place, kind, date1, date2):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()

    cursor.execute(
        'select goods.id as id,name,size,place,factory,price,number,kind,sum(change) as sum_change,price*sum(change) as money from goods left join records on goods.id = records.id where place=? and kind=? and time >=? and time<=? group by kind,goods.id order by goods.id;',
        (place, kind, date1, date2), )
    counts = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    return counts


def get_operating_personnel():
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('select name,id from empl_names')
    names = cursor.fetchall()
    cursor.close()
    conn.commit()
    conn.close()
    # print(names)
    return names

def add_empl_name(name):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('insert into empl_names values(null,?);', (name,))
    cursor.close()
    conn.commit()
    conn.close()


def del_empl_name(id):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('delete from empl_names where id=?', (id))
    cursor.close()
    conn.commit()
    conn.close()
def edit_empl_name(name,id):
    conn = sqlite3.connect('kucun.db')
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute('update empl_names set name=? where id = ?;',(name,id))
    cursor.close()
    conn.commit()
    conn.close()

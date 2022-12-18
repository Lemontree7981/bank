# a simple password manager
"""REMEMBER THIS REQUIRES SQL
For linux -> \"apt-get sqlite3\""""
import pyinputplus
import asyncio
import aiosqlite

async def main():
    db = await aiosqlite.connect('bank.db')
    c = await db.cursor()
    await c.execute('''CREATE TABLE "password_bank" (
	"account_name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("account_name")
);''')
    await db.commit()
    await c.close()
    await db.close()
    

class Main:
    def __init__(self,account_name=None,password=None):
        self.account_name = account_name
        self.password = password
    
    async def add(self):
        db = await aiosqlite.connect('bank.db')
        c = await db.cursor()
        await c.execute('''INSERT INTO password_bank VALUES (?,?)''',(self.account_name,self.password))
        await db.commit()
        await c.close()
        await db.close()
        
    async def view(self):
        db = await aiosqlite.connect('bank.db')
        c = await db.cursor()
        await c.execute("SELECT password FROM password_bank WHERE account_name='{}'".format(self.account_name))
        result = await c.fetchone()
        print(''.join(result))
        await c.close()
        await db.close()
    
    async def record(self):
        db = await aiosqlite.connect('bank.db')
        c = await db.cursor()
        await c.execute("SELECT account_name FROM password_bank")
        result = await c.fetchall()
        out = list(sum(result,()))
        print(', '.join(out))
        await c.close()
        await db.close()
        
    async def delete(self):
        db = await aiosqlite.connect('bank.db')
        c = await db.cursor()
        await c.execute(f"DELETE FROM password_bank WHERE account_name='{self.account_name}'")
        await db.commit()
        await c.close()
        await db.close()

async def final():
    running = True
    options = ["add","view","delete","list","exit"]
    
    while running:
        ask = input("Do you want to add a new account or view existing ones, also you can view the number of accounts saved {}: ".format((",").join(options)))
        
        if ask not in options:
            raise ValueError
            
        
        if ask ==  "add":
            ask2 = input("Write your account name: ")
            ask3 = pyinputplus.inputPassword("Write your password: ")
            Class = Main(ask2,ask3)
            await Class.add()
            quit()
        elif ask == "view":
            ask2 = input("Write your account name: ")
            Class = Main(ask2)
            await Class.view()
            break
        elif ask == "list":
            Class = Main()
            await Class.record()
            quit()
        elif ask == "delete":
            ask2 = input("Write your account name: ")
            Class = Main(ask2)
            await Class.delete()
            quit() 
        elif ask == "exit":
            quit()
            
        else:
            continue

try:
    asyncio.run(main())
except:
    pass
finally:
    asyncio.run(final())
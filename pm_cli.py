#!/usr/bin/env python

import mysql.connector
import typer
import inquirer


class PM:
    def __init__(self):
        self.cxn = mysql.connector.connect(
                user='root',
                password='ZSe45rdx##',
                database='logins',
                host='192.168.1.129',
                port=3306
                )

        self.cursor = self.cxn.cursor()

    # adds login info to database
    def add(self, wb, usr, pwd):

        add_login = ("INSERT INTO login "
                     "(website, username, password) "
                     "VALUES ( %s, %s, %s)")
        data_login = (wb, usr, pwd)

        self.cursor.execute(add_login, data_login)
        self.cxn.commit()

    # finds specific login
    def find(self, wb):
        query = ("SELECT username, password FROM login "
                 "WHERE website = %(website)s")
        query_condition = {'website': wb}

        self.cursor.execute(query, query_condition)

        for (username, password) in self.cursor: return username, password

    # todo: update to do either on
    # edit a saved username
    def edit_username(self, wb, usr):
        query = ("UPDATE login "
                 "SET username = %s "
                 "WHERE website = %s")
        query_condition = (
                usr,
                wb
                )

        self.cursor.execute(query, query_condition)
        self.cxn.commit()

    # edit a saved password
    def edit_password(self, wb, pwd):
        query = ("UPDATE login "
                 "SET password = %s "
                 "WHERE website = %s")
        query_condition = (
                pwd,
                wb
                )

        self.cursor.execute(query, query_condition)
        self.cxn.commit()

    # deletes a saved login
    def delete(self, wb):
        query = ("DELETE FROM login "
                 "WHERE website = %(website)s")
        query_condition = {'website': wb}

        self.cursor.execute(query, query_condition)
        self.cxn.commit()

    # shows all the websites with saved logins
    def show_all(self):
        saved_websites = []
        self.cursor.execute("SELECT * FROM login "
                            "ORDER BY website")
        for row in self.cursor.fetchall():
            saved_websites.append(row)
        return saved_websites


class CLI:
    pm = PM()

    def __init__(self):
        pass

    def cli_find(self):
        website = input("Enter the website you want the login for: ")
        login_info = self.pm.find(website)
        username = login_info[0]
        password = login_info[1]
        print(f'Username: {username}\nPassword: {password}\n')

    def cli_edit(self):
        website = input("Enter the website you want to edit the login for: ")
        decision = inquirer.list_input(f'Edit username or password for {website}', choices=['Username', 'Password'])
        if decision == 'Username':
            username = input(f'Enter the new username for {website}: ')
            self.pm.edit_username(website, username)
            print()
        elif decision == 'Password':
            password = input(f'Enter the new password for {website}: ')
            self.pm.edit_password(website, password)
            print()

    def cli_add(self):
        website = input("Enter the webstie you want to add a login for: ")
        username = input(f'enter the username for {website}: ')
        password = input(f'enter the password for {website}: ')
        self.pm.add(website, username, password)
        print()

    def cli_delete(self):
        website = input("Enter the webstie you want to delete a login for: ")
        self.pm.delete(website)
        print()

    def cli_main(self):
        while True:
            decision = inquirer.list_input("Add, find, edit, delete login or quit", choices=['Add', 'Find', 'Edit', 'Delete', 'Quit'])
            if decision == 'Add':
                self.cli_add()
            elif decision == "Find":
                self.cli_find()
            elif decision == "Edit":
                self.cli_edit()
            elif decision == "Delete":
                self.cli_delete()
            elif decision == "Quit":
                break


def main():
    cli = CLI()
    cli.cli_main()


if __name__ == "__main__":
    typer.run(main)

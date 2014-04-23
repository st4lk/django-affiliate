# -*- coding: utf-8 -*-
import logging
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
try:
    import MySQLdb as mdb
    from _mysql_exceptions import Warning as MysqlWarning
except ImportError:
    logging.error("MySQLdb is not installed")
    exit(1)


class Command(BaseCommand):
    help = '(Re)Create database (mysql) and tables for this project. '\
        'Example: python manange.py init_db --user=root --pwd=password'
    option_list = BaseCommand.option_list + (
        make_option('--user',
            action='store',
            dest='user',
            default='root',
            help='Database user name with rights to create database'),
        make_option('--pwd',
            action='store',
            dest='pwd',
            default=None,
            help='Database user password with rights to create database'),
        )

    def handle(self, *args, **options):
        db_name = settings.DATABASES['default']['NAME']
        self.stdout.write("Initializing database '{0}'".format(db_name))
        if not options['pwd']:
            self.stdout.write("Please, provide user password")
        else:
            try:
                con = mdb.connect('localhost',
                    options['user'], options['pwd'])
                cur = con.cursor()
                try:
                    cur.execute("DROP DATABASE IF EXISTS {0}".format(db_name))
                except MysqlWarning:
                    pass
                cur.execute("CREATE DATABASE {0} CHARACTER SET utf8;"
                    .format(db_name))
                db_user = settings.DATABASES['default']['USER']
                db_pwd = settings.DATABASES['default']['PASSWORD']
                cur.execute("GRANT ALL ON {db}.* TO '{user}'@'localhost' "
                    "IDENTIFIED BY '{pwd}';"
                    .format(db=db_name, user=db_user, pwd=db_pwd))
                call_command('syncdb', interactive=False)
                self.stdout.write("Done successfully")
            except mdb.Error as e:
                self.stdout.write("Error %d: %s" % (e.args[0], e.args[1]))

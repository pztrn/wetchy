# -*- coding: utf-8 -*-

# Wetchy database access class.
# Creates connection to database, execute queries, etc.

from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import text

from wetchy.lib import common

class Database:
    def __init__(self):
        common.INSTANCES["DATABASE"] = self
        self.config = common.SETTINGS["database"]
        
        # Create database connection.
        dbtype = self.config["type"]
        username = self.config["user"]
        password = self.config["password"]
        hostname = self.config["host"]
        port = self.config["port"]
        database = self.config["database"]
        db_string = "{0}://{1}:{2}@{3}:{4}/{5}?charset=utf8".format(dbtype, username, password, hostname, port, database)
        
        try:
            self.database = create_engine(db_string)
            self.database = self.database.connect()
            print("Connection to database established")
        except exc.OperationalError as e:
            print("Failed to connect to database: {0}".format(e))
            common.INSTANCES["RENDERER"].render_error(e)
            
        
    def execute(self, statement, parameters = None):
        """
        Execute some statement.
        
        @statement [str] - statement itself.
        @parameters [dict] - parameters dict. Will be used with
        SQLAlchemy text() method to avoid any possible injections.
        """
        result = None
        try:
            if not parameters:
                result = self.database.execute(statement).fetchall()
            else:
                result = self.database.execute(text(statement), parameters).fetchall()
        except exc.InternalError as e:
            print("Failed to execute statement: {0}".format(e))
            common.INSTANCES["RENDERER"].render_error(e)
        
        if result:
            if len(result) == 1:
                result = result[0]
            return result

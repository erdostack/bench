CREATE CONSTRAINT application_app_id IF NOT EXISTS FOR (a:Application) REQUIRE a.appId IS UNIQUE;

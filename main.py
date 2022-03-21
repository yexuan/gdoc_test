import gspread
import pandas as pd
import fire
import urllib
from sqlalchemy import create_engine


class gdoc(object):
    def __init__(self, private_key_id, private_key, dbpassword):
        self.credentials = {
        "type": "service_account",
        "project_id": "cpb100-163704",
        "private_key_id": private_key_id,
        "private_key": private_key.replace('\\n', '\n'),
        "client_email": "mobi-875@cpb100-163704.iam.gserviceaccount.com",
        "client_id": "109538201198876380083",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/mobi-875%40cpb100-163704.iam.gserviceaccount.com"
        }
        self.dbpassword = dbpassword

    def run(self):
        print(self.credentials)
        sa = gspread.service_account_from_dict(self.credentials)
        sh = sa.open("MO Operation Records")
        wks = sh.worksheet("2022 Operation TODO")
        df = pd.DataFrame(wks.get_all_records())
        DB_STRING = "mysql+pymysql://analyst:{}@cd-cdb-qptan8yq.sql.tencentcdb.com:61853/dashboard?charset=utf8".format(
            urllib.parse.quote_plus(self.dbpassword))
        engine = create_engine(DB_STRING)
        print(df.to_sql('operation_action', if_exists='append', con=engine))


if __name__ == '__main__':
    fire.Fire(gdoc)

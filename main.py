# from typing import Optional
import requests
import typer

from util import login, submit, server_jiang_push


def main(stu_id: str, passwd: str, seckey: str = typer.Option(None, help="Server酱的SCKEY")):
    session = requests.session()
    login(session, stu_id, passwd)
    message = submit(session)
    message = '疫情通丨' + message
    # print (message)
    if seckey:
        server_jiang_push(seckey, message)
    else:
        print(message)


if __name__ == "__main__":
    typer.run(main)

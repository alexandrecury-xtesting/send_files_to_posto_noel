
import pathlib
import requests
from ftp_service import send_file_to_remote_server
from xlsx_to_csv import convert

API_URL = 'http://zabbix.xtesting.com.br/orquestrador'
FILES_DIR: pathlib.Path = pathlib.Path('files')


def bootstrap():
    if not FILES_DIR.is_dir():
        FILES_DIR.mkdir()


def get_result_file(robot_id: int = 1, filename: str = ''):
    url = f"{API_URL}/robots/{robot_id}/resources/{filename}"
    response = requests.get(url, stream=True, timeout=60)
    if response.ok:
        filepath: pathlib.Path = pathlib.Path(FILES_DIR) / filename
        with open(filepath, "wb") as file:
            file.write(response.content)
        return filepath
    else:
        raise Exception('Failed to access orchestrator. ResponseError: %s', response.text)


if __name__ == "__main__":
    bootstrap()
    xlsx_filepath: pathlib.Path = get_result_file(filename='planilha_notebooks.xlsx')
    csv_filepath: pathlib.Path = pathlib.Path(FILES_DIR) / 'file.csv'
    convert(xlsx_filepath=xlsx_filepath.resolve(), csv_filepath=csv_filepath.resolve())
    if xlsx_filepath.exists():
        send_file_to_remote_server(
            filepath=csv_filepath.resolve(),
            filename='file.csv',
            path='/domains/innovatex.com.br/public_html/noel/files/csv/',
        )
    log_filepath: pathlib.Path = get_result_file(filename='log.html')
    if log_filepath.exists():
        send_file_to_remote_server(
            filepath=log_filepath.resolve(),
            filename='log.html',
            path='/domains/innovatex.com.br/public_html/noel/files/pdf/',
        )
    print("Arquivos enviados com sucesso!")

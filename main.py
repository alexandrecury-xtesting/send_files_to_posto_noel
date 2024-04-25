
import pathlib
import requests
from template_rpa import settings
from ftp_service import send_file_to_remote_server
from xlsx_to_csv import convert

API_URL = 'http://zabbix.xtesting.com.br/orquestrador'


def get_result_file(robot_id: int = 1, filename: str = ''):
    url = f"{API_URL}/robots/{robot_id}/resources/{filename}"
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        if response.ok:
            filepath: pathlib.Path = settings.output_dir / filename
            with open(filepath, "wb") as file:
                file.write(response.content)
            return filepath
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (4xx and 5xx status codes)
        if e.response.status_code == 404:
            raise FileNotFoundError(f'Resouce not found: {url}')
        else:
            raise Exception(f'Failed to access orchestrator. HTTPError: {e}')


if __name__ == "__main__":
    xlsx_filepath: pathlib.Path = get_result_file(filename=settings.variables['planilha'])
    # csv_filepath: pathlib.Path = settings.output_dir / 'file.csv'
    # convert(xlsx_filepath=xlsx_filepath.resolve(), csv_filepath=csv_filepath.resolve())
    if xlsx_filepath.exists():
        send_file_to_remote_server(
            filepath=xlsx_filepath.resolve(),
            filename='formulario.xlsx',
            path='/domains/innovatex.com.br/public_html/noel/files/csv/',
        )
    log_filepath: pathlib.Path = get_result_file(filename=settings.variables['log'])
    if log_filepath.exists():
        send_file_to_remote_server(
            filepath=log_filepath.resolve(),
            filename='log.html',
            path='/domains/innovatex.com.br/public_html/noel/files/pdf/',
        )
    # report_filepath: pathlib.Path = get_result_file(filename='report.html')
    # if log_filepath.exists():
    #     send_file_to_remote_server(
    #         filepath=log_filepath.resolve(),
    #         filename='report.html',
    #         path='/domains/innovatex.com.br/public_html/noel/files/pdf/',
    #     )
    print("Arquivos enviados com sucesso!")

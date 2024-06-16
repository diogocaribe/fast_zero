"""Api para estudo"""

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    """_summary_

    Returns:
        _type_: _description_
    """
    return {'message': 'Olá mundo'}

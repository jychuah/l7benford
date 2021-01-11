from unittest.mock import MagicMock
import pytest
import psycopg2
import json


@pytest.fixture
def postgres(mocker):
    yield mocker.patch('psycopg2.connect')


@pytest.fixture
def cursor(postgres, monkeypatch):
    import app
    mock = MagicMock()
    monkeypatch.setattr(app, 'cursor', mock)
    yield mock


@pytest.fixture
def client(cursor, monkeypatch):
    import app
    app.app.config['TESTING'] = True
    with app.app.test_client() as client:
        yield client


@pytest.fixture
def get_file(monkeypatch):
    import app
    mock = MagicMock()
    monkeypatch.setattr(app, 'get_file', mock)
    yield mock


def test_parse_tsv(postgres):
    from app import parse_file
    with open('./fixtures/census_2009b', 'r') as tsv:
        df = parse_file(tsv.read())
        assert len(df.columns) == 6


def test_make_histograms(postgres):
    from app import make_histograms, parse_file
    with open('./fixtures/histogram.csv', 'r') as csv:
        df = parse_file(csv.read(), delimiter=',')
        result = make_histograms(df)
        assert result['column_1'][1] == 0.375
        assert result['column_2'][9] == 0


def test_fetch_files(cursor, client):
    cursor.fetchall.return_value = [
      ('census_2009b', 'metadata')
    ]
    response = client.get('/api/files/')
    assert response.json == { 'census_2009b': 'metadata' }


def test_reparse(get_file, client):
    histogram = open('./fixtures/histogram.csv', 'rb').read()
    get_file.return_value = histogram
    response = client.post(
        '/api/reparse/',
        data=json.dumps({ 'filename': 'histogram.csv', 'delimiter': 'comma' }),
        content_type='application/json'
    )
    assert response.json['histogram']['column_1']['1'] == 0.375

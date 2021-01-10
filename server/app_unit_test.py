import pytest
import psycopg2


@pytest.fixture
def postgres(mocker):
    mocker.patch('psycopg2.connect')


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
        assert result['column_1'][0] == 0.25
        assert result['column_2'][9] == 0
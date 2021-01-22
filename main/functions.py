import datetime
import os
import pandas

from api.models import *


def read_file(filename, **kwargs):
    """Read file with **kwargs; files supported: xls, xlsx, csv, csv.gz, pkl"""

    read_map = {'xls': pandas.read_excel, 'xlsx': pandas.read_excel, 'csv': pandas.read_csv,
                'gz': pandas.read_csv, 'pkl': pandas.read_pickle}

    ext = os.path.splitext(filename)[1].lower()[1:]
    assert ext in read_map, "Input file not in correct format, must be xls, xlsx, csv, csv.gz, pkl; current format '{0}'".format(ext)
    assert os.path.isfile(filename), "File Not Found Exception '{0}'.".format(filename)

    return read_map[ext](filename, **kwargs)


def create_disease(request, item, dx_values):
    dx_id = dx_values.get('id')
    if dx_id and dx_id.isdigit():
        dx = Disease.objects.filter(pk=dx_id)
        old_dx = dict(dx.first().__dict__)
        dx.update(
            name=dx_values.get('name'), branch=dx_values.get('branch'), others=dx_values.get('others', ''),
            report=dx_values.get('report', ''), variant=item
        )

        dx_id = dx.first()
        if any(key in {k: None if old_dx[k] == dx_values[k] else dx_values[k] for k in dx_values} for key in dx_values.keys()):
            History.objects.create(content='Updated Disease: ' + str(dx_id), user=request.user, timestamp=datetime.datetime.now(), variant=item)
    else:
        dx_id = Disease.objects.create(
            name=dx_values.get('name'), branch=dx_values.get('branch'), others=dx_values.get('others', ''),
            report=dx_values.get('report', ''), variant=item
        )
        History.objects.create(content='Added Disease: ' + str(dx_id), user=request.user, timestamp=datetime.datetime.now(), variant=item)

    if 'key' in dx_values:
        create_functional(request, dx_id, dx_values)
    else:
        create_score(request, dx_id, dx_values)


def create_functional(request, item, func_values):
    func_id = func_values.get('id')
    if func_id and func_id.isdigit():
        func_id = Functional.objects.filter(pk=func_id)
        func_id.update(key=func_values.get('key', ''), value=func_values.get('value', ''))
    else:
        func_id = Functional.objects.create(key=func_values.get('key', ''), value=func_values.get('value', ''), disease=item)


def create_score(request, item, score_values):
    pass


def create_evidence(request, item, evidence_values):
    pass

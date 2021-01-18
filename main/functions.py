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
    dx_id = dx_values.pop('id', '')
    if dx_id.isdigit():
        dx = Disease.objects.filter(pk=dx_id)
        old_dx = dict(dx.first().__dict__)
        dx.update(**dx_values)
        dx_id = dx.first()
        # if any(key in {k: None if old_dx[k] == dx_values[k] else dx_values[k] for k in dx_values} for key in dx_values.keys()):
        #    History.objects.create(content='updated Disease: ' + str(dx_id), user=request.user, timestamp=datetime.datetime.now(), variant=item)
    else:
        dx_id = Disease.objects.create(**dx_values, variant=item)
        # History.objects.create(content='Added Disease: ' + str(dx_id), user=request.user, timestamp=datetime.datetime.now(), variant=item)

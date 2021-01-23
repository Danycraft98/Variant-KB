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


def create_disease(request, item, dx_values, other_values):
    dx_id = dx_values.get('id')
    branch = dx_values.get('branch')
    if dx_id and dx_id.isdigit():
        dx = Disease.objects.filter(pk=dx_id)
        old_dx = dict(dx.first().__dict__)
        dx.update(
            name=dx_values.get('name'), branch=branch, others=dx_values.get('others', ''),
            report=dx_values.get('report', ''), variant=item
        )

        dx_id = dx.first()
        if any(key in {k: None if old_dx[k] == dx_values[k] else dx_values[k] for k in dx_values} for key in dx_values.keys()):
            History.objects.create(content='Updated Disease: ' + str(dx_id), user=request.user, timestamp=datetime.datetime.now(), variant=item)
    else:
        dx_id = Disease.objects.create(
            name=dx_values.get('name'), branch=branch, others=dx_values.get('others', ''),
            report=dx_values.get('report', ''), variant=item
        )
        History.objects.create(content='Added Disease: ' + str(dx_id), user=request.user, timestamp=datetime.datetime.now(), variant=item)

    if branch == 'so':
        create_functional(request, dx_id, dx_values, other_values)
    else:
        create_score(request, dx_id, dx_values, other_values)


def create_functional(request, item, func_values, other_values):
    func_id = func_values.get('id')
    if func_id and func_id.isdigit():
        func_id = Functional.objects.filter(pk=func_id)
        func_id.update(key=func_values.get('key', ''), value=func_values.get('value', ''))
    else:
        func_id = Functional.objects.create(key=func_values.get('key', ''), value=func_values.get('value', ''), disease=item)
    create_evidence(request, [item, func_id], other_values)


def create_score(request, item, score_values, other_values):
    pass


def create_evidence(request, items, evidence_values):
    pass#print(dict(evidence_values))
    """for i, (e_id, source_type, source_id, statement) in enumerate(evidence_values):
        evid_dict = {'source_type': source_type, 'source_id': source_id, 'statement': statement}

        comp_result = None
        if e_id.isdigit():
            is_update = True
            evidence = Evidence.objects.get(pk=e_id)
            old_evidence = dict(evidence.__dict__)
            comp_result = {k: None if old_evidence[k] == evid_dict[k] else evid_dict[k] for k in evid_dict}
            Evidence.objects.filter(pk=e_id).update(**evid_dict)
        else:
            is_update = False
            sub_item = Evidence.objects.create(disease=items[0], **evid_dict)
            if items[1].__class__.__name__ == 'PathItem':
                Evidence.objects.filter(pk=sub_item.pk).update(item=items[1])
            elif items[1].__class__.__name__ == 'Functional':
                Evidence.objects.filter(pk=sub_item.pk).update(functional=items[1])
            evidence = Evidence.objects.get(pk=sub_item.pk)

        if request.POST.getlist(prefix + '_sig'):
            form_dict = {
                'level': request.POST.getlist(prefix + '_level')[i], 'evid_sig': request.POST.getlist(prefix + '_sig')[i],
                'evid_dir': request.POST.getlist(prefix + '_dir')[i], 'clin_sig': request.POST.getlist(prefix + '_clin_sig')[i],
                'drug_class': request.POST.getlist(prefix + '_drug')[i], 'evid_rating': request.POST.getlist(prefix + '_rating')[i]
            }

            if evidence.subevidences.count() > 0:
                evidence.subevidences.update(**form_dict, evidence=evidence)

            else:
                SubEvidence.objects.create(**form_dict, evidence=evidence)

        if (is_update and any(comp_result[key] for key in evid_dict.keys())) or not is_update:
            History.objects.create(content=statement, object=evidence, user=request.user, timestamp=datetime.datetime.now(), variant=item)"""

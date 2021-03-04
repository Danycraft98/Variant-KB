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
    disease = dx_values.pop('id', '')
    if disease:
        dx = Disease.objects.filter(id=disease.id)
        old_dx = dict(dx.first().__dict__)
        dx.update(**dx_values, variant=item)

        if any(key in {k: None if k in old_dx and old_dx[k] == dx_values[k] else dx_values[k] for k in dx_values} for key in dx_values.keys()):
            History.objects.create(content='Updated Disease: ' + str(disease), user=request.user, timestamp=datetime.datetime.now(), variant=item)

    else:
        disease = Disease.objects.create(**dx_values, variant=item)
        History.objects.create(content='Added Disease: ' + str(disease), user=request.user, timestamp=datetime.datetime.now(), variant=item)
    return disease


def create_child(model_class, dx, values):
    [values.pop(key, '') for key in ['DELETE', 'disease']]
    item = values.pop('id', None)
    if all(not values.get(key) or values.get(key) == '' for key in values):
        return None

    if item:
        item_filter = model_class.objects.filter(pk=item.id)
        item_filter.update(**values)
    else:
        item = model_class.objects.create(**values, disease=dx)
    return item


def create_evidence(request, dx, child, dx_prefix, i):
    item_dict = {
        'Functional': (dx_prefix + 'func-' + str(i), {'functional': child}),
        'Score': (dx_prefix + 'item-' + str(i), {
            'item': PathItem.objects.get(key=request.POST.get(dx_prefix + 'item-' + str(i) + '-key_val', '')) if child.__class__.__name__ == 'Score' else None
        })
    }
    prefix, other = item_dict.get(child.__class__.__name__, (dx_prefix[:-1], {}))
    for evid_id, s_type, s_id, stmt in zip(
            request.POST.getlist(prefix + '-evid-0-id', []),
            request.POST.getlist(prefix + '-evid-0-source_type', []),
            request.POST.getlist(prefix + '-evid-0-source_id', []),
            request.POST.getlist(prefix + '-evid-0-statement', [])
    ):
        if all(not key or key == '' for key in [s_type, stmt]):
            continue

        main_evid_dict = {'source_type': s_type, 'source_id': s_id, 'statement': stmt}
        if evid_id:
            evidence = Evidence.objects.get(pk=evid_id)
            old_evidence = dict(evidence.__dict__)
            comp_result = {k: None if old_evidence[k] == main_evid_dict[k] else main_evid_dict[k] for k in main_evid_dict}
            Evidence.objects.filter(pk=evidence.id).update(**main_evid_dict)
        else:
            evidence = Evidence.objects.create(disease=dx, **main_evid_dict, **other)

        sub_evid_dict = {
            'level': None, 'evid_sig': None,
            'evid_dir': None, 'clin_sig': None,
            'drug_class': None, 'evid_rating': None
        }
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

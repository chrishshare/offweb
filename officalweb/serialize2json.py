# encoding = utf-8

# Author:Administrator
# Email: siyzhou@163.com
# Date: 20181001
# Description:
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize


def queryset_to_json(querylist, resultinfo):
    queryset_to_list = list(querylist)
    data = {}
    data['body'] = queryset_to_list
    data['header'] = resultinfo

    aaa = []
    aaa.append(data)
    return json.dumps(aaa, ensure_ascii=False)
    # return json.dumps(list(data), ensure_ascii=False)






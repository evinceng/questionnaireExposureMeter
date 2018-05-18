# -*- coding: utf-8 -*-
"""
Created on Wed May 09 13:33:44 2018

@author: evin
@brief: flattens the objects in the inputDict dictionary for better use in DB
"""

from collections import OrderedDict

def flattenDict(inputDict, delimiter=':'):
    """
    flattens the objects in the inputDict dictionary for better use in DB
    """
    def expand(key, value):
        if isinstance(value, dict):
            return [
                (delimiter.join([key, k]), v)
                for k, v in flattenDict(value, delimiter).items()
            ]
        else:
            return [(key, value)]
    return OrderedDict(
		[item for k, v in inputDict.items() for item in expand(k, v)]
	)

#tobiiDict = OrderedDict([(u'timeStamp', u'30.12.2015 14:06:20.2412'), (u'leftPos', OrderedDict([(u'x', -0.228793755914194), (u'y', 11.5027813555582), (u'z', 60.912982163767)])), (u'rightPos', OrderedDict([(u'x', 5.89524352818696), (u'y', 11.2245013358383), (u'z', 61.0730322352786)])), (u'leftGaze', OrderedDict([(u'x', 3.15812377150551), (u'y', 17.3247499470179), (u'z', 4.61986983600664)])), (u'rightGaze', OrderedDict([(u'x', -2.49937069615642), (u'y', 17.3932511520527), (u'z', 4.64480229580618)])), (u'leftPupilDiameter', 2.645874), (u'rightPupilDiameter', 2.622345)])
#another method maybe useful for future
#def flatten(current, key, result):
#    if isinstance(current, dict):
#        for k in current:
#            new_key = "{0}.{1}".format(key, k) if len(key) > 0 else k
#            flatten(current[k], new_key, result)
#    else:
#        result[key] = current
#    return result

#result = flatten(tobiiDict, '', OrderedDict())

#result = flatten_dict(tobiiDict)
#print result

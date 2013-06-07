#!/usr/bin/env python
# -*- coding: utf-8 -*-

from itertools import izip

from .libsvm.svm import svm_problem, svm_parameter
from .libsvm.svmutil import svm_train, svm_predict

from .features import (
    generate_features,
    encode_features
)

__all__ = ('iterreg')


def _learn(x, y, opts=None):
    if opts is None:
        opts = ''

    prob = svm_problem(y, x, isKernel=True)
    param = svm_parameter('-s 3 {0}'.format(opts))
    return svm_train(prob, param)


def _predict(m, x, y=None):
    if y is None:
        y = (0.0,) * len(x)

    labels, _, _ = svm_predict(y, x, m)
    return labels


def iterreg(anew, sn, edges, pis=None, iterations=1, param=None):
    train_ids = tuple(i for i, s in enumerate(anew) if s is not None)

    y = tuple(anew[i] for i in train_ids)
    for it in xrange(0, iterations):
        features = generate_features(anew, sn, edges, pis)
        encoded_features = tuple(encode_features(features))

        x = tuple(encoded_features[i] for i in train_ids)
        m = _learn(x, y, param)
        pis = _predict(m, encoded_features)

        pis = [s if len(f) else None for s, f in izip(pis, encoded_features)]

    return pis
import math
from typing import Union, Collection

import tensorflow as tf

TFData = Union[tf.Tensor, tf.Variable, float]

class GMModel:
    def __init__(self, K):
        self.K = K
        self.mean = tf.Variable(tf.random.normal(shape=[K]))
        self.logvar = tf.Variable(tf.random.normal(shape=[K]))
        self.logpi = tf.Variable(tf.zeros(shape=[K]))

    @property
    def variables(self) -> Collection[TFData]:
        return self.mean, self.logvar, self.logpi

    @staticmethod
    def neglog_normal_pdf(x: TFData, mean: TFData, logvar: TFData):
        var = tf.exp(logvar)

        return 0.5 * (tf.math.log(2 * math.pi) + logvar + (x - mean) ** 2 / var)

    @tf.function
    def loss(self, data: TFData):
        mixing_coefficients = tf.nn.softmax(self.logpi)

        weighted_probs = [
        mixing_coefficients[i] * tf.exp(-self.neglog_normal_pdf(data, self.mean[i], self.logvar[i]))
        for i in range(self.K)
        ]

        total_prob = tf.add_n(weighted_probs)

        return -1  * tf.math.log(total_prob)  

    def p_xz(self, x: TFData, k: int) -> TFData:
        return tf.exp(-self.neglog_normal_pdf(x, self.mean[k], self.logvar[k])) 

    def p_x(self, x: TFData) -> TFData:
        mixing_coefficients = tf.nn.softmax(self.logpi)
        return tf.reduce_sum([mixing_coefficients[k] * self.p_xz(x, k) for k in range(self.K)], axis=0)  

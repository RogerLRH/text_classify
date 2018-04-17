import tensorflow as tf

from base_model import BaseModel


class FastText(BaseModel):
    def __init__(self, voca_size, input_len, hidden_size, num_class, embed_size=100, learning_rate=1e-3, decay_step=1000, decay_rate=0.8, batch_size=128, l2_ld=0.0001, pos_weight=1, clip_gradient=5.0, multi_label=False, initial_size=0.1):
        # set hyperparamter
        self.voca_size = voca_size
        self.embed_size = embed_size

        super(FastText, self).__init__(voca_size, input_len, num_class, embed_size, learning_rate, decay_step, decay_rate, batch_size, l2_ld, pos_weight, clip_gradient, multi_label, initial_size)


    def init_weights(self):
        # define all weights here
        with tf.name_scope("embed"):
            self.embedding = tf.get_variable("embedding", shape=[self.voca_size, self.embed_size], initializer=self.initializer)

        with tf.name_scope("full"):
            self.W_project = tf.get_variable("W_project", shape=[self.embed_size, self.num_class], initializer=self.initializer)
            self.b_project = tf.get_variable("b_project", shape=[self.num_class])

    def core(self):
        """main computation graph here: 1.embedding-->2.average-->3.linear classifier"""
        # emebedding
        embedded_sentence = tf.nn.embedding_lookup(self.embedding, self.input)  # [None, self.input_len, self.embed_size]

        # average of vectors
        self.embeds = tf.reduce_mean(embedded_sentence, axis=1)

        # fc
        self.logits = tf.matmul(self.embeds, self.W_project) + self.b_project